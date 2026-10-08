# 预约项目当前架构

资产 ID：ARCH-CURRENT；状态：current（描述实际实现，不表示已通过交付验收）。维护职责：架构。更新：2026-10-08。
源提交：`734473c138fe669e33d627bfac6472dda6d81e59`；本次检查相关源码、测试、产品及有效设计均无未提交变化，指纹见[来源证据](../../../evidence/runtime/cancel-architecture/source-manifest.json)。

## 当前结论和入口

当前是单进程 Node.js ESM 源码演示，预约与结算为进程内模块，使用 Map / 数组内存存储。不存在 HTTP 服务、远程调用或 Repository 端口。`npm start` 执行 `src/main.mjs`，装入一条演示预约，调用取消用例并输出 JSON 后退出；`npm test` 执行 Node 内置测试。无外部依赖、真实支付或持久化。重启会丢失数据。

原索引来自未核验设计草稿，错误地把独立服务、HTTP 和 Repository 写为已实现；本次用真实代码替代这一描述。已确认的[取消设计](changes/cancel/design.md)继续有效：单体范围不变，ARC-01/02 是尚未完全落实的约束；不将其降级为可选目标。

- [现行目录和模块地图](modules.md)：实际业务职责、层次、公开契约与依赖。
- [本轮代码复盘与检查](reviews/2026-10-08/cancel.md)：来源、覆盖、规则链路、实际检查和问题。
- [待处理偏差](debt.md)：交付阻断与后续建议。
- [产品权威规则](../../product.md)：RULE-01～03、AC-01～03；本次复用且未改写。

## 系统与数据流

源码依赖方向：`main → reservations/application/cancel → reservations/domain → reservations/infrastructure/store`；取消应用还直接依赖 `reservations/infrastructure/store` 与 `billing/infrastructure/store`。结算公开用例 `billing/application/refund` 依赖自己的存储，但未被取消链路调用。这些反向和跨域存储依赖属于实际偏差，不是推荐方向。

运行链路：main 初始化预约 → cancel 读取预约 → 校验存在性和本人身份 → cancelReservation 计算24小时退款并立即保存预约 → cancel 直接登记退款 → main 读取退款供演示输出。首次取消正确；重复取消返回已保存的正数 refundAmount 后再次登记退款。

数据归属：预约拥有 id/ownerId/status/price/startAt/refundAmount，结算拥有 reservationId/amount 退款登记。当前没有跨存储事务。入口是可信的本地源码调用，actorId 由调用者传入；身份认证及网络信任边界不在此演示中，也未被验证。

## 有效性与范围

本次读取全部现有 src 文件、package.json、测试、产品规则和有效取消设计；执行现有测试、实际启动及7项定向检查。现有2项测试通过，补查5项通过、2项失败。发现 RULE-03/AC-03 及 ARC-01/02 未满足，当前不得登记为交付完成。详细修复与复验要求见复盘。

只更新架构资产及本地检查证据，未修改源码、测试或有效设计。未验证真实支付、持久化、并发多进程、性能、网络权限、部署；这些均不属于本次交付范围。后续源码改变需重跑检查并更新来源指纹。
