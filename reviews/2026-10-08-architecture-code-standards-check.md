# 架构职责 v0.3：三类技术约定与代码规范检查

日期：2026-10-08。主 Agent 读取 dev-flow 总纲、dev-architecture 和系统 skill-creator 指导完成本轮，没有使用子 Agent 或原生职责派发。

## 本轮范围

用户明确确定 React Web、Next.js 全栈与 Astro 纯静态三项选择，其他类型暂不建设通用技术 Guide。现行[技术约定](../skills/dev-architecture/references/technology-stack.md)按此收敛；原多平台草案移出 Skill，保存为[历史文件](../docs/project-tech-stacks/archive/2026-10-08-stack-profiles-v0.1.md)，原调查标为 superseded。历史检查仅修复归档跳转并标明原路径，保留原检查范围与结论。

新增[代码规范](../skills/dev-architecture/references/code-standards.md)、可复制格式配置与实际命令约定，并在[架构设计](../skills/dev-architecture/references/design-and-contracts.md)中细化研发前应明确的基线。职责配置、能力目录与项目规范入口同步更新，模型/强度未固定，重要确认与 AI 计划复核协议保持现行规则。

## 工具选择与来源

新工程采用 EditorConfig + Prettier + ESLint + TypeScript；已有有效项目配置按范围复用。busy-fish 的项目格式配置提供现有风格参考；框架/插件与分工依据官方资料，具体来源已链接在代码 Guide 中。

复制资产覆盖通用 EditorConfig、Prettier 配置/忽略文件、Astro 官方 Prettier 插件配置和合并用 package scripts。`format` 只含格式器与写入选项，目标路径必须显式传入，避免传指定文件时仍隐式处理全仓。ESLint/类型配置沿用兼容的官方/项目配置，本轮未发布一套覆盖所有版本的自有 preset。

## 实际检查

工具案例在本仓库忽略的 `.dev-flow/` 中创建隔离安装/文件，使用 Prettier 3.9.9、prettier-plugin-astro 1.1.0，实际 Node v26.4.0。版本与完整输入/输出、命令结果和配置指纹见[实际记录](../evals/dev-architecture/runs/2026-10-08/code-standards/checks.json)；这是本次工具环境，未固定为所有项目版本要求。

| 检查 | 实际结果与证明范围 |
| --- | --- |
| React TSX | 检查拒绝未格式化文件；指定组件修复不改变另一组件；完整修复后通过，重复修复无变化 |
| Next 常用文件 | page.tsx 与 API route.ts 按相同项目配置格式化，指定页面修复不改变 route；完整修复后通过 |
| Astro | 带 TS frontmatter 的 `.astro` 与 TS 文件使用官方格式插件；指定页面修复保持其他源码，完整修复后通过 |
| 忽略范围 | 各案例的锁文件、根生成目录与临时捕获文件保持原字节；包含故意不可解析的生成/捕获内容，实际未被处理 |
| 执行记录 | 三组共 18 次 CLI 执行，预设格式错误的检查失败，完整修复后的检查通过；通过实际 npm script 验证目标范围 |
| Skill / 配置 | dev-architecture、dev-flow 结构检查通过，三个 TOML 解析通过且模型/强度字段保持省略 |
| 全局接入 | `install_global.py --check` 通过，四个 Skills/三个职责与指引仍链接本仓库；没有修改安装脚本 |
| 文档与预览 | 本地引用与 JSON 模板解析通过；URL 工具核验工具仓库、源文件和 PID 97533；实际浏览器查看代码 Guide，点击到 Astro 格式配置并确认源码显示。这是 Skill 文件呈现检查，不能证明业务项目文档预览 |

模板采用普通文件名，Guide 明确复制时恢复项目点文件名。用户随后明确预览应面向当前业务项目的产品、设计/UI 与技术成果，上述浏览器操作选错了对象；[预览范围修订](2026-10-08-project-document-scope-check.md)已校正流程。原项目源码、依赖与配置未修改，也未运行真实项目检查或部署。

## 限制与后续验证

格式模板检查只证明所用工具版本与代表文件的格式/作用范围；不能证明真实工程 lint/typecheck/build、业务行为、架构符合性或端到端交付。规范中的 ESLint/TS 方案根据已核验的官方文档提供接入指导，实际框架/插件版本要在具体项目接入时核验。

v0.1 的原生发现/派发及真实项目复用缺口继续保留；本轮没有新增模型行为评测。样本项目的技术事实仍以各项目当前源码/规范为准，历史调查不成为本轮自动整改指令。
