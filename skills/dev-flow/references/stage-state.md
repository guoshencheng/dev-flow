# 迭代状态格式与只读核验

适用范围与确认/Review/完成规则以[执行协议](execution-contract.md#按当前状态推进)为准。核验器只读检查声明的记录一致性；不是 Hooks、MCP 服务或运行时拦截，不能证明记录真实、依赖完整、设计质量或语义覆盖。

## 迭代独立 Progress，引用原记录

每轮迭代在独立 `Progress.md` 维护唯一总体进度，列出最终目标的完整阶段、当前阶段、未开展项、执行者和下一步；`index.md` 与原生 Todo 只链接或投影它。接续旧活动迭代时迁入有效总体状态及状态块，原入口改引用；历史证据不改写。**可读的全局 Progress 不以 JSON 状态块为前提。**需要结构化核验时，只在 Progress 内放**一个** `dev-flow-state` JSON 代码块，保存范围、有效版本及 gate 状态。规格、用例、实际 Review/确认原记录与本机运行证据仍在各自权威位置。

采用 [Progress 模板](../assets/templates/progress.md)，由[迭代索引](../../document-management/assets/templates/iteration-index.md)链接。需要看完整状态格式时参考[局部修复示例](../assets/examples/iteration-state.md)；这是合成示例，不能原样登记为项目通过。状态可以引用合并在索引内的规格、确认、Review 和结果。

流程确认按[执行协议](execution-contract.md#流程开始前的用户确认)实际执行，不以脚本通过代替。需要结构化登记时，以 `kind: confirmation`、`stage: workflow-confirmation` 关联独立的流程方案版本，把它加入后续 gate 的 `after` 依赖；只有答复明确包含实施授权时才填 `authorizes`。流程版本不随普通状态更新时间变化。schema 1 核验器仍只检查已声明依赖，不能自动发现遗漏的流程确认，也不强制文件名；本版收紧的是 Agent 执行规则，不宣称新增运行时拦截。

### 顶层与工作范围

| 字段 | 含义 |
| --- | --- |
| `schema_version` | 整数 `1`；未知版本拒绝核验 |
| `candidate` | 本轮源码/产物候选的可追溯标识；在正文关联提交及相关未提交指纹 |
| `scopes` | 各范围的 `id`、`route`、`reason`、`implementation`、`before_implementation` 和 `before_finish` |
| `artifacts` | `id`、`path`、`version`；本次有效规格、用例、计划等实际权威位置 |
| `gates` | 本次需核验的确认、Review 和真实检查，见下表 |
| `cases` | `id`、`scope`、`required_checks`；用户用例关联的全部必需 check ID；实施前正式 TC 尚未形成时可为 `[]`，不影响有效设计/计划/授权后的开工判断；标准/系统实现范围不能靠空列表声明完成 |

`route` 取 `quick/standard/system/incident/exploration`；尚未决定用 `undecided`，核验不给实施/结束通过。`reason` 说明目标、影响、复用/裁剪及验证依据；`implementation` 表示本次是否包含正式实现。前置/完成列表由主 Agent 按执行协议确定；脚本固定检查含正式实现范围的用户实施授权，**其他遗漏的设计/用例等前置不会自动补齐**。混合任务逐范围登记，不把一条局部更名路径套到新增平台。完整候选的整体 Review、集成与交付检查仍须列入相关范围的完成列表。

`before_implementation` 引用正式编码需要的已确认产品/设计完成标准、研发设计 Review、计划复核和实施授权；标准路径不引用完整候选后维护的正式 TC Review 或例行 TC 人工确认。`before_finish` 引用当前候选必须通过的完整实现 Review、正式 TC 独立 Review、验收执行、交付核验及必要资产同步检查。用户 TC 的 `required_checks` 自动加入完成核验，不能仅删掉完成列表中的检查就使 TC 通过。不适用阶段可以不建 gate 并在路径依据中说明；如需显式登记不适用，也须引用实际理由记录。

### Gate 通用字段

| 字段 | 要求 |
| --- | --- |
| `id/kind/stage` | 稳定 ID；kind 为 `confirmation/review/check`；stage 表达当前设计/方案/用例/计划/实现/验收/交付等对象 |
| `status` | `pending/passed/failed/blocked/not_applicable`；未执行/跳过用 pending 并在正文注明，不能写 passed |
| `inputs` | artifact ID → 实际核验版本；passed 必须非空，与现行 artifact 版本一致 |
| `required_coverage/coverage` | 预定范围与实际覆盖的 RULE/AC/UI/ARC/OUT/TC 或检查 ID；passed 时前者非空且必须全部被后者覆盖 |
| `after` | 前置 gate ID 列表；须成立且无循环。通过时间不得早于前置通过时间 |
| `record/completed_at` | 实际原记录的项目相对文件路径、实际执行完成时间（ISO 8601，含时区）；passed 必须有，禁止以填表时间伪装执行时间 |
| `reason` | not_applicable 必须说明依据并提供 record；已纳入 TC 的必需检查不能用不适用关闭 |
| `candidate` | 完成列表和用户用例中的 Review/check，以及其依赖中不属于实施前置的 Review/check，必须绑定候选；前置设计/方案 Review 绑定输入版本，不绑定尚未形成的源码 |
| `requires_independent` | review 可选布尔字段；用于明确任何路径都须独立执行。标准/系统范围的归属 Review 即使未填此字段，也必须独立 |
| `review_scopes` | review 可选的非空 scope ID 列表；跨范围合并授权后的 Review 必须声明实际归属，供脚本区分不同范围的依赖 |

多个逻辑产物可引用同一真实文件、使用各自版本和 gate；零发现及同一次合并答复均有效。作者自查须如实登记，不能作为要求独立 Review 的对象的独立结论。时间相同允许表示一次合并执行，但不得补造依赖次序。

### 确认、Review 与证据

- **confirmation**：提供 `source`（用户消息/既有确认来源）、`quote`（必要原话）。`coverage` 只列答复明确支持的内容，不能从“按此布局”推导其他规则或尚未写出的 TC 已确认；待决内容保留在正文。已有有效确认引用原来源，不再问一次。正式用例在既有预期内细化时无需例行人工确认；有歧义或新增业务只确认受影响部分。
- **实施授权**：含正式实现的 scope，必须在 `before_implementation` 或其 `after` 依赖中关联有效、passed 的 confirmation；该确认的 `authorizes: ["scope-ID"]` 明确覆盖本范围。仅 confirmation 可声明 `authorizes`，列表成员须为已登记 scope；普通设计确认、AI Review、未关联或不适用授权均不能放行。可在同一 gate 合并设计/用例和多个范围的实施同意，仍须分别核对其他前置。`inputs` 绑定已展示范围/预期/验证/交付的摘要或规格版本，`record/source/quote` 引用真实答复；范围变化更新受影响输入版本与授权，不能保留旧版本假装有效。
- **review**：提供 `actor`、`mode`（`self/independent/delegated`）、`checks`（具体核对项）和 `findings`（明确零发现写 `[]`）。发现项含 `text`、`severity: blocking/nonblocking`、`status: open/closed`；开放阻断项不能 passed。标准/系统范围从 `before_implementation` 出发，经单范围授权及 `after` 依赖闭包中的归属 Review 必须为 `mode: independent` 才能开工；从 `before_finish` 出发的归属 Review 同理决定完成。不能把 Review 移到 `after` 或省略 `requires_independent` 来绕过。跨范围合并授权后的依赖可能含另一快路径的作者自查，这时用 `review_scopes` 标明实际归属；缺失时标准/系统范围保持未通过。直接门槛或单范围授权链已指明归属，声明其他 scope 会被判冲突。`delegated` 只表示委派，不能单独证明独立性。快路径或纯文档任务的作者自查仍可如实用 `self`。执行者仍需核对作者身份、实际上下文与完整 Review 范围，脚本仅检查声明的一致性。
- **check**：提供 `expects` 与 `evidence`。每项 expects 含 `kind` 和非空 `observations`，表示用例真正需要的证据与观察；每项 evidence 含 `path`、`kind`、`observations`、`inputs`，候选检查另含 `candidate`。证据文件须存在，输入与 gate 一致，观察项必须在**相同 kind** 的有效证据中全部出现。

kind 取 `prototype/native-ui/web-ui/api/service/unit/artifact/other`，是证据边界，不是质量排序或必须全部使用的清单。观察项由专业用例确定，例如 `app-reopen/system-share/file-picker/native-layout`；同 kind 中的 `save-load` 也不能顶替 `app-reopen`。真正操控应用界面的自动化可登记 native-ui/web-ui；不强制人工、真机或所有场景做 E2E。

服务保存/读取不证明应用退出重开；导出协调器生成文件不证明用户导出与系统分享操作；HTML 预览不证明原生布局。若用例本来只需服务行为或原型检查，可以明确要求该类型。脚本不能识别被错误标注为 native-ui 的服务日志，执行者仍需阅读证据并核对观察边界。

### 版本变化与复用

受影响产物升版后旧确认/Review/检查失效，完成检查换候选后旧结果失效。有效版本来自权威文档，不因为了通过工具而改写旧结论。不要把无关产物加入 inputs 造成全部重审。

脚本比较已声明的版本，不读取任意规格正文推断真实版本；执行者须先从权威位置核对并更新 artifact.version。只改文档正文却保留旧版本，或把局部答复错误标为全部 coverage，工具无法自动识别。

未受影响的结果可以引用影响分析复用：gate 保留原 `candidate` 和证据候选，增加 `reuse: {"from_candidate": "旧候选", "to_candidate": "当前候选", "reason": "实现、输入与环境未变的具体依据", "record": "实际依据路径"}`。输入仍须匹配现行版本；脚本检查声明的一致性，不证明复用理由成立。复用不删除历史失败、不直接覆盖旧证据，也不替代最终整体集成检查。

## 调用与结果

状态格式继续使用 schema 1。Plugin 0.2.0 起的实施授权核验保持有效。旧记录缺少 `authorizes` 不再获得正式实施/完成通过；恢复已有真实开工同意时引用原答复、展示范围与有效版本，不倒填历史授权，也不为格式再次问用户。没有同意则保持 pending，展示摘要后请求确认。`implementation: false` 的纯评审/设计等范围不需要开工授权，不能将实际实现错误标为 false 规避检查。

本次独立 Review 核验仍沿用 schema 1，但旧标准/系统范围若把专业 Review 放在间接依赖中，跨范围授权后的 Review 缺 `review_scopes` 会阻断对应阶段；直接门槛和单范围授权链可从结构推断归属。迁移时对照原 Review 对象、实际作者/执行者和范围补写真实归属与方式，作者自查不得改记为独立执行。仅补状态字段无需重新向用户确认；原 Review 未独立执行时，应补真实独立 Review，不能倒填通过。

从本 Skill 所在目录定位脚本，使用宿主实际可用的 Python 3.9+。设 `PLUGIN_ROOT` 为当前已启用插件根目录、`PROJECT_ROOT` 为实际业务项目根目录，路径有空格时保留引号：

```sh
python3 "$PLUGIN_ROOT/skills/dev-flow/scripts/check_iteration.py" \
  "$PROJECT_ROOT/docs/dev-flow/iterations/<迭代ID>/Progress.md" \
  --root "$PROJECT_ROOT" --phase implementation
```

结束前使用 `--phase finish`（默认），核验全部范围。可用 `--scope <范围ID>` 调查/推进独立部分，结果会列出 selected_scopes，不能据此宣布整个迭代完成。JSON 夹具也可作为输入。脚本为读取旧记录和测试夹具继续接受显式 Markdown/JSON 路径，不限定文件名；当前迭代执行状态统一保存在独立 Progress，不因此允许沿用索引作为总体进度。

输出包含 `can_start_implementation/can_finish/blocking_items/next_action`、逐范围 current_stage 和逐用例结果。退出码：`0` 所选阶段记录成立，`1` 尚有阻断，`2` 格式/引用错误。脚本不修改任何记录，未知格式和坏引用失败关闭。

运行证据可在忽略的 `.dev/` 中；path 和 record 为业务根目录内的实际相对文件路径，不含 URL、锚点或目录穿越。外部确认链接放 source，必要内容提炼到既有项目记录。跨机器缺失的私有证据按需恢复或复跑，不临时创建空文件使核验通过。

核验器只检查已声明的 gate、cases、版本和依赖，不能从业务文档自动发现遗漏的 TC、交付场景或错误标注的证据。标准/系统实现范围的空 `cases` 只阻止完成、不阻止实施；主 Agent 须从实施前确认的完成标准逐项反查形成后的 cases 与必需交付检查。正式 TC 尚未形成时可先在 `before_finish` 声明待完成的验收/交付 gate，不虚构 TC 或通过结果。对未接入项目、新格式和新增行为，先运行必要工具检查并保存对应验证状态。确定性测试与[新上下文行为评测](../../../evals/dev-flow-stages/README.md)分别登记；工具通过不等于 Agent 流程通过。
