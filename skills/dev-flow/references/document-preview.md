# Vite 文档与原型预览

共享工具位于同包 `dev-flow/assets/document-workspace/`，采用 Vite + React + Ant Design 组织阅读入口，源文档继续由项目 Git 管理。产品与视觉使用同一入口；文档目录及归档按[共同协议](design-document-contract.md)维护。

## 接入与实际启动

优先复用项目已有有效文档工具。需要统一入口时可复制源码到项目；不依赖本仓库 npm 发布。以下命令中的项目绝对路径按本次实际工程替换，Node 满足工作区 engines，使用项目包管理器：

```sh
# 全局 Skill 的脚本先将工程复制到项目，冲突时保留项目修改
node "$HOME/.agents/skills/dev-flow/assets/document-workspace/scripts/preview.mjs" init --project /项目绝对路径
cd /项目绝对路径/tools/design-docs
npm ci
npm run dev -- --project /项目绝对路径 --roots docs/dev-flow,design --port 0
```

端口 0 请求空闲端口，程序读取 Vite 实际地址并写入 `.dev-flow/previews/documents.json`。项目已有权威目录时用 `--roots` 指定逗号分隔的项目相对目录，例如 `docs,design`；不存在的目录略过，全部不存在时先创建当前文档或改用有效目录。默认只监听本机，读取范围限定到选定目录，原型资源需在相同范围内。

本机已有同项目、同目录的有效服务时复用，不重复启动或停止其他任务。Ctrl+C 停止本次服务并清理它的运行记录；重启后重新取得实际地址。将 `.dev-flow/`、`node_modules/`、`dist/` 按项目约定加入忽略规则。

强制终止或系统退出可能留下旧记录；URL 工具会拒绝失效服务，重启覆盖本项目的旧记录。阅读器从 Markdown/MDX 元信息取得标题、版本和状态，其他格式的业务元信息由产品索引或相邻说明维护，当前没有自动读取 sidecar。任何格式进入 `archive/` 后都按历史资料显示。

也可直接在全局链接的工作区 `npm ci` 后运行服务，并显式指定 `--project`；复制到项目便于后续直接迭代工具。工具的构建检查验证阅读器编译，不包含静态站点导出；当前文件接口由 Vite 开发服务提供，远程发布按本次另行指定的交付处理。

## Agent 如何提供当前文档地址

在采用的工程内或使用全局脚本调用：

```sh
node scripts/preview.mjs url --project /项目绝对路径 --file docs/dev-flow/product/features/功能ID/spec.md
node scripts/preview.mjs url --project /项目绝对路径 --file docs/dev-flow/visual/features/功能ID/design.md
node scripts/preview.mjs url --project /项目绝对路径 --file design/prototypes/功能ID/方案/index.html
```

JSON 返回文件、格式、状态、实际 `viewUrl`/`rawUrl` 和 PID。工具核验服务身份、项目、允许目录、文件与索引；失效服务或不存在路径返回错误，Agent 先修复或实际启动再提供链接。目录与归档状态可以筛选，历史文件直接链接仍显示自身状态。

地址规则：`实际 origin + /view/ + 逐段 encodeURIComponent(项目相对路径)`；原文件入口使用 `/__docs/file/` 前缀。中文、空格、`#`、`?` 等文件名由工具编码，不能直接把 filesystem 路径或旧端口粘到 URL。必要场景参数按原型实际约定追加到地址，提供后在浏览器检查对应页面和状态。

## 格式与真实覆盖

| 格式 | 采用方式与边界 |
| --- | --- |
| Markdown | react-markdown + GFM：标题、表格、任务列表、脚注、相对链接/图片、代码高亮与锚点；YAML 元信息用于状态与索引 |
| MDX | 官方 `@mdx-js/rollup` 编译，可在文档中使用 React 示例和注入的 Ant Design Button/Alert/Space/Table；只编译项目可信源码，导入依赖需在工程中存在 |
| Mermaid、`.mmd` | 代码块或独立文件实际渲染流程/状态等图，解析失败明确显示错误 |
| HTML | 保留相对脚本、样式和资源，隔离 iframe 展示；`rawUrl` 可直接打开原型。完整 React 原型优先继续使用已有 Vite 工程，再从文档关联 |
| PDF | PDF.js 逐页渲染与翻页；原文件同时保留，文档的文本规则建议另有可读源 |
| PNG/JPEG/SVG/WebP/GIF/AVIF | 原生图片预览；用于设计图、截图等有版本的资产 |
| DOCX | Mammoth 转语义 HTML 并消毒，支持常见标题、段落和表格；精确排版需原件或同版本 PDF |
| XLSX、CSV | ExcelJS/Papa Parse，支持表格和工作表切换；最多显示 300 条数据/30 列，公式不重新计算，复杂图表/样式以原件为准 |
| JSON/YAML/TOML/XML、文本和常见源码 | 可读源码视图，JSON 格式化；不执行配置或业务脚本 |
| 音视频 | 浏览器原生播放，具体编码由浏览器支持 |
| PPTX、旧 Office、Figma/Sketch/Draw.io/Excalidraw 等专用源格式 | 保留原文件下载，关联同版本 PDF/HTML/SVG/图片导出或已有原工具入口；按实际需要接入相应转换器，不声称原格式已完整渲染 |

文本接口上限 2 MiB、单个原文件 50 MiB、索引 2500 个文件；过大内容拆分或使用原工具，明确截断与覆盖。对无法可靠解析的格式提供原件和具体错误，而不是显示空白后声称成功。新增格式优先使用已维护的成熟工具，补齐相关真实文件和浏览器验证后再登记支持。

来源：[react-markdown](https://github.com/remarkjs/react-markdown)、[MDX/Vite](https://mdxjs.com/docs/getting-started/#vite)、[Mermaid](https://mermaid.js.org/config/usage.html)、[Mammoth](https://github.com/mwilliamson/mammoth.js)、[ExcelJS](https://github.com/exceljs/exceljs)、[PDF.js](https://mozilla.github.io/pdf.js/)。工具采用版本与依赖许可随锁文件保留。

## 检查与讨论

实际打开当前文件，确认目录、元信息、相对链接、资源和所需格式正确显示；原型还要操作核心任务。对目标窗口、长文档/表格、相关错误状态进行必要检查，反馈写回权威规格，源码变化后重新核验。可打开不代表产品规则、视觉设计或生产功能已经验收。
