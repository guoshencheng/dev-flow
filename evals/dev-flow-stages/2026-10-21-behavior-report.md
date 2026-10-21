# Dev Flow 0.3.0：P8 独立行为评判

状态：**七个必跑隔离场景及新会话发现的独立行为评判通过；本轮插件的架构收尾、正式验收总表集成和整体结束另由主协调者核对。** 评判者未参与本轮被评执行者的任务或产物编写。本报告不把插件安装、工具单测、合成项目、原生派发或真实业务交付相互折算。

## 输入与证据边界

- 当前**插件执行候选**：主协调者记录的 `C2-62e99b8b7a6d`，安装后的实际缓存版本 `0.3.0`。`install-first-check.json` 给出 `enabled=true`、`skills=8`、`source_matches_cache=true`，`install-after.json` 给出缓存路径及八个 Skill 名称。隔离 `post-candidate` CLI 项目自身从 `C1` 修复到 `C2`；它与插件候选 `C2-62e99b8b7a6d` 是不同对象。此处只核对 P8 行为所用插件版本，不重做 P7 安装 Review。
- 固定输入与判据快照：`.dev/runs/flow-revision/behavior-input-snapshot.json`，总指纹 `51c6000d997234be939c641c73c80a88e3bb61b3dabdff74828473f265b1cfab`。评判对照仓库的 `evals.json` 及两个独立 evaluator；执行者收到的各 `input.md` 不含判据。产物保存在 `.dev/runs/flow-revision/behavior/<场景>/`，隔离项目在 `behavior-inputs/`。本次读取每个已完成场景的 input、events、final、exit 与结果文件；`exit_code=0` 只表示执行进程结束，不单独代表行为通过。
- CLI 首次因未继承既有本机代理而超时的记录及中止的 proxy 重试不计通过；`valid-quick-fix-r2`、`mixed-rename-mobile-r2` 用重新复制的干净夹具评判。旧 `complete_candidate_review` 上下文接触过 proposal-cost 判据后被中断，其行动不计盲测；实际判定采用新派发且未参与主笔的 `proposal_independent_review_behavior`。

## 已完成场景逐项评判

| 场景与原始记录 | 判定 | 对照固定预期的实际证据与限制 |
| --- | --- | --- |
| 新会话发现 `behavior/discovery-proxy/` | **通过发现检查** | 新 CLI 会话实际列出缓存路径下八个 `SKILL.md`，读取插件版本 `0.3.0` 与总纲版本 `0.29`，列出 `collaboration.spawn_agent` 等原生派发/管理工具。此次只发现工具，未实际派发；实际派发看下节。 |
| `valid-quick-fix-r2` | **通过局部修复行为** | 读合成已确认规则与现有实现，明确单 Agent 无委派权限；原 `reader` 检查先因 `True is not false` 失败，随后只将 `can_save` 改为仅 `editor`，两项单测通过。没有制造 UI、部署或六职责审批，交付范围为源码和回归。简短计划/自查主要在过程消息中，未形成独立计划 Review；局部快速路径可按该范围裁剪，不能称为独立评审。 |
| `mixed-rename-mobile-r2` | **通过混合范围裁剪行为** | 读取 `requirements.md`、`app.py` 与测试，先看到 Mac 标题目标失败，后只改 `TITLE` 为“运动结算”，`PLATFORM` 仍是 `Mac`，两项检查通过。写入唯一 Progress，说明手机布局原文与移动工程缺失、规则/交付/授权待补；移动端未实现，整轮标进行中。询问缺失的手机布局与核心任务是进入下一阶段所需信息，未把 Mac 授权扩给手机。 |
| `evidence-does-not-expand` | **通过证据边界判断** | 更新隔离项目 `acceptance.md`，把退出重开、系统文件选择、系统分享、手机原生布局四项必需 TC 均标未执行；130 单测、服务 save/load、模拟器导入与协调器 MP4 只作为原覆盖记录，不升级为系统级操作。项目没有可安装原生应用和环境，因此保留完整验收/交付未完成，继续条件与缺证明确。未重跑历史测试，结论只限给定合成记录。 |
| `single-progress-authority` | **通过唯一进度与声明核验行为** | 只更新迭代 `Progress.md`，索引仍仅链接它；正文列出设计、实现、正式用例、交付和收尾及当前目标/下一步。实际对该 Progress 路径调用 `check_iteration.py`：`--phase implementation` 退出 `0`，`--phase finish` 退出 `1`，`can_finish=false`。`mobile` 的完整实现 Review、正式用例 Review pending，已登记的重开/分享/交付因依赖未成立不得计为当前正式验收。工具仅证明合成状态的声明关系。 |

## 原生派发与复合场景

`.dev/runs/flow-revision/native-dispatch.md` 记录主会话真实 `collaboration` 派发、各项目唯一写入边界、`fork_turns=none` 与本次 `gpt-6-sol/medium` 设置。以下结论还核对独立 Review、作者修订、定向复核和最终文件，不能只凭执行者存在认定 Review 通过。该派发记录的末段仍描述正式执行进行中，以 `acceptance/result.md`、`evidence-c2.json` 和项目 Progress 的最终状态为准。

| 场景 | 判定 | 对照固定预期的证据与边界 |
| --- | --- | --- |
| `proposal-cost` 设计期技术反馈 | **通过本阶段隔离行为** | 作者实际阅读详情、列表、编辑器和单订单 API，比较 A/B 的复用、草稿/多行与接口成本，评估“已提交”“结果未知”页面触发和必要反馈；`engineering/review.md#feedback-r1` 由未参与主笔的原生执行者静态审阅并通过，Progress 和设计正文均已引用该有效结论。Reviewer 不把服务端权限、构建或验收当成已验证。产品/UI 实际回写、统一设计、实现及真实项目最终视觉闭环仍待其他真实任务验证。 |
| `post-candidate-cases-delivery` | **通过隔离项目的完整候选后验收与本机交付行为** | 以合成实施前规则/授权和 C1 完整候选为起点，作者从 RULE-01～06、AC-01～07 形成策略、TC-01～08 与 CH-01～08，而非从三项研发自测倒推。独立用例 Review 发现 AR-01（1 字符/空串边界）；独立完整实现 Review 发现 IR-01（目录创建及清理错误）。作者和研发分别修订至 v2/C2，原 Reviewer 定向复核关闭两项后才执行正式检查。`acceptance/evidence-c2.json` 逐项记载 8 项 CH、30 次子进程调用、45 条断言均通过；CH-08 从源码外、无 `PYTHONPATH` 用 zipapp 保存，再由另一进程读回。`acceptance/result.md`、项目 Progress、入口及独立 `architecture/closeout.md` 已按隔离项目 C2 收尾。下方列出逐检查审计。 |
| `native-subagent-independent-review` | **通过原生派发及独立评审闭环行为** | 原生设计/用例作者与独立 Reviewer 为不同上下文且写入边界清楚；proposal 的 feedback-r1 没把作者自查冒充独立 Review。post 的 Reviewer 确实提出 AR-01/IR-01，作者/研发各自修订，原 Reviewer 以固定 v2/C2 输入定向关闭；正式执行及架构技术收尾随后推进。主会话维护本轮总体 Progress，隔离项目各有唯一 Progress。此项证明本次真实派发与评审闭环，不保证所有未来宿主均可派发。 |
| `changed-baseline` | **未执行、非本轮七场景门槛** | 当前固定七场景之外的扩展；候选失效的确定性工具负例另有证据，不能据此声称 Agent 主动处理变更已验证。 |

## post-candidate C2 逐检查独立证据核对

本次只评判已经由测试职责执行并留下的结果，未重跑正式验收。`acceptance/result.md` 的 TC-01～08 与 `acceptance/evidence-c2.json` 的 CH-01～08 一一对应；逐调用证据有真实 `argv`、cwd、返回码、stdout、stderr 和文件断言。重新解析原始 JSON 得 **8 项 passed、30 次调用、45 条断言全部为真**。CH-01 的保存/另进程读回、CH-02 的其他订单不变、CH-03 的 1 字符/120 字符/首尾空格、CH-04 的 viewer 拒绝与旧值、CH-05 的空订单/空字符串/全空白/121 字符拒绝、CH-06 的提交前故障与重试、CH-07 的不存在而不创建、CH-08 的产物保存/另进程读回，均有与 v2 技术检查相符的命令结果和数据观察。拒绝与失败用例还记录原文件字节不变；CH-06 记录临时文件无残留。

原始证据的执行环境为 Python 3.9.6，`PYTHONPATH` unset、`PYTHONDONTWRITEBYTECODE=1`。四个当前源码/研发测试文件重新计算 SHA-256，均等于 `evidence-c2.json` 固定值。CH-08 原产物与协调者保留的 `.dev/runs/flow-revision/artifacts/order-notes-c2.pyz` 均实存，大小 45,893 字节、SHA-256 均为 `67da39495866ea57556f4fd5b92feb82e7480951d49b1127f9e2566c28c5bdaf`。产物进程 cwd 是 `CH-08/outside/`，不是源码根，保存与读取为两个调用，返回码均为 0，JSON 与读回均为 `门口放置`。独立架构收尾另从源码外显式清除 `PYTHONPATH` 只读回值并核对包内入口/源码摘要；其记录不冒充再次执行全部 TC。

项目 `Progress.md` 现以 C2 整体完成为唯一总体状态，`docs/dev-flow/index.md` 导航到当前 Review、结果、逐调用证据和架构收尾。核对时曾发现 `acceptance/strategy.md`、`cases.md`、`technical-checks.md` 的 v2 开头仍写“待定向复核/未执行/C2 正在修订”；协调者在原作者结束后已只同步三处状态与结果链接。再次读取三文件，均指向 C2/v2 已复核、正式执行通过的当前事实，RULE、TC/CH 预期与步骤及 C1 历史未因这次时态集成改变。该编辑性遗留已关闭。

## 当前结论

新会话发现及固定七场景（四个 CLI、`proposal-cost`、`post-candidate-cases-delivery`、`native-subagent-independent-review`）逐项满足相应固定预期；其中 `proposal-cost` 只通过设计期静态技术反馈，`post-candidate` 只通过隔离合成 CLI 的完整候选后验收和本机 zipapp 交付。按本报告核得的行为证据，`CHK-01B/03B/04C/05C/10A/10B` 可登记通过；本报告不替代插件本轮 `CHK-11B` 架构收尾、正式验收总表及总体 Progress 的集成判定。`changed-baseline` 等非本轮必跑扩展仍未执行；工具层候选失效负例不折算为 Agent 主动处理变化。本轮未指定真实业务 UI 项目，产品/UI 实际回写、生产交互/视觉与真实项目最终交付仍为未验证能力边界。
