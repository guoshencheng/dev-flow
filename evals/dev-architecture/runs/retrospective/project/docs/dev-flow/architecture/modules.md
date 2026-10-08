# 现行模块与目录地图

资产 ID：ARCH-MODULES；状态：current；维护：架构；更新：2026-10-08。源提交和工作区指纹沿用[index](index.md)及[来源清单](../../../evidence/runtime/cancel-architecture/source-manifest.json)。本次覆盖全部现有源码模块。

| 模块 ID / 路径 | 业务域与实际层次 | 职责、数据与公开入口 | 不负责事项 / 验证 |
| --- | --- | --- | --- |
| BOOT / `src/main.mjs` | 技术支撑；装配、演示入口 | 初始化预约，调用 cancel，打印退款；不拥有业务数据 | 不应承担取消规则；`npm start` 已执行 |
| RES-RULE / `src/modules/reservations/domain.mjs` | 预约；领域计算混入持久化 | `cancelReservation(reservation, now)`：已取消短路、24小时计算、构造 cancelled 并直接保存 | 应仅拥有状态转换/计算，当前写存储违反 ARC-01；定向纯规则检查失败 |
| RES-CANCEL / `src/modules/reservations/application/cancel.mjs` | 预约；应用用例混入跨域基础设施依赖 | `cancel({reservationId,actorId,now})`：存在性、本人授权、调用规则、直接 writeRefund | 不应直接拥有结算数据写入/去重；现有测试通过，重复取消失败 |
| RES-STORE / `src/modules/reservations/infrastructure/store.mjs` | 预约；内存持久化适配 | Map 数据拥有者；resetReservations/getReservation/saveReservation | 不拥有授权、退款规则；集成检查使用真实适配 |
| BILL-REFUND / `src/modules/billing/application/refund.mjs` | 结算；公开应用用例 | `refund({reservationId,amount})`：正数校验、按预约查重、调用存储 | 未被取消调用；独立调用重复退款检查通过；当前直接依赖本域存储 |
| BILL-STORE / `src/modules/billing/infrastructure/store.mjs` | 结算；内存持久化适配 | 数组数据拥有者；writeRefund/refundRows/resetRefunds | writeRefund 无去重策略，不能代替公开退款用例 |
| CHECK / `test/cancel.test.mjs` | 技术支撑；验证 | 真实内存适配集成，首次取消与非本人拒绝 | 缺失重复取消、24小时边界和领域隔离；本轮补查留在 evidence |
| CONFIG / `package.json` | 技术支撑；运行配置 | ESM、test/start 命令，无依赖声明 | 无网络服务器或发布配置 |
| SPEC / `docs/product.md`、`docs/dev-flow/architecture/` | 产品与架构资产 | 产品 owns RULE/AC；架构维护现状、已确认约束及偏差 | 文档不是运行模块；旧索引的已实现叙述已纠正 |

## 边界与合理性

业务域为预约（取消资格、时间/金额规则、预约状态）与结算（退款登记和去重）。这是单体内能力边界，不宣称独立限界上下文或独立运行服务。存储技术支撑仍按所服务的业务数据归属映射。维护者角色明确为研发/架构协同，无虚构个人负责人。

预约与结算分目录、公开退款函数、轻量纯对象输入均适合小型演示；无需增加服务、消息总线或四层空目录。时间通过 now 参数传入，有利于精确边界检查；预约状态使用复制对象，拒绝授权在修改前进行，这些当前合理做法应保留。

主要问题是实际业务调用绕过结算用例，且领域函数反向依赖 IO；目录名称不能证明已经隔离。希望的依赖为应用 → 领域/内层端口，存储 → 内层契约，由 main 装配真实内存实现；预约通过结算公开用例协作。该方向是有效约束/修复目标，尚未实现。结算应用依赖本域具体存储亦应在小型修复中用函数注入围住，避免以新反向耦合替换旧问题。

存储 getReservation 返回内部对象引用是可读到的封装弱点；当前取消路径没有原地修改它，未发现已发生故障。后续可用复制返回保持单一写入口，按 P3 管理并验证外部修改不影响存储。
