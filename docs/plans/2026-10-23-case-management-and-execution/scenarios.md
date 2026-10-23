---
id: ENG-case-management-scenarios
title: 用例管理与执行工具合成场景推演
status: superseded
version: 4
updated: 2026-10-23
supersededBy: docs/plans/2026-10-23-case-management-and-execution/design.md
owner: engineering
---

# 用例管理与执行工具合成场景推演

> 本文随原工具方案被替代，仅保留历史内容。当前以用户明确要求的[简化方案](design.md)为准，本文的额外字段、工具和证据门槛不再作为本次要求。


本页是 [研发设计 v4](design.md) 的纸面演算。ID、命令输出、时间、候选、状态均为虚构；没有运行工具、Runner、人工验收或 Dev Flow 核验器，不能登记为执行证据。[产品设计 v2](product.md) 提供 RULE/AC 输入，以下样例业务仅检查契约自洽。

## 固定输入与初始全量

假设三条业务规则：`RULE-X-01` 为普通用户保存偏好并重新读取仍一致；`RULE-X-02` 为无权限者不能修改他人的偏好；`RULE-X-03` 为用户能在目标设备上确认反馈提示。`suite=preferences` 声明这三条规则和相应 AC，按 CHK 要求选择普通用户、Web 或目标设备的必要组合。catalog `v4`、应用候选 `C1`（commit `abc` + dirty 指纹 `d1`）、测试脚本 `T1`、binding `B1`、Runner/adapter `A1`、环境 `ENV-1`、fixture `F1` 构成冻结输入。正式 TC 在此例中**假定**已在完整候选后形成并独立 Review；现实中尚未发生。

| TC / 预期 | 来源与独立用户任务 | 必需 CHK、观察与组合 | 方法 |
| --- | --- | --- | --- |
| `TC-01@2/E1` | RULE-X-01；保存后读回相同 | `CHK-API@3`，`save-read`，普通用户/Web | 自动 |
| `TC-01@2/E2` | RULE-X-01；刷新后仍相同 | `CHK-UI@2`，`refresh-persist`，普通用户/Web | 自动 |
| `TC-02@1/E1` | RULE-X-02；越权修改被拒绝且原值不变 | `CHK-AUTH@1`，`deny-and-no-change`，普通用户/Web | 自动 |
| `TC-03@1/E1` | RULE-X-03；设备反馈可见 | `CHK-MANUAL@1`，`feedback-visible`，普通用户/目标设备 | 真人手动 |

初始全量 run `R1` 的逻辑 `P={API,UI,AUTH,MANUAL}`，其中四个别名各代表含 TC/CHK revision、预期、候选和组合的完整 item 身份。业务视图有 **三条 TC、四个必需 item**。范围账 `L` 另逐一保存 RULE/AC→TC→预期→CHK。若从声明中去掉 `TC-03`，`L` 出现 `coverage_gap(RULE-X-03)`；若去掉 `TC-01/E2` 的必需 CHK，出现 `mapping_gap(TC-01/E2)`。它们无法展开为可执行 P item，却仍阻止清单完整及验收通过。

## 发现、共享与结果对账

### 缺入口的两个分支

**分支 A：临时发现故障。**`R1` 的 `CHK-UI` 脚本实际存在且 B1 指向正确入口，Runner 第一次发现因临时故障只给物理 `{API,AUTH}`。投影后 `D={API,AUTH}`，`P_auto-D={UI}`，UI 为 `blocked(reason=entry_missing)`。C1/T1/B1/A1/ENV-1/F1 及 catalog 指纹全部未变时，可在 **R1** 重新发现；保留第一次 D 记录，第二次 `D={API,UI,AUTH}`。这说明第一次诊断来自发现故障，不把旧事实改写。

**分支 B：真实缺脚本。**独立假设 `R1` 的 B1 指向不存在的 UI 测试。UI 一直 `blocked(reason=entry_missing)`。研发补脚本使 `T1→T2`（或改 binding 为 B2）后建立关联 **R2**，冻结新 manifest；R1 的 P、D 与受阻记录保留，R2 在 C1/T2/B1/A1/ENV-1/F1 下重新发现 `D={API,UI,AUTH}`。以下 Runner 漏结果和身份反例都以 **R2/T2** 为输入，与 R1 不混算。

### 物理 execution 与逻辑 item

R2 默认绑定 `EX-API→{API}`、`EX-UI→{UI}`、`EX-AUTH→{AUTH}`，分别保存物理 `runner_id/context`。假设 catalog 增至 v5，新增 `TC-04/E1` 与其专属 `CHK-UI-04`，和 `TC-01/E2` 的 `CHK-UI` 确实要求同一 UI 观察；两条 CHK 各有自己的 `tc_id`，但指向同一底层 binding。二者候选、环境、fixture、身份权限、隔离数据、观察点和组合上下文全相同，adapter 明确声明可共享，则新 run `R3` 可规划 `EX-UI/runner-id-X/context-c1 → {TC-01/CHK-UI,TC-04/CHK-UI-04}`。物理发现一次 X、物理执行一次 X，投影出两个逻辑 D/R 身份；每条 item 分别核自己的预期与证据，合格时都通过，原始物理结果只存一次并可追溯。

若 `TC-04` 需要管理员身份、不同 fixture 或额外 `permission-banner` 观察，规划拒绝上述 1:N；必须分别执行，或将其保持映射受阻，不能把 X 的结果借给它。另在共享条件成立的 R3 中，若 X 原始结果虽有共同 `refresh-persist`，adapter 只给 `TC-01` 逐预期结果而漏了 `TC-04` 的独立结果/证据关联，则 `TC-01` 可按证据通过，`TC-04` 仍 `result_missing/evidence_missing`；不能由一次物理 exit 0 填平。已声明可选或范围外的整 suite 结果另入附加账，不计入必需 P；范围内本应映射却成为错误身份仍阻断。

### 退出码与身份

R2 的 `D={API,UI,AUTH}`，Runner 退出码 0，但物理返回投影后只有 `R={API,AUTH}`：`P_auto-R={UI}`，UI 为 `result_missing`，执行未完成。另一个独立的 R2 反例是 `P_auto={API,UI,AUTH}`、投影结果 `R={API,AUTH,LEGACY}`；数量同为三，仍列缺 UI 和**范围内错误身份** LEGACY，不能判完整。若 LEGACY 是显式声明的范围外可选测试，列附加账，不当作 UI，也不因它本身阻断；UI 缺失仍阻断。原始 `execution_id/runner_id` 与上下文一并保留，不能只存投影集合。

## 中断、重试与三口径

R2 中 `CHK-API` attempt `a1` 在保存动作处崩溃。日志有 `attempt_started` 与 lease，无终结结果；lease 到期后为 `unknown`。恢复先查 fixture 副作用和原 Runner 报告；若已保存但读回未知，不能直接重做非幂等保存，应隔离或人工判定。已完成 AUTH 不重跑，未开始 UI 可领取；迟到 `a1` 返回进入隔离，不覆盖新 attempt。

R2 的 UI 首次失败 `a1`、同候选重试通过 `a2`：执行已结束，验收为 `flaky_pending`。再成功重试也不解锁；产品缺陷须修复到 C2 新 run 复验，测试/环境误判须有依据更正并升相应版本新 run，保留 R2 历史。若末次仍失败，则执行已结束、验收失败。

| R2 纸面状态组合 | 清单完整性 | 执行完成 | TC 判断 | 整轮判断 |
| --- | --- | --- | --- | --- |
| 规则无 TC，其他项均通过 | 不成立：`coverage_gap` | 已完成已有 P | 已有 TC 可逐项显示通过；缺规则无 TC | 未完成，列 gap |
| UI 已发现但缺结果，MANUAL 待验 | 成立：计划映射与发现无差集 | 未完成：UI 结果缺失、MANUAL 待验 | TC-01、TC-03 未完成；TC-02 可通过 | 未完成，逐项列两种原因 |
| AUTH 失败，MANUAL 受阻 | 清单可成立 | 未完成：MANUAL blocked | TC-02 失败、TC-03 未完成 | 首页标签“失败”，同时保留受阻责任与待验数量 |
| UI 失败后重试通过，其余通过 | 成立 | 已完成 | TC-01 `flaky_pending`，未完成 | 未完成，不自动绿 |

这里“首页失败优先”只决定摘要标签，不能隐藏同 run 的 gap、受阻或未运行。

## 人工无法验证、失败及修复

在 R2，目标设备不可用。甲尚未实际验证，可通过 CLI 提交 `outcome=unable_to_verify`、`reason=目标设备不可用`、`preparation_owner=设备管理员`、`recorded_at`、任务 token 与幂等键；**不填** `verified_at` 或伪造观察。该 attempt 已记录并归为 `blocked`，但执行完成口径为否，TC-03 与整轮未完成。设备恢复且 C1/T2/B1/A1/ENV-1/F1 均未变时，以新 attempt 在 R2 验证，旧 blocked 保留；若设备/fixture/候选输入变更，建立新 run。相同 key 与 payload 返回原事件，不同 payload 报冲突；旧 token 的迟到反馈只属原 run，不能推进新候选。

甲随后在可用的 C1/ENV-1 目标设备看到反馈不可见，提交 `tested_by=甲`、`recorded_by=甲`、`verified_at/recorded_at`、实际观察和证据，TC-03 失败并关联 `BUG-7`。研发提供修复候选 C2 后，TC-03 在关联新 run 待人工复验；甲实际观察到提示后提交新通过，旧失败及 BUG-7 保留。若 AI 代录甲的具体反馈，记录 `tested_by=甲`、`recorded_by=AI`、双时间与原话来源；“应该好了”无法判断观察，仍待验。单机身份只是声明，不等于强认证。

## 增量、复用与基线缺失

从 C1 到 C2，假设共享权限契约改变、TC-02 失败被修复、TC-01 实现未变，但目标设备配置 `ENV-1→ENV-2`。增量账把 TC-02 列原缺陷复验与共享消费者回归，TC-01 列关联旧场景影响评估，TC-03 因设备配置变化待人工复验。若权限影响 TC-01 的范围未知，扩大到整个 `preferences` suite 或保留 `impact_unknown`，不能写“无影响”。TC-01 的旧通过仅在规则/CHK/候选差异/环境/fixture/Runner/证据逐项无影响且有记录时可复用；TC-03 旧设备证据因 ENV-2 失效。此 run 标 `incremental`，即使选中项通过也只得增量范围结论。

若基线 run 或库版本丢失，无法对比“未变化”：工具给 `baseline_missing`，建议建立全量 run；若全量暂不可执行，则增量影响保持未决并写明阻断，不生成空的增量通过。私有原始证据丢失时，摘要中的内容 hash 只能帮助核对文件身份，不能替代必要观察；逐 item 标 `private_missing/evidence_missing`，归档期限由试点项目决定。

## 与 Dev Flow 的纸面桥接

未来 `export dev-flow` 输出 R2 或 C2 新 run 的候选、catalog、环境与 manifest 指纹，L/P/D/R、范围 gap/差集及 TC→CHK→预期→必要证据摘要。主 Agent 与验收者核对原始记录后，在唯一 Progress schema 1 中把 TC-01、TC-02、TC-03 列为 `cases` 并建立相应 `required_checks`。同一 scope 的 `before_finish` **另必须含范围对账 check gate**，其输入绑定 manifest/正式摘要的实际版本；例如 RULE-X-03 无 TC 时此 gate 为 `blocked`，即使 TC-01/02 gate 已通过也不能完成。增量 gate 仅表明增量范围。范围摘要可作对账观察的 artifact 证据，UI/设备逐预期仍须原始可复核证据。当前 [核验器](../../../skills/dev-flow/scripts/check_iteration.py) 不会自动创建或读取这些未来记录；本页未执行它。
