# 项目测试资产、目录与持续复用

先从当前业务项目的文档索引定位有效产品、UI、技术、用例、自动化和运行资料。优先维护已有权威位置；没有规范时采用以下布局，不一次生成全部空文件。

| 资产 | 默认位置/责任 |
| --- | --- |
| 测试入口 | `docs/dev-flow/acceptance/index.md`：策略、有效用例、自动化/数据/环境、缺陷、最新结果和缺口；项目主索引登记测试分类 |
| 项目策略 | `iterations/<迭代ID>/acceptance/strategy.md`：引用项目通用策略，定义本次层级/方案、实际工具、目标环境与依赖模式、必需检查、交付与回归选择 |
| 可读用例 | `iterations/<迭代ID>/acceptance/cases.md`：TC ↔ OUT/链路 ↔ RULE/AC/UI/ARC、前置/操作/预期、方案/用例版本、实际 AI Review 及人工确认来源、自动化映射 |
| 运行报告 | `iterations/<迭代ID>/acceptance/runs/<runID>/report.md`：候选、环境、真实执行、各用例结果、证据、缺陷与结论 |
| 缺陷与回归 | 复用实际 tracker；无规范时 `iterations/<迭代ID>/acceptance/defects/<缺陷ID>.md`，关联原问题/修复/复验及保护用例 |
| 自动化源码 | 项目现有 test/tests/e2e 等真实目录，按模块/层级组织；索引保存实际命令与配置路径，不复制第二套测试 |
| 数据/环境 | 项目实际 fixture/seed/环境契约，Git 保存可重复样例与准备/清理方法；凭据/认证状态留在忽略位置 |
| 必要原始证据 | 复用项目 evidence；无规范时 `docs/dev-flow/iterations/<迭代ID>/evidence/acceptance/<runID>/`；长期报告关联版本与可定位来源 |
| 历史替换 | `iterations/<迭代ID>/archive/acceptance/<资产ID>/`：必要完整旧方案/替代原因；普通修订由 Git 保存 |

表中短路径相对 `docs/dev-flow/`；迭代索引集中关联本次策略、用例、报告与证据，项目测试入口维护跨迭代回归和自动化索引。临时 runner 输出、浏览器状态和本机服务记录可放 `.dev-flow/`，新上下文不能仅依赖这些缓存恢复结论。大 trace/视频按项目资产存储约定留存，报告保留必要摘要、原始位置与版本；不要提交实际 Cookie/令牌。

按任务裁剪[策略](../assets/templates/test-strategy.md)、[用例](../assets/templates/acceptance-cases.md)、[报告](../assets/templates/acceptance-report.md)、[缺陷](../assets/templates/defect.md)模板。用户讨论/确认的是本项目可读用例，通过共同[项目文档协议](../../dev-flow/references/design-document-contract.md)与[预览指南](../../dev-flow/references/document-preview.md)提供真实入口，实际业务应用另给功能/交付入口。

任务开始核验原产品/UI/ARC 与技术方案/OUT、用例 Review/确认基线、源码/接口变化和证据版本，复用有效场景/数据，标明失效范围。方案 Review、用例 Review、人工确认及实际运行结果各有对象与版本，不能互相替代。任务结束维护场景到自动化、缺陷、证据和回归关系；下一任务从索引恢复并定向复验，不依赖聊天。架构约束或产品/UI/技术方案变化时明确影响与确认来源，不自动删除原验收编号。

通用模式和脚手架先保留适用条件、真实项目问题、反例与可重复验证，经过验证后作为共享候选；项目业务接口、凭据和数据留在项目。自有源码按复制/参考与 Git 来源约定维护，不能要求先发布内部 npm 包。
