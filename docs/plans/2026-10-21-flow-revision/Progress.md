---
id: flow-revision-progress-2026-10-21
title: Dev Flow 流程调整 · 整体计划与进度
status: complete
version: "0.3"
owner: coordinator
updated: 2026-10-21
---

# Dev Flow 流程调整 · 整体计划与进度

**本轮整体已完成。P1–P8 的必需改造、独立 Review、正式验收、安装/新会话验证和架构收尾均已完成；Dev Flow 0.3.0 已实际安装，源码与缓存核验通过。**

本页覆盖从方案到插件生效及验证的完整工作范围。阶段完成只关闭该阶段，后续事项继续保留；不能因为本次会话完成了方案整理，就把整体任务标成完成。

## 从哪里看计划

- **这次插件改造的整体安排**：本页“完整阶段计划”展示所有阶段、依赖、完成条件和实际状态；详细任务见[本次改造整体实施计划](implementation-plan.md)。
- **调整后的通用研发流程**：[研发协作新流程方案](../2026-10-21-flow-revision.md)，说明未来业务项目怎样运行。
- **当前有效设计**：流程方案及四篇讨论模板已形成；源码及已安装插件均为 0.3.0；执行候选 C2-62e99b8b7a6d，文档/运行结果另有引用，本地实现提交为 `0696a8e`，收尾后的安装核验另保留实际记录。

## 当前在哪里

- 当前阶段：**本轮已完成**，已完成阶段与原始成果见下表和文档入口。
- 本轮结果：0.3.0 新流程、正式模板、完整进度协议和状态工具已落地；全部适用正式检查通过。
- 已保存：实现与验证提交 `0696a8e`；正式验收总表和独立架构收尾完成，当前安装缓存为 `/Users/guoshencheng/.codex/plugins/cache/dev-flow-local/dev-flow/0.3.0`。
- 后续承接：在另一个明确指定的真实业务 UI 项目验证产品/视觉实际回应、完整交付和下一任务资产复用；尚未启动，不纳入本轮已完成结果。
- 本轮未完成项：**无必需交付遗留**；真实业务 UI、Kimi 原生运行及其余 11 个扩展策略输入未验证，边界见末尾。
- 阻塞/待决：本轮无阻塞；后续能力验证须有独立任务和具体项目，不以本轮隔离结果预填通过。
- 工作位置：`/Users/guoshencheng/Documents/work/dev-flow`，分支 `codex/engineering-document-template-preview`。

## 完整阶段计划

| 阶段 | 实际状态 | 主要工作与完成条件 |
| --- | --- | --- |
| **P1 方案与讨论模板** | **已完成** | 跨职责 Review、subagent、后置验收与进度管理方案形成；四篇讨论模板形成；方案 0.2 / 模板 0.4 的独立 Review 发现已修订复核。完整进度范围的补充 Review 已完成 |
| **P2 整体实施计划与 Review** | **已完成** | 实施计划 0.2 已形成；独立评审核对完整范围与唯一进度来源，计划引用和派发状态滞后已修订复核；P2 时已将后续 P3–P8 列全，当前执行状态见本表 |
| **P3 共同协议改造** | **已完成** | 修改总纲、执行协议、任务路由和文档约定，统一设计期技术反馈、四篇文档、用例后置及完整进度范围，清除相互冲突的现行入口 |
| **P4 专业职责与 Harness 执行** | **已完成** | 同步产品/UI/架构/研发/验收/运维职责、默认派发、作者与评审分离、窄上下文、等待/恢复与唯一写入者；跨职责交接能够闭环 |
| **P5 正式模板与状态/工具适配** | **已完成** | 将讨论稿落实为正式模板；更新迭代入口、Progress、状态说明、夹具及行为评测，核验完整 TC 不再前置且验收/交付仍是完成条件 |
| **P6 完整候选 Review 与后置验收** | **已完成** | 面向全部变更独立 Review；维护并 Review 本次改造的验收检查，执行相关工具/文档/行为检查；修复问题并定向复验 |
| **P7 版本升级与安装核验** | **已完成** | 按最终兼容影响升级版本，同步两份 manifest、宿主清单和版本说明；构建安装、check 核验实际启用、缓存版本与源码指纹；不将 Codex 安装结果视为其他宿主已更新 |
| **P8 运行验证与架构收尾** | **已完成** | 核验新会话能力发现及代表场景中的派发、交叉 Review、后置验收和进度恢复；架构核对长期资产与遗留，完成整体交接。缺少必需运行证据时保留待验证 |

依赖顺序：**P1 → P2 → P3/P4 → P5 → P6 → P7 → P8**。P3/P4 仅在输入稳定、共享文件明确唯一写入者后并行；P6 发现问题回到对应工作项修复。P7/P8 发现与安装或流程行为有关的问题时恢复相关工作，更新候选和受影响验证。

## 已完成阶段的证据

以下是 P1 的内部工作记录，不代表后续 P2–P8 已完成。

| 已完成事项 | 实际执行与结果 |
| --- | --- |
| 现行协议与用户要求恢复 | 已读取总纲、执行/派发/状态约定，确认本轮四篇文档及新增要求 |
| 三项领域分析 | `cross_role_review`、`post_implementation_acceptance`、`harness_progress` 完成只读分析，结论已综合 |
| 方案与讨论模板 | 形成流程方案 0.2 与四篇模板 0.4，讨论稿未替换现行源码模板 |
| 独立 Review 与修订 | `review_flow_candidate` 检出 F1/F2，两项经修订与定向复核关闭，原结论只覆盖当时方案与模板 |
| 文档预览与引用 | 七份文档引用/空白核验通过；实际打开方案和 Review 网页，文档预览服务可用 |

## 实际派发与接手

| 子任务 | 当前对象与写入边界 | 实际状态及下一步 |
| --- | --- | --- |
| cross_role_review | 早期技术反馈与跨职责 Review，只读分析 | P1 已完成；没有正在进行的插件修改 |
| post_implementation_acceptance | 用例后置与工具依赖，只读分析 | P1 已完成；没有正在进行的插件修改 |
| harness_progress | 仅编写本次改造整体实施计划 | P2 已完成，计划 0.2 已交付并通过独立 Review |
| review_flow_candidate | 独立评审新计划、完整进度范围与通用规则 | P2 已完成；补充 Review 通过，未执行 P3–P8 的验证 |

当前实际实现派发：

| 子任务 | 唯一写入范围 | 状态 |
| --- | --- | --- |
| engineering_architecture_implementation | 研发/架构 Skills、参考与模板，相关职责现状 | 已交付；保留原能力与历史验证导航 |
| roles_harness_implementation | 产品/视觉/运维及 Harness、进度指南/模板，相关现状 | 已交付 |
| acceptance_state_implementation | 验收 Skill、状态说明、迭代模板/样例、核验器必要变化及测试/评测 | 已交付；独立 Review 的 self 冒充及间接依赖问题修复后 44 项单测通过 |
| 主 Agent | 总纲、共同执行/目录/路由、能力索引、版本/集成及整体进度 | 已集成、保存实现提交并完成安装核验 |

当前正式 Review/验收派发：

| 子任务 | 范围 | 状态 |
| --- | --- | --- |
| complete_candidate_review | 基线至当前完整候选的需求符合性/实现质量 | F1/F2（含间接依赖反例）已独立复核关闭，完整源码 Review 通过 |
| acceptance_cases_author | 本轮正式验收用例及检查，未获独立覆盖 Review 前不执行正式验收 | P6/P7/P8 全部适用检查及 CHK-11B 汇总通过 |
| business_and_case_review | 业务/文档符合性与正式用例独立覆盖 Review | B1/B2、A1–A4 已关闭，覆盖 Review 通过 |
| behavior_fixture_author | 仅后置验收/交付隔离夹具与独立判据 | 已交付；夹具可运行自查通过，不替正式场景执行 |

P8 实际派发与下一步：

| 执行者/场景 | 唯一对象与范围 | 状态及接手 |
| --- | --- | --- |
| fresh Codex exec：发现与四个 CLI 场景 | 各自隔离项目和独立新上下文 | 已执行；新会话发现、局部修复、混合范围、证据边界与 Progress 恢复已独立评判 |
| proposal_cost_behavior / proposal_independent_review_behavior | 设计期代码/成本反馈与另一原生上下文的独立 Review | 本阶段已通过；作者已同步主设计引用，产品/UI 实际回应与后续业务阶段不在本场景范围 |
| post_candidate_acceptance_execution | 仅后置用例、实际验收/交付及项目进度/引用 | v2 用例、8项检查、30进程/45断言及源码外zipapp已独立核对，项目架构收尾/引用集成完成 |
| post_candidate_code_repair / post_candidate_independent_review | 仅隔离 CLI 修复/研发测试，以及独立 Review | AR-01/IR-01 修订后复核关闭；不把局部研发测试折算为正式验收 |
| business_and_case_review | 独立评判输入/动作/结果与证据边界 | 七场景与新会话发现最终通过，文档时态与引用遗留均已关闭 |
| 架构技术收尾 | 当前候选、Review、验收/安装/发现结果与长期资产 | complete_candidate_review 已完成技术收尾及相关长期资产更新；最终总表/提交/安装同步由主协调者完成 |

候选源码版本已调整为 0.3.0（总纲 0.29、执行协议 0.13），已实际安装，首次 check 通过。状态核验 44 项、隔离安装契约 6 项已通过；宿主适配回归发现旧用例仍按七个 Skills 断言，已按实际八个 Skills 修订并复验。P6 的44/6/6测试、四模板34链接及十个合成 CLI 场景已通过。新会话已发现当前0.3.0，P8 的独立行为汇总、后置交付和架构收尾均已闭环。

实施基线：`503fcb4768a658772fd4648ec19b7ceedcd5a1ac`。用户在展示完整计划后回复“继续吧”，覆盖本轮已列明的改造、Review、验证和本地插件安装；不扩大到远端推送、合并或其他项目发布。

本次既有派发使用 `gpt-6-sol / medium`，只作为执行事实保存。表中实际执行者及产物均已核对；历史拟派发不作为执行证据。

## 文档与成果入口

- [本次改造整体实施计划](implementation-plan.md)

- [通用研发流程方案](../2026-10-21-flow-revision.md)
- [完整实现 Review](../../../reviews/2026-10-21-flow-implementation-review.md)
- [业务与验收用例独立 Review](../../../reviews/2026-10-21-flow-business-acceptance-review.md)
- [正式验收用例与结果](../../../evals/dev-flow-stages/2026-10-21-acceptance.md)
- [新会话与隔离行为独立评判](../../../evals/dev-flow-stages/2026-10-21-behavior-report.md)
- [本轮独立架构技术收尾](architecture-closeout.md)
- [独立 Review 记录（含 P1 与 P2 补充评审）](../../../reviews/2026-10-21-flow-revision-review.md)
- [研发设计主文档模板](../2026-10-21-engineering-document-template.md)
- [Review 模板](../2026-10-21-engineering-review-template.md)
- [实施计划模板](../2026-10-21-engineering-implementation-plan-template.md)
- [架构技术收尾模板](../2026-10-21-architecture-closeout-template.md)

已进入插件的正式模板：[统一研发设计](../../../skills/dev-engineering/assets/templates/technical-delivery-design.md)、[独立 Review](../../../skills/dev-engineering/assets/templates/engineering-review.md)、[实施计划](../../../skills/dev-engineering/assets/templates/implementation-plan.md)、[架构技术收尾](../../../skills/dev-architecture/assets/templates/architecture-closeout.md)、[全局 Progress](../../../skills/dev-flow/assets/templates/progress.md)。上方四篇讨论模板保留设计过程，项目采用这些正式模板。

## 结束条件与恢复提示

整体结束需要 P3–P8 的必需改造、完整变更 Review、验收与交付检查、安装/发现/运行验证以及架构收尾真实完成，遗留有承接。源码、文档、安装和运行验证分别记录，不能互相代替。

接手先读本页定位当前阶段，再读整体实施计划和对应权威成果。设计主文档、实施计划和 Todo 仅引用/投影本页的执行状态；文档自身的候选状态与 Review 结论仍保存在原来源。本页由主 Agent 统一更新，不另维护第二份总体状态。

## 后续能力承接（不属于本轮已完成范围）

- 真实业务 UI 项目：产品/视觉实际回应技术反馈，核对实现、真实渲染、接口数据、验收/交付及下一任务资产复用。
- Kimi：原生安装/重载与真实模型专业行为；Codex 安装及生成入口检查不替代此项。
- 扩展策略：其余 11 个输入，包括 Agent 主动处理基线变化；本轮未执行，状态工具的负例不折算为这些行为通过。

本轮源码提交与当前安装版本已保存；最后安装字节级核验见本机 `.dev/runs/flow-revision/final-check.json`，不向其他项目或远端发布。
