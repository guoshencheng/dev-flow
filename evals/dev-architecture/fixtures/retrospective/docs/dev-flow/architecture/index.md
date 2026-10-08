# 预约项目架构

状态：current。来源：初始设计草稿，尚未记录代码核验版本。

系统已拆成预约服务和独立结算服务，通过 HTTP 调用。预约的 domain 只做纯规则计算，application 通过 ReservationRepository 端口保存；结算使用 refund 公开入口。规划中的 HTTP 服务与 Repository 实现在下轮补齐。

模块：预约/结算。现行模块地图和验证覆盖待维护。
