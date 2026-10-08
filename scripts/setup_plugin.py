#!/usr/bin/env python3
"""适配插件内的职责配置；只维护自己的链接、副本和全局指引区块。"""

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import sys

BEGIN = "<!-- dev-flow:begin -->"
END = "<!-- dev-flow:end -->"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def occupied(path):
    return path.exists() or path.is_symlink()


def atomic_text(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def snapshot(paths_to_save):
    return {path: (("link", os.readlink(path)) if path.is_symlink()
                   else ("file", path.read_bytes()) if path.is_file()
                   else ("missing", None)) for path in paths_to_save}


def rollback(saved):
    failures = []
    for path, (kind, value) in saved.items():
        try:
            if occupied(path):
                path.unlink()
            if kind != "missing":
                path.parent.mkdir(parents=True, exist_ok=True)
                if kind == "link":
                    path.symlink_to(value)
                else:
                    path.write_bytes(value)
        except OSError:
            failures.append(str(path))
    if failures:
        raise ValueError("写入未完成，部分入口无法恢复，请依据备份处理：" + ", ".join(failures))


def replace_block(original, block):
    if original.count(BEGIN) != original.count(END) or original.count(BEGIN) > 1:
        raise ValueError("全局指引的 Dev Flow 标记不完整或重复")
    if BEGIN in original:
        start, end = original.index(BEGIN), original.index(END)
        if end < start:
            raise ValueError("全局指引标记顺序错误")
        return original[:start] + block + original[end + len(END):]
    if not block:
        return original
    separator = "" if not original else ("\n" if original.endswith("\n") else "\n\n")
    return original + separator + block + "\n"


def paths(args):
    codex_dir = args.codex_dir.expanduser().resolve()
    managed = codex_dir / "dev-flow/plugin"
    return codex_dir, managed, managed / "state.json"


def state_at(path):
    if not path.exists():
        return None
    state = json.loads(path.read_text(encoding="utf-8"))
    if state.get("owner") != "dev-flow" or state.get("schema") != 1:
        raise ValueError("受管状态格式未知：" + str(path))
    return state


def inputs(root):
    manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    if manifest.get("name") != "dev-flow":
        raise ValueError("不是 Dev Flow 插件根目录：" + str(root))
    inventory = root / "package-files.json"
    if inventory.exists():
        for entry, expected in json.loads(inventory.read_text(encoding="utf-8"))["files"].items():
            path = root / entry
            if not path.resolve().is_relative_to(root) or not path.is_file() or digest(path) != expected:
                raise ValueError("插件包内容与指纹不符：" + entry)
    roles = {}
    for source in sorted((root / "agents").glob("dev_*.toml")):
        value = source.read_text(encoding="utf-8")
        if re.search(r"^(model|model_reasoning_effort)\s*=", value, re.M):
            raise ValueError("职责配置不应固定模型：" + source.name)
        # 只替换路径，保留原职责指令。转义后兼容 TOML 多行基本字符串。
        prefix = json.dumps(str(root / "skills") + "/", ensure_ascii=False)[1:-1]
        if "~/.agents/skills/" not in value:
            raise ValueError("职责模板缺少可适配的 Skill 入口：" + source.name)
        roles[source.name] = value.replace("~/.agents/skills/", prefix)
    if len(roles) != 6:
        raise ValueError("应存在六个职责 TOML")
    skills = [p.parent.name for p in sorted((root / "skills").glob("*/SKILL.md"))]
    if not skills or "dev-flow" not in skills:
        raise ValueError("插件缺少流程 Skill")
    return manifest, roles, skills


def guidance(root):
    return (BEGIN + "\n## 研发协作流程\n\n"
            "研发、设计、验收与交付任务使用已启用的 Dev Flow 插件及 $dev-flow，"
            "并先读取其总纲，按用户要求裁剪流程。\n"
            "用户明确指定其他流程时遵循用户要求；使用实际可用且已验证的职责能力。\n"
            "Skill 入口：" + str(root / "skills/dev-flow/SKILL.md") + "\n" + END)


def preflight(args, roles, state):
    codex_dir, managed, _ = paths(args)
    legacy = args.legacy_root.expanduser().resolve() if args.legacy_root else None
    allowed_roots = set(state.get("legacy_roots", []) if state else [])
    if legacy:
        if not (legacy / "skills/dev-flow/SKILL.md").is_file():
            raise ValueError("旧仓库入口无效：" + str(legacy))
        allowed_roots.add(str(legacy))
    for name in roles:
        target = codex_dir / "agents" / name
        allowed = [managed / "agents" / name] + [Path(p) / "agents" / name for p in allowed_roots]
        if occupied(target) and (not target.is_symlink() or target.resolve() not in allowed):
            raise ValueError("角色入口由其他来源占用：" + str(target))
        generated = managed / "agents" / name
        if occupied(generated):
            expected = state.get("role_hashes", {}).get(name) if state else None
            if generated.is_symlink() or not expected or digest(generated) != expected:
                raise ValueError("受管角色副本有未纳入的修改：" + str(generated))
    removed = {}
    skills_dir = args.skills_dir.expanduser().resolve()
    for folder in sorted(set(roles_name_to_skill(name) for name in roles) | {"dev-flow", "dev-flow-setup"}):
        target = skills_dir / folder
        if not occupied(target):
            continue
        allowed = [Path(p) / "skills" / folder for p in allowed_roots]
        if not target.is_symlink() or target.resolve() not in allowed:
            raise ValueError("同名全局 Skill 来自其他来源：" + str(target))
        removed[str(target)] = os.readlink(target)
    override = codex_dir / "AGENTS.override.md"
    if override.is_file() and override.read_text(encoding="utf-8").strip():
        raise ValueError("存在生效的全局 AGENTS.override.md，当前指引入口需明确")
    current = codex_dir / "AGENTS.md"
    if current.is_symlink():
        raise ValueError("全局 AGENTS.md 是链接，不在插件初始化中改写其来源")
    original = current.read_text(encoding="utf-8") if current.exists() else ""
    replace_block(original, "")
    if state and BEGIN in original and state["guidance"] not in original:
        raise ValueError("Dev Flow 指引区块已修改，保留并报告")
    return allowed_roots, removed, original


def roles_name_to_skill(name):
    return name.removesuffix(".toml").replace("_", "-")


def apply(args):
    root = args.plugin_root.expanduser().resolve()
    manifest, roles, skills = inputs(root)
    codex_dir, managed, state_path = paths(args)
    state = state_at(state_path)
    roots, removed, original = preflight(args, roles, state)
    block = guidance(root)
    updated = replace_block(original, block)
    # 完整预检后才开始写入；重复接入无变化时不制造备份。
    package_hash = digest(root / "package-files.json") if (root / "package-files.json").exists() else None
    current_ok = (state and state.get("plugin_root") == str(root) and state.get("guidance") == block
                  and state.get("package_hash") == package_hash and state.get("version") == manifest["version"])
    if current_ok and not removed and updated == original and all(
            (managed / "agents" / n).is_file() and (managed / "agents" / n).read_text(encoding="utf-8") == v
            and (codex_dir / "agents" / n).is_symlink() for n, v in roles.items()):
        return check(args)
    backup = codex_dir / "backups/dev-flow" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup.mkdir(parents=True)
    (backup / "AGENTS.md").write_text(original, encoding="utf-8")
    (backup / "links.json").write_text(json.dumps({"skills": removed, "agents": {
        n: os.readlink(codex_dir / "agents" / n) if (codex_dir / "agents" / n).is_symlink() else None
        for n in roles}}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    affected = [codex_dir / "AGENTS.md", state_path] + [Path(p) for p in removed]
    affected += [directory / name for name in roles for directory in (managed / "agents", codex_dir / "agents")]
    saved = snapshot(affected)
    try:
        for name, value in roles.items():
            generated = managed / "agents" / name
            atomic_text(generated, value)
            target = codex_dir / "agents" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if occupied(target):
                target.unlink()
            target.symlink_to(generated)
        for name in removed:
            Path(name).unlink()
        atomic_text(codex_dir / "AGENTS.md", updated)
        new_state = {"owner": "dev-flow", "schema": 1, "version": manifest["version"],
                     "plugin_root": str(root), "legacy_roots": sorted(roots), "skills": skills,
                     "guidance": block, "role_hashes": {n: digest(managed / "agents" / n) for n in roles},
                     "package_hash": package_hash, "backup": str(backup)}
        atomic_text(state_path, json.dumps(new_state, ensure_ascii=False, indent=2) + "\n")
        return check(args)
    except Exception:
        rollback(saved)
        raise


def check(args):
    root = args.plugin_root.expanduser().resolve()
    manifest, roles, skills = inputs(root)
    codex_dir, managed, state_path = paths(args)
    state = state_at(state_path)
    if not state or state["plugin_root"] != str(root) or state["version"] != manifest["version"]:
        raise ValueError("尚未初始化当前插件版本")
    for name, value in roles.items():
        target = codex_dir / "agents" / name
        generated = managed / "agents" / name
        if (not target.is_symlink() or target.resolve() != generated or not generated.is_file()
                or generated.read_text(encoding="utf-8") != value or digest(generated) != state["role_hashes"][name]):
            raise ValueError("角色接入不符合当前插件：" + name)
    original = (codex_dir / "AGENTS.md").read_text(encoding="utf-8")
    if replace_block(original, guidance(root)) != original:
        raise ValueError("全局流程指引不是当前插件入口")
    for skill in skills:
        if occupied(args.skills_dir.expanduser() / skill):
            raise ValueError("存在重复的同名全局 Skill：" + skill)
    inventory = root / "package-files.json"
    if inventory.exists() and digest(inventory) != state["package_hash"]:
        raise ValueError("插件已更新，需要重新初始化")
    return {"initialized": True, "plugin_root": str(root), "version": manifest["version"],
            "skills": len(skills), "roles": len(roles)}


def remove(args):
    codex_dir, managed, state_path = paths(args)
    state = state_at(state_path)
    if not state:
        return {"removed": False, "reason": "没有本插件受管状态"}
    for name, expected in state["role_hashes"].items():
        generated = managed / "agents" / name
        if occupied(generated) and (generated.is_symlink() or digest(generated) != expected):
            raise ValueError("受管角色已修改，保留并报告：" + str(generated))
    current = codex_dir / "AGENTS.md"
    original = current.read_text(encoding="utf-8") if current.is_file() else ""
    if BEGIN in original and state["guidance"] not in original:
        raise ValueError("Dev Flow 指引区块已修改，解除前需要明确该区块的归属")
    replacement = replace_block(original, "") if state["guidance"] in original else original
    if replacement != original and current.is_symlink():
        raise ValueError("全局指引已改为链接，保留其来源")
    for name in state["role_hashes"]:
        target = codex_dir / "agents" / name
        generated = managed / "agents" / name
        if target.is_symlink() and target.resolve() == generated:
            target.unlink()
        if generated.is_file():
            generated.unlink()
    if replacement != original:
        atomic_text(current, replacement)
    state_path.unlink()
    return {"removed": True, "legacy_restored": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("apply", "check", "remove"))
    parser.add_argument("--plugin-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--legacy-root", type=Path)
    parser.add_argument("--codex-dir", type=Path, default=Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))))
    parser.add_argument("--skills-dir", type=Path, default=Path.home() / ".agents/skills")
    args = parser.parse_args()
    print(json.dumps({"apply": apply, "check": check, "remove": remove}[args.command](args), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
