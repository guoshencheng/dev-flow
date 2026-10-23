#!/usr/bin/env python3
"""Manage the six Codex agent copies without changing other user configuration."""
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import quote

from sync_host_agents import LINK, ROLES

PLUGIN_ID = "dev-flow@dev-flow-local"
NAMES = tuple(f"dev_{role}" for role in ROLES)
FILES = tuple(f"{name}.toml" for name in NAMES)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def atomic_bytes(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=path.parent, prefix=".dev-flow-")
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_regular(path):
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise ValueError(f"角色管理路径不是普通文件，保留：{path}")
    return path.read_bytes() if path.exists() else None


def transaction(changes):
    """Rollback ordinary file errors; the external plugin CLI is not transactional."""
    previous = {path: read_regular(path) for path in changes}
    applied = []
    try:
        for path, content in changes.items():
            applied.append(path)
            if content is None:
                if path.exists():
                    path.unlink()
            else:
                atomic_bytes(path, content)
    except OSError as exc:
        failures = []
        for path in reversed(applied):
            try:
                if previous[path] is None:
                    if path.exists():
                        path.unlink()
                else:
                    atomic_bytes(path, previous[path])
            except OSError as rollback:
                failures.append(f"{path}: {rollback}")
        detail = "; ".join(failures) or "角色及记录文件已恢复原字节"
        raise ValueError(f"角色文件提交失败：{exc}；{detail}。插件 CLI 状态不在文件事务内，请修复后重新运行 install") from exc


def tokens(source):
    """Lex only what is needed to locate root assignments, not a TOML validator."""
    i = 0
    while i < len(source):
        char = source[i]
        if char in " \t\r":
            i += 1
        elif char == "#":
            end = source.find("\n", i)
            i = len(source) if end < 0 else end
        elif char in "\"'":
            delimiter = char * (3 if source.startswith(char * 3, i) else 1)
            start = i
            i += len(delimiter)
            while i < len(source):
                if source.startswith(delimiter, i):
                    # TOML permits four/five closing quotes on multiline strings.
                    i += len(delimiter)
                    if len(delimiter) == 3:
                        for _ in range(2):
                            if i < len(source) and source[i] == char:
                                i += 1
                    yield ("string", source[start:i])
                    break
                if len(delimiter) == 1 and source[i] == "\n":
                    raise ValueError("单行 TOML 字符串跨行")
                if char == '"' and source[i] == "\\":
                    i += 2
                else:
                    i += 1
            else:
                raise ValueError("TOML 字符串未闭合")
        elif char in "\n=[]{},.":
            yield (char, char)
            i += 1
        else:
            start = i
            while i < len(source) and source[i] not in " \t\r\n#\"'=[]{},.":
                i += 1
            yield ("bare", source[start:i])


def string_value(raw):
    literal = raw[0] == "'"
    width = 3 if raw.startswith(raw[0] * 3) else 1
    value = raw[width:-width]
    if width == 3 and value.startswith("\n"):
        value = value[1:]
    if literal:
        return value
    if width == 3:
        value = re.sub(r"\\[ \t\r]*\n[ \t\r\n]*", "", value)
    escapes = {'b': '\b', 't': '\t', 'n': '\n', 'f': '\f', 'r': '\r', '"': '"', '\\': '\\'}
    def decode(match):
        token = match.group(1)
        if token in escapes:
            return escapes[token]
        if token.startswith(('u', 'U')):
            number = token[1:]
            if len(number) == (4 if token[0] == 'u' else 8) and re.fullmatch('[0-9a-fA-F]+', number):
                point = int(number, 16)
                if point <= 0x10FFFF and not 0xD800 <= point <= 0xDFFF:
                    return chr(point)
        raise ValueError("name 包含无效 TOML 转义")
    return re.sub(r"\\(u.{0,4}|U.{0,8}|.|$)", decode, value)


def agent_name(source):
    """Conservatively extract a unique top-level name, ignoring nested text."""
    statements, current, stack = [], [], []
    for kind, value in tokens(source):
        if not current and not stack and kind == '[':
            # A genuine table header ends the root namespace.
            break
        if kind in ('[', '{'):
            stack.append(kind)
        elif kind in (']', '}'):
            if not stack or stack.pop() != ("[" if kind == ']' else '{'):
                raise ValueError("TOML 嵌套结构不匹配")
        if kind == '\n' and not stack:
            if current:
                statements.append(current)
            current = []
        else:
            current.append((kind, value))
    if stack:
        raise ValueError("TOML 嵌套结构未闭合")
    if current:
        statements.append(current)
    found = []
    for statement in statements:
        if len(statement) < 3 or statement[1][0] != '=':
            raise ValueError("无法可靠识别顶层 TOML 赋值")
        kind, raw = statement[0]
        if kind == 'string' and raw.startswith(("'''", '"""')):
            raise ValueError("TOML 键不能使用多行字符串")
        if kind == 'bare' and not re.fullmatch('[A-Za-z0-9_-]+', raw):
            raise ValueError("无法可靠识别顶层 TOML 键")
        key = string_value(raw) if kind == 'string' else raw
        if kind not in ('bare', 'string'):
            raise ValueError("无法可靠识别顶层 TOML 键")
        if key == 'name':
            if len(statement) != 3 or statement[2][0] != 'string':
                raise ValueError("name 必须是单个 TOML 字符串")
            found.append(string_value(statement[2][1]))
    if len(found) != 1 or not found[0]:
        raise ValueError("无法确定唯一顶层 name")
    return found[0]


def render_agents(plugin_root):
    root = Path(plugin_root).resolve()
    rendered = {}
    for filename in FILES:
        source = root / 'agents' / filename
        content = source.read_text(encoding='utf-8')
        line = next(line for line in content.splitlines() if line.startswith('developer_instructions = '))
        body = json.loads(line.partition(' = ')[2])
        def absolute(match):
            target = match.group(1)
            if target.startswith(('#', 'http://', 'https://', 'mailto:', 'data:', 'plugin://')):
                return match.group(0)
            bare, separator, fragment = target.partition('#')
            resolved = (source.parent / bare).resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():
                raise ValueError(f"角色资源缺失或越界：{source} -> {target}")
            encoded = quote(str(resolved), safe='/:')
            return match.group(0).replace(f'({target})', f'(<{encoded}{separator}{fragment}>)')
        body = LINK.sub(absolute, body)
        content = content.replace(line, 'developer_instructions = ' + json.dumps(body, ensure_ascii=False))
        rendered[filename] = content.encode('utf-8')
    return rendered


class NativeAgents:
    def __init__(self, source_root):
        self.source = str(Path(source_root).resolve())
        self.home = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex').expanduser().resolve()
        self.agents = self.home / 'agents'
        self.directory = self.home / 'dev-flow'
        self.state = self.directory / 'native-agents.json'

    def directories(self):
        for path in (self.agents, self.directory):
            if path.is_symlink() or (path.exists() and not path.is_dir()):
                raise ValueError(f"角色管理目录不是实际目录，保留：{path}")

    @contextmanager
    def locked(self):
        self.directories()
        self.directory.mkdir(parents=True, exist_ok=True)
        lock = self.directory / 'native-agents.lock'
        if lock.is_symlink():
            raise ValueError(f"操作锁不能为符号链接：{lock}")
        descriptor = os.open(lock, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        try:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise ValueError("另一个 Dev Flow 安装/检查/卸载正在执行，请稍后重试") from exc
            yield self
        finally:
            os.close(descriptor)

    def preflight(self, *, removing=False):
        self.directories()
        raw = read_regular(self.state)
        state = None
        if raw is not None:
            try:
                state = json.loads(raw)
                valid = (set(state) == {'schema', 'owner', 'plugin_id', 'source_root', 'plugin_root', 'files'}
                         and state['schema'] == 1 and state['owner'] == 'dev-flow'
                         and state['plugin_id'] == PLUGIN_ID and state['source_root'] == self.source
                         and isinstance(state['plugin_root'], str) and Path(state['plugin_root']).is_absolute()
                         and isinstance(state['files'], dict)
                         and set(state['files']) == set(FILES)
                         and all(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value)
                                 for value in state['files'].values()))
            except (ValueError, KeyError, TypeError):
                valid = False
            if not valid:
                raise ValueError(f"角色归属记录无效或属于其他来源，保留：{self.state}")
        snapshot = {self.state: raw}
        for filename in FILES:
            path = self.agents / filename
            if removing and state is None:
                continue
            data = read_regular(path)
            snapshot[path] = data
            if data is not None and (state is None or sha(data) != state['files'][filename]):
                raise ValueError(f"角色冲突或受管文件已被修改，保留：{path}；请另存个人修改或移开冲突后重试")
        if not removing:
            for path in sorted(self.agents.glob('*.toml')):
                if path.name in FILES:
                    continue
                try:
                    name = agent_name(path.read_text(encoding='utf-8'))
                except (OSError, ValueError) as exc:
                    raise ValueError(f"无法核验外来角色名称，保留：{path}；{exc}") from exc
                if name in NAMES:
                    raise ValueError(f"原生角色名称冲突，保留：{path}（{name}）")
        return state, snapshot

    def unchanged(self, snapshot, *, removing=False):
        _, current = self.preflight(removing=removing)
        if current != snapshot:
            raise ValueError("角色或归属记录在操作期间发生变化，保留现场，请重新运行")

    def register(self, plugin_root, snapshot, record_path, record):
        files = render_agents(plugin_root)
        state = {'schema': 1, 'owner': 'dev-flow', 'plugin_id': PLUGIN_ID,
                 'source_root': self.source, 'plugin_root': str(Path(plugin_root).resolve()),
                 'files': {name: sha(data) for name, data in files.items()}}
        self.unchanged(snapshot)
        changes = {self.agents / name: data for name, data in files.items()}
        changes[self.state] = (json.dumps(state, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
        changes[record_path] = (json.dumps(record, indent=2) + '\n').encode('utf-8')
        transaction(changes)
        return {'count': len(files), 'directory': str(self.agents), 'registry': str(self.state)}

    def check(self, plugin_root):
        state, snapshot = self.preflight()
        if state is None or state['plugin_root'] != str(Path(plugin_root).resolve()):
            raise ValueError("六职责尚未注册或缓存来源已变化，请运行 install")
        expected = render_agents(plugin_root)
        for filename, data in expected.items():
            if snapshot[self.agents / filename] != data or state['files'][filename] != sha(data):
                raise ValueError(f"原生角色缺失或未同步，请运行 install：{self.agents / filename}")
        return {'count': len(expected), 'directory': str(self.agents), 'registry': str(self.state)}

    def remove(self, snapshot, record_path):
        self.unchanged(snapshot, removing=True)
        changes = {path: None for path in snapshot if path != self.state}
        changes[self.state] = None
        changes[record_path] = None
        transaction(changes)
