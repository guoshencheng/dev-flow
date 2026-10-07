# 共享组件清单

版本 0.1.0。源码与此清单一起由 Git 管理。当前组件为隔离示例起点，尚无真实项目采用记录。

| 组件 | 契约与适用条件 | 来源与示例 |
| --- | --- | --- |
| `ui-antd/SelectionSummary` | `selectedCount` 与 `scopeLabel` 展示选择数量及范围；`onClear`、`onConfirm` 由调用方实现；数量为零或 `busy` 时不允许动作。数量须为非负整数，选择一致性由项目维护。适合所选项操作，不负责跨页选择策略、提交确认或异步结果恢复 | 直接组合 antd Flex、Typography、Button；`apps/antd-lab` 展示当前页选择、清空与模拟确认 |
| `ui-web/ActionCard` | `title`、`description`、`actionLabel`、`onAction` 形成单一行动；`pending` 或 `disabled` 阻止操作。调用方负责状态、结果与必要恢复。适合简单主行动，不负责复杂表单、支付或多个竞争行动 | 组合 shadcn/ui Card 与 Button；`apps/web-lab` 展示模拟处理、完成与重置 |
| `ui-web/Button`、`Card` 系列 | shadcn/ui 基础源码组件与公开属性；按对应上游用途采用，业务规则由调用方维护 | 来源与采用方式见 `packages/ui-web/THIRD_PARTY_NOTICES.md` |

## 验证与采用

截至 2026-10-08 已完成：所有工作区类型检查与构建；两个示例的浏览器渲染与实际操作；打包后的组件在独立 React/Vite 工程中安装、公开类型约束与 B/C 双入口构建核验。证据、复现方式与范围见[验证记录](../../../../evals/dev-product/runs/2026-10-07/react-kit/report.md)。依赖内部声明使用 Vite 模板的 skipLibCheck 设置，不登记为全量依赖类型检查通过。

实际项目采用后增加项目与版本、使用场景、差异与例外、对应证据；没有实际采用时保留“无项目验证”。版本或行为改变后，标记受影响证据待复验。
