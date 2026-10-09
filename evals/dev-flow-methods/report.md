# 可执行研发方法改造与行为验证

日期：2026-10-09。范围：测试先行/回归有效性、系统实验诊断、完整实现评审/意见闭环。沿用六职责。方法、模板、工具对照及本轮隔离行为均取得证据，真实业务项目采用和生产能力仍待验证。

## 方法与字段

新增[测试先行](../../skills/dev-engineering/references/test-first-and-regression.md)及[意见处理](../../skills/dev-engineering/references/review-feedback.md)，扩充[实验诊断](../../skills/dev-engineering/references/diagnosis-and-feedback.md)、[完整实现评审](../../skills/dev-architecture/references/retrospective-and-evolution.md)和[验收回归核验](../../skills/dev-acceptance/references/execution-and-feedback.md)。

实施计划/工程交接补目标行为、测试位置、失败与通过证据；缺陷记录补假设—实验—结果和意见处理；架构模板补完整变更、需求符合性/实现质量两类结论与意见关闭证据。总纲 v0.17、能力目录和相关 Skill 路由至这些参考，继续复用原 tracker 与 bugfix 裁剪规则，不增加人工计划审批或新职责。

## 基线、输入与执行方式

初始仓库基线 `eb43ef0`，核对期间另一会话的公共 Git/委派指导提交为 `7c5926d`，本轮在该已稳定基线上合并方法/模板字段，保留另一会话改动。实施计划来源于已获准的[建设计划](../../docs/plans/2026-10-09-executable-engineering-methods.md)；主 Agent 实施前按原要求、源码、既有案例和写入范围 AI 自查，后由独立上下文对完整改造候选作[实现 Review](../../reviews/2026-10-09-executable-methods-review.md)。

新输入引用既有[产品契约](../dev-acceptance/fixtures/http-ui/docs/product.md)及 HTTP/UI 服务，但构造为独立单一源码，不沿用运行时 broken/fixed 开关。工具对照使用单独副本，与行为执行工程分离；原案例和历史报告未改写。[初始指纹](runs/2026-10-09/independent/initial-manifest.json)固定本轮输入。

首次执行者通过 `fork_turns=none`、派发参数 `gpt-6-sol` / `medium` 独立启动；T01/T02、D01、R01 初审、R01 研发处理分别派发。R01 原评审者没有参与实现，修复后复用其上下文作定向复评。实际[任务输入、投递顺序及澄清](task-inputs.md)已归档；[T 输入声明](runs/2026-10-09/independent/T02/input-and-negative-check.md)、[D 输入声明](runs/2026-10-09/independent/D01/input-scope.md)及 R01 报告记录实际读取范围。

宿主共享文件系统，没有文件级访问隔离或完整访问审计；构造脚本/判据未作为执行输入提供，并被明确排除在读取范围，读取声明来自执行者。不能据此保证技术上无法访问答案或证明每次读取。独立上下文、输入范围、实际检出/修复与独立复验分别说明，不把它们升级为强制沙箱盲测或原生职责注册证据。

## 工具与行为结果

| 案例 | 实际证据与结论 | 主要限制 |
| --- | --- | --- |
| T01 | [执行报告](runs/2026-10-09/independent/T01/report.md)：先编写测试，原源码 viewer POST 201 且存储变化，目标断言退出 1；增加服务端权限校验后同一测试退出 0。红/绿测试指纹一致，主 Agent 独立复跑通过 | Node HTTP/存储，未作浏览器 UI 验收；未做无必要的重构，因此不虚构重构后结果 |
| T02 | [执行报告](runs/2026-10-09/independent/T02/report.md)：同一新测试 previous 201+写入失败，current 403+无写入通过，主 Agent 复跑旧红/新绿一致；识别 `assert.ok(true)` 无保护，保留它作负面对照，以有效测试承担保护 | 保留旧/新源码与指纹，不修改旧实现；测试说明不证明生产身份 |
| D01 | [诊断报告](runs/2026-10-09/independent/D01/report.md)：实际浏览器成功提示/刷新、HTTP/磁盘和同数据重启实验分别定位漏写盘、读取旁路文件、启动快照；保留被否定假设。三例目标红、修复绿，主 Agent 浏览器/HTTP/磁盘复跑均通过 | Node+JSON 遗留样本，不证明数据库事务或其他框架；使用现有本机浏览器/runtime |
| R01 | [原独立评审](runs/2026-10-09/independent/R01/review.md)覆盖三个提交和未提交差异，检出权限与标题两缺陷；[研发处理](runs/2026-10-09/independent/R01/handling.md)分别修复、反驳、澄清，保持待验；[独立复评](runs/2026-10-09/independent/R01/re-review.md)实测五个断言场景通过后形成[关闭记录](runs/2026-10-09/independent/R01/closure.md) | 未执行 R01 浏览器刷新/呈现、生产部署与并发；复评复用原评审上下文，独立于研发实现 |

T01 的红灯执行前 `server.mjs` 指纹为 `01c90bc0…`，绿灯为 `e528a9cd…`，测试 `0478b460…` 不变。T02 旧/新源码与上述对应，测试 `24e9ceff…` 不变。D01 三个修复候选均为 `e528a9cd…`。R01 最终源码为 `8a99e24a…`，独立断言脚本及完整指纹见对应 `record.json`，不仅采用报告自报。

主 Agent 对[证据不变量](runs/2026-10-09/independent/evidence-checks.json)核验了目标红/绿、相同测试、旧候选未改、T01 先后顺序、R01 三提交和当前独立复验候选一致。runner 后续补充实际命令参数文件指纹，以覆盖位于 `evidence/` 的测试脚本；R01 用同一 `handling-http.mjs` 在独立旧/新副本补取[权限红](runs/2026-10-09/independent/R01/retest-old/evidence/protection-auth/record.json)、[标题红](runs/2026-10-09/independent/R01/retest-old/evidence/protection-title/record.json)及[完整绿](runs/2026-10-09/independent/R01/retest-new/evidence/protection-green/record.json)，脚本指纹一致。该补充是工具/保护证据复跑，不再次登记独立盲测检出。

工具对照另确认：T01/T02 旧/R01 错误权限候选返回 201 且写入，新候选 403 且无写入；D01 分别表现为“磁盘无条目”、“磁盘有/读取无且重启无”、“磁盘有/读取无但重启有”。[工具原结果](runs/2026-10-09/controls/control-results.json)与行为结果独立保存，工具本身的成功不代表模型行为。

## 保留的失败与结论边界

语法负例 `node --input-type=module -e 'const = 1'` 退出 1，原始错误为 SyntaxError，未触发 viewer 请求；执行者[判读](runs/2026-10-09/independent/T02/input-and-negative-check.md)明确它不能证明权限缺陷被捕获。D01 首轮三次 `pre-fix` 失败来自错误等待空列表“可见”，尚未保存；执行者将其记为测试方法错误，修正为等待加载完成后才取得 `baseline-red` 目标失败，没有把首次超时登记为检出。

R01 原评审观察脚本退出 0 仅代表采集成功，观察结果实际违反契约，因此评审判阻断；最终复评采用真实断言，五个场景执行通过才关闭。原待验报告保持历史状态，关闭另关联当次候选/证据，不把旧报告刷新日期作为新通过。

runner 的命令、退出码和前后指纹不自动判目标失败；超时与环境失败不能通过。所有用例服务结束后关闭，D01 固定样本端口 19011–19013 已核验停止。独立执行者不改主仓库，主 Agent 核验实际源码和证据后复跑 T/D 必要行为；未重复无关全仓测试。

另以父命令启动子服务后持续运行的[超时对照](runs/2026-10-09/controls/evidence/timeout-process-group/record.json)验证 runner：55 秒后退出 124，进程组终止，子服务[端口关闭](runs/2026-10-09/controls/timeout-check.json)。这是 runner 工具验证，不登记目标行为通过。

## 复用、静态检查与接入

四个改动 Skill 的 `quick_validate.py` 通过；方法/入口相对引用与差异检查通过。独立实现 Review 的 M-01（实际输入范围证据）和 M-02（R01 投递与时序）由本报告、任务输入、读取声明、原评审/待验/独立复评/关闭记录提供定向复核入口；宿主隔离限制如实保留，不以记录文件代替行为证据。

本轮使用已有安装脚本更新七个 Skills，实际 check 返回 enabled/source_matches_cache 均为 true、skills 为 7，见[接入记录](../../reviews/2026-10-09-methods-plugin-check.md)及[当次原始输出](runs/2026-10-09/install-check.json)。安装不会注册新 Agent，未修改安装工具。归档与计划状态更新后再执行最终 install/check 核验全部源码，不以旧缓存结果推定新版本已加载。

原始过程在 `runs/2026-10-09/independent/`，固定对照在 `runs/2026-10-09/controls/`；长期保存原始输出、实际测试、候选源码、补丁、初始指纹和 R01 全部提交/未提交差异，不保存运行数据目录、依赖缓存或 `.git`。运行记录中的原绝对路径保留历史位置，本文链接是仓库内证据入口。

复跑方法见[README](README.md)及案例报告。新行为评测必须用新输入/独立上下文，不能把本轮答案和补丁交给执行者；复跑已知测试仅证明工具/候选行为，不再次登记盲测检出。D01 实测脚本含本机依赖/浏览器绝对路径，跨机器需要明确替换并核验；不声称全新机器可用。
