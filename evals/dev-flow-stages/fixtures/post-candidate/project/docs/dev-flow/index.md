# 订单备注功能文档入口

本目录均为评测用合成项目资产，记录的“确认”“授权”“Review”是夹具预设事实，不冒充真实用户行为。总体状态唯一权威为 [本轮 Progress](iterations/order-note/Progress.md)。

| 对象 | 当前有效文件 |
| --- | --- |
| 产品规则与可观察完成标准 | [产品规格 v1](product/spec.md) |
| 研发设计与实施前 Review | [研发设计 v1](iterations/order-note/engineering/design.md)、[设计 Review](iterations/order-note/engineering/design-review.md) |
| 计划、复核与实施授权 | [实施计划 v1](iterations/order-note/engineering/plan.md)、[前置决定](iterations/order-note/decisions.md) |
| 当前源码和研发自测 | `order_notes/`、`tests/test_engineering.py`、[自测记录](iterations/order-note/engineering/self-test.md) |
| 启动、产物与运行 | [运行说明](operations/runbook.md) |

正式验收文档及运行结果尚未形成。执行者可在本轮 `acceptance/` 下建立适当权威文件，并从本入口关联。研发自测记录不充当正式用例或交付证据。
