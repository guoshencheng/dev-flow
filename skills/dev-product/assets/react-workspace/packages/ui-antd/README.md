# @dev-flow/ui-antd

B 端 React 组合组件，沿用 Ant Design 规范。基础控件直接从 `antd` 导入，此包只补充有明确用途的组合。版本 0.1.0，尚未发布到包仓库。

`SelectionSummary` 展示调用方提供的选择数量和范围；数量为零或忙碌时禁用动作。`selectedCount` 是非负整数，`scopeLabel` 必须与实际选择范围一致，跨页选择策略由项目维护。`onClear`、`onConfirm` 接收用户动作；本组件不执行 API、不确认提交结果，也不代替必要的二次确认。

```tsx
import { SelectionSummary } from '@dev-flow/ui-antd'

<SelectionSummary
  selectedCount={selectedKeys.length}
  scopeLabel="当前页"
  onClear={() => setSelectedKeys([])}
  onConfirm={openConfirmation}
  confirmLabel="发布所选项"
  busy={submitting}
/>
```

React、ReactDOM 与 antd 由调用方按 peerDependencies 提供，主题沿用调用方的 ConfigProvider；包构建将它们排除在产物外。当前组件由本仓库组合 antd Flex、Typography 与 Button，没有复制其内部实现。验证与项目采用记录保存在同仓库 React 工作区清单，采用时登记包版本和源码提交。
