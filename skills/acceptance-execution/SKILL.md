---
name: acceptance-execution
description: 对可运行候选执行界面、API、数据、E2E 与交付用例，保存证据、反馈问题并进行定向复验。
---

# 验收执行与复验

接收有效用例、固定候选、实际环境、身份/数据及交付入口，核验版本和执行依赖。优先复用项目已有 runner，明确 Mock 与真实链路边界。

按被测对象选择下列方法，记录每项真实结果与证据。发现问题立即反馈；作者推进新候选时保留被测版本或暂停受影响检查。修复后复验原问题、相邻契约和相关回归。

交接逐必需用例结果、候选/环境、命令/证据、缺陷/复验与未执行项，由测试职责判断范围内结论。端口/健康正常、Mock 或局部通过不能替代约定真实 E2E。

## 按需读取

- [界面及交互](references/frontend-and-ui.md)。
- [真实接口和数据](references/backend-and-api.md)。
- [完整链路和交付](references/end-to-end-and-delivery.md)。
- [运行、证据、缺陷和复验](references/execution-and-feedback.md)。
- [结果模板](assets/templates/acceptance-report.md)。
- [技术检查模板](assets/templates/technical-checks.md)。
- [缺陷与复验模板](assets/templates/defect.md)。
