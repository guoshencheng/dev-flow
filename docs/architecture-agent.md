---

> 2026-10-21 结构调整：当前专业责任源为 [agents/prompts/architecture.md](../agents/prompts/architecture.md)，操作路由见 [能力清单](../capabilities.json)。长篇规范和模板随职责参考/资产或对应操作 Skill。下文首版建设及既有验证记录保留历史版本事实；本轮实际结果见[实施进度](plans/2026-10-21-agent-skill-reorganization/Progress.md)，不因迁移自动视为行为或原生派发通过。
id: ROLE-dev-architecture
title: 架构设计与演进 Agent
status: current
version: 0.6
owner: architecture
---

# 架构职责现状

更新日期：2026-10-21。专业入口为[dev-architecture](../agents/prompts/architecture.md)。本轮新流程已有源码、安装及隔离代表场景证据，尚未以真实业务 UI 项目验证完整协作；历史评测只证明各自原对象与范围。

架构在产品/UI 候选期间基于真实代码反馈功能位置、交互形式、成本及状态 UI 的必要性。完整功能的架构和具体实现由研发主笔统一写入 `engineering/design.md`，架构执行者独立 Review 模块、依赖、契约、数据、权限与恢复；发现和定向复核写入 `engineering/review.md`。项目总架构作为长期唯一基线，所有迭代架构变化含重大系统调整统一写入研发设计；收尾依据实际有效结果更新总架构并记录版本与来源。

架构独立复核 `engineering/implementation-plan.md` 的依赖、测试保护、集成及交付。实施前核对有效业务完成标准、设计/计划 Review 与授权；正式 TC 在完整实现后维护、独立 Review 并执行。完整候选形成后架构独立 Review 全部代码变化；实际验收和交付核验后在 `architecture/closeout.md` 核对设计差异、真实结果、长期资产和遗留。模板见[技术收尾](../agents/assets/architecture/templates/architecture-closeout.md)。

标准领域任务在 Harness 可用且允许委派时默认使用专业 subagent，作者和独立评审分离；整体进度只由唯一 Todo/Progress 维护。旧项目有效权威文件可索引映射复用。模型与强度按用户本次要求及宿主配置，不固化到专业方法。

## 具体能力与产物

| 能力 | 当前指导与项目产物 |
| --- | --- |
| A01 系统理解 | 从真实入口追踪业务、数据与运行组成，输出有源码依据和覆盖边界的系统地图 |
| A02 模块划分 | 细化业务域/层次、目录映射、分工与不负责事项、允许依赖、数据所有权及公开契约；结合代码规范检查真实边界 |
| A03 接口契约 | 用例/API/事件、错误、兼容与必要幂等语义，关联权威接口定义和消费方 |
| A04 数据与不变量 | 数据语义、状态/规则、读写责任、事务/并发与适用迁移，关联真实验证 |
| A05 技术与质量取舍 | 复用已定技术约定，核对规范、入口、代码工具链与交付并维护基线；根据实际目标确定性能/可靠性/容量/成本假设和测量证据 |
| A06 信任与权限 | 身份/租户、数据访问、可信执行边界和对应正向/拒绝检查 |
| A07 演进与恢复 | 分阶段变化、兼容期、数据检查、切换/恢复条件，避免将代码回滚当成数据恢复 |
| A08 复盘与维护 | 完整实现独立 Review、技术收尾、现状/模块地图更新与有证据的改动建议 |

首版重点 A01/A02/A03/A08，涉及数据时同时落实 A04；当前 A05 保留三类技术约定和持续基线，代码规范支撑 A02/A05。指导覆盖与实际验证分开，配置存在不表示全部能力已经成熟。

## 专业内容如何拆分

- [整洁架构](../agents/references/architecture/clean-architecture.md)：领域、应用、适配、基础设施和装配的职责，跨域边界、React/后端/CLI/库、轻量和遗留工程。
- [系统与模块地图](../skills/codebase-mapping/references/system-and-module-map.md)：从业务链路读真实代码，目录 ↔ 模块 ↔ 域/层次，实际依赖、合理性和证据覆盖。
- [设计与契约](../agents/references/architecture/design-and-contracts.md)：重要选择、可执行 ARC 约束、接口/数据/权限/运行，以及 AI 计划复核和研发测试对焦。
- [复盘与演进](../agents/references/architecture/review-and-closeout.md)：参与时机、代码业务 Review、优先级、具体建议与改进关闭。
- [项目资产](../skills/document-management/references/professional-assets.md#架构)：现状、目标、决策、复盘、债务的目录和归档、版本核验及下一任务复用。
- [技术栈约定](../agents/references/architecture/technology-stack.md)：React Web、Next.js 全栈、Astro 纯静态的已定选择及项目有效基线。
- [代码规范](../agents/references/architecture/code-standards.md)：成熟格式/lint/类型方案、命名与依赖、配置源码复用、研发/CI 检查和项目规范维护。

## 研发结束后如何参与

实质研发完成后，基于最终候选、有效设计和验收证据复核相关代码业务，更新当前系统和模块分工，评价依赖、数据与业务规则的合理性。首次接入、跨域变化、迁移和重复缺陷扩大到相应影响；局部修复定向核验，无变化时记录复用。交付前必需约束与技术收尾可合并检查；设计/计划/完整实现的独立意见保存在 `engineering/review.md`。

每条建议给出代码/运行证据、业务影响、优先级、具体模块/目录/契约改动、收益与代价、实施依赖及验证/恢复方式。当前事实、有效目标、偏差和待验证风险分别记录。违反本次必需条件的问题回到修复循环；可选演进入待办。仅 Review 时不自动修改生产代码。

“实时总结”采用变更触发的持续更新：相关规则、模块、接口、数据或运行变化后重核受影响资产，并在交付复盘写回当前版本；此首版没有独立后台监听器。

## 项目文档与共享

优先沿用项目权威目录，无规范时使用 `docs/dev-flow/architecture/`：index 关联项目总架构的唯一权威位置（默认 design.md，已有 system.md 等有效位置沿用），modules 按需保存其核验/源码映射支撑，stack 保存技术/工具链和交付基线，decisions 保存重要取舍；本轮统一设计和独立 Review 在迭代 `engineering/`，技术收尾在迭代 `architecture/`，debt 关联改进。代码规范使用 `docs/dev-flow/engineering/code-standards.md` 并链接实际配置与命令。小工程允许合并，复杂业务域按需拆分。架构可在需求中、重要变更后、发布前或用户授权的定期窗口参与联合维护检查，和测试以同一版本核对 ARC/OUT/TC 关系；已验证的当前事实写回长期入口，被替代的完整方案才按协议归档，不能把最新有效架构移入历史。普通历史由 Git 保存，完整替换方案按协议归档。

随包提供[当前地图](../agents/assets/architecture/templates/current-architecture.md)、[技术基线](../agents/assets/architecture/templates/technology-baseline.md)、[项目总架构](../agents/assets/architecture/templates/architecture-design.md)、[专项代码复核](../agents/assets/architecture/templates/architecture-review.md)和[技术收尾](../agents/assets/architecture/templates/architecture-closeout.md)模板，复用共享 Vite 文档预览。项目事实留在项目，经过验证的通用方法再沉淀到本 Skill。

## 验证状态

2026-10-21 的[本轮技术收尾](plans/2026-10-21-flow-revision/architecture-closeout.md)区分四层证据：C2-62e99b8b7a6d 的完整源码独立 Review 与 P6 静态/工具检查、Plugin 0.3.0 的 Codex 实际安装及首次 check、P8 新会话/原生派发的隔离代表场景、未执行的真实业务 UI 项目。[P8 独立行为报告](../evals/dev-flow-stages/2026-10-21-behavior-report.md)对新会话发现及固定七场景逐项判通过。隔离订单备注项目另有独立[技术收尾](../.dev/runs/flow-revision/behavior-inputs/post-candidate/docs/dev-flow/iterations/order-note/architecture/closeout.md)，核对 C2 项目源码、正式 TC/CH 与本机 zipapp；该项目的 C2 与插件执行候选不是同一对象，不能从 P6 检查或合成项目推断真实业务完整交付。

v0.5 增加与测试验收的联合维护检查及逻辑归档：按用户手动或授权定期触发，核对同一版本的架构现状、ARC/OUT/TC 与实际证据，先更新当前基线，再归档迭代或被替代候选；`current`、`needs-review`、`superseded` 和 `archived` 分开表达。保留[完整实现评审与复盘](../agents/references/architecture/review-and-closeout.md)要求的开始基线至最终候选覆盖及定向复评。

本轮[行为评测](../evals/dev-flow-methods/report.md)中，独立评审者实际覆盖三提交与未提交差异，检出早期权限与未提交标题问题；研发处理后，原评审者未参与实现，定向阅读并实际断言复验，四条意见按证据关闭。模型参数为本次派发策略，不进入可复用要求；宿主共享文件系统与输入声明的证明限制单列。此证据不代表全仓审计、生产身份、并发或真实项目成熟度。

源配置、专业指导、项目资产和代表案例分别登记；本次检查与限制见[验证记录](../evals/dev-architecture/report.md)。原生发现/派发、不同模型和真实项目复用需要对应实际证据，隔离评测不能代替生产验收。

v0.1 的四个 Skill、三个 TOML 与全局链接检查通过。Sol medium 通用子 Agent 在隔离案例实际完成代码业务复盘和模块变化后的资产复用，主 Agent 核验源码/证据并复跑一致。已证明该案例中的现状恢复、域/模块地图、业务/架构偏差识别和持续更新；尚未验证 `dev_architecture` 原生派发、全新上下文与真实项目，也未将全部能力登记为成熟。

v0.2 技术选型新增指导基于只读项目调查与官方平台资料，结构、引用、职责配置和全局链接的实际检查见[本轮记录](../reviews/2026-10-08-architecture-stack-check.md)。现有隔离案例不证明新增选型能力；尚未实际运行样本项目或验证新项目采用和端到端交付。

v0.3 技术约定、代码规范与格式配置的检查见[本轮记录](../reviews/2026-10-08-architecture-code-standards-check.md)。格式工具的实际案例与其他静态/行为/真实项目检查分别登记，不将格式通过延伸为端到端验收。

已建设[测试验收职责](acceptance-agent.md)，与架构使用同一 ARC/RULE/AC 和版本化证据推进完整交付。已建设[研发职责](engineering-agent.md)与[运维交付职责](operations-agent.md)，以实际实现/环境同步运行边界和恢复条件；下一步用真实任务检验完整协作。

## Kimi 宿主接入（2026-10-09）

本职责已提供独立 Kimi Markdown Agent 入口，与 Codex 角色参考从共用 Skill 元信息生成；专业方法仍只在 Skill/参考维护。Kimi 2.1.1 已通过原生发现、派发、包内文件读取和交接的模型替身冒烟；真实模型的专业行为及项目结果尚未验证，不能将接入检查登记为专业验收。见 [适配记录](../reviews/2026-10-09-kimi-agent-adaptation.md)及 [执行说明](integrations/kimi-agent-configuration.md)。

## 服务端架构视图补充（2026-10-23，0.6.1）

[研发设计模板](../agents/assets/engineering/technical-delivery-design.md)、[项目总架构](../agents/assets/architecture/templates/architecture-design.md)与[当前地图](../agents/assets/architecture/templates/current-architecture.md)明确服务端的整洁架构分层图/源码映射、Service/Usecase 业务操作清单、具体业务时序和数据模型 ER 图；相关 Review 模板承接交叉核对。共享规则见[服务端架构视图](../agents/references/architecture/technical-diagrams.md#服务端架构视图)，[订单三图示例](../agents/assets/architecture/examples/technical-diagrams.md#服务端整洁架构分层与业务数据示例)为虚构教学资产。

本轮 0.6.1 完善模板与规范，独立复核、图示渲染、内容/引用及实际安装交付状态见[本轮 Progress](plans/2026-10-23-service-architecture-template/Progress.md)；尚未在真实业务服务上验证梳理效果，不将示例渲染等同于业务项目架构核验。

本轮补充统一总架构与迭代分工：总架构默认 `docs/dev-flow/architecture/design.md` 或项目已有权威位置，现状地图是其核验章节/支撑资料；迭代研发设计引用基线并维护架构增量，技术收尾按最终源码/产物及核验证据同步实际有效部分，记录前后版本与环境覆盖。模板、职责正文、目录/索引及相关规范同步调整，验证范围仍见同一 Progress。

## SVG 结构图表达维护（2026-10-23，0.6.2）

[技术图示规范](../agents/references/architecture/technical-diagrams.md)将结构总览、整洁架构分层、模块依赖与部署拓扑默认调整为可编辑SVG；时序、流程、状态及ER优先Mermaid。配套[示例](../agents/assets/architecture/examples/technical-diagrams.md)用独立图表达归属、源码依赖及运行拓扑，保留可编辑文字、相对嵌入和源文件入口。相关总架构、现状、研发设计和Review模板同步。

图示语义及1280宽浏览器呈现经独立复核，运行示例的云端部署边界与公网入口歧义已修正。此为方法/模板及安装交付验证，真实项目采用后的架构效果不在本轮冒认；发布、宿主实际缓存及主干状态见[本轮Progress](plans/2026-10-23-architecture-svg/Progress.md)。
