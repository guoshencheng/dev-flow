# @dev-flow/ui-web

C 端 Web React 组件，基于 shadcn/ui 源码。版本 0.1.0，尚未发布到包仓库。入口导出 Button、Card 系列及组合 ActionCard。

```tsx
import '@dev-flow/ui-web/styles.css'
import { ActionCard } from '@dev-flow/ui-web'

<ActionCard
  title="保存选择"
  description="保存后可以从记录中重新查看。"
  actionLabel="保存"
  onAction={saveSelection}
  pending={saving}
  disabled={saved}
/>
```

ActionCard 的 `pending` 或 `disabled` 阻止动作；等待提示与 `aria-busy` 表达处理状态。调用方维护状态、结果、失败恢复与业务文案。卡片适合单一主要行动，不负责复杂表单或多步交易。

`styles.css` 为预编译的组件样式、默认主题和 Tailwind 基础样式，调用方无需为此包安装 Tailwind；项目已有全局样式或设计主题时检查其影响，按需要采用源码组件并在项目主题中构建。React/ReactDOM 是 peerDependencies。上游来源与许可证见 THIRD_PARTY_NOTICES.md 和 LICENSE.shadcn。验证与项目采用记录保存在同仓库工作区清单。
