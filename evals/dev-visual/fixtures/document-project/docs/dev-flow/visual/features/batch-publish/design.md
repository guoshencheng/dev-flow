---
id: VISUAL-batch-publish
title: 批量发布视觉规格
status: candidate
version: 1
owner: visual
related: [PRODUCT-batch-publish, PT-batch-publish]
---

# 批量发布视觉规格

输入：[产品规则 v2](../../../product/features/batch-publish/spec.md)。方向：Ant Design 的数据操作呈现；当前只是隔离示例，未取得品牌或真实用户偏好。

## 布局与代码

角色与配额条件、选择数量、范围和主操作依次呈现。使用 Ant Design Select、InputNumber、Button、Alert、Space；不用自建基础控件。

| 层级 | 实际来源 | 规则 |
| --- | --- | --- |
| 主操作 | 原型的 antd Button | 一处 primary，处理中 loading |
| 范围摘要 | 原型 React 文本 | “当前页”始终出现，数量与提交反馈对应 |
| 条件解释 | 原型 antd Alert | 超限/配额/查看者用文字解释，不单靠颜色 |
| 间距与主题 | 阅读器 ConfigProvider / 原型 Space | 当前页复用 antd 默认尺寸，相关长文案允许换行 |

## 状态与窗口

桌面检查阅读与操作层级；390px 检查条件控件、说明和操作换行，不遮挡数量。查看者隐藏操作遵循 RULE-batch-002；配额耗尽与超限禁用说明分别遵循 RULE-batch-001/003。动态提交反馈遵循 RULE-batch-004。

[同一 React 原型](../../../../../design/prototypes/batch-publish/demo.mdx)。静态规格不是实际视觉通过证据，检查结果和未覆盖项记录在本轮报告。
