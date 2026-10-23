> 2026-10-23 / 0.6.5 当前约定：用例使用可提交的中文列表，全量与增量共用；每次测试执行的执行表和可选截图等证明另存忽略目录，不提交。技术拆解按需，不默认要求。方法权威见[用例设计](../skills/acceptance-case-design/SKILL.md)和[验收执行](../skills/acceptance-execution/SKILL.md)；下方建设与评测保留当时事实，不自动成为当前附加要求。

---

> 2026-10-21 结构调整：当前专业责任源为 [agents/prompts/acceptance.md](../agents/prompts/acceptance.md)，操作路由见 [能力清单](../capabilities.json)。长篇规范和模板随职责参考/资产或对应操作 Skill。下文首版建设及既有验证记录保留历史版本事实；本轮实际结果见[实施进度](plans/2026-10-21-agent-skill-reorganization/Progress.md)，不因迁移自动视为行为或原生派发通过。

当前接入：通过专业 Skill 承担职责；2026-10-09 已移除 setup，旧 TOML 仅作参考，不参与当前安装。下文历史配置/派发证据保留原验证范围。
id: ROLE-dev-acceptance
title: 测试与验收 Agent
status: current
version: 0.6
owner: acceptance
---

# 测试与验收 Agent v0.6

更新日期：2026-10-10。原生职责 `dev_acceptance`，配置见[dev_acceptance.toml](../agents/dev_acceptance.toml)，专业入口为[dev-acceptance](../agents/prompts/acceptance.md)。配置不固定模型/强度，实际执行方式与成熟度分别登记。

## 职责与执行关系

2026-10-21 调整正式用例时点：测试早期反馈可测性、准备数据/自动化/环境；完整候选就绪后依据实施前已确认的业务完成标准维护正式用例并独立 AI Review，随后集中验收与交付核验。具体缺陷即时反馈并定向复验。指导已更新，隔离代表场景有实际执行证据，真实业务 UI 项目的完整效果仍待验证，规则见[执行协议](../skills/dev-flow/references/execution-contract.md)。

测试从原要求与实施前确认的产品/设计完成标准出发，综合有效 UI、架构与经 Review 的研发设计，在完整候选后依据实际入口编写可读用例与技术检查；从原产品反查遗漏，不能以设计或实现缺项缩减需求。独立 AI Review 后，既有预期内细化直接执行；歧义或新增业务只确认受影响部分。研发的局部测试和主链路自测随实现进行。

测试持续实际执行、反馈和复验，以当前版本端到端及适用架构证据验收。研发设计 Review、正式用例独立 Review、实施前完成标准确认和实际验收分开保存版本/来源，不能改写用例来迁就实现。

测试主责用例、测试策略与自动化、执行/证据、缺陷复验和验收结论。研发主责生产修复；产品/视觉/架构分别维护语义、呈现和契约；运维维护启动与实际环境。测试脚本可以维护，重要验收含义变更仅确认受影响部分，不增加人工计划审批。实施中发现需求变化时，先更新受影响的产品/设计完成标准及决定，已有用例同步受影响部分；测试判断 E2E 门槛。尚未形成的正式用例在完整候选后补齐。

## 不同测试验收方案

v0.2 明确阶段与对象：设计文档/原型的流程、规则、交互及恢复走查由产品主责，呈现由视觉主责；测试可读取设计，早期检查用例/覆盖/可测性，实际验收默认面向可运行实现与交付候选。原型可点或使用 Mock/浏览器工具不改变路由。用户明确指定测试检查原型时限定范围、单列证据，不登记实现验收。修订依据与范围见[边界回溯](../reviews/2026-10-08-prototype-review-routing.md)。

| 方案 | 首版要求 |
| --- | --- |
| 局部规则/组件 | 沿用现有工具，React 可用 Vitest/Testing Library；断言用户行为与业务规则，标明模拟边界 |
| 前端界面 | 实际浏览器操作导航、表单、列表、状态、透出/键盘及目标设备；Mock 场景单独记录，视觉检查与行为分别验收 |
| 后端接口/数据 | 真实调用检查输入输出、权限/拒绝、业务状态和读写结果；必要重复、并发、兼容/恢复按契约补充 |
| 前后端 E2E | 实际界面动作 → 对应请求/响应 → 服务端结果/读回 → 刷新或重新进入，以及相关异常恢复 |
| 交付启动 | 在声明版本/环境实际构建、准备、启动/安装/访问并完成核心任务；本机与目标部署分别记录 |
| 回归与专项 | 依据变化、共享契约/组件和历史缺陷选择；性能/可靠性等已有目标采用对应场景与测量 |

成熟工具优先复用，新 Web 浏览器/API 自动化默认 Playwright。React Web、Next 全栈、Astro 静态的既定技术选择继续有效；纯 API 或纯静态按对象裁剪。不能只以截图、2xx 或 Mock 全绿登记完整验收。

## 八项能力如何落实

| 能力 | 首版专业内容与项目产物 |
| --- | --- |
| T01 场景与可测性 | 可读 TC ↔ OUT/链路 ↔ RULE/AC/UI/ARC，前置/操作/预期、需求变化补用例、完整候选后的独立用例 AI Review、实施前完成标准基线与真实覆盖 |
| T02 功能与边界 | 正常/边界/拒绝/异常、接口与业务数据不变量，当前候选真实执行 |
| T03 界面交互 | 实际导航、输入、状态和恢复；B/C 任务、目标窗口/键盘与呈现检查 |
| T04 端到端交付 | 按真实入口、跨层依赖、持久性/破坏性边界和交付变化触发 E2E，关联 UI/请求/响应/服务端结果与持久性，核验约定启动/交付 |
| T05 回归 | 变化影响到场景/消费者，原缺陷保护与本轮必要回归 |
| T06 专项 | 适用的架构/权限、性能/可靠性/兼容等目标与对应证据；不默认全专项成熟 |
| T07 缺陷对焦 | 最小复现、版本/证据、研发反馈、修复版本、原问题复验与关闭 |
| T08 自动化与复用 | 项目工具/数据隔离、稳定检查、失效管理与新任务可恢复资产 |

对应方法分为[策略与用例](../skills/acceptance-case-design/references/strategy-and-cases.md)、[前端与界面](../skills/acceptance-execution/references/frontend-and-ui.md)、[后端接口](../skills/acceptance-execution/references/backend-and-api.md)、[完整链路与交付](../skills/acceptance-execution/references/end-to-end-and-delivery.md)、[执行与反馈](../skills/acceptance-execution/references/execution-and-feedback.md)、[项目资产](../skills/document-management/references/professional-assets.md#测试验收)。主入口按需加载，工具兼容与实际命令在项目采用时核验。

## 项目目录、预览与持续建设

已有测试规范优先；没有时使用 `docs/dev-flow/acceptance/index.md`、`strategy.md`、`features/<功能ID>/cases.md`、`runs/<日期>/<runID>/report.md`，缺陷优先用现有 tracker，自动化继续保存在项目实际测试目录。策略、用例、报告与缺陷各有随包模板，普通历史用 Git，完整替代方案按共同归档规则保留。

项目主索引关联测试与产品、UI、技术、运行入口。用户讨论/确认通过业务项目的文档服务预览该项目的用例/方案，执行时操作实际应用；Skill 文件是方法来源。每轮维护测试/数据/缺陷与证据版本，下一任务读取有效资产及待复验范围。用户可手动触发架构与测试联合维护检查，也可授权定期触发；检查使用同一源码/候选版本，补充并提升已验证的稳定 TC、真实 E2E 和回归入口到项目级基线，再逻辑归档迭代或被替代候选。最新有效用例不移入 `archive/`，失效或替代关系保留来源、状态和承接。

## 验证状态与后续

本轮[插件改造正式用例](../evals/dev-flow-stages/2026-10-21-acceptance.md)经[独立 Review](../reviews/2026-10-21-flow-business-acceptance-review.md)关闭 A1–A4；P6 在 C2-62e99b8b7a6d 执行了声明契约、模板与工具检查。P8 隔离订单备注项目按原规格在完整候选 C1 后维护正式 TC/CH，独立 Review 指出 1 字符合法和空字符串拒绝边界 AR-01，用例 v2 定向复核关闭；项目源码修复为 C2 后，[正式结果](../.dev/runs/flow-revision/behavior-inputs/post-candidate/docs/dev-flow/iterations/order-note/acceptance/result.md)记录 TC/CH-01～08 实际通过，30 次子进程、45 项断言，并从源码目录外使用 zipapp 保存及另起进程读回。[P8 独立行为报告](../evals/dev-flow-stages/2026-10-21-behavior-report.md)判定新会话发现及固定七场景通过；该项目 C2 是隔离业务候选，不是插件执行候选，本机 CLI/zipapp 结果不证明真实业务 UI、线上部署或 Kimi 运行。能力边界见[技术收尾](plans/2026-10-21-flow-revision/architecture-closeout.md)。

2026-10-21 新流程使正式用例及其 Review 后置于完整候选；标准任务按宿主能力默认领域原生 subagent，作者与独立评审分离。四篇技术文档默认 `engineering/design.md`、`engineering/review.md`、`engineering/implementation-plan.md`、`architecture/closeout.md`；已有权威位置可索引复用。总体进度只维护一个权威 Progress/索引。当前核验器仅检查声明事实，不能发现漏报的必需业务 TC；本轮状态夹具与工具测试不代表独立行为或真实项目通过。

2026-10-12 在[共同协议](../skills/dev-flow/references/execution-contract.md#必需检查与完成结论)明确逐必需检查汇总 TC、服务/原型/真实界面证据边界及结束时入口同步，验收模板与[状态核验器](../skills/dev-flow/references/stage-state.md)对齐。工具契约检查及未执行的新上下文评测分别见[记录](../evals/dev-flow-stages/report.md)，不将合成证据认作业务验收。

2026-10-09 增加用户行为用例与技术验证拆解两层表达：用户确认普通中文的场景、操作和具体结果，技术层保存协议/数据/执行/证据，同一次用例 Review 检查对齐。模板及边界推演见[修改记录](../reviews/2026-10-09-readable-acceptance-cases.md)；这是主 Agent 文档自查，不登记独立 Review 或真实项目验收。业务项目用例尚需按新指导改写并复核。

v0.6 增加与架构的联合维护检查及逻辑归档：按用户手动或授权定期触发，以同一版本核对架构现状、ARC/OUT/TC、自动化、数据、环境和真实证据；先补齐并更新项目级稳定回归资产，再归档迭代或被替代候选，最新有效用例保持当前可达。保留[需求变更闸门](../skills/dev-flow/references/execution-contract.md#实施中的需求变更闸门)、E2E 风险触发和验收完成门槛：实施中新增或改变前置、结果、恢复、契约或交付边界时，先补受影响用例并 Review；局部测试、E2E 和交付分别记录，必需 E2E 未执行或阻塞不能汇总为完整通过。

本轮[隔离评测](../evals/dev-flow-methods/report.md)已取得旧红/新绿、无写入副作用、无效测试与语法负例判读、实际浏览器保存/刷新，以及 R01 独立断言复验后关闭的证据。工具对照、研发自测、主 Agent 复跑和独立复评分别登记；读取范围未由宿主文件沙箱强制隔离，真实业务项目与生产验收仍待执行。

本轮专业方法、静态配置和代表工具案例的实际记录见[首版验证](../evals/dev-acceptance/report.md)。主 Agent 执行的工具检查不登记独立角色行为；原生发现/派发、新上下文资产复用和真实项目完整协作分别需要实际验证。

历史 v0.3 曾增加经 Review 技术方案输入、原产品与 OUT 双向覆盖、用例 AI Review 后人工确认的要求；2026-10-21 已由上述后置规则替代；本次检查/推演与未验证范围见[调整记录](../reviews/2026-10-08-technical-delivery-stage.md)，历史工具案例不证明新增阶段已在真实项目执行。

已建设[研发职责](engineering-agent.md)和[运维交付职责](operations-agent.md)，共同提供当前候选、真实环境与入口；测试按原用例实际验收并复验。下一步真实任务检验完整协作，现有能力按范围持续配合。

## Kimi 宿主接入（2026-10-09）

本职责已提供独立 Kimi Markdown Agent 入口，与 Codex 角色参考从共用 Skill 元信息生成；专业方法仍只在 Skill/参考维护。Kimi 2.1.1 已通过原生发现、派发、包内文件读取和交接的模型替身冒烟；真实模型的专业行为及项目结果尚未验证，不能将接入检查登记为专业验收。见 [适配记录](../reviews/2026-10-09-kimi-agent-adaptation.md)及 [执行说明](integrations/kimi-agent-configuration.md)。
