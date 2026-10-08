#!/usr/bin/env python3
"""将仓库 Skill 和已建职责链接到全局，维护一段可定位的流程指引。"""

import argparse
from datetime import datetime
import os
from pathlib import Path
import shutil
import sys


BEGIN = "<!-- dev-flow:begin -->"
END = "<!-- dev-flow:end -->"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="仅核验，不写入")
    parser.add_argument("--codex-dir", type=Path,
                        default=Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))))
    parser.add_argument("--skills-dir", type=Path, default=Path.home() / ".agents/skills")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parent.parent
    codex_dir = args.codex_dir.expanduser().resolve()
    skills_dir = args.skills_dir.expanduser().resolve()
    if (codex_dir / "dev-flow/plugin/state.json").exists():
        raise ValueError("当前使用 Plugin 模式，请用 scripts/manage_plugin.py check/install；切换源码链接模式前先解除插件接入")
    links = [(p.parent.resolve(), skills_dir / p.parent.name)
             for p in sorted((repo / "skills").glob("*/SKILL.md"))]
    links += [(p.resolve(), codex_dir / "agents" / p.name)
              for p in sorted((repo / "agents").glob("dev_*.toml"))]
    if not links:
        raise ValueError("没有可安装的 Skill 或职责配置")

    for source, target in links:
        if target.is_symlink() and target.resolve() == source:
            continue
        if target.exists() or target.is_symlink():
            raise ValueError("全局入口已由其他来源占用：" + str(target))

    guidance = codex_dir / "AGENTS.md"
    if guidance.is_symlink() and not guidance.exists():
        raise ValueError("全局 AGENTS.md 是失效链接")
    override = codex_dir / "AGENTS.override.md"
    if override.is_file() and override.read_text(encoding="utf-8").strip():
        raise ValueError("存在生效的全局 AGENTS.override.md，请先明确指引应维护在哪个文件")
    original = guidance.read_text(encoding="utf-8") if guidance.exists() else ""
    if original.count(BEGIN) != original.count(END) or original.count(BEGIN) > 1:
        raise ValueError("全局指引的 dev-flow 区块标记不完整或重复")
    block = (BEGIN + "\n## 研发协作流程\n\n"
             "研发、设计、验收与交付任务使用 $dev-flow，并先读取其总纲，按用户要求裁剪流程。\n"
             "用户明确指定其他流程时遵循用户要求；使用实际可用且已验证的职责能力。\n"
             "Skill 入口：" + str(skills_dir / "dev-flow/SKILL.md") + "\n" + END)
    if BEGIN in original:
        start = original.index(BEGIN)
        end_position = original.index(END)
        if end_position < start:
            raise ValueError("全局指引的 dev-flow 区块标记顺序错误")
        stop = end_position + len(END)
        updated = original[:start] + block + original[stop:]
    else:
        separator = "" if not original else ("\n" if original.endswith("\n") else "\n\n")
        updated = original + separator + block + "\n"

    if args.check:
        missing = [str(target) for source, target in links
                   if not target.is_symlink() or target.resolve() != source]
        if missing or original != updated:
            raise ValueError("接入尚未完整：" + ", ".join(missing +
                             ([str(guidance)] if original != updated else [])))
        print("全局链接和流程指引检查通过；Skill " +
              str(len(list((repo / "skills").glob("*/SKILL.md")))) +
              " 个，原生职责 " + str(len(list((repo / "agents").glob("dev_*.toml")))) + " 个")
        return

    for source, target in links:
        if not target.is_symlink():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(source, target_is_directory=source.is_dir())
            print("已链接：" + str(target))
    if updated != original:
        codex_dir.mkdir(parents=True, exist_ok=True)
        if guidance.exists():
            backup = codex_dir / "backups/dev-flow" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            backup.mkdir(parents=True)
            shutil.copy2(guidance, backup / "AGENTS.md")
            print("既有指引已备份：" + str(backup / "AGENTS.md"))
        guidance.write_text(updated, encoding="utf-8")
        print("已更新流程指引：" + str(guidance))
    print("全局接入完成")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
