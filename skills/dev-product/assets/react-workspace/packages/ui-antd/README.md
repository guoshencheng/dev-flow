# B 端组合源码

基于 Ant Design 的 React 组合，基础控件直接使用 antd。`@dev-flow/ui-antd` 是内部预览工作区名称；项目复制或参考源码，从本地文件导入并直接维护。

`SelectionSummary` 展示调用方提供的选择数量与范围。数量为零或 busy 时禁用动作；数量须为非负整数，选择范围保持一致。`onClear`、`onConfirm` 由项目实现，跨页选择、权限、提交确认和异步结果恢复由项目定义。

```tsx
import { SelectionSummary } from './components/dev-flow/business/selection-summary'

<SelectionSummary
  selectedCount={selectedKeys.length}
  scopeLabel="当前页"
  onClear={() => setSelectedKeys([])}
  onConfirm={openConfirmation}
  confirmLabel="发布所选项"
  busy={submitting}
/>
```

在 React 工作区使用 `copy:component -- antd-selection-summary --to /项目/src/components/dev-flow` 复制源码；沿用项目 React、antd 与 ConfigProvider，核验版本与行为。源码直接组合 antd Flex、Typography、Button，采用来源、文件哈希、项目差异和验证记录由项目维护。
