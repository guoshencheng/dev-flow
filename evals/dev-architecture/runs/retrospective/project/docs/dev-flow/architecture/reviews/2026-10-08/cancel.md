# 预约取消交付前架构复盘

资产 ID：ARCH-REVIEW-CANCEL-20261008；状态：current（本版本评审事实）；执行/维护：通用子 Agent 读取 dev-architecture Skill 承担架构职责，非原生 dev_architecture 角色；日期：2026-10-08。
源提交：`734473c138fe669e33d627bfac6472dda6d81e59`；全部相关源码/测试/配置/产品/有效设计无未提交修改。逐文件 SHA-256 和执行时间见[清单](../../../../../evidence/runtime/cancel-architecture/source-manifest.json)。该提交后的架构文档变化由本次评审产生，不代表源实现变化。

## 结论、有效输入及范围

研发所述现有测试通过属实，本次重新执行2项均通过；演示 `npm start` 正常输出 cancelled 和一笔退款。交付仍被 P1 问题阻断：重复取消产生重复退款，且已确认的领域/存储隔离和跨域公开用例约束未落实。复盘任务已完成，但源码功能未修复、未验收完成。

复用[产品规则](../../../../product.md)、[已确认设计](../../changes/cancel/design.md)，保持单进程内存源码演示，不拆 HTTP 服务，不增加真实支付/持久化。读取 package.json、src/main.mjs、预约/结算全部5个业务模块文件、test/cancel.test.mjs 和已有架构索引。旧索引的服务描述与有效设计、实际代码冲突，已据后两者纠正。未改写产品规则/确认决定，未写 src、test、package.json。

## 规则、用例、适配与实际检查

| 原始依据 | 实际源码链路 | 实际检查及结论 |
| --- | --- | --- |
| RULE-01 / AC-02 | cancel.mjs:6–8，读取后校验 ownerId，未进入领域和退款写入 | 现有拒绝测试通过；补查预约/退款均不变通过 |
| RULE-02 / AC-01 | domain.mjs:5–7，>=24小时计算全额，否则0；保存状态；cancel.mjs:10 正数退款 | 首次提前取消现有测试通过；恰好24小时120退款、不足24小时 cancelled/0/无退款补查通过 |
| RULE-03 / AC-03 | domain.mjs:4 返回已取消对象（带正数refundAmount）；cancel.mjs:10 再次 writeRefund；billing/store.mjs:2 无条件 push | 补查同一预约同一actor同一now连续取消两次，实际2笔而非1笔，失败 |
| ARC-01 | domain.mjs:1 导入基础设施、:7 写预约；cancel.mjs:1 直接导入存储，无内层 Repository/函数端口 | 领域计算后实际 Map 状态由 active 变 cancelled，独立无IO检查失败；源码依赖偏差已确认 |
| ARC-02 | cancel.mjs:3、:10 直接写另一域存储；已有 billing/application/refund.mjs:3–8 公开用例未调用 | 已有 refund 独立调用两次只有1笔，通过；取消链路绕过该规则为直接证据 |
| ARC-03 | package.json:5 / main.mjs:1–8 单进程脚本与内存数据 | npm start 实际退出0；无外部服务；维持范围成立 |

本次检查文件[check.mjs](../../../../../evidence/runtime/cancel-architecture/check.mjs)只保存在授权 evidence 目录，不改正式测试。命令 `node evidence/runtime/cancel-architecture/check.mjs` 原始程序退出码1，7项中5通过、2失败，[输出](../../../../../evidence/runtime/cancel-architecture/check-output.txt)保留失败差异。现有测试和启动结果分别见[npm-test](../../../../../evidence/runtime/cancel-architecture/npm-test.txt)、[npm-start](../../../../../evidence/runtime/cancel-architecture/npm-start.txt)。Node v26.4.0；检查均使用项目实际内存适配，无外部模拟服务。

## 发现及具体改进

### ARCH-01：P1，开放，重复取消重复退款

影响：违反 RULE-03/AC-03，演示返回重复退款登记；不是实际支付重复扣付，因项目未接支付。根因是预约应用绕过结算公开退款用例，导致去重规则无效，违反 ARC-02。责任：研发修复、测试复验、架构核查边界。

最小修复：取消应用调用已有 `refund({reservationId, amount})` 公开用例，不再导入/调用 billing/infrastructure/store 的 writeRefund；退款去重保留由结算负责。不要只给预约应用加一个 status 短路来掩盖跨域存储写入。已有单线程同步内存用例可复用，不需事务框架或服务拆分。

验证：将重复取消、公开退款去重纳入正式回归；同一预约连续两次、不同 now 的重复取消都只有1笔；不同预约仍分别登记；首次提前取消、拒绝他人、24小时边界、不足24小时均回归。失败恢复/持久化事务不属于当前已确认范围，未来引入外部支付时另行设计。

### ARCH-02：P1，开放，已确认内层隔离未落实

影响：违反 ARC-01，领域独立计算会写全局存储，无法通过仅给领域对象就获得无 IO 规则行为的验收；应用也依赖具体预约存储，尚无内层保存契约。此问题基于明确必需约束定 P1，不是因 import 命名定严重度。

最小修复：cancelReservation 仅计算并返回结果，移除存储 import/save；取消应用声明其需要的 get/save 函数契约并接受注入，保存责任移至应用；main 组装实际内存适配与公开结算用例，保持 npm start。结算公开用例可同样以轻量函数注入 get-existing/write 适配，保持策略向内，避免新增框架与空目录。更改公开构造方式时 main 和正式测试一起迁移，数据形状、产品行为及单体决定不变。

验证：调用领域函数前后存储完全一致；不用任何存储初始化亦可验证24小时规则；应用使用独立内存测试适配验证授权在保存之前、正常保存一次；正式真实内存集成、重复请求及 npm start 回归；静态核对领域无 infrastructure import、应用无具体存储及跨域私有 import。

### ARCH-03：文档现状失真，已纠正

旧 index.md:5 把双服务/HTTP/Repository 说为已实现，与已确认单体决定及源码冲突。已更新当前入口和模块地图，明确未实现约束及失败，不修改确认设计。普通修订交给 Git 历史追踪，无需另造重复目标文档。

### ARCH-04：P3，开放，存储读引用封装改善

RES-STORE getReservation 直接返回内部对象；当前取消未原地修改，未发现此风险导致故障。可在未来维护时返回复制对象，减少绕过 save 的可能，代价为少量复制和契约调整；验证外部修改返回值后内部预约不变。不得因该建议阻断当前范围之外的事项。

## 合理性与演进取舍

现有单体分域、直接同步用例和内存适配足以支持演示；now 参数使边界验证可靠，授权先于写入成立，应复用。公开退款用例已有且可证明去重有效，恢复其调用收益高于新建抽象。轻量函数注入即可闭合已确认隔离，新增独立服务会增加启动、通信和失败处理成本，且与 ARC-03 冲突。当前没有证据要求微服务、事件总线、数据库迁移或性能重构。

## 资产变化与交接

复用：docs/product.md 和 changes/cancel/design.md 原样保留；现有用例与命令作为检查入口。更新：index.md 从草稿现状改为实际版本基线。新增：modules.md、此复盘、debt.md，以及 evidence/runtime/cancel-architecture/ 中可重跑检查、原始日志和指纹。

本轮静态阅读能证明依赖、规则和数据写入位置；本轮运行能证明记录的单进程场景。未验证网络认证、真实支付、持久化、并发多进程、故障恢复、性能、生产部署和UI；没有长期服务，未联网。后续仅需修复两个 P1 并复验当前规则与架构约束；本评审无源码写权限，已交接具体改动范围而未擅改。

能力边界：本次成功执行专业 Skill 的源码追踪、事实地图、产品/架构约束对照及实际检查沉淀；不能凭此声称原生角色配置已可加载，或这些方法已经跨项目通用验证。
