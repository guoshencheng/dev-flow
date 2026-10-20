# 可复用 React 设计稿模板

Vite + React + TypeScript 独立工程。页面、组件、设计规范、主题、场景和尺寸容器分别维护，通过一个总览整合展示。模板内使用虚构的 B 端订单任务，桌面与移动 Web 均使用 antd；示例为候选，采用时替换项目内容与规则。C 端 Web 沿用项目 shadcn/ui 基底，保留总览/容器/注册表结构，替换对应业务视图，不把 B/C 固定绑定到桌面/移动。

## 复制到项目并启动

使用满足 package.json engines 的 Node.js。推荐从实际安装的视觉 Skill 目录执行：

```sh
DEV_VISUAL_SKILL_DIR="/实际安装目录/skills/dev-visual"
node "$DEV_VISUAL_SKILL_DIR/scripts/design-template.mjs" init \
  --project /项目绝对路径 --dir docs/dev-flow/visual/prototype
cd /项目绝对路径/docs/dev-flow/visual/prototype
npm ci
npm run dev
```

初始化只复制源码、规范与锁文件，生成 `.template-source.json` 来源哈希；不安装依赖、不改写项目指引、包清单或文档入口。目标已有内容时拒绝覆盖，直接继续维护该工程。也可手动完整复制本目录到一个空目标，排除 `node_modules`、`dist` 与 `.dev`。副本运行不依赖 Skill 目录、自有 npm 包或全局链接。

打开 Vite 实际输出地址。总览为 `#/overview/pages`，菜单进入组件与规范区；本机服务默认只监听 127.0.0.1，Ctrl+C 停止。`npm run dev -- --port 0` 可请求空闲端口，以实际输出为准。

## 目录与权威位置

| 内容 | 位置 | 维护方式 |
| --- | --- | --- |
| 桌面 / 移动页面 | `src/features/orders/views/` | 各端独立组合，引用公共领域组件 |
| 领域组件 / 模拟场景 | `src/features/orders/components/`、`scenarios.ts` | 组件纯输入或显式回调，实例状态由视图持有 |
| 实际主题 | `src/theme/tokens.ts` | antd、CSS 变量与规范展示共同读取 |
| 独立规范 / 页面 / 组件契约 | `docs/visual/` | Markdown 为权威文本，规范和组件展示直接读取原文 |
| 总览与注册表 | `src/preview/DesignOverview.tsx`、`registry.ts` | 引用实际页面/展示模块，不复制它们的实现 |
| 屏幕尺寸外壳 | `src/preview/DeviceViewport.tsx` | 宽高、显示缩放和 iframe；不模拟设备操作 |
| 迭代增量格式 | `docs/iteration-change.example.md` | 小变化写项目迭代索引，复杂时才拆变更记录 |

资产入口见 [docs/visual/index.md](docs/visual/index.md)。模板文档供初始化参考；采用后将现行规范合并到项目的 `docs/dev-flow/visual/`，调整 `?raw` 导入和链接，保留一个现行权威位置。不要为了每次迭代再次复制模板、规范或页面源码。

## 各端入口与尺寸边界

路由采用 hash，开发服务与静态构建均无需业务路由回退规则：

- `#/overview/pages`：桌面/移动/多端对照、状态和屏幕尺寸控制。
- `#/page/orders-desktop?scenario=normal`、`#/page/orders-mobile?scenario=error`：独立页面，支持 normal/loading/empty/error。
- `#/overview/components`、`#/components`：组件组合、状态与真实契约文本。
- `#/overview/system`、`#/system`：真实主题展示与独立规范原文。

总览 iframe 和独立入口从同一注册表取组件。每个 iframe 有独立页面 state 与样式上下文，弹层挂在其内部 body；移动内部视口实际采用控制区的 CSS 像素宽高。默认适应展示区域且不放大，标明缩放比例；“查看 1:1”显示原尺寸，外部滚动不会改变内部布局。长内容在 iframe 内滚动，底部分类固定在内部视口；不模拟触摸、软键盘、UA、设备 API 或真实系统。

## 新增页面与后续迭代

1. 先从项目 UI 索引查找有效页面/组件/规范及确认基线；已有资产原位更新，缺少时才新增。
2. 新领域在 `features/<领域>/` 维护组件/场景与各端 views，保留共享组件的明确边界。
3. 在 `pageRegistry` 增加稳定 ID、视图组件、平台名称、`kind`（desktop/mobile）、默认尺寸、源码/规格位置；独立路由与总览清单自动消费该注册表。更多端类别按业务需要扩展筛选项与容器类型，不复制页面到总览。
4. 独立规范继续引用真实主题；复杂规范可拆多个文档并在规范展示模块引用。Markdown 中的相对文件链接通过 `MarkdownDocument` 的 `links` 映射到展示入口；文档源文件仍保留正常相对链接。需要新的展示区时修改 `sectionRegistry`。
5. 迭代索引仅记录受影响资产、基线/候选/确认版本、增量和实际检查。主题/共享组件变化后复查消费者、各端独立页与总览；历史确认保留当时版本。

## 检查和产物

```sh
npm run typecheck
npm run build
npm run preview
```

构建产物为 `dist/`，可按已授权的目标部署静态资源；`preview` 仅作本机产物检查。提交源码与锁文件，忽略依赖和产物。搜索、分类、详情和错误恢复都只是本地示例行为，生产采用需落实真实规则/数据/API，再检查实际集成视觉和业务任务。

第三方依赖按锁文件安装并保留各包许可；本模板没有复制上游组件源码或外部图片/字体。基础控件直接导入 antd，自有组合归项目副本维护。
