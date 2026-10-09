# 共享组件清单

源码与此清单一起由 Git 管理，默认复制或参考到项目、本地维护。当前组件为隔离示例起点，尚无真实项目采用记录。

B 端先参考 Ant Design 官方组件、示例和项目已有实现，现成控件直接导入 antd；本清单补充组合与参考源码。SelectionSummary、ActionCard 是本仓库的组合，Button/Card 来自官方 shadcn/ui 源码。按需联用方式见[Ant Design 能力指南](../../references/ant-design-capabilities.md)。

| 组件 | 契约与适用条件 | 来源与示例 |
| --- | --- | --- |
| `ui-antd/SelectionSummary` | `selectedCount` 与 `scopeLabel` 展示选择数量及范围；`onClear`、`onConfirm` 由调用方实现；数量为零或 `busy` 时不允许动作。数量须为非负整数，选择一致性由项目维护。适合所选项操作，不负责跨页选择策略、提交确认或异步结果恢复 | 直接组合 antd Flex、Typography、Button；`apps/antd-lab` 展示当前页选择、清空与模拟确认 |
| `ui-web/ActionCard` | `title`、`description`、`actionLabel`、`onAction` 形成单一行动；`pending` 或 `disabled` 阻止操作。调用方负责状态、结果与必要恢复。适合简单主行动，不负责复杂表单、支付或多个竞争行动 | 组合 shadcn/ui Card 与 Button；`apps/web-lab` 展示模拟处理、完成与重置 |
| `ui-web/Button`、`Card` 系列 | shadcn/ui 基础源码组件与公开属性；按对应上游用途采用，业务规则由调用方维护 | 来源与采用方式见 `packages/ui-web/THIRD_PARTY_NOTICES.md` |

## 预览与快速引用

运行 `npm run dev:gallery` 查看 B/C 两个入口中的四类组件；支持搜索、状态预览、本地导入的使用示例、完整源码文件集与候选 JSON。机器可读索引为 [catalog.json](catalog.json)，Agent 使用 `npm run --silent catalog -- <组件 ID>` 查询源码、依赖与 Git/文件哈希来源。操作和接入规则见[指南](../../references/component-preview-and-reuse.md)。项目已有明确选择时直接接入。

## 验证与采用

项目采用按源码复制或参考实现进行，构建、隔离示例与实际项目验证分别记录；目录中的示例不自动证明项目端到端行为。

实际项目采用后增加项目与来源提交或哈希、使用场景、差异与例外、对应证据；没有实际采用时保留“无项目验证”。版本或行为改变后，标记受影响证据待复验。
