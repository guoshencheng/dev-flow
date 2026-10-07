# React 原型与共享组件工作区

版本 0.1.0。此目录与 `dev-product` Skill 一起在 Git 中维护，可经全局 Skill 链接发现。Vite + React + TypeScript 提供开发与构建；两个示例用于核验组件行为，任务原型仍按实际需求生成。

## 目录与边界

| 目录 | 用途 |
| --- | --- |
| `packages/ui-antd` | B 端基于 antd 的组合与扩展；基础控件仍直接使用 antd |
| `packages/ui-web` | C 端 Web 的 shadcn/ui 源码组件、主题与组合 |
| `apps/antd-lab` | Table 与 SelectionSummary 的选择范围、清空和确认示例 |
| `apps/web-lab` | ActionCard 的行动、处理中、完成与重置示例 |

项目特有业务留在项目中，组件不内置 API、权限或部署环境。两套样式分别使用，`ui-web` 的 Tailwind 基础样式应在对应 C 端 Web 应用中加载，避免全局进入 antd 应用。完整契约和验证状态见[组件清单](catalog.md)。

## 开发与检查

使用满足 `package.json` engines 的 Node.js。首次在本目录执行 `npm ci`，复现采用锁文件中的依赖。经全局入口可执行：

```sh
cd "$HOME/.agents/skills/dev-product/assets/react-workspace"
npm ci
npm run dev:antd
```

需要明确指定端口时直接调用工作区：

```sh
npm run dev --workspace @dev-flow/antd-lab -- --port 5173
npm run dev --workspace @dev-flow/web-lab -- --port 5174
```

两条开发命令分别保持运行，打开实际输出地址；修改源码热更新，Ctrl+C 停止。可以用 `npm run dev:antd` 或 `npm run dev:web` 使用默认端口，端口占用时以 Vite 实际输出为准。

```sh
npm run typecheck
npm run build
npm run check:packages
```

构建同时生成组件包与两个示例的静态产物。`vite preview` 用于本机检查构建产物，不代表已上线。源码示例使用工作区别名实现热更新；对外安装使用 `dist` 和声明文件，需分别核验。

`check:packages` 重建并打包两个组件包，在系统临时目录生成独立 React/Vite 工程，分别接入 B/C 两个入口，安装真实包后执行调用方的严格类型检查与构建，并用错误类型用例核验公开声明没有退化为 any。与 Vite 模板一致使用 `skipLibCheck`，不将依赖声明的内部一致性列为通过项。检查需要访问依赖源，失败时保留实际错误，成功时输出临时目录；测试入口仅核验分发，不是任务原型。浏览器操作仍在各示例或实际项目中检查。

## 在其他项目中共享

先在本目录运行构建，再打包：

```sh
npm run build
npm run pack:antd
npm run pack:web
```

命令输出两个 `.tgz` 的实际路径。在目标 React 项目中用其包管理器安装需要的文件。B 端安装匹配 peerDependencies 的 antd；C 端 Web 导入 `@dev-flow/ui-web/styles.css`。仅 C 端包使用 CSS 基础样式；已有主题时检查与项目全局样式的影响。React/ReactDOM 为 peerDependencies，沿用调用方版本。

```tsx
// B 端：基础控件继续从 antd 导入。
import { Table } from 'antd'
import { SelectionSummary } from '@dev-flow/ui-antd'

// C 端 Web：在对应应用入口加载组件样式。
import '@dev-flow/ui-web/styles.css'
import { ActionCard, Button } from '@dev-flow/ui-web'
```

组件包尚未发布到 npm，不能把包名当成已有公共包直接安装。项目记录包版本、源码 Git 提交、接入方式和已验证场景；锁定依赖，后续升级定向复验。源码复制适用于需要项目独立维护的 shadcn 组件，保留来源、许可与修改记录。仓库目前为本地 Git；设置远程后团队可按同一提交获取、构建与打包。

## 继续建设

按[共同组件约定](../../../dev-flow/references/ui-stack-and-components.md)维护组件契约、来源、例外、采用项目与验证。变更公共 Props 或状态含义时更新版本、清单和迁移说明，再检查受影响示例和采用项目。新增项目优先读取清单，按任务需要采用；不一次生成完整组件体系。

shadcn 底层组件来源及许可见 `packages/ui-web/THIRD_PARTY_NOTICES.md`。当前配置与依赖在锁文件固定；升级时读取当前官方文档并核验行为，不把本次测试版本固化为所有未来项目的要求。
