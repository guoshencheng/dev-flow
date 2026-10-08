# 视觉首版与文档预览验证记录

日期：2026-10-08。执行方式：主 Agent 建设指导、工具与虚构案例，使用本机 Node/npm、文件/HTTP 检查及 Codex 内置浏览器操作；没有原生职责派发或独立子 Agent 评测。

## 候选与成果

本轮候选为总纲 v0.5、产品指导 v0.8、视觉指导 v0.1、共同文档协议 v0.1、文档工程 v0.1.0。基于仓库提交 `bda13bb` 的工作副本检查，本轮源文件哈希见 [checks.json](checks.json)，历史产品证据不变。

视觉具有单独的 TOML、Skill、四份按需专业参考和设计规格模板，复用已有 React 组件源码及 Ant Design/shadcn 约定，没有固定模型或强度。共同协议明确当前产品/视觉规格、原型、证据、状态与归档；产品规格增加原型结构、使用限制、功能透出、执行条件、具体逻辑与 RULE/AC。

Vite + React 阅读器位于 `skills/dev-flow/assets/document-workspace/`，使用成熟渲染器，支持复制整套源码/锁文件到项目后迭代。UI 默认 Ant Design。源文件路径可以生成当前服务的编码地址，运行记录进入被忽略的 `.dev-flow/`。

## 实际工具检查

| 检查 | 结果及覆盖 |
| --- | --- |
| Skill/TOML | 三个 Skill 的 quick_validate 通过；两个职责 TOML 解析通过，必需字段存在且没有模型/强度字段 |
| 全局安装 | 临时目录验证 3 Skills/2 职责、重复安装、既有指引保留及全量冲突预检；实际全局安装与 `--check` 通过 |
| 类型与构建 | TypeScript 通过；阅读器常规构建、包含样例 MDX 的构建通过；构建有大于 500 kB 的 chunk 提示 |
| 回归 | `npm run check` 三项通过：路径/范围/归档，复制冲突保护，真实进程的地址/MDX/复用/读取范围/退出/失效记录 |
| 独立源码副本 | 临时项目复制 15 个工程文件，自身 `npm ci`、类型检查和启动通过；本地 Markdown 与含 antd 导入的 MDX 编译接口通过 |
| 服务恢复 | 独立副本重启获得不同实际端口，URL 工具返回新地址；正常退出清理由最终回归验证，旧失效记录不能生成可用地址 |
| 范围与方法 | 未选定文件、缺失文件、编码跨目录和 Vite `/@fs/etc/passwd` 请求被拒绝；文档写请求返回 405；链接逃逸由路径测试覆盖 |

独立副本安装使用本轮临时 npm 缓存，未修改用户原缓存的所有权。安装出现 ExcelJS 等依赖树的弃用提示，保留锁文件，未将其作为依赖安全审计通过。阅读器构建不包含静态文件服务导出或远程部署。

## 实际浏览器检查

使用隔离[样例项目](../../../fixtures/document-project/docs/dev-flow/index.md)，所有角色、配额和发布都是本地模拟。

| 场景 | 实际观察 |
| --- | --- |
| Markdown | 产品规则、表格、元信息和 Mermaid 实际显示；产品→原型/视觉的相对链接有效 |
| 原型 AC-batch-001 | 输入 4 项禁用并显示“单次最多发布 3 项”；调整为 3 项恢复可操作 |
| 原型 AC-batch-002 | 查看者隐藏发布按钮，保留当前页数量摘要 |
| 原型 AC-batch-003 | 配额耗尽禁用并解释，3 项选择保留 |
| 原型 AC-batch-004 | 提交 2 项时按钮/数量输入处于等待状态；随后反馈模拟发布 2 项并清空选择 |
| DOCX | 两段中文规则显示，语义预览与精确排版的边界可见 |
| XLSX/CSV | 中文规则与数值显示；XLSX 从“规则”切到“验收”，显示 AC-batch-001；CSV 同一规则显示 |
| PDF | 真实 PDF 的第 1 页文字绘制、下一页 2/2 与边界禁用有效，保存两页截图 |
| 图片/源码/图 | SVG 以 640×220 加载；JSON 格式化、YAML/TypeScript 原文可读；独立 `.mmd` 节点文字可见 |
| HTML | iframe 中相对脚本执行成功；`state=quota-exhausted` 实际传入，显示对应场景；样式与相对资源加载 |
| 未知格式 | `.custom` 展示原工具/导出说明并保留原文件入口，不显示假预览 |
| 归档 | 开关显示历史候选，历史警告与现行规格链接有效；当前工具对任何 `archive/` 内文件识别历史状态 |
| 中文路径与更新 | 中文、空格和 `#` 文件编码定位及刷新有效；修改源文档自动显示临时验证文本，随后恢复原文 |
| 窗口 | 桌面 1280×720；390×844 下目录抽屉、产品页面和原型可操作，产品与原型 documentWidth 均为 390；表格保留区域内滚动 |
| 正式协议 | 实际打开本仓库的共同协议，跳转产品模板成功；新的正式文档标签页没有 warn/error 日志 |

浏览器检查中发现并修复了 Mermaid 12 的 HTML 标签配置位置、MDX 编译顺序、React 函数组件状态保存和入口热更新清理问题。最终相关页面已重新加载并操作；旧标签页日志保留先前故障，不声明历史日志从未出现错误。

截图：[产品桌面](product-desktop.png)、[手机规则](product-mobile.png)、[原型限制](prototype-mobile-limit.png)、[模拟成功](prototype-success.png)、[表格](spreadsheet.png)、[PDF 1](pdf-page1.png)、[PDF 2](pdf-page2.png)、[归档](archived.png)、[正式协议](document-contract.png)。

## 复现

```sh
cd skills/dev-flow/assets/document-workspace
npm ci
npm run typecheck
npm run check
DEV_FLOW_DOC_PROJECT=/实际仓库路径/evals/dev-visual/fixtures/document-project npm run build
npm run dev -- --project /实际仓库路径/evals/dev-visual/fixtures/document-project --port 0
node scripts/preview.mjs url --project /实际仓库路径/evals/dev-visual/fixtures/document-project --file docs/dev-flow/product/features/batch-publish/spec.md
```

复制验证使用 `preview.mjs init --project <临时项目>` 后，在副本工程内 `npm ci`、类型检查、实际启动和 HTTP 读取。临时副本已停止；预览地址由当前服务重新取得，记录中的端口不是永久地址。

## 未覆盖和后续

- 原生 `dev_visual` 发现、派发和实际模型设置未验证；全局链接、TOML 和 Skill 检查不能替代。
- 本轮指导未进行独立模型行为评测；真实品牌、用户反馈、跨任务视觉资产复用、研发集成与生产端到端交付未验证。
- 音视频保留浏览器原生能力，本轮无相关播放样例；PPTX、旧 Office、专用设计文件使用原件与同版本导出，不声明原格式完整渲染。
- DOCX 不证明精确排版；XLSX 不重算公式/完整还原图表；文本 2 MiB、原文件 50 MiB、目录 2500 文件、表格 300 数据行/30 列上限已明确。
- 复杂大文档性能、生产体积优化、远程部署与外部文件转换未执行。非 Markdown/MDX 的业务元信息暂由索引/相邻说明维护，没有自动 sidecar 读取。

后续在真实 UI 任务补专业行为和持续交接证据，再建设测试验收职责，保持研发测试来回对焦与可运行交付要求。
