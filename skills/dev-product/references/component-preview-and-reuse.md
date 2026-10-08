# 组件预览、源码选择与快速接入

适用于直观设计讨论或寻找可复用组合。先读任务和项目现有组件；已明确的选择直接实施，目录按讨论需要启动。

## 找到候选

随包 [React 工作区](../assets/react-workspace/README.md)提供预览、源码文件集和使用示例。`catalog.json` 记录用途、边界、必要文件和基础依赖；完整契约见源码与说明。B 端基础控件直接使用 antd，C 端 Web 优先使用项目已有 shadcn/ui 基底。

B 端先参考官方完整组件与示例，按需联合[官方 Skill、CLI 或 MCP](../../dev-flow/references/ant-design-capabilities.md)。现成组件可满足时直接使用；本目录提供额外组合，组件选择不限于随包四类。当前 SelectionSummary/ActionCard 为自有组合，Button/Card 为保留许可的官方 shadcn/ui 源码。

```sh
cd "$HOME/.agents/skills/dev-product/assets/react-workspace"
npm ci
npm run dev:gallery
npm run --silent catalog -- antd-selection-summary
```

打开 Vite 实际输出地址，`/index.html`、`/web.html` 分别预览 B/C；按问题展示组件和相关状态。目录可查看、复制真实源码和本地导入的使用示例，也可复制整个源码文件集 JSON 给 Agent。命令查询返回源码、依赖、来源提交与文件哈希，不必每次启动预览。

讨论材料可以加入候选并复制或下载 JSON，跨两个入口保存在当前浏览器会话。`status: candidate` 表示待讨论，`previewScenario` 表示演示状态；选中组件不代表全部设计或功能已经确认。用户文字选择同样有效。目录预览是模拟，不代替任务页面检查。

## 复制或参考源码

共享组件默认进入项目源码，项目直接修改和交付。两种方式按现有工程选择：完整复制组件及必要支持文件；或者参考其组合和状态契约，在项目现有组件体系中实现。已存在的 Button、Card、cn 和主题优先复用，避免引入第二套相同基底。

```sh
npm run --silent copy:component -- antd-selection-summary --to /目标项目/src/components/dev-flow
npm run --silent copy:component -- web-action-card --to /目标项目/src/components/dev-flow
```

复制工具处理源码、目录内相对导入、所需支持文件、样式起点和许可，并在目标目录 `.component-sources/` 生成来源记录。只接受相同内容的既有文件；有差异时保留项目实现，Agent 比较后按需要合并。工具不替项目改依赖、入口或主题。

接入时读取项目依赖及主题，核对索引中验证过的基础依赖；只补缺失依赖并检查实际兼容性。使用示例以 `src/Example.tsx` 和 `src/components/dev-flow/` 为基准，其他位置修改相对导入；替换模拟数据、定时结果、scenario 参数和业务回调。

B 端沿用项目 React、antd、ConfigProvider。C 端采用项目 shadcn/Tailwind 主题；随包 styles.css 是 Tailwind v4 源码起点，需要对应 Vite 插件，已有主题时合并所需 Tokens、源码扫描和状态样式，保留项目现有主题。B/C 全局样式保持各自应用边界。

## 项目迭代与持续沉淀

复制后的源码归项目维护，局部迭代直接在项目修改。采用记录保存组件 ID、来源文件、Git 提交或实际源码哈希、项目路径、业务用途、改动与实际检查证据；不要求先形成发布版本。未提交来源记录基准提交、修改状态与文件哈希，保持准确追溯。

共享源码更新后，比较原采用快照、当前参考源码和项目修改，按任务需要合并，保护项目定制；升级不是自动覆盖。项目验证过的通用改进作为候选回收到共享仓库，更新契约、必要文件集、示例与证据，再供其他项目参考。

在实际任务页面运行并验证相关交互、键盘、状态、反馈、主题和尺寸。按[项目资产协议](project-assets.md)将有效决定、采用记录和证据关联；当前仅有隔离案例时保持该成熟度。新增共享组件补齐 catalog.json、源码文件映射和可编译预览，保持源码文件集完整、使用示例为本地导入。
