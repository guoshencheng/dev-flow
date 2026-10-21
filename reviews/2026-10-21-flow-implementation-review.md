---
title: Dev Flow 新流程完整候选独立 Review
status: passed-for-source-candidate
date: 2026-10-21
reviewer: independent-architecture-reviewer
baseline: 503fcb4768a658772fd4648ec19b7ceedcd5a1ac
---

# Dev Flow 新流程完整候选独立 Review

## 结论

**当前结论：源码候选 C2-62e99b8b7a6d 的完整变更 Review 通过。** 首轮 F1/F2 与第二轮间接依赖反例均经修订和定向复核关闭。此结论只针对当前源码候选的需求符合性与实现质量，可作为 P6 后续正式验收检查的输入；不表示插件已安装、生效、经过新会话行为评测或真实业务项目验证。下列发现保留初审事实与修复过程，最终状态以文末第三轮定向复核为准。

## 输入、范围与独立性

- 原始设计输入：[新流程方案 0.3](../docs/plans/2026-10-21-flow-revision.md)、[整体实施计划 0.2](../docs/plans/2026-10-21-flow-revision/implementation-plan.md)、四篇 0.4 讨论模板（研发设计、独立 Review、实施计划、架构技术收尾），以及仓库 `AGENTS.md` 指引与 [Dev Flow 总纲](../skills/dev-flow/references/constitution.md)。
- 代码范围：从 `503fcb4768a658772fd4648ec19b7ceedcd5a1ac` 到当前暂存候选的全部 83 个变更文件；检查共同协议、六职责入口与方法、正式模板、进度/状态协议、核验器及测试、评测输入、宿主生成入口、版本说明与现行仓库入口。当前完整性以 `git diff <基线>` 为准，不以作者摘要代替。
- 本 Review 执行者未主笔上述改造，仅读取和运行只读检查；本文件由评审执行者独立写入。主笔处理后仍由本评审执行者核对原发现与受影响差异。

## 实际方法与证据

读取方案、计划、Progress、四篇讨论模板，并逐组检查完整差异和对应现行文件。对照总纲逐项核对：设计前真实代码/成本反馈、统一研发设计、独立评审与技术收尾、窄上下文委派、完成标准与范围授权、实现后正式 TC、交付核验、唯一 Progress、历史证据边界。检索现行入口的旧流程语句及相对文档链接。对核验器检查阶段依赖、候选失效、证据类型与只读行为，并用合成夹具复现边界。

已运行：`python3 -m unittest discover -s tests -p test_iteration_checks.py -v`，36 项通过；`python3 scripts/sync_host_agents.py --check`，Codex/Kimi、六职责与八 Skills 同步；`python3 -m unittest discover -s evals/host-adapters -p test_host_adapters.py -v`，6 项通过。上述只验证代码和声明契约，不证明真实评审、用例、交付或宿主安装。

## 需求符合性与实现质量

方案 0.3 的主体阶段已进入总纲、任务路由、执行协议和六职责入口。正式模板保留主设计与独立 Review/计划/架构收尾的双向链接及真实状态栏；技术反馈、状态 UI 必要性、测试后置与持续研发自测均有明确位置。`Progress` 模板和状态协议允许在选定 Markdown/JSON 文件维持唯一结构化状态；测试实际覆盖 Progress 路径、空 cases 仅阻止完成、候选变化和交付 gate。Kimi/历史 Codex 包装由生成器同步，没有把模型选择固化到专业 Skills。

核验器的定位是检查**已声明记录**。它无法从业务文档自动发现遗漏用例或交付场景，这一限制在 `stage-state.md` 已明确。正式落地仍需主 Agent 从实施前完成标准反查 TC、交付检查和实际证据，不应将 36 个合成测试解释成真实业务验收。当前两项问题超出这一正常限制：一个现行入口直接发布相反流程；另一个已声明为自查的 Review 仍被当作独立评审的通过条件。

## 发现、处理与定向复核

### F1 · 现行概览仍指导旧流程（阻断）

**位置与事实：** `docs/overview.md` 第 17、30、34、48、52 行仍写正式用例 AI Review、人工确认在实施计划和编码前；将每轮架构设计与研发技术方案拆篇；当前版本仍称 Plugin 0.2.2、总纲 0.27。该页是仓库现行概览，不是明确标注的历史记录。

**影响与依据：** 新接手者从现行入口可能执行已被方案 0.3 和总纲 0.29 废止的实施前 TC 门槛，并遗漏统一设计和后置交付核验，违反 P3/P6 的“所有现行入口一致”。

**修改要求：** 将该页现行流程、职责表、实施授权关系、版本与文档位置同步到候选；历史能力叙述清楚标记为历史，不把旧结论写成新流程现状。

**处理结果：** 主笔已更新 `docs/overview.md` 的日期/版本、六职责说明、完整功能顺序、实施授权与四篇文档结构；`docs/overview.md:28` 仍写需求变化后先“更新规则、方案、用例和计划，再恢复受影响实现”，没有将“用例”限定为已存在用例，容易重新引入完整正式 TC 前置。主笔已收到该残余措辞。

**定向复核：** 已读 `docs/overview.md` 实际差异；旧顺序和旧当前版本已清除。第二轮时第 28 行仍待校准，第三轮已修订并关闭，见文末。

### F2 · 标准范围的自查 Review 可被核验为完整通过（阻断）

**位置与事实：** `skills/dev-flow/scripts/check_iteration.py` 仅检查 review `mode` 属于 `self/independent/delegated`，未对标准/系统范围要求的独立 Review 区分已声明的 `self`。`tests/test_iteration_checks.py` 的 `mixed_state()` 标准范围中，设计/计划/实现 Review 默认就是 `self`。将该夹具的 `solution-review`、`mobile-plan`、`implementation-review`、`cases-review` 均设为 `self` 后，`inspect()` 仍返回 `can_start_implementation: true`、`can_finish: true`、空阻断项。

**影响与依据：** 新流程明确作者与独立评审分离，正式用例须独立 AI Review。即使工具不能验证执行者身份，也能拒绝记录中明确的自查；当前结果会把未满足独立性的标准任务显示为可完成。合成测试未覆盖该负例。

**修改要求：** 为适用标准/系统范围的关键设计、计划、正式用例及完整实现 Review 声明并检查独立性要求；无法委派时保留真实降级/待评审状态，不把 `self` 解释成独立通过。增加明确 `self` 不放行、合法独立/裁剪可通过的回归例，避免硬编码所有局部任务都要委派。

**处理结果：** 状态作者已为标准/系统范围直接列入 `before_implementation` 或 `before_finish` 的 Review 增加独立方式检查，给 `requires_independent` 添加声明校验，并新增五项相关回归。原四项 `self` 反例已被拒绝，快速范围原 `self` 夹具仍可通过。但同范围 Review 通过 `after` 间接进入前置时仍可绕过。

**定向复核：** 第二轮已读 `check_iteration.py`/测试实际差异并重跑当时 41 项单测，均通过；`git diff --check` 通过。新增反例：保留标准范围 `mobile-start.after → mobile-plan → solution-review`，将 mobile `before_implementation` 只列 `design-preview/design-confirm/mobile-start`，把 `mobile-plan` 与 `solution-review` 的 `mode` 设为 `self`。当时 `inspect()` 返回该范围 `can_start_implementation=true`、`can_finish=true`、`blocking_items=[]`。原因是独立性检查只覆盖直接列项，不覆盖同范围经 `after` 依赖的专业 Review。第三轮对此已修订并关闭，见文末。

### O1 · 版本阶段描述需校准（观察项）

三个插件清单已写 `0.3.0`，README 也称当前源码 0.3.0；本轮计划把定版升级放在 P7，Progress 仍在 P6。定向复核见实施计划 P7 已补“候选版本可提前预置，P7 才冻结正式发布版本”；Progress 也明示源码候选尚未安装/交付。该观察项已关闭，不把预置版本号当作安装完成。

## 未覆盖与后续

未运行安装、未核对安装缓存指纹、未执行新会话 Harness 派发/模型行为评测、未在真实业务项目中验证完整流程。这些属于计划 P7/P8，不应从本次静态 Review 或合成单测推断通过。以下记录 F1/F2 修订后的实际定向复核；最终候选变化需重新绑定本 Review 的范围与结论。

## 第三轮定向复核：C2-62e99b8b7a6d

**候选绑定与方法：** 主 Agent 的 `.dev/runs/flow-revision/source-candidate.json` 记录基线、C2 标识和 230 个执行协议/源码文件 SHA-256；本评审逐文件重算，230 个文件均与清单一致。此前完整变更审阅覆盖原 83 个文件，本轮只复核 F1/F2 修订及相关新增行为夹具，不将文档报告或 Progress 的独立更新误算为同一源码候选的运行结果。

**F1 关闭：** `docs/overview.md` 已改为总纲 0.29、Plugin 0.3.0 *源码候选*、统一研发设计和实现后正式用例/交付顺序。第 28 行现在明确“已有用例同步受影响部分，尚未形成的正式用例在完整候选后维护”，不再把完整 TC 重新设为变化实现的前置。旧方案只作为历史调整引用。

**F2 关闭：** `check_iteration.py` 从本范围 `before_implementation`、`before_finish` 沿完整 `after` 依赖链核对专业 Review 的归属与 `mode`。单范围授权链可推归属，跨范围合并授权后的 Review 用 `review_scopes` 声明实际归属；声明冲突或缺失按相应范围阻断，`delegated` 本身不冒充独立。手工重跑第二轮反例：间接 `solution-review`/`mobile-plan` 设为 `self` 时，mobile 的 `can_start_implementation=false`、`can_finish=false`，阻断理由分别指向独立执行者。跨范围合并授权中 quick 的合法 `self` 不误伤 mobile，quick 自身可完成；独立 `mixed_state()` 和局部 `quick_state()` 正常通过。状态协议及 `docs/plugin.md` 解释了旧结构化记录的真实归属迁移，不能倒填不存在的独立 Review。

**相关测试与新增评测资产：** 运行 `python3 -m unittest discover -s tests -p test_iteration_checks.py -v`，44 项通过，包含间接 Review、归属冲突/缺失、跨范围授权及快路径回归；宿主适配 6 项通过；`git diff --check` 通过。新增 `proposal-cost`、`post-candidate` 的 task/project 与独立 evaluator 路径存在、JSON 可解析；README 要求执行者只接收任务/项目/Skill，把评判条件留给独立评判者，并先复制到忽略运行目录。前者提供详情/列表/单订单 API 源码用于设计期成本反馈，明确不含可运行 UI；后者提供标准库 CLI、原规则、合成的实施前确认/Review/授权、唯一 Progress 与研发局部测试，把正式 TC/独立 Review/zipapp 交付留待 P8 实际执行。其他 mixed/quick/evidence/progress 夹具分别限定授权、局部修复、证据分类和结构化进度边界；评测输入存在不代表新会话行为通过，也不是真实业务项目证据。

**后续边界：** 本 Review 到此结束，P6 可基于 C2 继续本轮正式验收用例的独立 Review 和适用检查。P7 安装/缓存指纹与 P8 新会话行为、真实业务项目适用性均保持未执行；执行或包内源码再次变化时按影响判断本结论失效并定向复核。
