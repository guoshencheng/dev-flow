#!/usr/bin/env python3
"""从单一能力清单与职责提示词生成、检查宿主入口；不安装或修改用户配置。"""
import argparse
import json
import os
from pathlib import Path
import re
import sys

ROLES = ("product", "visual", "architecture", "engineering", "acceptance", "operations")
LINK = re.compile(r'(?<!!)\[[^\]]*\]\(([^)]+)\)')


def confined(root, relative, *, required=True, directory=False):
    """Resolve a package-relative path while rejecting traversal and symlinks."""
    if not isinstance(relative, str) or not relative or relative.startswith(("/", "~")):
        raise ValueError(f"无效包内路径：{relative}")
    pure = Path(relative)
    if any(part in (".", "..") for part in pure.parts):
        raise ValueError(f"包内路径越界：{relative}")
    root = Path(root).resolve()
    path = root / pure
    if not path.resolve().is_relative_to(root) or any(piece.is_symlink() for piece in (path, *path.parents) if piece != root and root in piece.parents):
        raise ValueError(f"包内路径越界或为符号链接：{relative}")
    if required and not (path.is_dir() if directory else path.is_file()):
        raise ValueError(f"缺少包内文件：{relative}")
    if directory and not any(path.rglob("*")):
        raise ValueError(f"包内资源目录为空：{relative}")
    return path


def markdown_targets(path):
    text = path.read_text(encoding="utf-8")
    for match in LINK.finditer(text):
        target = match.group(1).strip().split()[0].strip('<>')
        if target and not target.startswith(("#", "http://", "https://", "mailto:", "data:", "plugin://")):
            yield target


def validate_links(root, files):
    root = Path(root).resolve()
    for path in files:
        path = path.resolve()
        for target in markdown_targets(path):
            bare = target.split("#", 1)[0].split("?", 1)[0]
            if not bare:
                continue
            resolved = (path.parent / bare).resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():
                raise ValueError(f"包内引用缺失或越界：{path.relative_to(root)} -> {target}")
            if resolved.is_symlink() or not (resolved.is_file() or resolved.is_dir()):
                raise ValueError(f"包内引用不是实际资源：{path.relative_to(root)} -> {target}")


def load_capabilities(root):
    root = Path(root)
    data = json.loads(confined(root, "capabilities.json").read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("不支持的能力清单版本")
    required_files = data.get("required_files")
    if not isinstance(required_files, list) or not required_files or len(required_files) != len(set(required_files)):
        raise ValueError("必需资源清单为空或重复")
    for resource in required_files:
        confined(root, resource)
    skills = data.get("skills")
    if not isinstance(skills, list) or len(skills) != len(set(skills)) or not skills:
        raise ValueError("能力清单 Skills 为空或重复")
    for skill in skills:
        if not isinstance(skill, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", skill):
            raise ValueError(f"无效 Skill 名称：{skill}")
        source = confined(root, f"skills/{skill}/SKILL.md")
        head = source.read_text(encoding="utf-8").split("---", 2)
        if len(head) < 3 or not re.search(rf"(?m)^name: {re.escape(skill)}$", head[1]):
            raise ValueError(f"Skill frontmatter 名称不匹配：{skill}")
    found = {p.parent.name for p in (root / "skills").glob("*/SKILL.md")}
    if found != set(skills):
        raise ValueError(f"Skill 清单与实际入口不一致；缺失={sorted(set(skills)-found)}，未声明={sorted(found-set(skills))}")
    roles = data.get("roles")
    if not isinstance(roles, dict) or set(roles) != set(ROLES):
        raise ValueError("职责清单必须声明六个现有职责")
    common = data.get("common_prompt")
    if common != "agents/prompts/common.md":
        raise ValueError("公共提示词路径不匹配")
    confined(root, common)
    for role, spec in roles.items():
        if not isinstance(spec, dict) or not isinstance(spec.get("description"), str) or not spec["description"].strip():
            raise ValueError(f"职责缺少描述：{role}")
        if spec.get("prompt") != f"agents/prompts/{role}.md":
            raise ValueError(f"职责提示词路径不匹配：{role}")
        confined(root, spec["prompt"])
        routed = spec.get("skills")
        if not isinstance(routed, list) or not routed or len(routed) != len(set(routed)) or set(routed) - set(skills):
            raise ValueError(f"职责 Skill 路由无效：{role}")
        for resource in spec.get("resources", []):
            confined(root, resource, directory=True)
        linked_skills = set()
        for target in markdown_targets(root / spec["prompt"]):
            bare = target.split("#", 1)[0]
            resolved = ((root / spec["prompt"]).parent / bare).resolve()
            if resolved.parent.parent == (root / "skills").resolve() and resolved.name == "SKILL.md":
                linked_skills.add(resolved.parent.name)
        if linked_skills - set(routed):
            raise ValueError(f"职责提示词引用未声明 Skill：{role} -> {sorted(linked_skills-set(routed))}")
    files = [root / common] + [root / roles[role]["prompt"] for role in ROLES]
    files += list((root / "skills").glob("*/SKILL.md"))
    files += list((root / "skills").glob("*/references/**/*.md"))
    files += list((root / "agents/references").glob("**/*.md"))
    files += list((root / "agents/assets").glob("**/*.md"))
    files += [path for path in (root / "skills").glob("*/assets/**/*.md")
              if not {"node_modules", "dist"}.intersection(path.parts)]
    validate_links(root, files)
    return data


def rewrite_links(content, source, output, root):
    """Make relative Markdown links valid from each generated host entry."""
    root = Path(root).resolve()
    source, output = Path(source).resolve(), Path(output).resolve()
    def replace(match):
        target = match.group(1)
        bare, marker, fragment = target.partition("#")
        if not bare or bare.startswith(("http://", "https://", "mailto:", "data:", "plugin://")):
            return match.group(0)
        resolved = (source.parent / bare).resolve()
        if not resolved.is_relative_to(root) or not resolved.exists():
            raise ValueError(f"提示词引用缺失或越界：{source.relative_to(root)} -> {target}")
        relative = os.path.relpath(resolved, output.parent).replace(os.sep, "/")
        return match.group(0).replace(f"({target})", f"({relative}{marker}{fragment})", 1)
    return LINK.sub(replace, content)


def expected_files(root):
    root = Path(root)
    data = load_capabilities(root)
    portable = json.loads(confined(root, "plugin.json").read_text(encoding="utf-8"))
    compatibility = json.loads(confined(root, ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    if any(portable[key] != compatibility[key] for key in ("name", "version", "description")):
        raise ValueError("便携清单与 Codex 清单的身份/版本/描述不一致")
    manifest = {key: portable[key] for key in ("name", "version", "description")}
    manifest.update({
        "skills": "./skills/", "agents": "./adapters/kimi/agents/",
        "skillInstructions": "按任务对象发现并派发六职责原生 Agent；派发时提供业务项目根路径、目标/阶段、有效输入与版本、授权来源、可写范围和交接要求。专业操作 Skills 按任务选用。宿主或用户不允许委派时主 Agent 执行并记录独立性缺口；会话监控不自动创建调度或发送通知。",
        "interface": {"displayName": "Dev Flow", "shortDescription": "六职责研发协作、会话监控与可运行交付"},
    })
    files = {"kimi.plugin.json": json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"}
    for role in ROLES:
        spec = data["roles"][role]
        source_paths = [root / data["common_prompt"], root / spec["prompt"]]
        for host, relative in (("codex", f"agents/dev_{role}.toml"), ("kimi", f"adapters/kimi/agents/dev-{role}.md")):
            output = root / relative
            body = "\n\n".join(rewrite_links(path.read_text(encoding="utf-8").strip(), path, output, root) for path in source_paths)
            routed = "、".join(spec["skills"])
            instructions = f"{body}\n\n本职责可按任务选用已声明的操作 Skills：{routed}。按宿主实际发现的包内路径读取；无法定位时说明缺口，不猜测开发机器路径。\n"
            if host == "codex":
                files[relative] = ("# 由 scripts/sync_host_agents.py 生成；Codex 角色参考，不自动注册。\n"
                    f'name = "dev_{role}"\n'
                    f'description = {json.dumps(spec["description"], ensure_ascii=False)}\n'
                    f'developer_instructions = {json.dumps(instructions, ensure_ascii=False)}\n')
            else:
                files[relative] = ("---\n" + f"name: dev-{role}\n"
                    + f'description: {json.dumps(spec["description"], ensure_ascii=False)}\n'
                    + "override: false\nsubagents: []\ndisallowedTools:\n  - Agent\n  - AgentSwarm\n---\n\n"
                    + "${base_prompt}\n\n" + instructions)
    return files


def check(root):
    expected = expected_files(root)
    mismatches = [relative for relative, content in expected.items()
                  if not (Path(root) / relative).is_file() or (Path(root) / relative).read_text(encoding="utf-8") != content]
    for directory, wanted in (("agents", {f"dev_{role}.toml" for role in ROLES}),
                              ("adapters/kimi/agents", {f"dev-{role}.md" for role in ROLES})):
        suffix = "*.toml" if directory == "agents" else "*.md"
        found = {p.name for p in (Path(root) / directory).glob(suffix)}
        mismatches.extend(f"{directory}/{name}" for name in sorted(found - wanted))
    if mismatches:
        raise ValueError("宿主入口未同步，运行 python3 scripts/sync_host_agents.py --write：" + ", ".join(mismatches))
    return {"hosts": ["codex-reference", "kimi-native"], "roles": len(ROLES),
            "shared_skills": len(load_capabilities(root)["skills"]), "synchronized": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="更新仓库内生成文件")
    mode.add_argument("--check", action="store_true", help="只读检查（默认）")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    if args.write:
        for relative, content in expected_files(root).items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    print(json.dumps(check(root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
