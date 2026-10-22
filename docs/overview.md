# Dev Flow 当前能力概览

日期：2026-10-22。当前源码 Plugin **0.4.1**、流程总纲 **0.30**，共 **16 个 Skill** 和六职责提示词。本轮唯一总体状态是[重组 Progress](plans/2026-10-21-agent-skill-reorganization/Progress.md)，验证与安装分别见[验收记录](plans/2026-10-21-agent-skill-reorganization/verification.md)和[安装指南](plugin.md)。版本声明不替代实际启用、缓存和新会话发现结果。

## 能力分层

| 层次 | 权威位置 | 回答的问题 |
| --- | --- | --- |
| 流程编排 | [dev-flow](../skills/dev-flow/SKILL.md) | 何时、由谁、依赖什么、如何确认/变更/完成 |
| 专业职责 | [agents/prompts](../agents/prompts/) | 专业目标、判断、边界、交接和成果责任 |
| 长篇专业参考与职责资产 | [agents/references](../agents/references/)、[agents/assets](../agents/assets/) | 规范、评审清单、设计/计划/收尾模板和配置 |
| 可复用操作 | [capabilities.json](../capabilities.json) 中的 Skills | 明确输入、操作方法、工具和可核验输出 |
| 项目事实 | 所属项目有效资产及源码 | 当前规则、版本、技术基线、实现和运行结果 |

六职责为[产品](../agents/prompts/product.md)、[视觉](../agents/prompts/visual.md)、[架构](../agents/prompts/architecture.md)、[研发](../agents/prompts/engineering.md)、[测试验收](../agents/prompts/acceptance.md)、[运维交付](../agents/prompts/operations.md)。提示词包含本质专业责任，具体操作按需调用 Skill；不再通过六个旧职责 Skill 转读才能工作。

三个公共操作分别是[Git](../skills/git-workflow/SKILL.md)、[subagent](../skills/subagent-coordination/SKILL.md)、[文档管理](../skills/document-management/SKILL.md)。Git保存/集成不裁定业务验收；派发/结果收集不等于专业通过；文档归档不自动表示整体完成。

专业操作覆盖产品规格、原型、组件接入、呈现检查、代码地图、回归、诊断、正式用例、验收执行、运行、发布恢复；会话监控保持独立授权范围。完整清单见[README](../README.md)。

## 协作与完成

[总纲](../skills/dev-flow/references/constitution.md)和[执行协议](../skills/dev-flow/references/execution-contract.md)保留有效产品/UI与真实代码技术反馈、研发统一设计及独立Review/计划复核、明确范围实施授权、连续实现/集成/自测、完整候选后正式TC/独立Review/验收交付、架构技术收尾。快速路径仍须有效授权，已有同范围授权不重复请求。

设计原型由产品/视觉走查，正式实现验收由测试主责；工具和Mock不改变对象。完整变更评审覆盖开始基线至最终候选，区分需求符合性和实现质量；修复后实际复评/复验，不凭“已修改”关闭。

主Agent维护唯一总体进度和最终目标，实际子Agent承担有边界的任务。不能委派时如实记录自查及独立性限制，不能把角色配置、等待结束或状态核验通过当作真实专业结果。

“开始收尾”进入[收尾流程](../skills/dev-flow/references/closeout.md)，由专业职责核对结果，再调用Git保存与文档组织归档。阶段未执行/受阻、证据失效和交付缺口保持真实未完成；用户明确只整理文档时按范围裁剪。

## 本轮迁移与验证入口

- [设计与归纳图](plans/2026-10-21-agent-skill-reorganization.md)、[逐文件迁移](plans/2026-10-21-agent-skill-reorganization/migration-plan.md)、[正式验收用例](plans/2026-10-21-agent-skill-reorganization/acceptance-cases.md)。
- [实现Review](../reviews/2026-10-21-agent-skill-reorganization-implementation.md)、[规划边界Review](../reviews/2026-10-21-agent-skill-reorganization-boundaries.md)。
- [文档归类](document-organization.md)、[权威归属](document-ownership.md)、[生成器](../scripts/sync_host_agents.py)和[能力声明](../capabilities.json)。

Codex参考入口不自动注册个人角色；Kimi生成原生入口且需分别安装/重载。按用户本轮选择先完成Codex，Kimi留待原生会话更新。新会话的能力刷新、隔离工具样本、Harness专业演练、原生角色发现和真实项目验证分别登记。

历史建设、48项能力编号与旧版本评测保留原事实，[旧能力目录](history/2026-10-21-role-capabilities.md)可追溯；不以旧结果宣称新结构已通过。未来按真实调用需要提取操作Skill，不按角色名或文档数量增加入口。

主干集成维护版 0.4.1 保留既有技术图示规范，迁入职责参考、示例和统一设计模板；实际验证与交付见[收尾记录](../reviews/2026-10-22-main-integration.md)。
