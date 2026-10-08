# 预约摘要导出变化架构复核

资产 ID：ARCH-REVIEW-EXPORT-20261008；状态：current；维护/执行：架构，由同一通用子 Agent 持续读取专业 Skill 执行，非全新上下文或原生职责派发。更新：2026-10-08。

## 当前结论与来源

当前提交 `992d110be38c5c8e2ae834bc9561b23111682927` 新增摘要查询、公开边界、导出编排与 main 装配，保持单体/内存/npm start。新增导出链路已核验，只读和字段契约成立，未发现新增交付阻断。旧取消两个 P1 仍开放，整个演示不能因此登记交付完成。

复用[现状](../../index.md)、[模块地图](../../modules.md)、[债务](../../debt.md)、[取消复盘](cancel.md)、[产品规则](../../../../product.md)、[有效设计](../../changes/cancel/design.md)。新增有效输入为 [docs/export.md](../../../../export.md)，本轮不改其业务含义，也不变更 ARC-01～03。

旧证据属于 `734473c138fe669e33d627bfac6472dda6d81e59`，保留原文原日志。本轮 git diff 证明只增加 docs/export.md、query/public/export 三文件并修改 main；package、产品、有效设计、取消/领域/预约存储、结算两模块和正式测试的 SHA-256 与旧清单一致。见[当前来源与版本对照](../../../../../evidence/runtime/export-architecture/source-manifest.json)。相关源码/测试/规格无未提交变化，已有架构未提交资产被继续维护，未回退他人工作。

本轮实际阅读变化文件及入口、package、导出/产品规格、有效设计、上轮 index/modules/debt/review/manifest；旧业务文件沿用旧阅读，经指纹校验并重跑检查，不能声称本轮重新全文评审全部代码。

## 业务链路、分工与依赖

`main.mjs:10–13` 动态加载预约 public 和报表 export，将真实 getReservation 注入 reservationSummary，再传入 readSummary 闭包；main 把结果 JSON.stringify 输出。动态边已解析，不漏记为无依赖。

`reservations/public.mjs:1` 仅 re-export query。`application/query.mjs:1–5` 是预约应用只读投影：readReservation(id) → 不存在返回 null → 新建 id/status/price 对象；不导入具体存储，不写数据。预约拥有字段与数据语义。

`reporting/application/export.mjs:1–3` 消费同步 readSummary 函数，map 后过滤严格 null，保留输入次序；属于只读报表/导出应用能力，无数据所有权和 IO，不独立运行。是否发展为稳定独立业务域待后续真实规则决定。

源码依赖：main → public → query；main → reporting/export；main → reservations/store（装配）。query/export 均无 import。运行回调方向：export → readSummary → query → 注入 readReservation → store。两种方向明确区分，回调运行向外不构成源码反向依赖。

摘要契约为 `{id,status,price}`，缺失 null；export 返回数组，JSON 序列化在演示入口，函数名不意味着其自身执行文件/网络导出。同步函数端口是轻量内层契约，无需类接口或 DI 框架。当前公开边界仅覆盖 query，旧 cancel 仍由 main/test 直接导入应用，不能声称预约全部入口已统一。

## 实际检查与结果

Node v26.4.0；命令及退出码见当前 manifest。所有检查位于授权 evidence 目录，未改正式 test。

| 检查 | 结果与可证明范围 |
| --- | --- |
| `node evidence/runtime/export-architecture/check.mjs` | 5/5通过，退出0：字段精确/注入对象不变、缺失null、跳过null/保序、空输入无查询、真实取消后摘要可JSON序列化/预约退款不变/修改摘要不回写 |
| `npm test` | 现有2/2通过，退出0；不能替代新增导出或重复取消覆盖 |
| `npm start` | 退出0；第一行仍是取消结果，第二行为 summaries，仅 r-1/cancelled/120，missing被跳过；证明新增实际入口可运行 |
| 旧 `cancel-architecture/check.mjs` 在当前版执行 | 7项5通过2失败，退出1；仍重复退款2笔、领域计算写存储；输出存到本轮新目录，不覆盖旧日志 |

[导出检查脚本](../../../../../evidence/runtime/export-architecture/check.mjs)、[输出](../../../../../evidence/runtime/export-architecture/check-output.txt)、[测试](../../../../../evidence/runtime/export-architecture/npm-test.txt)、[启动](../../../../../evidence/runtime/export-architecture/npm-start.txt)、[旧问题本轮复查](../../../../../evidence/runtime/export-architecture/cancel-recheck-output.txt)。

## 合理性与必要建议

新增结构内聚清楚，查询投影属于预约，报表消费公开摘要，存储装配仅在 main；无外层类型泄漏、跨域私有存储访问或全局新状态。应保留并可作为旧取消问题的轻量注入参照，但不把一次项目验证提升为通用成熟能力，也不借此改写旧架构约束。

ARCH-05，P2，开放：正式回归未覆盖导出，虽然本轮补查全部通过，未来修改 query 字段或 main 装配时现有 npm test 无法发现偏差。建议研发把本轮5种有业务意义的场景收敛到正式测试，并明确同步 readSummary 返回摘要/null；无需复制 evidence 的执行包装。收益是保持只读/字段/缺失语义，代价是少量测试维护。验证 npm test 包含导出场景，并运行 npm start 确认两行结果，不改变取消规则或单体范围。此为维护建议，非本轮新增阻断。

未发现理由拆服务、建报表存储、事件总线或扩大认证设计。undefined、异步或抛错读取函数没有本轮业务约定和实际入口，不报为已发生缺陷；将来引入异步/网络需重新确定错误、授权和序列化契约。旧 ARCH-01/02 P1 保持原建议与关闭条件，ARCH-03 文档纠正有效，ARCH-04 引用封装建议仍P3开放。

## 更新、复用与未覆盖

更新 index/modules/debt 的现状、稳定模块 ID、依赖和版本/覆盖；新增此续轮复核与 export-architecture 证据。未改写旧取消报告、旧证据、有效产品与设计；未修改 src/test/package 或其他项目。

未覆盖真实支付、持久化、部署、网络认证、跨进程并发、性能和UI，范围与旧轮一致。新增外部异步适配及异常/重复id策略无产品要求，未宣称已验证；当前查询读取合法演示对象与同步内存适配成立。后续源码变化应更新指纹并按影响重跑，而不是将旧日志改为新版本。
