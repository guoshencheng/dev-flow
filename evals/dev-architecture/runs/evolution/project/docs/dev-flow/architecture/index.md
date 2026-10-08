# 预约项目当前架构

资产 ID：ARCH-CURRENT；状态：current（描述实际实现，不表示已通过交付验收）。维护职责：架构。更新：2026-10-08。
当前源提交：`992d110be38c5c8e2ae834bc9561b23111682927`；本轮相关源码/测试/规格无未提交变化，指纹和旧版关系见[本轮来源证据](../../../evidence/runtime/export-architecture/source-manifest.json)。上一轮取消证据属于 `734473c`，原样保留。

## 当前结论和入口

当前是单进程 Node.js ESM 源码演示，预约、结算与报表导出为进程内模块，使用 Map / 数组内存存储。不存在 HTTP 服务、远程调用或 Repository 端口。`npm start` 执行 `src/main.mjs`，装入一条演示预约，调用取消用例输出 JSON，再导出预约摘要 JSON 后退出；`npm test` 执行 Node 内置测试。无外部依赖、真实支付或持久化。重启会丢失数据。

原索引来自未核验设计草稿，错误地把独立服务、HTTP 和 Repository 写为已实现；本次用真实代码替代这一描述。已确认的[取消设计](changes/cancel/design.md)继续有效：单体范围不变，ARC-01/02 是尚未完全落实的约束；不将其降级为可选目标。

- [现行目录和模块地图](modules.md)：实际业务职责、层次、公开契约与依赖。
- [最新导出变化复核](reviews/2026-10-08/export.md)：当前检查及旧证据关系。
- [上一轮取消复盘](reviews/2026-10-08/cancel.md)：保留 `734473c` 的检查事实。
- [导出规格](../../export.md)：摘要字段、跳过缺失、只读和单体范围。
- [待处理偏差](debt.md)：交付阻断与后续建议。
- [产品权威规则](../../product.md)：RULE-01～03、AC-01～03；本次复用且未改写。

## 系统与数据流

源码依赖方向：`main → reservations/application/cancel → reservations/domain → reservations/infrastructure/store`；取消应用还直接依赖 `reservations/infrastructure/store` 与 `billing/infrastructure/store`。结算公开用例 `billing/application/refund` 依赖自己的存储，但未被取消链路调用。这些反向和跨域存储依赖属于实际偏差，不是推荐方向。

运行链路：main 初始化预约 → cancel 读取预约 → 校验存在性和本人身份 → cancelReservation 计算24小时退款并立即保存预约 → cancel 直接登记退款 → main 读取退款供演示输出。首次取消正确；重复取消返回已保存的正数 refundAmount 后再次登记退款。

数据归属：预约拥有 id/ownerId/status/price/startAt/refundAmount，结算拥有 reservationId/amount 退款登记。当前没有跨存储事务。入口是可信的本地源码调用，actorId 由调用者传入；身份认证及网络信任边界不在此演示中，也未被验证。

新增源码依赖：main 动态 import 预约 public 与报表 export，public → application/query；query 与 export 均无存储/框架 import。运行方向：main 将 getReservation 注入 reservationSummary，再将摘要读取闭包注入 exportSummaries；报表返回数组，main 承担 JSON.stringify 输出。报表不拥有预约/退款数据，摘要不是独立服务或持久化副本。

## 有效性与范围

本轮重读变化的 main、预约 query/public、报表 export，以及导出规格、既有架构资产和有效决定；未变化的取消/领域/存储/结算模块与正式测试沿用上轮阅读，经 SHA-256 确认一致，不宣称重新全文检查。新增模块全部覆盖；旧模块来源明确保留。

当前版本重新执行正式测试2/2、启动成功，导出检查5/5通过；旧检查脚本在当前版重跑，取消7项仍5通过、2失败，新输出保存于 export-architecture。RULE-03/AC-03、ARC-01/02 保持开放；导出通过不能替代取消验收。
只更新架构资产及本地检查证据，未修改源码、测试或有效设计。未验证真实支付、持久化、并发多进程、性能、网络权限、部署；这些均不属于本次交付范围。后续源码改变需重跑检查并更新来源指纹。
