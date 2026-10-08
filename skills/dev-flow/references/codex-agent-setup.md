# Codex 职责 Agent 的配置与建设方式

更新日期：2026-10-08。当前阶段：总纲、六职责、共同文档与原型预览。产品专业 Skill 的历史隔离行为和连续资产复用已验证；六个职责源配置逐个维护，实际全局链接、发现和派发分别验收。

本文件说明如何把[总纲](constitution.md)逐步落实为 Codex 原生职责 Agent。每次建设一个职责，并配套专业方法、项目资产协议和实际验证。

## 原生配置能力

Codex 支持个人和项目范围的自定义 Agent。个人配置放在 `~/.codex/agents/`，项目配置放在项目根目录的 `.codex/agents/`；每个 Agent 使用一个 TOML 文件。必需字段是 `name`、`description` 和 `developer_instructions`，可以同时设置模型和推理强度。[官方自定义 Agent 文档](https://learn.chatgpt.com/docs/agent-configuration/subagents)

这些文件用于派生 Agent 会话的配置。定义角色后仍需由主 Agent 按任务派发；角色定义本身不会建立长期自主运行的服务。桌面应用与 CLI、IDE 使用共同的 Codex 配置体系，具体发现和派发行为在目标宿主中实测。[官方开发者设置说明](https://learn.chatgpt.com/docs/developer-settings)

源文件在独立 `dev-flow` 仓库维护。流程与专业 Skills 通过 `~/.agents/skills/` 的逐个链接使用，全局 `AGENTS.md` 维护简短入口。原生配置通过个人 `~/.codex/agents/` 的逐个文件链接接入；隔离行为、宿主实际派发及真实项目验证分别登记。只有原生发现和执行经过验证，才登记为已启用的职责。Plugin 是否能直接分发原生 Agent 配置，需要在打包阶段核验。

## 本机已核对的情况

- CLI 为 `codex-cli 0.156.1`。
- 个人 Agent 目录逐个接入 `dev_product.toml`、`dev_visual.toml`、`dev_architecture.toml`、`dev_acceptance.toml`、`dev_engineering.toml`、`dev_operations.toml`，符号链接指向本仓库源文件；实际接入结果见安装检查，不据此声称原生发现与派发通过。
- 个人默认模型与强度继续由用户现有全局配置维护，本仓库不另设固定值。
- 现有全局配置通过 CLI 的严格配置检查；这不证明新角色已被发现或角色行为已经合格。
- `dev-flow`、`dev-product`、`dev-visual`、`dev-architecture`、`dev-acceptance`、`dev-engineering`、`dev-operations` Skills 逐个链接，当前结果见安装验证；2026-10-07 的 CLI 新上下文预览已发现前两个 Skills 并加载全局流程指引。链接和专业指导评测不证明新增角色的原生发现与派发。
- v0.1 原生派发试跑在父任务调用 `gpt-6.1-sol` 时被 CLI 账号通道拒绝，未发生子角色派发。当时的 Sol medium 子 Agent 执行了同一专业 Skill；这仅证明专业指导在该执行方式下的行为。

当前职责配置省略 `model` 与 `model_reasoning_effort`。Codex 依次从本次显式派发、全局 `[agents]` 默认和父会话取得这些设置；派发或全局默认只选择模型而没有强度时，采用该模型默认强度。职责文件若设置这些字段，会覆盖之前解析出的选择，因此本仓库默认由调用方与宿主配置管理模型。具体任务遵循用户最新要求，实际执行设置进入验证记录。[官方配置优先级说明](https://learn.chatgpt.com/docs/agent-configuration/subagents)

## 四类内容各自维护

| 内容 | 用途 |
| --- | --- |
| 原生 Agent TOML | 角色名称、适用任务、最小执行要求与交接方式；默认省略模型与强度 |
| 专业 Skill 与参考 | 按能力提供方法、工具、示例和评测，随任务按需读取 |
| 项目长期资产 | 当前项目有效的用户流程、交互规则、设计系统、契约、回归和运行知识 |
| 总纲 | 各职责共同遵守的协作、证据、交付与沉淀协议 |

Skill 中的 `agents/openai.yaml` 用于该 Skill 的界面元信息与调用策略。原生职责 Agent 使用这里说明的 TOML 文件；建设时分别管理两者。

在配置中写下文档路径或角色名称，不会自动注入全部专业知识。配置要明确什么时候读取哪个入口；主 Agent 派发时提供有效路径、输入版本和可写范围。随包分发的引用需要在实际安装位置核验。

## 首个职责：产品与交互

实际源文件是[dev_product.toml](../../../agents/dev_product.toml)，角色名为 `dev_product`，没有固定模型或推理强度。配置要求开始时读取全局 `dev-product` Skill，再按需读取共同协议、专业方法和项目入口。

配套[专业 Skill](../../dev-product/SKILL.md)细化流程与状态、规则与验收、验证与交接、项目资产持续维护四类方法。设计与能力状态见[职责说明](../../../docs/product-agent.md)，实际案例与调用方式见[验证记录](../../../evals/dev-product/README.md)。

当前先使用专业 Skill 承担产品工作；需要原生派发时，在支持所选模型的宿主核验实际发现、派发和模型设置。后续职责沿用这四部分结构，根据代表任务细化能力和失败处理。

## 视觉职责

[dev_visual.toml](../../../agents/dev_visual.toml) 与 [dev-visual Skill](../../dev-visual/SKILL.md)维护参考与方向、设计系统、页面呈现、实际渲染检查、交接与资产复用。产品与视觉使用[共同文档协议](design-document-contract.md)和[统一预览工具](document-preview.md)，分别负责规则与呈现。当前完成指导、配置、工具和模拟案例检查；独立专业行为、原生派发及真实项目复用仍需验证，见[视觉职责说明](../../../docs/visual-agent.md)。

## 架构职责

[dev_architecture.toml](../../../agents/dev_architecture.toml) 与 [dev-architecture Skill](../../dev-architecture/SKILL.md)细化整洁架构、技术与代码规范基线、业务域/模块责任、接口/数据契约、实际代码复核与研发后的架构复盘。当前技术 Guide 只定义 React Web、Next.js 全栈与 Astro 纯静态；以当前源码维护系统和目录模块地图、合理性判断与改进建议，复用共同确认协议、文档预览和 Git 资产，配置无固定模型。专业产物和验证范围见[架构职责说明](../../../docs/architecture-agent.md)、[v0.1 行为验证](../../../evals/dev-architecture/report.md)、[v0.2 历史选型检查](../../../reviews/2026-10-08-architecture-stack-check.md)与[v0.3 规范检查](../../../reviews/2026-10-08-architecture-code-standards-check.md)。

## 测试验收职责

[dev_acceptance.toml](../../../agents/dev_acceptance.toml) 与 [dev-acceptance Skill](../../dev-acceptance/SKILL.md)定义可确认的用例与策略，分别指导前端交互、真实接口/数据、前后端 E2E、交付与回归。依据有效 RULE/AC/ARC 执行，持续反馈研发、复验原问题和相关回归，保留 Mock 边界、失败/跳过/不稳定与当前版本证据；项目维护策略/用例/报告和回归资产。配置不固定模型，工具与行为、原生派发与真实项目证据见[职责说明](../../../docs/acceptance-agent.md)和[首版验证](../../../evals/dev-acceptance/report.md)。

## 研发职责

[dev_engineering.toml](../../../agents/dev_engineering.toml) 与 [dev-engineering Skill](../../dev-engineering/SKILL.md)细化工程基线与代码映射、实现计划和 AI 复核、整洁架构下的可运行切片、前后端实现、证据诊断与测试复验、兼容重构/升级/迁移、集成和可启动交接。项目持续维护工程/运行资产，已确认基线不由实现反推，内部步骤自主调整；配置无固定模型，当前行为和接入边界见[职责说明](../../../docs/engineering-agent.md)与[首版验证](../../../evals/dev-engineering/report.md)。

## 运维与交付职责

运维职责见[dev_operations.toml](../../../agents/dev_operations.toml) 与 [dev-operations Skill](../../dev-operations/SKILL.md)，细化环境/启动、产物版本/实际发布、存活/就绪/业务信号、故障恢复、应用回退/数据恢复与迁移、依赖资源及退役交接。运行资产在项目 README/runbook 或按需 `docs/dev-flow/operations/` 持续维护；外部动作依实际授权，未知发布先查询，配置无固定模型。方法与接入状态见[职责说明](../../../docs/operations-agent.md)，隔离源码包/HTTP 数据恢复工具案例见[首版验证](../../../evals/dev-operations/report.md)。

## 逐个建设的交付和验收

每个职责交付四部分：原生配置、关键能力参考、项目资产读写规则、代表案例与验证记录。六个候选角色名是 `dev_product`、`dev_visual`、`dev_acceptance`、`dev_engineering`、`dev_operations` 和 `dev_architecture`。使用独立名称，保留宿主已有内置角色。

验证按四层记录，前一层通过不能代替后一层：

1. 静态检查：TOML 合法，必需字段和文件引用正确；默认没有职责级模型覆盖，显式例外应有用户依据。
2. 宿主发现：新会话能够发现并派发该角色，实际模型和推理强度符合要求。
3. 专业行为：代表任务产生合格成果，输入缺失、职责冲突和验收缺口处理正确。
4. 项目复用：下一任务或新上下文读取并实际使用上一任务的有效资产，能识别失效部分。

若当前版本没有发现角色或派发工具不能选择它，保留专业成果，由主 Agent 明确接管，并记录宿主适配缺口。以实际发现和派发结果决定下一步配置修正，不把一次普通配置检查当成启用成功。

建设顺序和每个职责的首次验证重点以[总纲中的建设顺序](constitution.md#当前建设顺序)为准。六职责首版现已定义，证据分别登记，后续真实任务检验完整循环与资产复用。各职责接入[确认与自主实施协议](execution-contract.md)，用户确认设计与验收预期，实现计划由 AI 复核，相关职责相互反馈并分别维护专业资产。
