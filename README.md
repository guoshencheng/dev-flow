# dev-flow

以 Codex 为主的多角色研发协作体系，覆盖产品与交互、视觉、架构、研发、测试验收、运维交付。当前已有总纲 v0.11、产品/视觉/架构/测试验收/研发职责配置与 Skills、共享 React 组件和面向当前业务项目的 Vite 文档预览工程。职责配置采用宿主模型策略。工具、专业行为、原生角色派发与真实项目成熟度分别登记；后续逐个建设职责，再验证完整交付并按实际需要形成 Plugin。

## 维护入口

- [总纲概述](docs/overview.md)：当前简介；v0.1 经 Astra medium 独立审阅和修订稿复核，后续修改分别记录；[历史审阅记录](reviews/2026-10-07-overview-review.md)。
- [总纲](skills/dev-flow/references/constitution.md)：共同协作、交付与项目沉淀协议。
- [流程 Skill](skills/dev-flow/SKILL.md)：调用入口和按需阅读规则。
- [设计确认与自主实施](skills/dev-flow/references/execution-contract.md)：用户确认体验、架构与测试预期，AI 复核实现计划后自主实现，以端到端及架构约束检查交付。
- [产品与交互 Agent](docs/product-agent.md)：职责边界、首版能力与验证状态；[专业 Skill](skills/dev-product/SKILL.md)和[案例证据](evals/dev-product/README.md)。
- [视觉与界面 Agent](docs/visual-agent.md)：专业方法、共同基础复用、视觉资产与实际检查；[专业 Skill](skills/dev-visual/SKILL.md)。
- [架构设计与演进 Agent](docs/architecture-agent.md)：整洁架构、项目技术基线、业务域与模块分工、设计契约、代码业务 Review 与研发复盘；[专业 Skill](skills/dev-architecture/SKILL.md)。
- [测试验收 Agent](docs/acceptance-agent.md)：用例与策略、前端界面、真实接口/数据、前后端 E2E、交付验证与持续反馈复验；[专业 Skill](skills/dev-acceptance/SKILL.md)及[验证状态](evals/dev-acceptance/report.md)。
- [研发 Agent](docs/engineering-agent.md)：工程接入、计划 AI 复核、可运行切片、前后端实现、诊断修复、兼容演进及可启动交接；[专业 Skill](skills/dev-engineering/SKILL.md)和[首版验证](evals/dev-engineering/report.md)。
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

在仓库根目录执行：

```sh
python3 scripts/install_global.py
python3 scripts/install_global.py --check
```

安装脚本将本仓库的 `dev-flow`、`dev-product`、`dev-visual`、`dev-architecture`、`dev-acceptance`、`dev-engineering` Skills 逐个链接到 `~/.agents/skills/`，将五个 `agents/dev_*.toml` 职责配置链接到 `~/.codex/agents/`，并在 `~/.codex/AGENTS.md` 中维护一个简短的流程指引区块。更改既有指引前备份到 `~/.codex/backups/dev-flow/`，其他原文保留。链接冲突时停止，不覆盖其他来源。

在 Codex 中使用 `$dev-flow` 指定本流程。全局指引在新会话加载；若 Skill 列表没有刷新，重新启动 Codex。Codex 官方支持用户级 Skill 目录和符号链接扫描。[官方 Skills 说明](https://learn.chatgpt.com/docs/build-skills)

产品或交互任务可使用 `$dev-product` 读取专业指导。原生职责文件省略 `model` 与 `model_reasoning_effort`，采用本次显式派发、宿主默认或父会话设置；具体任务遵循用户最新要求。只有宿主实际发现并派发 `dev_product` 后，才能记录原生角色执行。当前会话也可以由主 Agent 或获准的子 Agent 读取专业 Skill 承担工作，并如实记录调用方式。

架构设计、代码架构评审或研发复盘可使用 `$dev-architecture`。源码与当前架构地图一并核验，研发结束后同步受影响模块的实际职责/域/层次和有证据的改进建议；配置不固定模型。

测试策略/用例、接口与界面验证、前后端 E2E 或交付验收可使用 `$dev-acceptance`。从项目有效产品/UI/ARC 与测试资产选择方案，实际执行并持续反馈研发，修复后复验原问题及回归；Mock/替身、真实依赖与部署结果分别登记。原生职责 `dev_acceptance` 是否实际可派发在当前宿主核验。

功能实现、诊断修复、兼容变更与集成交付可使用 `$dev-engineering`。实施前实际 AI 复核计划，通过后自主实现；按原始规格修复测试反馈并交回待验候选，维护项目工程索引/计划/诊断和真实启动支持。

源码更新通过链接反映到全局文件，不需要重新复制。新增 Skill 或原生职责配置后再运行安装脚本；`agents/dev_*.toml` 逐个链接到 `~/.codex/agents/`，保留其他角色文件。原生角色的发现、模型设置和专业行为需要独立验证。

2026-10-07 已验证：Skill 结构、全局链接、既有指引保留与备份、重复安装和冲突保护；CLI 新上下文预览已加载全局流程指引，先后发现 `dev-flow`、`dev-product` Skills。当时链接两个 Skills、一个原生职责配置。产品专业指导由两次独立的 Sol medium 执行验证，覆盖首次设计和新上下文变更复用；CLI 在原生派发尝试前拒绝了所选模型，原生发现、派发及实际模型设置仍未验收，详见[验证记录](evals/dev-product/README.md)。视觉阶段增加第三个 Skill，见[视觉与工具记录](evals/dev-visual/runs/2026-10-08/visual-and-documents/report.md)；架构阶段增加第四个 Skill 和第三个职责设置，见[架构验证](evals/dev-architecture/report.md)。

当前是本地 Git 仓库，远程发布在需要时设置。原 `business-guide/docs/development-harness` 入口链接到同一份参考文档，已有文件链接继续可用。

## 下一项建设

产品 v0.8、视觉 v0.1、架构 v0.3、测试验收 v0.2 和研发 v0.1 已定义专业方法与资产维护，复用共享 UI 基础和项目文档预览。研发首版方法和主 Agent 隔离修复案例见[记录](evals/dev-engineering/report.md)；测试首版细化界面/API/前后端 E2E 与交付方案，实际范围见[首版验证](evals/dev-acceptance/report.md)；架构代码规范检查见[记录](reviews/2026-10-08-architecture-code-standards-check.md)。历史原型/组件证据保持原版本，范围见[视觉与文档验证](evals/dev-visual/runs/2026-10-08/visual-and-documents/report.md)。总纲 v0.11 明确设计原型走查与实现验收的路由，见[边界回溯](reviews/2026-10-08-prototype-review-routing.md)，保留 v0.10 研发方法与工程资产、v0.9 测试验收方法、v0.8 的业务项目文档入口、v0.7 架构复盘和 v0.6 确认/自主实施协议继续有效。下一职责为运维交付；真实执行依用户确认的基线推进。在可用宿主核验原生派发和实际模型设置，用真实项目验证完整循环及资产复用。

## 解除全局接入

删除由本仓库管理的六个 Skill 链接，并从全局 `AGENTS.md` 删除 `<!-- dev-flow:begin -->` 与 `<!-- dev-flow:end -->` 之间的完整区块。职责配置只删除实际指向本仓库的链接。保留原有全局规则与项目资产。
