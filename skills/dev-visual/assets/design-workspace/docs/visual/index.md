# 示例 UI 资产入口

当前资产由本工程独立维护。采用到业务项目后，将现行文档合并到项目的 `docs/dev-flow/visual/` 并修正 raw 导入，由项目 `docs/dev-flow/index.md` 关联；不要复制出两套可分别编辑的现行规范。

| 资产 | 权威来源 | 展示入口 |
| --- | --- | --- |
| 设计规范 | [system.md](system.md)、主题源码 `src/theme/tokens.ts` | `#/overview/system` / `#/system` |
| 页面规格 | [pages/orders.md](pages/orders.md) | `#/overview/pages` / `#/page/orders-desktop` / `#/page/orders-mobile` |
| 组件契约 | [components/order-summary.md](components/order-summary.md) | `#/overview/components` / `#/components` |
| 总览清单 | `src/preview/registry.ts` | 同一总览引用实际模块 |

本机地址来自 Vite 实际输出。所有内容是虚构的 B 端任务示例和设计候选，未获得真实业务确认；移动 Web 展示仅模拟屏幕宽高。

迭代记录采用项目既有索引或 [迭代增量示例](../iteration-change.example.md)，本轮只引用稳定资产与版本，不复制页面和规范。
