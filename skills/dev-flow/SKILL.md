---
name: dev-flow
description: 按用户最终目标编排研发路径、跨职责依赖、授权、独立 Review、实现后正式验收、交付与收尾；适用于完整功能、修复、评审、运行维护和“开始收尾”等流程任务。
---

# 研发协作流程

首次使用先读[总纲](references/constitution.md)，再按任务读取[任务路由](references/task-routing.md)、[执行协议](references/execution-contract.md)和[总体进度](references/progress-management.md)。设计文档和实施计划用中文。项目事实及有效决定从所属项目读取，不从本 Skill 推定。

本 Skill 决定阶段、职责、依赖、授权复用和整体完成条件。具体 Git 操作使用[git-workflow](../git-workflow/SKILL.md)，实际派发、等待及独立性核验使用[subagent-coordination](../subagent-coordination/SKILL.md)，文件组织、预览与归档使用[document-management](../document-management/SKILL.md)。局部 Git、文档或派发任务可单独调用对应 Skill，不因此启动完整研发流程。

## 从目标推进到完成

1. 明确最终目标、交付范围、现有有效基线和未决事项，在唯一总体进度中保留全部后续阶段；单阶段完成不等于目标完成。
2. 按行为、交互、契约和交付变化选择标准、快速、修复、系统变更、故障或探索路径。快速路径须指出具体有效预期和裁剪依据。
3. 核对设计层业务预期、重要取舍、统一研发设计 Review、计划复核及本次正式实施授权。首次进入正式实现前取得明确同意；同范围已有授权直接复用。完整正式 TC 在完整功能候选后维护，不是实施前置。
4. 组织专业职责完成当前阶段。产品/UI 候选接受真实代码技术反馈；研发统一主笔架构与实现设计，独立 Review 后形成实施计划并复核。连续实现、集成、自测后，针对完整候选做完整变更 Review、正式用例及其独立 Review、验收执行和交付核验。问题进入关联修复、定向复评和复验。
5. 基线、范围或候选变化时判断确认、Review、用例和验证证据是否受影响；只复用仍有效的结论。结束前核对全部必需结果、技术收尾、约定交付与项目沉淀。缺失项保持未完成。

“开始收尾”进入[收尾流程](references/closeout.md)：核对完整变更、验收、交付和技术收尾的状态后，分别调用 Git 与文档 Skill 完成已授权的保存和归档。明确只整理文档时按范围裁剪，不重走功能实施。

## 按对象选择职责

| 对象 | 专业职责提示词 |
| --- | --- |
| 用户任务、流程、规则、原型可用性 | [产品](../../agents/prompts/product.md) |
| 布局、Tokens、组件、响应、实际呈现 | [视觉](../../agents/prompts/visual.md) |
| 边界、契约、技术规范、独立技术 Review 与收尾 | [架构](../../agents/prompts/architecture.md) |
| 技术设计、计划、实现、诊断和自测 | [研发](../../agents/prompts/engineering.md) |
| 正式用例、实现验收、反馈与复验 | [测试验收](../../agents/prompts/acceptance.md) |
| 环境、产物、运行、发布与恢复 | [运维交付](../../agents/prompts/operations.md) |

职责按对象和问题选择，不因浏览器、Mock 或自动化工具改变主责。产品/视觉主责设计原型走查；测试可在设计期反馈可测性，正式验收面向完整实现与交付候选。需要独立 Review 时作者与评审执行者分离；实际派发受限时如实记录独立性缺口，不把自查登记为独立通过。模型和推理强度遵循用户本次要求与宿主配置。

持续或跨会话任务按[总体进度](references/progress-management.md)维护唯一状态权威。需要核对声明的候选、版本和证据依赖时使用[状态格式与只读核验器](references/stage-state.md)；核验通过不证明实际 Review、测试或交付。主 Agent 对整体依赖、结果集成和完成结论负责，派发结束或等待超时不构成任务结束。
