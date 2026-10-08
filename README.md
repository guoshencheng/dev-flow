# dev-flow

以 Codex 为主的多角色研发协作体系，覆盖产品与交互、视觉、架构、研发、测试验收、运维交付。当前已有总纲 v0.13、六职责配置与专业 Skills、共享 React 组件和面向当前业务项目的 Vite 文档预览工程。职责配置采用宿主模型策略；本地 Plugin 0.1.0 包装和接入方式见[安装指南](docs/plugin.md)及[验证记录](reviews/2026-10-09-plugin-installation.md)。工具、专业行为、原生角色派发与真实项目成熟度分别登记；完整真实任务和运行内核继续按实测需要建设。

## 维护入口

- [总纲概述](docs/overview.md)：当前简介；v0.1 经 Astra medium 独立审阅和修订稿复核，后续修改分别记录；[历史审阅记录](reviews/2026-10-07-overview-review.md)。
- [总纲](skills/dev-flow/references/constitution.md)：共同协作、交付与项目沉淀协议。
- [流程 Skill](skills/dev-flow/SKILL.md)：调用入口和按需阅读规则。
- [设计确认与自主实施](skills/dev-flow/references/execution-contract.md)：用户确认体验与重要架构，研发技术方案经符合性 Review，测试综合产品/方案设计用例并 AI Review，人工确认后计划/AI 复核、自主实现与端到端交付。
- [产品与交互 Agent](docs/product-agent.md)：职责边界、首版能力与验证状态；[专业 Skill](skills/dev-product/SKILL.md)和[案例证据](evals/dev-product/README.md)。
- [视觉与界面 Agent](docs/visual-agent.md)：专业方法、共同基础复用、视觉资产与实际检查；[专业 Skill](skills/dev-visual/SKILL.md)。
- [架构设计与演进 Agent](docs/architecture-agent.md)：整洁架构、项目技术基线、业务域与模块分工、设计契约、代码业务 Review 与研发复盘；[专业 Skill](skills/dev-architecture/SKILL.md)。
- [测试验收 Agent](docs/acceptance-agent.md)：综合产品/技术方案的用例及 AI Review/人工确认、真实界面/API/E2E、交付验证与反馈复验；[专业 Skill](skills/dev-acceptance/SKILL.md)及[验证状态](evals/dev-acceptance/report.md)。
- [研发 Agent](docs/engineering-agent.md)：架构后端到端技术方案与符合性 Review、计划 AI 复核、可运行切片、诊断修复及可启动交接；[专业 Skill](skills/dev-engineering/SKILL.md)和[首版验证](evals/dev-engineering/report.md)。
- [运维与交付 Agent](docs/operations-agent.md)：环境与快速启动、产物版本/发布、运行信号/故障、回退/数据恢复、依赖演进与退役；[专业 Skill](skills/dev-operations/SKILL.md)和[首版验证](evals/dev-operations/report.md)。
- [技术栈约定](skills/dev-architecture/references/technology-stack.md)：Web React、全栈 Next.js、纯静态 Astro；[历史项目调查](docs/project-tech-stacks/2026-10-08-survey.md)仅保存当时事实与建议，其他类型暂不进入通用技术 Guide。
- [代码规范 Guide](skills/dev-architecture/references/code-standards.md)：EditorConfig/Prettier、ESLint、TypeScript 与实际依赖规则；随包提供可复制格式配置，项目维护自己的规范和检查入口。
- [项目文档目录与归档](skills/dev-flow/references/design-document-contract.md)：明确当前业务项目的产品、交互原型、设计/UI、技术及相关验收/交付资料；[索引模板](skills/dev-flow/assets/templates/project-document-index.md)映射现行权威位置；[项目 Vite 预览](skills/dev-flow/references/document-preview.md)生成对应项目成果的实际地址，Skill 维护默认使用源文件链接。
- [原型与设计稿指南](skills/dev-product/references/html-prototyping.md)：AI 按任务构建页面、新建默认 Vite + React、启动预览与持续讨论；随包示例可选。[参考研究](skills/dev-product/references/reference-research-and-ideation.md)和[C/B 设计指导](skills/dev-product/references/consumer-and-business-design.md)。
- [UI 技术与共享组件约定](skills/dev-flow/references/ui-stack-and-components.md)：B 端 Ant Design/antd、C 端 Web shadcn/ui、其他 C 端先研究参考；[React 工作区](skills/dev-product/assets/react-workspace/README.md)及[组件清单](skills/dev-product/assets/react-workspace/catalog.md)由本 Git 仓库维护。
- [组件预览与源码复用](skills/dev-product/references/component-preview-and-reuse.md)：可操作组件目录、完整源码文件集、快速复制到项目和定制后的差异合并；[当前验证记录](evals/dev-product/runs/2026-10-08/component-gallery/report.md)。
- [Ant Design 能力联用](skills/dev-flow/references/ant-design-capabilities.md)：B 端优先官方现成组件，按需联合官方 Skill、CLI 或 MCP，支持任务范围内自主接入；[临时项目核验记录](evals/dev-product/runs/2026-10-08/ant-design-capabilities/report.md)。
- [能力与项目沉淀](skills/dev-flow/references/2026-10-07-role-capabilities-and-project-assets.md)：六职责四十八项能力。
- [Codex 配置](skills/dev-flow/references/codex-agent-setup.md)：原生职责 Agent 的建设方式。
- [完整建设方案](skills/dev-flow/references/2026-10-07-development-harness-plan.md)：后续试点、运行内核与分发路线。

## 全局安装与使用

当前推荐 Plugin 模式，在仓库根目录执行：

```sh
python3 scripts/manage_plugin.py install
python3 scripts/manage_plugin.py check
```

共八个 Skills（流程、六专业职责、安装初始化）和六个职责配置。install 同时用于更新，先构建 Git 管理文件的干净包，再通过 Codex 安装缓存和初始化适配；自动迁移指向本仓库的旧链接，其他来源冲突时保留并报告。详情见[插件指南](docs/plugin.md)。

源码链接模式作为可选回退；与 Plugin 模式择一。解除插件接入后在仓库根目录执行：

```sh
python3 scripts/install_global.py
python3 scripts/install_global.py --check
```

源码链接脚本将本仓库八个 Skills 逐个链接到 `~/.agents/skills/`，将六个 `agents/dev_*.toml` 职责配置链接到 `~/.codex/agents/`，并在 `~/.codex/AGENTS.md` 中维护一个简短的流程指引区块。更改既有指引前备份到 `~/.codex/backups/dev-flow/`，其他原文保留。链接冲突时停止，不覆盖其他来源。

在 Codex 中使用 `$dev-flow` 指定本流程。全局指引在新会话加载；若 Skill 列表没有刷新，重新启动 Codex。Codex 官方支持用户级 Skill 目录和符号链接扫描。[官方 Skills 说明](https://learn.chatgpt.com/docs/build-skills)

产品或交互任务可使用 `$dev-product` 读取专业指导。原生职责文件省略 `model` 与 `model_reasoning_effort`，采用本次显式派发、宿主默认或父会话设置；具体任务遵循用户最新要求。只有宿主实际发现并派发 `dev_product` 后，才能记录原生角色执行。当前会话也可以由主 Agent 或获准的子 Agent 读取专业 Skill 承担工作，并如实记录调用方式。

架构设计、代码架构评审或研发复盘可使用 `$dev-architecture`。源码与当前架构地图一并核验，研发结束后同步受影响模块的实际职责/域/层次和有证据的改进建议；配置不固定模型。

测试策略/用例、接口与界面验证、前后端 E2E 或交付验收可使用 `$dev-acceptance`。从有效产品/UI/ARC 和经符合性 Review 的技术方案设计端到端用例，实际 AI Review 后交人工确认，再执行并持续反馈研发，修复后复验原问题及回归；Mock/替身、真实依赖与部署结果分别登记。原生职责 `dev_acceptance` 是否实际可派发在当前宿主核验。

技术实现方案、功能实现、诊断修复、兼容变更与集成交付可使用 `$dev-engineering`。架构后定义页面/功能/OUT/链路，经产品符合性及相关 UI/架构 AI Review 后交测试；用例 AI Review/人工确认后实际复核实施计划并自主编码；按原始规格修复测试反馈并交回待验候选，维护项目工程索引/计划/诊断和真实启动支持。

启动交付、产物/部署核验、运行诊断/恢复或环境维护可使用 `$dev-operations`。恢复真实环境/版本与授权范围，操作当前候选与核心任务，维护项目 runbook、交付和故障/恢复记录；部署未知先查询，应用回退与数据恢复分别取证。

以下说明适用于源码链接回退模式：源码更新通过链接反映到全局文件，不需要重新复制。新增 Skill 或原生职责配置后再运行安装脚本；`agents/dev_*.toml` 逐个链接到 `~/.codex/agents/`，保留其他角色文件。原生角色的发现、模型设置和专业行为需要独立验证。

2026-10-07 已验证：Skill 结构、全局链接、既有指引保留与备份、重复安装和冲突保护；CLI 新上下文预览已加载全局流程指引，先后发现 `dev-flow`、`dev-product` Skills。当时链接两个 Skills、一个原生职责配置。产品专业指导由两次独立的 Sol medium 执行验证，覆盖首次设计和新上下文变更复用；CLI 在原生派发尝试前拒绝了所选模型，原生发现、派发及实际模型设置仍未验收，详见[验证记录](evals/dev-product/README.md)。视觉阶段增加第三个 Skill，见[视觉与工具记录](evals/dev-visual/runs/2026-10-08/visual-and-documents/report.md)；架构阶段增加第四个 Skill 和第三个职责设置，见[架构验证](evals/dev-architecture/report.md)。

当前是本地 Git 仓库，远程发布在需要时设置。原 `business-guide/docs/development-harness` 入口链接到同一份参考文档，已有文件链接继续可用。

## 下一项建设

产品 v0.8、视觉 v0.1、架构 v0.3、测试验收 v0.3、研发 v0.2 与运维交付 v0.1 已定义专业方法与项目资产维护。运维的源码包启动、运行故障与恢复工具案例见[首版验证](evals/dev-operations/report.md)，研发隔离修复案例见[记录](evals/dev-engineering/report.md)，测试执行范围见[记录](evals/dev-acceptance/report.md)，架构规范检查见[记录](reviews/2026-10-08-architecture-code-standards-check.md)。历史原型/组件证据保持原版本，见[视觉与文档验证](evals/dev-visual/runs/2026-10-08/visual-and-documents/report.md)。总纲 v0.13 增加架构后端到端技术方案、符合性及用例 AI Review/人工确认，见[调整记录](reviews/2026-10-08-technical-delivery-stage.md)；保留运行/交付资产和 v0.11 的[设计与实现路由边界](reviews/2026-10-08-prototype-review-routing.md)及确认/自主实施规则。下一步选择真实任务检验完整循环和下一任务资产复用；原生派发/实际模型设置与真实项目分别实测，本地 Plugin 已接入，见[安装验证](reviews/2026-10-09-plugin-installation.md)；运行内核继续按真实任务需要建设。

## 解除全局接入

Plugin 模式使用 `python3 scripts/manage_plugin.py remove`。源码链接模式删除由本仓库管理的八个 Skill 链接，并从全局 `AGENTS.md` 删除 `<!-- dev-flow:begin -->` 与 `<!-- dev-flow:end -->` 之间的完整区块。职责配置只删除实际指向本仓库的链接。保留原有全局规则与项目资产。
