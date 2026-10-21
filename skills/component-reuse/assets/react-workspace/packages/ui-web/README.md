# C 端 Web 组件源码

基于 shadcn/ui，提供 Button、Card 系列以及组合 ActionCard。`@dev-flow/ui-web` 是内部预览工作区名称；项目复制或参考所需源码，直接导入本地组件并维护。

```tsx
import { ActionCard } from './components/dev-flow/web/action-card'

<ActionCard
  title="保存选择"
  description="保存后可以从记录中重新查看。"
  actionLabel="保存"
  onAction={saveSelection}
  pending={saving}
  disabled={saved}
/>
```

ActionCard 适合单一主要行动；pending 或 disabled 阻止动作，aria-busy 与等待文案表达处理状态。项目维护状态、结果、失败恢复与业务文案；复杂表单或多步交易另行设计。

在工作区用 `copy:component -- web-action-card --to /项目/src/components/dev-flow` 复制组件、支持文件、主题起点和上游许可，保留相对导入。项目已有 Button、Card、cn 或主题时优先复用现有基底，按需要复制组合并调整导入。

`src/styles.css` 是 Tailwind v4 源码示例，需要 Tailwind Vite 插件编译。已有 shadcn/Tailwind 主题时合并所需 Tokens 和源码扫描；独立起点可在入口导入本地 web/styles.css。React、Radix、CVA、clsx、tailwind-merge 等基础依赖按实际源码核对，验证过的组合见 catalog.json。第三方来源与许可见 THIRD_PARTY_NOTICES.md 和 LICENSE.shadcn。

来源提交或文件哈希、采用路径、项目修改与验证留在项目；通用改进核验后可回收共享源码。
