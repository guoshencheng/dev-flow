# React 原型与共享源码工作区

此目录与 `dev-product` Skill 在同一 Git 仓库维护。Vite + React + TypeScript 提供预览与检查；共享组件按源码复制或参考实现进入项目，由项目直接迭代。

## 目录与边界

| 目录 | 用途 |
| --- | --- |
| `packages/ui-antd/src` | B 端基于 antd 的组合源码；基础控件直接使用 antd |
| `packages/ui-web/src` | C 端 Web 的 shadcn/ui 源码、主题起点与组合 |
| `apps/antd-lab`、`apps/web-lab` | 两套设计体系的独立行为示例 |
| `apps/component-gallery` | B/C 独立预览入口，搜索、状态、使用示例、源码文件集和候选记录 |
| `catalog.json`、`scripts/catalog.mjs` | 源码索引、依赖文件闭包、用途与查询 |
| `scripts/copy-component.mjs` | 将源码、所需工具文件、样式与许可复制到指定项目，登记来源哈希 |

`packages/` 和内部工作区名称用于本仓库组织与预览热更新；目标项目导入自己的本地源码。项目业务、权限、接口和文案由项目定义。两套设计体系分别运行，C 端样式按项目现有主题接入。契约与验证见[组件清单](catalog.md)。

## 预览与查询

使用满足 package.json engines 的 Node.js：

```sh
cd "$HOME/.agents/skills/dev-product/assets/react-workspace"
npm ci
npm run dev:gallery
```

打开实际输出地址：`/index.html` 是 B 端，`/web.html` 是 C 端 Web；可分享带组件 ID 和状态的实际 URL。可以查看使用示例或源码文件，复制当前代码或完整源码文件集 JSON，加入候选并复制、下载选择记录。候选在当前浏览器会话中跨入口保留。

```sh
npm run dev --workspace @dev-flow/component-gallery -- --port 5177
npm run --silent catalog
npm run --silent catalog -- antd-selection-summary
```

按 ID 查询返回用途、依赖清单、源码内容、使用示例、来源提交与各文件 SHA-256。使用示例已经改为本地相对导入，基准位置为 `src/Example.tsx` 和 `src/components/dev-flow/`，其他目录调整相对路径。源码有未提交修改时记录基准提交、修改状态与实际文件哈希，允许立即采用当前源码。

## 复制到项目并直接迭代

先读取目标项目现有组件、依赖和主题。按需直接复制，或参考源码在项目现有组件中实现。快速复制命令：

```sh
npm run --silent copy:component -- antd-selection-summary --to /目标项目/src/components/dev-flow
npm run --silent copy:component -- web-action-card --to /目标项目/src/components/dev-flow
```

工具复制必要组件与支持文件，保留目录内相对导入；生成 `.component-sources/<ID>.json`，包含来源、文件哈希与验证过的基础依赖。相同内容可重复使用；发现不同内容的目标文件时先停止，保留项目修改，由 Agent 比较后合并。工具不修改项目 package.json、入口或主题，输出的依赖版本是已验证组合，接入时核对项目现有版本、只补缺失依赖。

```tsx
// B 端：基础组件继续使用 antd，组合从本项目导入。
import { Table } from 'antd'
import { SelectionSummary } from './components/dev-flow/business/selection-summary'

// C 端 Web：组件从本项目导入，接入本项目的 shadcn/Tailwind 主题。
import { ActionCard } from './components/dev-flow/web/action-card'
```

C 端 Web 已有 Button、Card、cn 或主题时优先复用现有实现，按需要复制组合并调整导入；完整复制适用于独立起点。随包 styles.css 是 Tailwind v4 源码主题示例，需使用对应 Vite 插件编译；已有主题时合并所需 Tokens 和类扫描，保留项目主题。许可与来源文件一并留存。

复制后在项目直接修改、构建和交付。共享仓库后续改动由 Agent 比较来源与项目差异，按任务需要合并；项目验证过的通用改进可以回收到共享源码。具体流程见[组件预览与复用指南](../../references/component-preview-and-reuse.md)。

## 检查与持续维护

```sh
npm run typecheck
npm run build
npm run check:source
```

类型与构建检查覆盖本工作区。`check:source` 在系统临时目录创建独立 React/Vite 工程，复制四类源码，直接导入本地文件并检查严格类型与 B/C 构建；同时验证重复复制、冲突前核验、保留项目修改，以及项目副本迭代不改变来源。临时工程只安装公开基础依赖，运行不依赖 Skill 工作区或自有组件包；安装检查需要访问依赖源。浏览器验证仍需检查实际入口和操作。

内部构建目录只用于本仓库检查；`vite preview` 是本机产物检查。项目采用登记来源文件、提交或哈希、用途、差异与实际证据；当前没有真实项目采用或远程 Git 同步证据。通用组件变更更新契约、索引、可运行示例及受影响检查，按需要回收真实项目经验。
