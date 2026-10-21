---

> 2026-10-21 结构调整：当前专业责任源为 [agents/prompts/engineering.md](../agents/prompts/engineering.md)，操作路由见 [能力清单](../capabilities.json)。长篇规范和模板随职责参考/资产或对应操作 Skill。下文首版建设及既有验证记录保留历史版本事实；本轮实际结果见[实施进度](plans/2026-10-21-agent-skill-reorganization/Progress.md)，不因迁移自动视为行为或原生派发通过。
id: ROLE-dev-engineering
title: 研发实现与修复 Agent
status: current
version: 0.4
owner: engineering
---

# 研发职责现状

更新日期：2026-10-21。专业入口为[dev-engineering](../agents/prompts/engineering.md)。本轮新流程已有源码、安装及隔离代表场景证据，尚未以真实业务 UI 项目验证完整协作；下列历史记录保持原验证对象和范围。

研发在产品/UI 设计期间基于真实代码反馈功能位置、交互形式和状态必要性。完整功能由研发主笔 `engineering/design.md`，合并架构与实现；独立架构执行者 Review，产品/UI 核对业务和呈现，详细意见在 `engineering/review.md`。设计有效后研发编写独立 `engineering/implementation-plan.md`，接受独立计划复核；已有同范围实施授权直接复用。正式 TC 在完整实现后维护、独立 Review 并执行，研发局部测试和回归随实施进行。

研发连续实现、集成和自测后交完整候选，架构独立 Review 完整变化，测试正式验收并执行交付核验；架构在 `architecture/closeout.md` 整合实际设计差异、Review、验证、资产和遗留。整体进度只由现行 Todo/Progress 维护，各文档引用。已有有效权威文件可以索引映射复用，不强制迁移。

标准领域工作在 Harness 可用且允许委派时默认使用专业 subagent，作者与独立评审分离，主会话负责协调和集成。模型和强度按本次用户与宿主配置，不固定在专业方法中。无法独立委派时如实记录执行方式和缺口。模板见[设计](../agents/assets/engineering/technical-delivery-design.md)、[Review](../agents/assets/engineering/engineering-review.md)和[计划](../agents/assets/engineering/implementation-plan.md)。

## 八项能力如何落实

| 能力 | 具体判断与项目产物 | 验证方式 |
| --- | --- | --- |
| E01 工程理解 | 真实入口、代码功能映射、依赖/消费者、有效规范和候选 | 对照实际源码与命令，识别过期资产和他人修改 |
| E02 方案、计划与切片 | 统一研发设计及独立跨职责 Review；有效业务预期和设计 Review 后编写独立计划并复核 | 设计忠于产品/UI/ARC，计划覆盖完整链路及交付；正式 TC 在完整实现后维护、Review 与执行 |
| E03 前端实现 | 组件、真实数据、状态/恢复、设计和规则映射 | 实际操作及相关渲染/目标设备符合基线 |
| E04 业务与接口 | 用例、输入/权限/错误、持久化与适用副作用 | 真实接口/数据结果、拒绝场景和相关不变量 |
| E05 诊断修复 | 最小复现、原因证据、实现补丁与待验候选 | 原场景与受影响回归，不能放宽验收关闭 |
| E06 兼容演进 | 重构/升级/迁移的消费者、阶段与恢复安排 | 原行为或已确认新契约成立，集成重新取证 |
| E07 工程工具 | 适用自动化、格式/lint/类型、行为与构建入口 | 实际执行并证明目标，不以实现镜像测试代替 |
| E08 集成交付 | 集成版本/锁文件、配置样例、真实运行支持和交接 | 声明环境按说明准备/启动并完成核心任务 |

专业方法分为[统一研发设计与独立 Review](../agents/references/engineering/technical-delivery-design.md)、[基线与计划](../agents/references/engineering/baseline-and-plan.md)、[切片与集成](../agents/references/engineering/slices-and-integration.md)、[前端](../agents/references/engineering/frontend-implementation.md)、[诊断与反馈](../skills/defect-diagnosis/references/diagnosis.md)、[兼容变更](../agents/references/engineering/compatible-changes.md)、[工程资产与交付](../agents/references/engineering/handoff.md)，入口按需读取。

## 职责边界与项目持续维护

研发拥有生产实现和必要工程/测试工具修改，保留他人工作。产品/视觉拥有有效语义与呈现，架构拥有边界/契约与重要取舍，测试拥有实际验收和缺陷复验，运维拥有目标环境/运行。研发可以调整内部实现和测试执行方法，不能将实现偏差改写为产品预期或更换 Mock 掩盖失败。

已有工程规范优先，没有时使用 `docs/dev-flow/engineering/index.md`、迭代 `engineering/design.md`、`engineering/review.md`、`engineering/implementation-plan.md` 和 `architecture/closeout.md` 与按需待验交接，复杂诊断关联既有缺陷记录。随包模板对应工程入口、统一设计、独立 Review、实施计划及交接；自动化和实现保留实际源码位置。统一设计方法见[专业参考](../agents/references/engineering/technical-delivery-design.md)。

项目索引关联工程、产品/UI、架构、测试及运行；每轮更新受影响设计/Review、代码映射、规范、计划、诊断/回归和交付知识，新任务读取并核验有效性。讨论/确认预览业务项目成果，Skill 方法文件使用源文件。研发结束向架构交接实际模块/契约/业务变化与证据，参与现状同步和有范围的复盘。

## 验证与后续

2026-10-21 新流程源码候选 C2-62e99b8b7a6d 的[独立完整变更 Review](../reviews/2026-10-21-flow-implementation-review.md)已关闭现行概览旧入口 F1、标准范围间接 `self` Review 冒充独立的 F2；[P6 检查](../.dev/runs/flow-revision/p6/static-review.md)覆盖四篇正式模板的 34 个实例链接、状态核验 44 项与宿主适配 6 项。0.3.0 已在 Codex 本机安装并首次 check 一致。[P8 独立行为报告](../evals/dev-flow-stages/2026-10-21-behavior-report.md)判定新会话发现及固定七个隔离场景通过，覆盖设计期真实代码成本反馈、局部修复、混合范围和订单备注 C2 的作者修复/独立复评；技术边界见[本轮收尾](plans/2026-10-21-flow-revision/architecture-closeout.md)。订单备注的独立实现 Review 关闭 IR-01，研发局部 5 项自测与正式 8 项 TC 各自记录，不互相折算。真实业务 UI 项目的产品/视觉回应和完整交付仍待验证。

2026-10-12 将[代码收尾](../skills/git-workflow/references/git-and-worktree.md#代码收尾)接入“开始收尾”，研发整理本轮完整变更，核对 Review/必要验证、相关源码/测试/文档保存与集成交付，保留无关修改并交接资源状态。方法与模板已同步，验证范围见[收尾记录](../reviews/2026-10-12-code-closeout.md)；不据此登记真实项目收尾或独立角色行为已通过。

2026-10-12 将正式实施前的状态恢复、确认覆盖和有效计划复核统一引用[共同执行协议](../skills/dev-flow/references/execution-contract.md#按当前状态推进)，并提供[迭代索引核验](../skills/dev-flow/references/stage-state.md)。这是记录一致性工具及方法更新，实际边界见[验证记录](../evals/dev-flow-stages/report.md)，不登记新增独立角色行为或真实功能协作通过。

v0.3 补[测试先行与回归有效性](../skills/regression-verification/references/test-first-and-regression.md)、假设/控制实验诊断和[实现评审意见处理](../agents/references/engineering/review-feedback.md)，计划与交接关联目标行为、失败/通过证据和测试位置。研发主责必要局部测试，验收核验证据与实际复验；低影响任务按对象裁剪。

2026-10-09 的[隔离行为评测](../evals/dev-flow-methods/report.md)已记录独立上下文中的先测后实现、事后补测旧红/新绿、无效测试与语法失败识别、三类保存丢失实验诊断及意见修复/反驳/澄清。主 Agent 复跑 T/D，R01 原评审者独立于研发实现作定向复评。宿主无文件级输入隔离，记录派发范围与实际读取声明；不等同强制沙箱盲测、生产能力或真实项目完整协作。

首版方法、配置、全局接入和隔离诊断修复记录见[验证记录](../evals/dev-engineering/report.md)。主 Agent 自查/自执行案例不代表独立角色行为；原生发现/派发、框架工程、真实项目协作和新上下文复用需要对应实测。

v0.2 增加架构后技术方案和产品符合性 Review、给测试的 OUT/链路映射；本次内容/协议检查与主 Agent 推演见[调整记录](../reviews/2026-10-08-technical-delivery-stage.md)。历史修复案例不证明新增阶段已在真实项目执行。

已建设[运维与交付职责](operations-agent.md)，研发移交实际工程候选、配置/产物与诊断入口，运维维护目标环境和运行证据。下一步用真实任务验证完整协作，再按重复操作与实际失败建设运行内核和 Plugin。

## Kimi 宿主接入（2026-10-09）

本职责已提供独立 Kimi Markdown Agent 入口，与 Codex 角色参考从共用 Skill 元信息生成；专业方法仍只在 Skill/参考维护。Kimi 2.1.1 已通过原生发现、派发、包内文件读取和交接的模型替身冒烟；真实模型的专业行为及项目结果尚未验证，不能将接入检查登记为专业验收。见 [适配记录](../reviews/2026-10-09-kimi-agent-adaptation.md)及 [执行说明](integrations/kimi-agent-configuration.md)。
