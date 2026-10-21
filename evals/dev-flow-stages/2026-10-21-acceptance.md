# 2026-10-21 Dev Flow 流程改造正式验收用例与技术检查

状态：**正式用例独立 AI Review、C2 候选 P6、Codex 0.3.0 实际安装与 P8 七场景均有通过证据；架构收尾资产一致性均有通过证据；本轮技术与正式验收条件通过，整体进度由主 Agent 最终判断。** 本文件是完整候选后的验收依据和运行记录，不替代 [唯一总体进度](../../docs/plans/2026-10-21-flow-revision/Progress.md)。未参与用例主笔的执行者在[独立 Review](../../reviews/2026-10-21-flow-business-acceptance-review.md)中关闭 A1–A4；P6 原始检查与 P7/P8 证据分别在文末登记，互不折算。首轮失败、修订与复核事实保留在原 Review 和行为报告中。

## 基线、候选与判定方法

- 原要求与可观察预期依据：[流程方案 0.3](../../docs/plans/2026-10-21-flow-revision.md)、[整体实施计划 0.2](../../docs/plans/2026-10-21-flow-revision/implementation-plan.md)、[总纲](../../skills/dev-flow/references/constitution.md)、[执行协议](../../skills/dev-flow/references/execution-contract.md)及本仓库 AGENTS.md。方案 0.2 与四篇讨论模板 0.4 的既有 Review 不自动覆盖当前源码候选。本轮预期从上述要求推导；实际实现只用于定位执行入口和观察点。
- 源码候选：**C2-62e99b8b7a6d**；任务开始基线 `503fcb4768a658772fd4648ec19b7ceedcd5a1ac`，权威清单 `.dev/runs/flow-revision/source-candidate.json` 包含 230 个执行协议文件及 SHA-256。P6 执行前后以及本次汇总时均实核清单内文件零不匹配；本文件、Progress 和报告属于观察记录，其后续编辑不改变 C2 执行协议候选。完整源码 Review 由独立执行者另记。P7 实际安装包曾为 716 文件，后因文档/评测记录纳入包内重建为 **718 文件**；最新 `install-sync-check.json` 已证明缓存与源码相符，本次独立核对源码和缓存 `package-files.json` 均为 718 条且清单字节 SHA-256 相同。主 Agent 在最终 Progress/引用/提交后须再按全包文件检查，不预填未来包哈希。源码或包内文件变化时逐项判断受影响证据与复验，不能沿用旧候选通过填充新结果。
- 每项 TC 的“必需”表示**整体任务结束前**必须通过；阶段门槛按文末逐检查清单判断。P6 只要求 P6 检查、完整候选 Review 与本文件独立 Review 通过；P7/P8 的必需项仍可未执行，故 P6 阶段完成不等于整个 TC 或整体通过。“条件必需”须记录适用判断及来源，适用后同样必须通过。每项检查编号是独立证据要求，不能以一层的局部成功替代另一层。记录状态使用 `待准备/未执行/通过/失败/受阻/不适用/失效`；待准备亦属未执行，不得通过。只填实际命令、日期、环境、候选、原始结果位置和观察事实。任一整体必需检查未执行、失败、受阻、跳过或失效，其 TC 与整体均不能通过。
- 证据分栏为**工具契约**、**隔离行为/原生派发**、**实际 Codex 宿主**、**真实业务项目**。前一栏不能折算后一栏。后续若使用模拟器、CLI 替身或合成状态，写明替身边界。未指定真实业务项目，不编造项目或生产验收结果；若本轮最终交付范围增加真实项目，先补该项目用例与环境再执行。

## 工具契约与文档用例

### TC-01 设计期代码成本反馈与状态 UI

- **原要求/预期：** 在产品/UI 候选确认之前，研发根据当前代码、入口、组件、接口和状态管理，比较至少两种实际交互位置或形式的改动范围、复用与成本；架构核对边界。产品/视觉回应业务收益并修订或说明取舍。对争议状态逐个说明真实触发、用户操作价值、实现成本和处理决定；等待、错误、权限拒绝、数据保留与恢复等必要反馈完整保留。技术不能单方降需求。
- **步骤/检查：** `CHK-01A` 对照方案第二节检查总纲、执行协议及产品/视觉/研发/架构 Skills 和参考中的时点、角色、真实代码依据、给产品/UI 的建议与其后续取舍责任；`CHK-01B` 固定使用 `evals/dev-flow-stages/fixtures/proposal-cost/` 隔离项目，其 `task.md` 给出详情页复用备注编辑器与列表多行编辑两种候选，以及“已提交”“结果未知”争议状态，`project/` 提供产品目标、Progress 和页面/编辑器/单订单 API 源码。执行前记录夹具版本及文件清单。新上下文执行者只收到任务、项目和有效 Skill；评判者另读 `evals/dev-flow-stages/evaluators/proposal-cost.json`，逐项核查真实代码读取、改动范围/成本比较、状态触发/价值、给产品/UI 的可执行建议与必要反馈保留。本场景只要求技术反馈，不假称产品/UI 已实际修订。原始会话、派发、代码引用和产物保存在本轮隔离行为记录，并在此填路径与候选。
- **证据/属性：** P6 静态协议、P8 固定代码夹具与原生派发/独立评审记录；**整体必需**。`CHK-01A/B` **通过，TC-01 在本轮插件方法及隔离技术反馈范围内通过**。[独立行为报告](2026-10-21-behavior-report.md)核查详情/列表/编辑器/单订单 API 的真实代码比较、争议状态和必要反馈，以及 `feedback-r1` 的独立 Review。产品/UI 对该方案的**实际业务回应与真实 UI 效果仍未验证**，不得把此 TC 扩写为真实项目闭环。

### TC-02 四篇技术文档独立且链接可采用

- **原要求/预期：** 研发主笔一篇架构与实现合一的设计；独立 Review、实施计划、架构技术收尾各有独立正式模板和实际可采用链接。主设计引用其他三篇的有效版本、状态和结论；Review 记录对象、执行者、发现与闭环；计划说明步骤、依赖、自测和交付；收尾引用实际实现、验收/交付与长期资产。讨论稿不能冒充正式模板。
- **步骤/检查：** `CHK-02A` 从 `skills/dev-engineering/assets/templates/`、`skills/dev-architecture/assets/templates/`、职责入口及项目索引模板，逐个打开四篇正式模板及相互引用，核对路径真实且内容分工无第二份总体进度；`CHK-02B` 在隔离临时项目按模板建四篇实例，填写同一虚构迭代的版本/链接与一项 Review 闭环，逐链接访问并由未主笔者核对可接手性；`CHK-02C` 对照本轮讨论模板与有效方案检查正式模板没有遗漏必要字段。
- **证据/属性：** 链接检查清单、隔离实例和 Review 记录（工具契约/隔离行为）；**必需**。`CHK-02A/B/C` 在 C2 **通过**：四篇独立正式模板、一个合成实例的 34 个相对链接/锚点可解析，Review 多对象两轮与稳定 `plan-r1` 均保留；见 P6 模板实例及链接结果。TC-02 **通过（合成模板适用性）**，不代表真实项目文档已经完成。

### TC-03 原生 subagent、唯一写入者与独立评审

- **原要求/预期：** 标准跨职责专业工作在宿主可用且允许时默认使用实际 Harness subagent；任务包给原目标、Skill/有效输入版本、候选、问题、窄读写边界和回报条件。作者不把自查登记为独立 Review，共享文件有唯一写入者；主会话在委派/等待超时后持续集成和推进。不能用角色名称或生成入口代替真实派发。
- **步骤/检查：** `CHK-03A` 核对 `subagent-guidance.md`、`codex-agent-configuration.md`、总纲、相关 Skills 与生成宿主入口，执行 `python3 scripts/sync_host_agents.py --check`；`CHK-03B` 在隔离代表任务真实派发设计作者与另一个独立评审上下文，记录实际模型/强度、输入版本、读写范围、评审发现、作者修订、定向复核以及主会话在等待后的下一步；若宿主限制派发，如实记降级及独立性缺口。
- **证据/属性：** P6 同步输出、P8 [原生派发记录](../../.dev/runs/flow-revision/native-dispatch.md)、独立 Reviewer 的 AR-01/IR-01 发现及定向复核；**整体必需**。`CHK-03A/B` **通过，TC-03 通过**。作者、评审者和写入边界实际分离，主会话继续集成；首次代理超时及曾接触判据的上下文不计盲测通过，相关重试与剔除理由见[行为报告](2026-10-21-behavior-report.md)。

### TC-04 全生命周期唯一 Progress

- **原要求/预期：** 多阶段任务从起点展示到最终交付/运行验证的全部阶段、已完成/当前/未开始、阶段目标和下一步；一个 Progress/Todo/既有索引为总体状态权威，其他文档只引用或投影。候选变化、阻塞、派发、Review 与结束前更新；状态脚本读取实际权威路径。
- **步骤/检查：** `CHK-04A` 对照方案第六节检查 `progress-management.md`、`stage-state.md`、Progress/索引模板与本轮 Progress。本轮明确选择**人读 `docs/plans/2026-10-21-flow-revision/Progress.md` 为唯一总体权威**：核对最终目标、P1–P8 完整阶段、当前阶段/目标、下一步、未开始项及其他文档无人工双写。本轮未选择结构化机器核验，不要求本轮 Progress 存在 `dev-flow-state` 块；以后若实际选择结构化状态，须在唯一权威放一个有效块并以其真实路径运行核验器。`CHK-04B` 执行 `python3 -m unittest discover -s tests -p test_iteration_checks.py -v`，检查隔离夹具中 Progress 路径作为唯一结构化权威的可用性及只读 CLI 断言；`CHK-04C` 在固定 `proposal-cost` 夹具的新上下文恢复场景观察执行者是否先读取当前阶段及全部后续阶段，再按其实际写入权限说明当前目标/下一步，不能把一次设计反馈当整体完成；候选失效的机器判定另由 TC-06 负例证明。
- **证据/属性：** 本轮人读 Progress、44/44 状态测试及 P8 隔离场景记录；**整体必需**。`CHK-04A/B/C` **通过，TC-04 通过**：`proposal-cost` 保留设计期反馈后的全部后续阶段，`single-progress-authority` 只更新 Progress 并对该真实路径运行核验器，实施阶段退出 0、结束阶段退出 1。该合成实例不替代本仓库最终 Progress 由主 Agent 收口；本轮人读 Progress 无结构化块不构成失败。

### TC-05 正式 TC 后置，同时保留实施前预期与授权

- **原要求/预期：** 完整功能实施前受影响业务规则、边界、成功/拒绝/恢复结果、重要取舍和交付形态已有有效确认；设计 Review、计划复核与明确范围实施授权成立。完整正式 TC 的维护、独立 Review 与执行在完整候选后，不能作为开工前置；研发局部测试与回归随实现继续。
- **步骤/检查：** `CHK-05A` 核对共同协议、研发/验收 Skills、正式模板及现行入口，不得残留“完整 TC Review/人工确认后才能开工”强制门槛，也不得删除设计层预期和授权；`CHK-05B` 使用状态测试中的授权、设计确认、后置用例与依赖夹具验证：缺授权拒绝开工，只有设计答复拒绝开工，同范围有效授权可复用，空 TC 不妨碍已有全部前置条件的开工；`CHK-05C` 使用 eval ID `post-candidate-cases-delivery` 的**同一次运行**，把 `evals/dev-flow-stages/fixtures/post-candidate/task.md` 和同目录 `project/` 作为其固定项目输入增强，在新上下文观察执行者是否从项目原规则/确认推导正式 TC、独立 Review 后执行验收与真实 zipapp 交付，评判者另读 `evals/dev-flow-stages/evaluators/post-candidate.json`。执行者不能看到 evaluator；运行前记录输入/判据版本、新会话 ID、产物及原始结果路径。`proposal-cost` 仅用于设计期“不预写完整 TC、计划保留研发自测”的边界，不能证明已实现后的正式用例行为。
- **证据/属性：** P6 静态/状态测试及 P8 合成订单备注项目的正式[验收结果](../../.dev/runs/flow-revision/behavior-inputs/post-candidate/docs/dev-flow/iterations/order-note/acceptance/result.md)、[逐调用证据](../../.dev/runs/flow-revision/behavior-inputs/post-candidate/docs/dev-flow/iterations/order-note/acceptance/evidence-c2.json)与独立 Review；**整体必需**。`CHK-05A/B/C` **通过，TC-05 在隔离 CLI 项目范围内通过**：从 RULE-01～06、AC-01～07 推导 TC/CH-01～08，AR-01/IR-01 修复并复核后执行 30 次子进程、45 项断言和源码外 zipapp 读回。研发自测与正式验收分开记录；合成项目不登记为真实业务 UI 项目。

### TC-06 空 cases、候选与输入失效

- **原要求/预期：** 标准/系统实现范围在有效设计、计划及授权后，`cases: []` 可开工但不得结束。正式 TC、Review 和检查绑定当前候选；源码候选变化使受影响结果失效，输入规格升版使相应确认/Review 失效；未受影响结果仅凭具体影响分析和原证据复用，不覆盖历史失败。
- **步骤/检查：** `CHK-06A` 复跑状态测试，重点检查 `test_standard_scope_can_start_before_cases_but_cannot_finish_empty_cases`、`test_formal_case_review_is_bound_to_current_candidate`、输入版本变化、旧候选证据拒绝及有依据复用；`CHK-06B` 以合成 Progress/状态实例分别模拟空 cases、改变候选、改变有效输入、无关候选变更，运行 `python3 skills/dev-flow/scripts/check_iteration.py <隔离状态文件> --root <隔离项目根> --phase implementation` 和 `--phase finish`；记录 JSON 及退出码；`CHK-06C` 核对失效与复用规则在协议、模板和实际用例记录中一致。
- **证据/属性：** runner 输出、合成状态和逐场景 JSON（工具契约）；**必需**。C2 的 `CHK-06A/B/C` **通过**：状态套件 44 项中的对应断言通过；五个额外合成 CLI 正反例均得到预期退出码和 JSON（空 cases 可开工/不可结束、旧候选、输入变更、有依据复用）；协议/模板静态一致。TC-06 **通过（声明契约）**，不证明真实业务变化处理。

### TC-07 交付缺项与逐检查完成结论

- **原要求/预期：** 完整候选必须在独立实现 Review、正式 TC 独立 Review、全部必需验收检查及约定实际交付成立后结束。任一交付/验收检查未执行、失败、受阻、跳过或失效，所属 TC 与整体不得通过；服务保存读取、导出协调器或 HTML 预览不得冒充应用重开、系统分享或原生布局。
- **步骤/检查：** `CHK-07A` 复跑状态测试中的 `test_formal_case_review_and_delivery_are_finish_conditions`、必需检查非通过、旧候选及证据类型边界；`CHK-07B` 在合成完整候选中分别留空交付证据、把交付标为 pending、使用错误 kind/观察项、提供有效证据，执行核验器 `--phase finish` 并核对逐 TC 与总体结论；`CHK-07C` 核对验收/运维/收尾模板的逐项汇总和实际交付入口字段。
- **证据/属性：** 合成实例、退出码/JSON、模板检查（工具契约）；**必需**。C2 的 `CHK-07A/B/C` **通过**：状态套件对应断言通过；五个额外合成 CLI 场景显示交付 pending、空证据、证据 kind 错误、必需检查 blocked 均不能结束，合成有效证据才可结束；验收/运维/架构收尾模板静态一致。TC-07 **通过（声明契约）**，不证明本轮真实交付完成。

### TC-08 八 Skills、生成清单与隔离安装

- **原要求/预期：** 发布候选按 0.x 不兼容变化升级 minor，两份 plugin manifest 与 Kimi 清单、README/安装说明一致；同步生成六个职责入口，包内共八个 Skills。新文件入 Git 后打包；隔离验证篡改缓存/异来源拒绝、安装/检查/移除及用户 AGENTS.md、个人 Agent 配置保留。不以历史七 Skills 预期验收当前候选。
- **步骤/检查：** **P6 隔离契约：** `CHK-08B` 运行 `python3 -m unittest discover -s tests -p 'test_plugin_installation.py' -v`，核对六项隔离打包/缓存/来源/用户配置保留；`CHK-08C` 运行 `python3 evals/host-adapters/test_host_adapters.py -v`，核对六项宿主适配回归中的八 Skills 预期，旧七 Skills 断言须纠正后复跑。两项检查绑定 P6 已就绪源码候选，不要求此时最终发布版本。**P7 交付候选：** `CHK-08A` 由主 Agent 确定语义版本后核对 `plugin.json`、`.codex-plugin/plugin.json`、`kimi.plugin.json`、`README.md`、`docs/plugin.md` 的版本与八 Skills 清单；运行 `python3 scripts/sync_host_agents.py --write` 后 `--check`，核对六个生成职责入口；`CHK-08D` 在新文件纳入 Git 后运行 `python3 scripts/manage_plugin.py build`，核对 package-files.json、八 Skills、源码/包指纹和版本。P7 若改动包内文件或候选版本，先判定 P6 Review/检查受影响范围并定向复评/复验，再安装。
- **证据/属性：** P6 隔离测试 6/6、宿主适配 6/6；P7 三份 manifest、生成入口、实际 install 内 build 与清单/缓存指纹；**整体必需**。`CHK-08A/B/C/D` **通过，TC-08 通过**：两份插件 manifest 与 Kimi 清单均为 `0.3.0`；`sync_host_agents.py --write` 已由主 Agent 运行，本次再独立执行只读 `--check`，得八 Skills、六 roles、`synchronized: true`。[最新安装构建输出](../../.dev/runs/flow-revision/install-sync.log)为 718 文件，包哈希 `ada34c791aa2ab6d61d791ea538d7e8e9b7b86f091a690dde011cef6e26ff194`；源码和缓存 inventory 字节 SHA-256 与其一致。[check](../../.dev/runs/flow-revision/install-sync-check.json)为 enabled、8 Skills、source_matches_cache。首次 716 文件包亦保留在原记录，不能冒充最新包。

## 实际宿主、隔离行为与真实项目

### TC-09 Codex 实际升级安装与 check

- **原要求/预期：** P6 必需检查通过并冻结同一源码候选后，执行实际 Codex 插件安装/更新与 `check`；启用状态、缓存版本、八 Skills、源码/缓存指纹一致，记录产物和位置。安装后包内文件变化须重新验证、构建、安装。Kimi 是否更新另按其原生流程判断。
- **步骤/检查：** 主 Agent 执行 `python3 scripts/manage_plugin.py install`，随后 `python3 scripts/manage_plugin.py check`；核对返回的 `enabled=true`、`skills=8`、`source_matches_cache=true`，及 `.dev-flow/plugin-install.json` 指向的实际缓存、manifest 版本和包指纹。验收者读取原始命令输出与候选，核对安装先后及未变更。**本用例编写阶段不运行安装。**
- **证据/属性：** 真实 Codex CLI [安装前状态](../../.dev/runs/flow-revision/install-before.json)为旧 `0.2.2`，[实际安装后状态](../../.dev/runs/flow-revision/install-after.json)为已启用 `0.3.0`、八 Skills、缓存 `/Users/guoshencheng/.codex/plugins/cache/dev-flow-local/dev-flow/0.3.0`；[首次 check](../../.dev/runs/flow-revision/install-first-check.json)及[718 文件重装 check](../../.dev/runs/flow-revision/install-sync-check.json)均为 enabled、skills=8、source_matches_cache=true。**TC-09 通过（目前已记录的 Codex 本机安装候选）**。文档/引用最终收尾后主 Agent 会再次全包 check，其未来哈希不在本记录预填；Codex 成功不表示 Kimi 已安装/更新。

### TC-10 新会话发现与代表专业行为

- **原要求/预期：** 实际安装后新会话可发现当前八 Skills 和可用 Harness 派发能力；标准任务能按领域真实派发，独立 Review 与作者分离，设计期代码反馈、完整候选后用例/验收、基线内修复、候选失效、Progress 恢复及主会话持续运行符合协议。入口存在或模拟模型文字均不能证明专业判断。
- **步骤/检查：** `CHK-10A` 安装后新建会话读取当前已启用版本/Skill 列表和实际派发工具，必要时重启宿主后复查。`CHK-10B` 按 [行为评测入口](README.md) 在相互独立的新 Codex 上下文必跑**七个场景**：`evals.json` 的 `mixed-rename-mobile`（混合范围/局部授权）、`evidence-does-not-expand`（原生证据边界）、`valid-quick-fix`（合法局部修复）、`post-candidate-cases-delivery`（后置用例/交付）、`single-progress-authority`（唯一进度）、`native-subagent-independent-review`（真实派发/独立评审），另加 `proposal-cost`（代码成本、两种交互候选、争议状态和 Progress 恢复）。`mixed-rename-mobile`、`evidence-does-not-expand`、`valid-quick-fix`、`single-progress-authority` 分别使用 `fixtures/mixed-rename/`、`fixtures/evidence/`、`fixtures/quick-fix/`、`fixtures/progress/` 下的隔离项目；执行者仅获取 `evals.json` 对应 `prompt` 字段、项目输入和 Skill，不获取同一 JSON 的 `expected_behavior`。`post-candidate-cases-delivery` 在**一次运行中**使用 `fixtures/post-candidate/task.md` 和其 `project/` 作为固定项目输入增强，评判取 `evaluators/post-candidate.json`，不额外启动一次抽象问答；`proposal-cost` 输入取 `fixtures/proposal-cost/task.md` 和其 `project/`，评判取 `evaluators/proposal-cost.json`；原生派发场景使用实际 Harness 工具上下文。候选/输入失效的确定性负例由 TC-06 承担，若要声称 Agent 在变化后主动处理失效，还须另运行 `changed-baseline` 并单独登记。各场景先记录夹具和判据版本；评判者逐项看实际动作、引用版本、派发/Review、用例时点、交付与结束判断。记录每次新会话 ID、输入快照、原始会话/产物路径、评判者和逐场景结果；`CHK-01B`、`CHK-05C` 可复用本 TC 对应场景的同一次运行，但须分别判断各自预期。
- **证据/属性：** [P8 独立行为报告](2026-10-21-behavior-report.md)逐读固定输入快照、每场景 `input/events/final/exit` 与产物；**必需**。`CHK-10A/B` **通过，TC-10 在新会话发现和七个固定隔离场景范围内通过**。新会话发现缓存 `0.3.0`、总纲 `0.29`、八 Skills 和原生派发工具；四个 CLI 场景加 `proposal-cost`、`post-candidate-cases-delivery`、`native-subagent-independent-review` 均经未参与主笔者独立评判。17 个策略输入仅执行其中六个并另跑 proposal；未执行的 11 个与 `changed-baseline` 保留未覆盖。先前超时、失明盲测上下文剔除及重试记录仍在原报告，退出码 0 本身不当作行为通过。

### TC-11 真实业务项目与架构收尾边界

- **原要求/预期：** 若本轮指定真实业务项目，须在其真实入口核验设计/实现/验收/交付链路及最终结果，保存项目版本、环境、核心操作和回读/恢复证据；本轮未指定业务项目时明确缺口，不虚构“真实项目通过”。架构收尾基于当前源码、完整 Review、验收、安装/发现结果核对技术差异、长期资产和遗留。
- **步骤/检查：** `CHK-11A` 在明确项目和范围后补项目专属 TC 并实际执行；无项目时登记“不适用本次插件源码候选，真实业务能力未验证”，附本轮范围来源；`CHK-11B` P8 读取架构技术收尾、能力现状、Progress 与最终交接，逐项核对引用的证据候选和未完成项，确认没有将工具/宿主结果写成真实项目结果。
- **证据/属性：** `CHK-11A` **不适用本次插件源码/安装任务**：用户未指定真实业务 UI 项目；P8 的订单备注是有明确合成规则的隔离 CLI/zipapp 项目，不能登记为真实客户/生产 UI 验收。该能力仍未验证。`CHK-11B` **通过，TC-11 在本轮适用范围内通过**：[架构技术收尾 1.0](../../docs/plans/2026-10-21-flow-revision/architecture-closeout.md)准确区分 C2 插件候选、隔离项目自身 C2、P6/P7/P8 证据与 Kimi/真实 UI 缺口；[产品](../../docs/product-agent.md)、[视觉](../../docs/visual-agent.md)、[运维](../../docs/operations-agent.md)职责现状已修正本轮原生执行时态，并分别保留各职责自身未验证的边界。最终 Progress/交接由主 Agent 更新，不在此预填完成。

## 执行登记与汇总

### P6 当前候选执行记录（2026-10-21）

本次执行绑定 `C2-62e99b8b7a6d`、基线 `503fcb4768a658772fd4648ec19b7ceedcd5a1ac`。[候选清单](../../.dev/runs/flow-revision/source-candidate.json)包含 230 个执行协议文件；执行前后按 SHA-256 复核均为 **0 项不匹配**。原始日志、合成实例与 JSON 均在 [P6 证据目录](../../.dev/runs/flow-revision/p6/static-review.md)，其中静态检查详情见该记录；这批结果不证明 P7 安装或 P8 Agent 行为。

| 检查 | 实际入口、证据类型和原始结果 | 当前判定 |
| --- | --- | --- |
| `CHK-01A` | 对照总纲、执行协议及产品/视觉/研发/架构入口；[静态检查](../../.dev/runs/flow-revision/p6/static-review.md)记录确认前真实代码成本、争议状态与产品/UI 回写规则 | **通过**；P8 真实反馈待验 |
| `CHK-02A` | 打开四篇正式模板和相关职责入口；[静态检查](../../.dev/runs/flow-revision/p6/static-review.md)核对独立分工与主设计链接 | **通过** |
| `CHK-02B` | 在 [合成实例目录](../../.dev/runs/flow-revision/p6/templates/engineering/design.md)填四篇，运行 `python3 .dev/runs/flow-revision/p6/check_templates.py`，退出码 0；[链接结果](../../.dev/runs/flow-revision/p6/template-links.json)为 4 文档、34 个可解析相对链接/锚点，Review 保留 `design-r1/r2` 与 `plan-r1` | **通过**；实例明确为合成数据 |
| `CHK-02C` | 将正式四篇与方案 0.3、四篇讨论模板对照；[静态检查](../../.dev/runs/flow-revision/p6/static-review.md)记录主设计、Review、计划、收尾字段 | **通过** |
| `CHK-03A` | 核对 Harness/职责规则；`python3 scripts/sync_host_agents.py --check` 退出码 0，[原始输出](../../.dev/runs/flow-revision/p6/sync-check.log)显示 8 Skills、6 roles、`synchronized: true` | **通过**；原生派发待 P8 |
| `CHK-04A` | 核对本轮人读 Progress、进度指南与状态协议；[静态检查](../../.dev/runs/flow-revision/p6/static-review.md)确认 P1–P8、当前目标/下一步与无第二份手工进度 | **通过**；本轮不要求结构化块 |
| `CHK-04B` | `python3 -m unittest discover -s tests -p test_iteration_checks.py -v`，退出码 0，[原始输出](../../.dev/runs/flow-revision/p6/state-tests.log)为 **44/44**，含隔离 Progress 路径和只读 CLI | **通过**；不把合成测试当 P8 恢复行为 |
| `CHK-05A` | 检索现行 Skills、入口、README 与插件说明中旧 TC 前置/七 Skills/逐片正式验收表达；[静态检查](../../.dev/runs/flow-revision/p6/static-review.md)核对命中语义 | **通过**；未见旧门槛复现 |
| `CHK-05B` | 同一 [44 项状态测试日志](../../.dev/runs/flow-revision/p6/state-tests.log)中的实施授权、设计确认、后置用例及空 cases 场景 | **通过**；P8 执行者真实选择待验 |
| `CHK-06A` | 同一 [44 项状态测试日志](../../.dev/runs/flow-revision/p6/state-tests.log)中的空 cases、候选、输入、复用与格式负例 | **通过** |
| `CHK-06B` | 执行 `python3 .dev/runs/flow-revision/p6/scenarios/run_cases.py`，退出码 0；[逐场景汇总](../../.dev/runs/flow-revision/p6/scenarios/scenario-summary.json)及各目录 `state.json`、`stdout.json`、`stderr.txt`：空 cases 开工 0/结束 1、旧候选 1、输入变更 1、未受影响复用 0 | **通过**；合成状态声明一致性 |
| `CHK-06C` | [静态检查](../../.dev/runs/flow-revision/p6/static-review.md)对照状态协议、执行协议和正式验收模板的失效/复用规则 | **通过** |
| `CHK-07A` | 同一 [44 项状态测试日志](../../.dev/runs/flow-revision/p6/state-tests.log)中的交付缺项、必需检查状态与证据 kind 边界 | **通过** |
| `CHK-07B` | 同一 [十场景 JSON 汇总](../../.dev/runs/flow-revision/p6/scenarios/scenario-summary.json)：交付 pending/空证据/错误 kind/必需 blocked 的完成退出码均为 1；合成有效证据完成退出码 0，逐用例 status 与预期一致 | **通过**；不能折算真实交付 |
| `CHK-07C` | 对照验收报告、技术检查、运维交付和架构收尾模板；[静态检查](../../.dev/runs/flow-revision/p6/static-review.md)确认逐检查与实际产物/环境字段 | **通过** |
| `CHK-08B` | `python3 -m unittest discover -s tests -p test_plugin_installation.py -v`，退出码 0，[原始输出](../../.dev/runs/flow-revision/p6/installation-tests.log)为 **6/6**，覆盖隔离打包、缓存篡改/异来源与用户配置保留 | **通过**；实际安装待 P7 |
| `CHK-08C` | `python3 evals/host-adapters/test_host_adapters.py -v`，退出码 0，[原始输出](../../.dev/runs/flow-revision/p6/host-adapters.log)为 **6/6**，适配断言为八 Skills | **通过**；真实新会话发现待 P8 |

`CHK-06B/07B` 的 JSON 是状态核验器 CLI 输出；其中“通过”只指预设正反例与退出码符合协议，不声明合成记录中的用户确认、原生界面或交付真的发生。四篇实例由未主笔正式模板的本次验收执行者编写与检查，多对象 Review 中的“独立评审者”明确为示例角色，不充作本轮插件源码独立 Review。

### P7/P8 实际证据（2026-10-21）

| 检查 | 已核对的当前事实与原始位置 | 判定及边界 |
| --- | --- | --- |
| `CHK-08A` | `plugin.json`、`.codex-plugin/plugin.json`、`kimi.plugin.json` 均为 `0.3.0`；主 Agent 已运行生成器 `--write`，本次只读 `--check` 返回八 Skills/六 roles 同步 | **通过**；Kimi 清单同步不等于 Kimi 原生安装 |
| `CHK-08D` | [718 文件 install 内 build](../../.dev/runs/flow-revision/install-sync.log) 包哈希 `ada34c791aa2ab6d61d791ea538d7e8e9b7b86f091a690dde011cef6e26ff194`；独立读取源码/缓存 `package-files.json` 均 718 条且字节 SHA-256 一致 | **通过**；先前 [716 文件安装](../../.dev/runs/flow-revision/install-first.log)是保留的旧包历史，最终收尾再改包需重建/check |
| `TC-09` | [安装前](../../.dev/runs/flow-revision/install-before.json) `0.2.2` → [安装后](../../.dev/runs/flow-revision/install-after.json) 已启用 `0.3.0`，八 Skill 名称及实际缓存路径；[首次 check](../../.dev/runs/flow-revision/install-first-check.json)和[同步后 check](../../.dev/runs/flow-revision/install-sync-check.json)均为启用、八 Skills、源码/缓存相符 | **通过**；真实 Codex 本机安装，不折算 Kimi 及未来文档收尾后的包状态 |
| `CHK-10A` | [行为报告的新会话发现](2026-10-21-behavior-report.md#已完成场景逐项评判)读取缓存 `0.3.0`/总纲 `0.29`、八个 `SKILL.md` 与原生派发工具 | **通过**；仅发现，派发结果见 `CHK-03B/10B` |
| `CHK-01B`、`CHK-04C` | [proposal-cost 与 Progress 场景评判](2026-10-21-behavior-report.md#原生派发与复合场景)和[唯一 Progress 场景](2026-10-21-behavior-report.md#已完成场景逐项评判)；技术实际读代码、比较两交互候选与争议状态，恢复当前/后续阶段，状态核验实施 0、结束 1 | **通过隔离行为**；产品/UI 实际决定及真实 UI 未验证 |
| `CHK-03B` | [真实原生派发/作者与 Reviewer 边界](../../.dev/runs/flow-revision/native-dispatch.md)、[行为独立评判](2026-10-21-behavior-report.md#原生派发与复合场景)及 AR-01/IR-01 原评审者定向关闭 | **通过**；不由角色名或一次进程完成推断独立性 |
| `CHK-05C` | [合成订单备注正式结果](../../.dev/runs/flow-revision/behavior-inputs/post-candidate/docs/dev-flow/iterations/order-note/acceptance/result.md)及[逐调用 JSON](../../.dev/runs/flow-revision/behavior-inputs/post-candidate/docs/dev-flow/iterations/order-note/acceptance/evidence-c2.json)：v2/C2 的 TC/CH-01～08 全通过，30 次进程、45 项断言；源码目录外 zipapp 独立保存/读回 | **通过隔离 CLI/zipapp 行为**；不是插件执行候选变更，也不证明真实业务 UI 交付 |
| `CHK-10B` | [P8 独立报告](2026-10-21-behavior-report.md#当前结论)对固定七场景逐项判通过；输入快照 `.dev/runs/flow-revision/behavior-input-snapshot.json` 与每场景原始 `input/events/final/exit` 分存 | **通过固定七场景**；未执行的 11 个策略输入及 `changed-baseline` 不扩大本轮结论 |
| `CHK-11A` | 本轮范围为插件改造、安装及隔离评测；未指定真实业务 UI 项目。隔离订单备注 [项目技术收尾](../../.dev/runs/flow-revision/behavior-inputs/post-candidate/docs/dev-flow/iterations/order-note/architecture/closeout.md)明确自身 C2 与本仓库插件 C2 不同 | **不适用本轮，真实业务 UI 能力未验证** |
| `CHK-11B` | [本仓库架构收尾 1.0](../../docs/plans/2026-10-21-flow-revision/architecture-closeout.md)已核实际源码、完整 Review、P6/P7/P8 及未验证边界；复读[产品](../../docs/product-agent.md)、[视觉](../../docs/visual-agent.md)、[运维](../../docs/operations-agent.md)现状，均链接本轮行为报告并区分已验证技术反馈/验收与各职责自身、真实业务及发布缺口 | **通过**；技术收尾及长期资产一致，最终 Progress/总交接由主 Agent 判断 |

P8 行为报告保留首次 CLI 超时、代理重试、混合/quick 夹具重置及曾接触 evaluator 的旧评审上下文剔除。通过判断只依据最终干净夹具、新上下文与独立评判；未执行的扩展和真实业务 UI 不借由工具层负例或合成 zipapp 取代。

阶段门槛按**检查编号**登记，不把一个跨阶段 TC 提前判为通过：

| 阶段 | 本阶段必需检查 | 阶段通过边界 |
| --- | --- | --- |
| P6 完整源码候选 | `CHK-01A`、`CHK-02A/B/C`、`CHK-03A`、`CHK-04A/B`、`CHK-05A/B`、`CHK-06A/B/C`、`CHK-07A/B/C`、`CHK-08B/C` | **已通过**：C2 完整差异与用例独立 Review、所有列项及合成实例/CLI 记录均有证据。 |
| P7 发布候选及 Codex 安装 | `CHK-08A/D`、TC-09 | **已通过当前 718 文件安装候选**：`0.3.0` 启用、八 Skills 与源码/缓存相符；后续包内文档变化须由主 Agent 重建/check。 |
| P8 新会话与收尾 | `CHK-01B`、`CHK-03B`、`CHK-04C`、`CHK-05C`、`CHK-10A/B`、`CHK-11B`；`CHK-11A` 按真实项目适用性 | 新会话、固定七场景及长期资产一致性 **已通过**；`CHK-11A` 本轮不适用，真实业务 UI 未验证。 |

| 证据层 | 对应用例 | 当前结论 | 后续记录入口 |
| --- | --- | --- | --- |
| 工具契约、文档与模板 | P6 全部；P7 `CHK-08A/D`；P8 `CHK-11B` | P6/P7 **已通过**；技术收尾文档及长期资产一致性 **已通过** | C2 清单、日志、718 文件 inventory 和 P7/P8 表分别保留原始边界 |
| 隔离行为与原生派发 | P6 `CHK-02B`；P8 `CHK-01B/03B/04C/05C/10B` | **已通过指定合成/隔离场景** | 实际 Harness、新会话与独立评判见 P8 报告；不能推广为真实业务 UI |
| 实际 Codex 宿主 | TC-09、`CHK-10A` | **已通过当前安装和发现** | 实际安装/check、缓存路径/版本及八 Skills；最终文档收尾后的 check 由主 Agent 再核 |
| 真实业务项目 | `CHK-11A` | **本轮不适用；能力未验证** | 未指定真实业务 UI 项目；订单备注仅为隔离合成 CLI |

**当前验收判定：C2 的 P6、当前 718 文件的 P7、本轮固定七场景的 P8 行为及 TC-11B 资产一致性均通过；本轮适用的技术与正式验收条件通过。** [完整源码独立 Review 第三轮](../../reviews/2026-10-21-flow-implementation-review.md#第三轮定向复核c2-62e99b8b7a6d)已关闭 F1/F2；[架构收尾 1.0](../../docs/plans/2026-10-21-flow-revision/architecture-closeout.md)已完成其技术文档。最终包再 check、Progress/交接集成后，由主 Agent 判断整体结束；此处不预填未来哈希，也不把真实业务 UI 能力登记为通过。历史失败、修订、复核与未执行扩展仍保留在原记录。
