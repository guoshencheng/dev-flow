# 当前项目的文档与原型预览

预览对象是本次业务项目的产品文档、交互原型、设计/UI 文档、技术文档及相关验收、交付资料。共享工具位于同包 `dev-flow/assets/document-workspace/`，采用 Vite + React + Ant Design 组织阅读入口；工具源码与项目文档分别定位，源文档继续由所属项目 Git 管理。各职责使用同一项目入口，文档目录及归档按[共同协议](design-document-contract.md)维护。

## 先定位当前项目及其文档

从用户指定对象、任务关联的业务代码和项目入口确定项目名称、绝对根路径；工具仓库、全局 Skill 目录和启动命令的工作目录不能自动成为业务项目。多仓库/monorepo 任务标明文档所属项目与受影响执行单元，复用有效项目索引。

先从项目索引定位本次迭代索引，在迭代索引中明确产品、交互原型、设计/UI、技术文档各自的权威路径、职责、版本/状态和预览方式；验收、交付文档按范围关联。已有目录保留，通过索引映射。技术文档指该项目的架构、模块、契约、工程规范和重要决定。缺少资产标明尚未建立、待核验或不适用，不能用通用 Skill 指导代替项目成果。无现行入口时按[项目文档索引模板](../assets/templates/project-document-index.md)建立 `docs/dev-flow/index.md`，只登记实际存在的文件与已知缺口。

向用户讨论、确认或交付本次项目设计文档时，复用或启动该项目的阅读入口，提供项目名称、文档类别与名称、源路径/版本和对应预览链接；原型另给实际可操作入口和场景。一次提供本次相关成果与项目索引即可，不轮流打开所有资料。仅维护 Skill/Agent 方法时使用源文件链接和内容/引用检查；只有用户明确要求阅读 Skill 网页或验证预览工具时，才预览工具仓库资料。

## 接入与实际启动

优先复用项目已有有效文档工具。需要统一入口时，默认直接调用已安装 Skill 中的阅读器脚本，并显式传入项目目录；不依赖本仓库 npm 发布。以下命令中的项目绝对路径按本次实际工程替换，Node 满足工作区 engines：

```sh
# 从宿主 Skill 列表取得实际绝对目录，替换下面的占位路径
DEV_FLOW_SKILL_DIR="/实际安装目录/skills/dev-flow"
node "$DEV_FLOW_SKILL_DIR/assets/document-workspace/scripts/preview.mjs" \
  serve --project /项目绝对路径 --roots docs/dev-flow,design --port 0
```

首次直启时脚本按 `package-lock.json` 在共享阅读器模板目录准备依赖；其他项目复用同一份依赖，不创建 `tools/design-docs`。项目只需保留文档源文件和 `.dev/previews/documents.json` 运行记录。运行记录和健康接口包含阅读器模板版本/指纹，便于核对实际候选。

需要项目级修改阅读器或兼容旧项目时，仍可复制源码到项目：

```sh
node "$DEV_FLOW_SKILL_DIR/assets/document-workspace/scripts/preview.mjs" init --project /项目绝对路径
cd /项目绝对路径/tools/design-docs
npm ci
npm run dev -- --project /项目绝对路径 --roots docs/dev-flow,design --port 0
```

复制入口会先核验全文件集，发现已有不同内容时保留项目修改并终止，不自动覆盖。

端口 0 请求空闲端口，程序读取 Vite 实际地址并写入该业务项目的 `.dev/previews/documents.json`。先根据项目文档索引确定实际目录，再用 `--roots` 指定逗号分隔的项目相对目录，例如 `docs,design`；这两个目录名只是示例。不存在的目录略过，全部不存在时先创建本次确需的项目文档或改用有效目录。默认只监听本机，读取范围限定到选定目录，原型资源需在相同范围内。

本机已有同项目、同目录的有效服务时复用，不重复启动或停止其他任务。Ctrl+C 停止本次服务并清理它的运行记录；重启后重新取得实际地址。将 `.dev/`、`node_modules/`、`dist/` 按项目约定加入忽略规则。

强制终止或系统退出可能留下旧记录；URL 工具会拒绝失效服务，重启覆盖本项目的旧记录。阅读器从 Markdown/MDX 元信息取得标题、版本和状态，其他格式的业务元信息由产品索引或相邻说明维护，当前没有自动读取 sidecar。任何格式进入 `archive/` 后都按历史资料显示。

也可在可写的源码工作区运行服务，并显式指定 `--project`。安装包作为复制来源；在项目副本安装依赖和迭代工具。工具的构建检查验证阅读器编译，不包含静态站点导出；当前文件接口由 Vite 开发服务提供，远程发布按本次另行指定的交付处理。

## Agent 如何提供当前文档地址

在采用的项目工具工程内调用：

```sh
node scripts/preview.mjs url --project /项目绝对路径 --file docs/dev-flow/iterations/迭代ID/product/spec.md
node scripts/preview.mjs url --project /项目绝对路径 --file docs/dev-flow/visual/pages/页面ID.md
node scripts/preview.mjs url --project /项目绝对路径 --file docs/dev-flow/iterations/迭代ID/architecture/design.md
node scripts/preview.mjs url --project /项目绝对路径 --file docs/dev-flow/iterations/迭代ID/product/prototypes/方案/index.html
```

命令中的文件路径替换为项目索引登记的实际路径。JSON 返回文件、格式、状态、实际 `viewUrl`/`rawUrl` 和 PID。工具核验服务身份、项目、允许目录、文件与文件清单；它不自动判断产品/UI/技术文档的业务分类与权威性，这些由 Agent 维护的项目文档索引说明。失效服务或不存在路径返回错误，Agent 先修复或实际启动再提供链接。目录与归档状态可以筛选，历史文件直接链接仍显示自身状态。

地址规则：`实际 origin + /view/ + 逐段 encodeURIComponent(项目相对路径)`；原文件入口使用 `/__docs/file/` 前缀。中文、空格、`#`、`?` 等文件名由工具编码，不能直接把 filesystem 路径或旧端口粘到 URL。必要场景参数按原型实际约定追加到地址。首次接入阅读入口、改变渲染方式/资源路径或交互原型时，实际打开本次相关项目页面检查；普通文字修订检查内容和引用，需要提供链接时用 URL 工具核验，不逐篇打开浏览器。

## 格式与真实覆盖

| 格式 | 采用方式与边界 |
| --- | --- |
| Markdown | react-markdown + GFM：标题、表格、任务列表、脚注、相对链接/图片、代码高亮与锚点；YAML 元信息用于状态与索引 |
| MDX | 官方 `@mdx-js/rollup` 编译，可在文档中使用 React 示例和注入的 Ant Design Button/Alert/Space/Table；只编译项目可信源码，导入依赖需在工程中存在 |
| Mermaid、`.mmd` | 代码块或独立文件实际渲染流程/状态等图，解析失败明确显示错误 |
| HTML | 保留相对脚本、样式和资源，隔离 iframe 展示；`rawUrl` 可直接打开已有纯 HTML 原型。模块化 React 设计稿由自身应用/Vite 工程运行，再从文档关联，源码 `index.html` 不等于可独立运行的设计稿 |
| PDF | PDF.js 逐页渲染与翻页；原文件同时保留，文档的文本规则建议另有可读源 |
| PNG/JPEG/SVG/WebP/GIF/AVIF | 原生图片预览；用于设计图、截图等有版本的资产 |
| DOCX | Mammoth 转语义 HTML 并消毒，支持常见标题、段落和表格；精确排版需原件或同版本 PDF |
| XLSX、CSV | ExcelJS/Papa Parse，支持表格和工作表切换；最多显示 300 条数据/30 列，公式不重新计算，复杂图表/样式以原件为准 |
| JSON/YAML/TOML/XML、文本和常见源码 | 可读源码视图，JSON 格式化；不执行配置或业务脚本 |
| 音视频 | 浏览器原生播放，具体编码由浏览器支持 |
| PPTX、旧 Office、Figma/Sketch/Draw.io/Excalidraw 等专用源格式 | 保留原文件下载，关联同版本 PDF/HTML/SVG/图片导出或已有原工具入口；按实际需要接入相应转换器，不声称原格式已完整渲染 |

文本接口上限 2 MiB、单个原文件 50 MiB、索引 2500 个文件；过大内容拆分或使用原工具，明确截断与覆盖。对无法可靠解析的格式提供原件和具体错误，而不是显示空白后声称成功。新增格式优先使用已维护的成熟工具，补齐相关真实文件和浏览器验证后再登记支持。

## 模块化设计稿入口

React 设计稿的持续维护与模块组织采用[视觉指南](../../dev-visual/references/system-and-pages.md#原型与工程复用)。文档阅读器展示规格、决定、组件/源码映射及局部 MDX 示例；完整设计稿复用同一项目的应用或独立 Vite 服务，在项目索引登记其源码路径、启动命令、场景路由和确认版本。

各端页面/组件、设计规范与尺寸容器独立维护，由设计总览组合渲染；总览采用自身 React 服务，提供同一整合页与必要独立入口，不在文档阅读器中复制业务页面。移动端总览按[屏幕尺寸预览](../../dev-visual/references/system-and-pages.md#移动端屏幕尺寸预览)展示指定内部宽高，模拟范围默认仅屏幕尺寸。现行规范/页面文档在项目级持续维护，迭代文档地址按需指向变更记录，不每轮创建完整 UI 文档。

`preview.mjs url` 核验文档文件地址，不生成独立 React 应用的业务路由，也不把任意 `.tsx` 源文件编译成可操作设计稿。提供页面入口时读取该应用服务实际输出的 origin，再定位确实存在的路由并打开检查；不要将 Vite 源码 `index.html` 经 HTML 阅读器打开后当成 React 运行结果。已有 MDX 编译依赖按阅读器实际工程核验，不默认把业务应用的组件依赖安装进共享阅读器。

来源：[react-markdown](https://github.com/remarkjs/react-markdown)、[MDX/Vite](https://mdxjs.com/docs/getting-started/#vite)、[Mermaid](https://mermaid.js.org/config/usage.html)、[Mammoth](https://github.com/mwilliamson/mammoth.js)、[ExcelJS](https://github.com/exceljs/exceljs)、[PDF.js](https://mozilla.github.io/pdf.js/)。工具采用版本与依赖许可随锁文件保留。

## 检查与讨论

需要渲染/交互检查时，实际打开当前项目的相关文件，确认目录、元信息、相对链接、资源和所需格式正确显示；原型还要操作核心任务。对目标窗口、长文档/表格、相关错误状态进行必要检查，反馈写回该项目的权威规格，受影响的呈现/行为变化后定向复验。可打开不代表产品规则、视觉设计或生产功能已经验收。没有项目文档预览需求的 Skill 维护任务，无需启动或轮询文档服务。
