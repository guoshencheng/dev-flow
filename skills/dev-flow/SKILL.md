---
name: dev-flow
description: 组织研发、产品交互、视觉、架构、测试验收与运维交付任务，推进连续实现与集成、完整候选集中验收和项目资产复用；识别实施中的需求变化并同步基线、用例与端到端门槛；按用户要求裁剪范围，适用于完整功能、修复、评审、交付或运行维护工作。
---

# 研发协作入口

首次使用读取[总纲](references/constitution.md)。从用户目标和当前项目事实确定交付范围，复用有效决定；设计文档与实现计划使用中文。共同依赖、确认和完成规则以[执行协议](references/execution-contract.md)为准。

## 每次按阶段推进

1. **恢复状态**：明确业务项目和根路径，从项目入口与本轮迭代索引读取当前范围、阶段、产物版本、确认来源、Review、候选及未完成项。历史总结不能代替现行基线。
2. **选择路径**：按[任务路由](references/task-routing.md)逐范围判断。混合请求分别裁剪并写依据；小改动不能替新增平台/完整行为裁掉前置，有效基线内修复也不重新制造审批。
3. **核对前置**：实施前核验受影响设计与用例确认、实际 Review 和计划复核。用户答复只覆盖明确对象/版本/范围；需要决定时展示可审阅成果与实际预览，同时继续独立的已授权工作。
4. **执行当前工作**：读取下表中的相关专业 Skill，完成真实操作。完整功能连续实现、集成与自测，完整候选集中实现 Review/验收，问题按关联范围修复并定向复评/复验。用户提出行为、契约或交付变化时先走[变更闸门](references/execution-contract.md#实施中的需求变更闸门)。
5. **更新并继续**：更新现有索引的有效状态和成果引用；按必需 TC/检查汇总结果，再决定下一步。必需结果未执行、受阻或失效时保持未完成，不以测试数量或阶段成果报告任务完成。

持续实现、多阶段、跨会话接手或含不同证据层级的任务，在现有迭代索引采用[状态格式与核验器](references/stage-state.md)。进入受影响实现、基线变化后和结束前运行核验；已有项目工具能同等检查时复用。局部一次性任务可用同等简短记录，不为工具另建台账。工具仅核验已声明记录，不证明真实执行、不判断设计质量、不拦截操作；主 Agent 仍对前置与完成判断负责。

## 按对象读取职责

| 工作对象 | 专业入口 |
| --- | --- |
| 用户任务、流程、规则、原型与可用性 | [产品](../dev-product/SKILL.md) |
| UI、Tokens、组件、响应与实际呈现 | [视觉](../dev-visual/SKILL.md) |
| 系统/模块、契约、技术基线与代码复盘 | [架构](../dev-architecture/SKILL.md) |
| 技术方案、计划、实现、诊断与自测 | [研发](../dev-engineering/SKILL.md) |
| 测试策略/用例、实现验收、反馈与复验 | [测试验收](../dev-acceptance/SKILL.md) |
| 环境/启动、产物/发布、运行与恢复 | [运维交付](../dev-operations/SKILL.md) |
| 会话进度、阻塞、完成与授权摘要通知 | [会话监控](../codex-session-monitor/SKILL.md) |

先按阶段、对象和问题确定职责。产品/视觉主责设计文档与原型走查，测试早期提供覆盖/可测性意见，正式验收面向可运行实现及交付候选；能点击、Mock 或自动化工具不改变对象。技术方案和计划默认没有额外人工审批。

未委派时主 Agent 读取相应 Skill 承担工作；需要且获准时再使用实际可用子 Agent，提供输入版本、成果位置、写入边界与验收要求，共享文件明确写入者。模型/推理强度遵循用户和宿主本次设置。自查、委派评审和独立复核如实记录；派发或等待超时不构成结束，生命周期按[执行协议](references/execution-contract.md#实施与正式验收的边界)处理。

## 工程与项目资产

开始写入前按[分支/worktree 建议](references/git-and-worktree.md)核对基线、现有修改、目标分支和工作位置；执行者选择遵守[subagent 使用建议](references/subagent-guidance.md)及当前委派权限。实现/修复按研发的[测试保护](../dev-engineering/references/test-first-and-regression.md)和[诊断方法](../dev-engineering/references/diagnosis-and-feedback.md)进行，实际实现 Review 检查[完整变更](../dev-architecture/references/retrospective-and-evolution.md)，按[意见闭环](../dev-engineering/references/review-feedback.md)处理。

项目知识保存在所属项目。迭代索引关联范围、版本、Review、确认与结果，阶段产物按 `docs/dev-flow/iterations/<迭代ID>/` 维护；长期资产通过项目入口引用。建文档、委派写入和提交采用[文档协议](references/design-document-contract.md#agent-文档控制)，单次运行/Review 过程默认保存在忽略的本机目录，交接只提炼接手所需内容。

UI 按[视觉资产协议](../dev-visual/references/project-assets.md)持续维护独立规范、各端页面/组件规格和源码，总览组合展示。迭代只引用现行资产、记录版本与增量；无变化不创建 UI 文件，少量变化合并到索引，复杂时按需拆变更记录，不因阶段产物按迭代组织而重写完整 UI。

讨论/确认/交付项目设计时按[文档预览](references/document-preview.md)复用或启动业务项目的阅读入口，提供真实文档/原型地址；维护 Skill 本身不默认进入项目预览。结束时同步项目入口及相关长期资产，交接给出范围、版本、成果入口、实际证据、未执行项和能力缺口；区分实现、自测、验收、可运行交付及部署。

## 按需深入

- 职责边界、实际执行与可用性：[能力目录](references/role-capabilities.md)、[职责执行说明](references/codex-agent-configuration.md)。
- 资产复用、整理与归档：[持续沉淀](references/project-asset-maintenance.md)、[文档归档](references/document-archive.md)。
- 安装/更新/诊断插件：[安装指南](../../docs/plugin.md)。不要求初始化 Agent。
- 会话监控/通知：[监控 Skill](../codex-session-monitor/SKILL.md)。会话范围、收件人、身份和定期调度须明确授权。

安装检查、核验器测试、专业行为、原生派发与真实项目验证分别登记，不能互相折算。
