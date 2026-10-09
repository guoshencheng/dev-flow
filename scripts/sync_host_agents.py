#!/usr/bin/env python3
"""从共用 Skills 生成并检查 Codex/Kimi 职责入口，不安装或修改用户配置。"""
import argparse
import json
from pathlib import Path
import re
import sys

ROLES = ("product", "visual", "architecture", "engineering", "acceptance", "operations")


def skill_metadata(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError(f"缺少 Skill frontmatter：{path}")
    fields = {}
    for key in ("name", "description"):
        field = re.search(rf"^{key}: (.+)$", match[1], re.M)
        if not field:
            raise ValueError(f"缺少单行 {key}：{path}")
        fields[key] = field[1].strip()
    return fields


def expected_files(root):
    portable = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    compatibility = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    if any(portable[key] != compatibility[key] for key in ("name", "version", "description")):
        raise ValueError("便携清单与 Codex 清单的身份/版本/描述不一致")
    manifest = {key: portable[key] for key in ("name", "version", "description")}
    manifest.update({
        "skills": "./skills/",
        "agents": "./adapters/kimi/agents/",
        "skillInstructions": "在 Kimi 中需要且获准委派时，使用实际发现的 dev-product、dev-visual、dev-architecture、dev-engineering、dev-acceptance 或 dev-operations Agent。派发必须包含专业 Skill 的实际绝对路径、业务项目根路径、目标/阶段、有效输入与版本、确认/授权、可写范围和交接要求；读取 dev-flow/references/kimi-agent-configuration.md。宿主或用户不允许委派时由主 Agent 执行并记录独立性缺口。",
        "interface": {"displayName": "Dev Flow", "shortDescription": "六职责研发协作、持续验收与可运行交付"},
    })
    files = {"kimi.plugin.json": json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"}
    for role in ROLES:
        skill = f"dev-{role}"
        meta = skill_metadata(root / "skills" / skill / "SKILL.md")
        if meta["name"] != skill:
            raise ValueError(f"Skill 名称不匹配：{skill}")
        instructions = f"""你承担 Dev Flow 的 {skill} 专业职责。设计文档、实施计划、评审和交接使用中文。
专业方法的唯一维护入口是共用 skills/{skill}/SKILL.md；本文件由 scripts/sync_host_agents.py 生成，不手工复制专业规则。

开始先读取调用方提供的该 Skill 实际绝对路径，再读取同包 dev-flow/references/constitution.md 和本次所需参考。没有路径时，使用宿主 Skill 发现/调用能力按名称 {skill} 加载；仍无法定位则报告缺口，不猜测 ~/.agents、源码仓库或安装缓存路径。Markdown 相对引用以被读取文件所在目录为基准。

你只依赖派发任务中实际提供的上下文，不假定继承主会话历史。恢复业务项目绝对根路径、目标/阶段、有效输入与版本、候选提交及相关未提交差异、确认/授权来源、可写范围、验收与停止条件。缺少依赖性决定时先完成独立调查，在交接中提出缺失项，不自行登记用户确认。

只在指定工作目录及可写范围内行动；只读 Review 不修改源码，实施任务遵守明确写入者和共享资源约定。工具可用不代表获得额外动作授权。模型与推理强度由用户和宿主执行配置决定，本入口不固定模型。

只承担本次派发职责，不再派发子 Agent。按实际工具验证当前候选，区分静态阅读、自测、独立评审、实际验收和部署；不能用角色名或配置存在证明已经完成验证。发现阻断项按共用方法处理，不能降低已确认预期。

最终回复是交给主 Agent 的完整、自包含交接，至少包含结论与完成范围、输入/候选版本、成果路径和实际差异、命令与证据、问题/未覆盖项、资产变化及下一步依赖。由主 Agent 负责综合结果、用户沟通和最终集成。
"""
        files[f"agents/dev_{role}.toml"] = (
            "# 由 scripts/sync_host_agents.py 生成；历史 Codex 角色参考，不自动注册。\n"
            + f'name = "dev_{role}"\n'
            + f'description = {json.dumps(meta["description"], ensure_ascii=False)}\n'
            + 'developer_instructions = """\n' + instructions + '"""\n'
        )
        files[f"adapters/kimi/agents/{skill}.md"] = (
            "---\n" + f"name: {skill}\n"
            + f'description: {json.dumps(meta["description"], ensure_ascii=False)}\n'
            + "override: false\nsubagents: []\ndisallowedTools:\n  - Agent\n  - AgentSwarm\n---\n\n"
            + "${base_prompt}\n\n" + instructions
        )
    return files


def check(root):
    mismatches = []
    for relative, expected in expected_files(root).items():
        path = root / relative
        if not path.is_file() or path.read_text(encoding="utf-8") != expected:
            mismatches.append(relative)
    for role in ROLES:
        root_skill = root / "skills" / f"dev-{role}" / "SKILL.md"
        if not root_skill.is_file():
            mismatches.append(str(root_skill.relative_to(root)))
    agent_dir = root / "adapters/kimi/agents"
    expected_agents = {f"dev-{role}.md" for role in ROLES}
    if agent_dir.exists():
        unexpected = [str(p.relative_to(root)) for p in agent_dir.rglob("*.md")
                      if p.relative_to(agent_dir).as_posix() not in expected_agents]
        mismatches.extend(unexpected)
    if mismatches:
        raise ValueError("宿主入口未同步，运行 python3 scripts/sync_host_agents.py --write：" + ", ".join(mismatches))
    return {"hosts": ["codex", "kimi"], "roles": len(ROLES), "shared_skills": 7, "synchronized": True}


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
