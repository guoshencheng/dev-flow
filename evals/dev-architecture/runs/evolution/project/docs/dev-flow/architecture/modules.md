# 现行模块与目录地图

资产 ID：ARCH-MODULES；状态：current；维护：架构；更新：2026-10-08。源提交和工作区指纹沿用[index](index.md)及[本轮来源清单](../../../evidence/runtime/export-architecture/source-manifest.json)。本轮全文核验 BOOT/RES-QUERY/RES-PUBLIC/REPORT-EXPORT；其他源码模块沿用 `734473c` 阅读，指纹确认未变；正式测试重跑。

| 模块 ID / 路径 | 业务域与实际层次 | 职责、数据与公开入口 | 不负责事项 / 验证 |
| --- | --- | --- | --- |
| BOOT / `src/main.mjs` | 技术支撑；装配、演示入口 | 初始化预约，调用 cancel 打印退款，动态装配摘要查询及导出函数并输出摘要 JSON；不拥有业务数据 | 不应承担取消规则；`npm start` 已执行 |
| RES-RULE / `src/modules/reservations/domain.mjs` | 预约；领域计算混入持久化 | `cancelReservation(reservation, now)`：已取消短路、24小时计算、构造 cancelled 并直接保存 | 应仅拥有状态转换/计算，当前写存储违反 ARC-01；定向纯规则检查失败 |
| RES-CANCEL / `src/modules/reservations/application/cancel.mjs` | 预约；应用用例混入跨域基础设施依赖 | `cancel({reservationId,actorId,now})`：存在性、本人授权、调用规则、直接 writeRefund | 不应直接拥有结算数据写入/去重；现有测试通过，重复取消失败 |
| RES-QUERY / `src/modules/reservations/application/query.mjs` | 预约；应用只读查询/投影 | reservationSummary(id, readReservation)：查询后仅投影 id/status/price，缺失返回 null；消费者所需函数端口 | 不负责存储实现、退款或序列化；注入与真实适配检查通过 |
| RES-PUBLIC / `src/modules/reservations/public.mjs` | 预约；模块公开边界 | re-export reservationSummary，无外层类型泄漏；预约拥有摘要契约 | 不声称所有入口统一（旧 cancel 仍直接应用导入）；公开入口检查通过 |
| REPORT-EXPORT / `src/modules/reporting/application/export.mjs` | 报表/导出能力；应用编排 | exportSummaries(ids, readSummary)：函数端口、顺序遍历过滤 null，返回数组，无持久数据所有权 | 不读预约私有存储、不计算字段、不序列化；5项定向检查通过 |
| RES-STORE / `src/modules/reservations/infrastructure/store.mjs` | 预约；内存持久化适配 | Map 数据拥有者；resetReservations/getReservation/saveReservation | 不拥有授权、退款规则；集成检查使用真实适配 |
| BILL-REFUND / `src/modules/billing/application/refund.mjs` | 结算；公开应用用例 | `refund({reservationId,amount})`：正数校验、按预约查重、调用存储 | 未被取消调用；独立调用重复退款检查通过；当前直接依赖本域存储 |
| BILL-STORE / `src/modules/billing/infrastructure/store.mjs` | 结算；内存持久化适配 | 数组数据拥有者；writeRefund/refundRows/resetRefunds | writeRefund 无去重策略，不能代替公开退款用例 |
| CHECK / `test/cancel.test.mjs` | 技术支撑；验证 | 真实内存适配集成，首次取消与非本人拒绝 | 缺失重复取消、边界、领域隔离及导出；补查在 evidence，尚未进入正式回归 |
| CONFIG / `package.json` | 技术支撑；运行配置 | ESM、test/start 命令，无依赖声明 | 无网络服务器或发布配置 |
| SPEC / `docs/product.md`、`docs/export.md`、`docs/dev-flow/architecture/` | 产品与架构资产 | 产品 owns RULE/AC；架构维护现状、已确认约束及偏差 | 文档不是运行模块；旧索引的已实现叙述已纠正 |

## 边界与合理性

业务域为预约（取消资格、时间/金额规则、预约状态）与结算（退款登记和去重）。新增报表/导出是只读消费预约摘要的能力，规则少、无独立数据，稳定业务域边界仍属候选，不因新增目录断言限界上下文。这是单体内能力边界，不宣称独立限界上下文或独立运行服务。存储技术支撑仍按所服务的业务数据归属映射。维护者角色明确为研发/架构协同，无虚构个人负责人。

预约与结算分目录、公开退款函数、轻量纯对象输入均适合小型演示；无需增加服务、消息总线或四层空目录。时间通过 now 参数传入，有利于精确边界检查；预约状态使用复制对象，拒绝授权在修改前进行，这些当前合理做法应保留。

主要问题是实际业务调用绕过结算用例，且领域函数反向依赖 IO；目录名称不能证明已经隔离。希望的依赖为应用 → 领域/内层端口，存储 → 内层契约，由 main 装配真实内存实现；预约通过结算公开用例协作。该方向是有效约束/修复目标，尚未实现。结算应用依赖本域具体存储亦应在小型修复中用函数注入围住，避免以新反向耦合替换旧问题。

存储 getReservation 返回内部对象引用是可读到的封装弱点；当前取消路径没有原地修改它，未发现已发生故障。后续可用复制返回保持单一写入口，按 P3 管理并验证外部修改不影响存储。

## 导出结构评价与契约

query 使用注入读取函数并返回新对象，export 无基础设施引用，装配集中 main；业务数据和投影属于预约，报表消费公开摘要，符合轻量整洁架构。保持现有3个新文件即可，不需要报表领域/存储空目录。

当前摘要 `{id,status,price}`、缺失 null 是实际契约；readSummary 同步返回摘要或 null，export 严格过滤 null；main 的公开查询满足它。异步、undefined、异常字段行为尚无约定，不能当作本轮缺陷。建议用源码注释和正式回归固化当前同步契约，保持轻量。
