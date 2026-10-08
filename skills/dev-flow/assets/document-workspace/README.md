# 项目文档预览工程

Vite + React 阅读器，供产品、视觉、架构与研发共用，读取本次业务项目的产品、交互原型、设计/UI、技术及相关验收/交付资料。先从项目文档索引确定实际目录，显式用 `--project` 指向该业务项目、`--roots` 指向其文档目录；阅读器所在的工具/Skill 仓库不自动成为文档项目。按项目源路径预览 Markdown、MDX、Mermaid、HTML、PDF、图片、DOCX、XLSX/CSV 和常见文本；完整格式边界、目录及地址协议读取全局 `dev-flow` Skill 的 `references/document-preview.md`，复制到项目后本工程继续独立运行。

```sh
npm ci
npm run dev -- --project /项目绝对路径 --roots docs/dev-flow,design --port 0
npm run url -- --project /项目绝对路径 --file docs/dev-flow/product/index.md
```

复制到项目：`node scripts/preview.mjs init --project /项目绝对路径`，默认目标 `tools/design-docs`。全文件集先核验，既有不同内容保留；复制后在目标直接迭代。所需包是公开依赖，工程不发布为自有 npm 包。

当前 origin、PID、根目录保存在项目 `.dev-flow/previews/documents.json`。URL 工具核验实际服务和文件；停止后链接不可用，源文档和重启命令长期保留。采用记录保存来源 Git 提交/实际文件哈希、项目差异和验证。

`npm run typecheck`、`npm run build`、`npm run check` 分别检查公开工程类型、阅读器编译与路径/采用边界。构建不包含静态导出后的文件服务。MDX 是项目可执行源码，需采用已核验来源；其他文档转换的预览不改变权威原件。
