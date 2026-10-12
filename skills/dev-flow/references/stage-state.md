# 迭代状态格式与只读核验

适用范围与确认/Review/完成规则以[执行协议](execution-contract.md#按当前状态推进)为准。核验器只读检查声明的记录一致性；不是 Hooks、MCP 服务或运行时拦截，不能证明记录真实、依赖完整、设计质量或语义覆盖。

## 放在已有索引，引用原记录

在现有 `docs/dev-flow/iterations/<迭代ID>/index.md` 放**一个** `dev-flow-state` JSON 代码块。它是范围、有效版本及阶段状态的维护位置；正文表格介绍成果和链接，不再手工维护另一组阶段状态。规格、用例、实际 Review/确认原记录与本机运行证据仍在各自权威位置。无须迁移已有文档或补抄历史日志；仅恢复本次所需的有效事实。

采用[迭代模板](../assets/templates/iteration-index.md)。需要看完整格式时参考[局部修复示例](../assets/examples/iteration-state.md)；这是合成示例，不能原样登记为项目通过。状态可以引用合并在同一索引内的规格、确认、Review 和结果。

### 顶层与工作范围

| 字段 | 含义 |
| --- | --- |
| `schema_version` | 整数 `1`；未知版本拒绝核验 |
| `candidate` | 本轮源码/产物候选的可追溯标识；在正文关联提交及相关未提交指纹 |
| `scopes` | 各范围的 `id`、`route`、`reason`、`implementation`、`before_implementation` 和 `before_finish` |
| `artifacts` | `id`、`path`、`version`；本次有效规格、用例、计划等实际权威位置 |
| `gates` | 本次需核验的确认、Review 和真实检查，见下表 |
| `cases` | `id`、`scope`、`required_checks`；用户用例关联的全部必需 check ID；无用例的文档/探索任务允许 `[]` |

`route` 取 `quick/standard/system/incident/exploration`；尚未决定用 `undecided`，核验不给实施/结束通过。`reason` 说明目标、影响、复用/裁剪及验证依据；`implementation` 表示本次是否包含正式实现。前置/完成列表由主 Agent 按执行协议确定，**脚本不会自动补齐遗漏的前置**。混合任务逐范围登记，不把一条局部更名路径套到新增平台。完整候选的整体 Review、集成与交付检查仍须列入相关范围的完成列表。

`before_implementation` 引用正式编码需要的有效确认和 Review；`before_finish` 引用当前候选必须通过的实现 Review、验收、交付及必要资产同步检查。用户 TC 的 `required_checks` 自动加入完成核验，不能仅删掉完成列表中的检查就使 TC 通过。不适用阶段可以不建 gate 并在路径依据中说明；如需显式登记不适用，也须引用实际理由记录。

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

多个逻辑产物可引用同一真实文件、使用各自版本和 gate；零发现、同一执行者及同一次合并答复均有效。时间相同允许表示一次合并执行，但不得补造依赖次序。

### 确认、Review 与证据

- **confirmation**：提供 `source`（用户消息/既有确认来源）、`quote`（必要原话）。`coverage` 只列答复明确支持的内容，不能从“按此布局”推导其他规则/用例已确认；待决内容保留在正文。已有有效确认引用原来源，不再问一次。
- **review**：提供 `actor`、`mode`（`self/independent/delegated`）、`checks`（具体核对项）和 `findings`（明确零发现写 `[]`）。发现项含 `text`、`severity: blocking/nonblocking`、`status: open/closed`；开放阻断项不能 passed。检查视角和结论依据按实际填写，不以角色名称或“自查通过”代替执行。
- **check**：提供 `expects` 与 `evidence`。每项 expects 含 `kind` 和非空 `observations`，表示用例真正需要的证据与观察；每项 evidence 含 `path`、`kind`、`observations`、`inputs`，候选检查另含 `candidate`。证据文件须存在，输入与 gate 一致，观察项必须在**相同 kind** 的有效证据中全部出现。

kind 取 `prototype/native-ui/web-ui/api/service/unit/artifact/other`，是证据边界，不是质量排序或必须全部使用的清单。观察项由专业用例确定，例如 `app-reopen/system-share/file-picker/native-layout`；同 kind 中的 `save-load` 也不能顶替 `app-reopen`。真正操控应用界面的自动化可登记 native-ui/web-ui；不强制人工、真机或所有场景做 E2E。

服务保存/读取不证明应用退出重开；导出协调器生成文件不证明用户导出与系统分享操作；HTML 预览不证明原生布局。若用例本来只需服务行为或原型检查，可以明确要求该类型。脚本不能识别被错误标注为 native-ui 的服务日志，执行者仍需阅读证据并核对观察边界。

### 版本变化与复用

受影响产物升版后旧确认/Review/检查失效，完成检查换候选后旧结果失效。有效版本来自权威文档，不因为了通过工具而改写旧结论。不要把无关产物加入 inputs 造成全部重审。

脚本比较已声明的版本，不读取任意规格正文推断真实版本；执行者须先从权威位置核对并更新 artifact.version。只改文档正文却保留旧版本，或把局部答复错误标为全部 coverage，工具无法自动识别。

未受影响的结果可以引用影响分析复用：gate 保留原 `candidate` 和证据候选，增加 `reuse: {"from_candidate": "旧候选", "to_candidate": "当前候选", "reason": "实现、输入与环境未变的具体依据", "record": "实际依据路径"}`。输入仍须匹配现行版本；脚本检查声明的一致性，不证明复用理由成立。复用不删除历史失败、不直接覆盖旧证据，也不替代最终整体集成检查。

## 调用与结果

从本 Skill 所在目录定位脚本，使用宿主实际可用的 Python 3.9+。设 `PLUGIN_ROOT` 为当前已启用插件根目录、`PROJECT_ROOT` 为实际业务项目根目录，路径有空格时保留引号：

```sh
python3 "$PLUGIN_ROOT/skills/dev-flow/scripts/check_iteration.py" \
  "$PROJECT_ROOT/docs/dev-flow/iterations/<迭代ID>/index.md" \
  --root "$PROJECT_ROOT" --phase implementation
```

结束前使用 `--phase finish`（默认），核验全部范围。可用 `--scope <范围ID>` 调查/推进独立部分，结果会列出 selected_scopes，不能据此宣布整个迭代完成。JSON 夹具也可作为输入，生产状态仍保存在原迭代索引。

输出包含 `can_start_implementation/can_finish/blocking_items/next_action`、逐范围 current_stage 和逐用例结果。退出码：`0` 所选阶段记录成立，`1` 尚有阻断，`2` 格式/引用错误。脚本不修改任何记录，未知格式和坏引用失败关闭。

运行证据可在忽略的 `.dev/` 中；path 和 record 为业务根目录内的实际相对文件路径，不含 URL、锚点或目录穿越。外部确认链接放 source，必要内容提炼到既有项目记录。跨机器缺失的私有证据按需恢复或复跑，不临时创建空文件使核验通过。

对未接入项目、新格式和新增行为，先运行必要工具检查并保存对应验证状态。确定性测试与[新上下文行为评测](../../../evals/dev-flow-stages/README.md)分别登记；工具通过不等于 Agent 流程通过。
