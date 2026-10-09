# dev-flow

以 Codex 为主的多角色研发协作体系，覆盖产品与交互、视觉、架构、研发、测试验收、运维交付。当前已有总纲 v0.17、六职责专业 Skills、共享 React 组件和面向当前业务项目的 Vite 文档预览工程。专业职责由主 Agent 或获准委派的可用子 Agent 承担，模型遵循本次用户要求与宿主策略；本地 Plugin 0.1.0 包装和接入方式见[安装指南](docs/plugin.md)及[验证记录](reviews/2026-10-09-setup-removal-and-task-routing.md)。工具、专业行为、实际委派与真实项目成熟度分别登记；完整真实任务和运行内核继续按实测需要建设。

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
- [UI 技术与共享组件约定](skills/dev-visual/references/ui-stack-and-components.md)：B 端 Ant Design/antd、C 端 Web shadcn/ui、其他 C 端先研究参考；[React 工作区](skills/dev-visual/assets/react-workspace/README.md)及[组件清单](skills/dev-visual/assets/react-workspace/catalog.md)由本 Git 仓库维护。
- [组件预览与源码复用](skills/dev-visual/references/component-preview-and-reuse.md)：可操作组件目录、完整源码文件集、快速复制到项目和定制后的差异合并；[当前验证记录](evals/dev-product/runs/2026-10-08/component-gallery/report.md)。
- [Ant Design 能力联用](skills/dev-visual/references/ant-design-capabilities.md)：B 端优先官方现成组件，按需联合官方 Skill、CLI 或 MCP，支持任务范围内自主接入；[临时项目核验记录](evals/dev-product/runs/2026-10-08/ant-design-capabilities/report.md)。
- [职责能力目录](skills/dev-flow/references/role-capabilities.md)：六职责四十八项能力与执行契约。
- [项目迭代目录协议](skills/dev-flow/references/design-document-contract.md)：每轮集中保存各阶段产物，项目级基线持续复用；[迭代索引模板](skills/dev-flow/assets/templates/iteration-index.md)。
- [项目资产持续沉淀](skills/dev-flow/references/project-asset-maintenance.md)：现行资产、更新、有效性与后续复用。
- [分支、worktree、验证与合并](skills/dev-flow/references/git-and-worktree.md)：何时分支/隔离、阶段验证、合并条件与清理。
- [subagent 使用建议](skills/dev-flow/references/subagent-guidance.md)：两类流程的执行者选择、独立 Review、并行边界与集成责任。
- [职责 Skills 与执行者](skills/dev-flow/references/codex-agent-configuration.md)：通过 Skills 承担职责、可用性和委派边界。
- [文档与资产职责归属](docs/document-ownership.md)：七个 Skills 的权威边界、共享工具维护者与迁移说明。
- [仓库文档归类](docs/document-organization.md)：执行参考、建设计划和验证证据的边界。
- [职责建设与验证](docs/agent-development.md)、[初期总体建设方案](docs/plans/2026-10-07-development-harness-plan.md)和[能力/资产建设原始方案](docs/plans/2026-10-07-role-capabilities-and-project-assets.md)：仓库建设资料。
- [测试先行、系统诊断与实现评审改造计划](docs/plans/2026-10-09-executable-engineering-methods.md)：补齐执行方法、记录字段和行为评测，沿用现有六职责；当前待实施。
- [Codex 配置历史](docs/history/2026-10-08-codex-agent-setup.md)、[Ant Design 接入核验](docs/integrations/ant-design.md)及[共享组件验证](docs/integrations/shared-components.md)：历史事实与证据入口。

## 插件安装与使用

```sh
python3 scripts/manage_plugin.py install
python3 scripts/manage_plugin.py check
```

插件包含七个 Skills：流程入口及产品、视觉、架构、研发、测试验收、运维交付。没有 setup Agent 步骤，安装不注册个人角色或改写全局指引。使用 `$dev-flow` 按[任务路由](skills/dev-flow/references/task-routing.md)选择 bugfix、正常需求、系统变更或故障流程；主 Agent 或实际可用且获准委派的子 Agent 读取专业 Skill。模型由宿主与用户本次要求决定。安装详情见[指南](docs/plugin.md)。

## 下一项建设

产品 v0.8、视觉 v0.1、架构 v0.3、测试验收 v0.3、研发 v0.2 与运维交付 v0.1 已定义专业方法与项目资产维护。运维的源码包启动、运行故障与恢复工具案例见[首版验证](evals/dev-operations/report.md)，研发隔离修复案例见[记录](evals/dev-engineering/report.md)，测试执行范围见[记录](evals/dev-acceptance/report.md)，架构规范检查见[记录](reviews/2026-10-08-architecture-code-standards-check.md)。历史原型/组件证据保持原版本，见[视觉与文档验证](evals/dev-visual/runs/2026-10-08/visual-and-documents/report.md)。总纲 v0.13 增加架构后端到端技术方案、符合性及用例 AI Review/人工确认，见[调整记录](reviews/2026-10-08-technical-delivery-stage.md)；保留运行/交付资产和 v0.11 的[设计与实现路由边界](reviews/2026-10-08-prototype-review-routing.md)及确认/自主实施规则。下一步选择真实任务检验完整循环和下一任务资产复用；实际委派/模型设置与真实项目分别实测，本地 Plugin 已接入，见[安装验证](reviews/2026-10-09-setup-removal-and-task-routing.md)；运行内核继续按真实任务需要建设。

## 解除插件

运行 `python3 scripts/manage_plugin.py remove`，或使用宿主插件卸载入口。当前安装没有额外 Agent 接入需要解除，源码与业务项目资产保留。
