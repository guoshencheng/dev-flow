# dev-flow

以 Codex 为主的多角色研发协作体系，覆盖产品与交互、视觉、架构、研发、测试验收、运维交付。当前已有总纲 v0.1、全局流程入口，以及产品与交互职责的首版配置和专业 Skill。产品专业行为与连续资产复用已通过隔离案例，原生角色派发及真实应用验证尚待完成；后续逐个建设职责，再验证完整交付并按实际需要形成 Plugin。

## 维护入口

- [总纲概述](docs/overview.md)：经 Astra medium 独立审阅和修订稿复核通过的简介；[审阅记录](reviews/2026-10-07-overview-review.md)。
- [总纲](skills/dev-flow/references/constitution.md)：共同协作、交付与项目沉淀协议。
- [流程 Skill](skills/dev-flow/SKILL.md)：调用入口和按需阅读规则。
- [产品与交互 Agent](docs/product-agent.md)：职责边界、首版能力与验证状态；[专业 Skill](skills/dev-product/SKILL.md)和[案例证据](evals/dev-product/README.md)。
- [能力与项目沉淀](skills/dev-flow/references/2026-10-07-role-capabilities-and-project-assets.md)：六职责四十八项能力。
- [Codex 配置](skills/dev-flow/references/codex-agent-setup.md)：原生职责 Agent 的建设方式。
- [完整建设方案](skills/dev-flow/references/2026-10-07-development-harness-plan.md)：后续试点、运行内核与分发路线。

## 全局安装与使用

在仓库根目录执行：

```sh
python3 scripts/install_global.py
python3 scripts/install_global.py --check
```

安装脚本将本仓库的 `dev-flow`、`dev-product` Skills 逐个链接到 `~/.agents/skills/`，将 `agents/dev_product.toml` 链接到 `~/.codex/agents/`，并在 `~/.codex/AGENTS.md` 中维护一个简短的流程指引区块。更改既有指引前备份到 `~/.codex/backups/dev-flow/`，其他原文保留。链接冲突时停止，不覆盖其他来源。

在 Codex 中使用 `$dev-flow` 指定本流程。全局指引在新会话加载；若 Skill 列表没有刷新，重新启动 Codex。Codex 官方支持用户级 Skill 目录和符号链接扫描。[官方 Skills 说明](https://learn.chatgpt.com/docs/build-skills)

产品或交互任务可使用 `$dev-product` 读取专业指导。原生配置显式使用 `gpt-6.1-sol` 和 `medium`；只有宿主实际发现并派发 `dev_product` 后，才能记录原生角色执行。当前会话也可以由主 Agent 或获准的 Sol medium 子 Agent 读取专业 Skill 承担工作，并如实记录调用方式。

源码更新通过链接反映到全局文件，不需要重新复制。新增 Skill 或原生职责配置后再运行安装脚本；`agents/dev_*.toml` 逐个链接到 `~/.codex/agents/`，保留其他角色文件。原生角色的发现、模型设置和专业行为需要独立验证。

2026-10-07 已验证：Skill 结构、全局链接、既有指引保留与备份、重复安装和冲突保护；CLI 新上下文预览已加载全局流程指引，先后发现 `dev-flow`、`dev-product` Skills。当前全局链接两个 Skills、一个原生职责配置。产品专业指导由两次独立的 Sol medium 执行验证，覆盖首次设计和新上下文变更复用；CLI 在原生派发尝试前拒绝了所选模型，原生发现、派发及实际模型设置仍未验收，详见[验证记录](evals/dev-product/README.md)。

当前是本地 Git 仓库，远程发布在需要时设置。原 `business-guide/docs/development-harness` 入口链接到同一份参考文档，已有文件链接继续可用。

## 下一项建设

先在可用的 Codex 宿主核验 `dev_product` 原生派发，并在真实项目验证 P06 的应用操作或用户观察；随后按总纲建设视觉职责。两者保持专业边界，小任务允许同一执行者兼任，交互和渲染分别提供依据。其他职责顺序以总纲为准。

## 解除全局接入

删除由本仓库管理的 `~/.agents/skills/dev-flow`、`~/.agents/skills/dev-product` 链接，并从全局 `AGENTS.md` 删除 `<!-- dev-flow:begin -->` 与 `<!-- dev-flow:end -->` 之间的完整区块。职责配置只删除实际指向本仓库的链接。保留原有全局规则与项目资产。
