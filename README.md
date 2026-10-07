# dev-flow

以 Codex 为主的多角色研发协作体系，覆盖产品与交互、视觉、架构、研发、测试验收、运维交付。当前完成总纲 v0.1 和全局 Skill 入口，后续逐个建设职责 Agent，再验证完整交付并按实际需要形成 Plugin。

## 维护入口

- [总纲](skills/dev-flow/references/constitution.md)：共同协作、交付与项目沉淀协议。
- [流程 Skill](skills/dev-flow/SKILL.md)：调用入口和按需阅读规则。
- [能力与项目沉淀](skills/dev-flow/references/2026-10-07-role-capabilities-and-project-assets.md)：六职责四十八项能力。
- [Codex 配置](skills/dev-flow/references/codex-agent-setup.md)：原生职责 Agent 的建设方式。
- [完整建设方案](skills/dev-flow/references/2026-10-07-development-harness-plan.md)：后续试点、运行内核与分发路线。

## 全局安装与使用

在仓库根目录执行：

```sh
python3 scripts/install_global.py
python3 scripts/install_global.py --check
```

安装脚本建立 `~/.agents/skills/dev-flow` 到本仓库 `skills/dev-flow` 的符号链接，并在 `~/.codex/AGENTS.md` 中维护一个简短的流程指引区块。更改既有指引前备份到 `~/.codex/backups/dev-flow/`，其他原文保留。链接冲突时停止，不覆盖其他来源。

在 Codex 中使用 `$dev-flow` 指定本流程。全局指引在新会话加载；若 Skill 列表没有刷新，重新启动 Codex。Codex 官方支持用户级 Skill 目录和符号链接扫描。[官方 Skills 说明](https://learn.chatgpt.com/docs/build-skills)

源码更新通过链接反映到全局文件，不需要重新复制。新增 Skill 或完成原生 Agent 后再运行安装脚本；未来 `agents/dev_*.toml` 逐个链接到 `~/.codex/agents/`，保留其他角色文件。原生角色的发现、模型设置和专业行为需要独立验证。

2026-10-07 已验证：Skill 结构、全局链接、既有指引保留与备份、重复安装和冲突保护；CLI 新上下文预览已加载全局流程指引并发现 `dev-flow` Skill。当前安装一个流程 Skill，原生职责 Agent 为零；专业行为验证随职责建设进行。

当前是本地 Git 仓库，远程发布在需要时设置。原 `business-guide/docs/development-harness` 入口链接到同一份参考文档，已有文件链接继续可用。

## 下一项建设

产品与交互 Agent：先落实 P03 用户流程、P04 交互状态、P05 业务规则与验收、P06 可用性验证，配套原生配置、能力指导、项目资产协议和实际案例。后续顺序以总纲为准。

## 解除全局接入

删除由本仓库管理的 `~/.agents/skills/dev-flow` 链接，并从全局 `AGENTS.md` 删除 `<!-- dev-flow:begin -->` 与 `<!-- dev-flow:end -->` 之间的完整区块。已有职责配置只删除实际指向本仓库的链接。保留原有全局规则与项目资产。
