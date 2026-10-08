# 架构技术选型 v0.1 / 架构职责 v0.2 检查记录

日期：2026-10-08。主 Agent 按 dev-flow、dev-architecture 和 skill-creator 指导完成本轮；没有派发子 Agent 或原生 `dev_architecture`。本轮只修改协作仓库，不修改样本项目，也不运行它们的安装、构建、测试、迁移或部署。

## 范围与来源

项目根为 `/Users/guoshencheng/Documents/work`；元数据扫描覆盖 31 个一级目录，样本来源覆盖 18 个项目目录 / 117 个相关文件，metrix-content 内 News 和媒体单元分开说明。沿项目规范、入口与必要实现进行定向阅读，未进行这些项目的全仓代码审计。

来源清单与内容指纹保存在[来源快照](../docs/project-tech-stacks/2026-10-08-sources.json)；声明/入口、限制和候选分别写入[项目调查](../docs/project-tech-stacks/2026-10-08-survey.md)。Node、Vite、Next、Hono、Astro、Flutter、Apple、Electron、WXT、Three.js、Godot 和 MCP 的官方文档用于核验通用推荐，引用放在对应指导处。

## 本轮成果

- [技术栈选型](../skills/dev-architecture/references/technology-stack.md)：执行形态与用户任务、现状与决定、候选默认、包管理/CI 依据、基线更新及重要选择的确认边界。
- [各平台约束（历史归档）](../docs/project-tech-stacks/archive/2026-10-08-stack-profiles-v0.1.md)：检查时位于 `skills/dev-architecture/references/stack-profiles.md`，后续按用户要求移出 Skill；本记录保留当时检查范围。
- [项目技术基线模板](../skills/dev-architecture/assets/templates/technology-baseline.md)：工具链/锁、入口、有效决定、模块与数据关系、交付/证据与演进。
- 架构 Skill、职责 TOML、设计/资产协议和说明接入上述参考；A05 细化技术与质量取舍，保持六类四十八项主能力。共同确认与 AI 计划复核协议未改变；职责配置省略模型与强度。

## 实际检查

本轮实际执行结果：

| 检查 | 结果与证明范围 |
| --- | --- |
| Skill 结构 | 系统 skill-creator 的 `quick_validate.py` 检查 dev-architecture、dev-flow，均通过；证明结构/元信息合法 |
| 职责配置 | Python tomllib 解析三个职责 TOML，name/入口说明成立，均未设置 model/model_reasoning_effort；不证明原生发现/派发 |
| 全局接入 | `python3 scripts/install_global.py --check` 通过：四个 Skills、三个原生配置及全局指引；沿用现有链接，未改安装脚本或覆盖全局配置 |
| 调查版本 | 重新计算 117 个来源文件 SHA-256，均与来源快照一致；核对主要 manifest 的版本声明与清单描述 |
| 文档引用 | 14 个新增/修改 Markdown 中 122 个本地文件引用均存在；外部资料使用官方入口 |
| 实际预览 | URL 工具核验工程、源文件、索引和服务 PID 97533；浏览器查看调查、选型指导、平台约束，截图核验调查排版，点击指导到平台约束的相对链接成功 |
| 差异检查 | 本仓库 `git diff --check` 通过；历史行为评测/来源文件保持原版本 |

本次[调查预览](http://127.0.0.1:49688/view/docs/project-tech-stacks/2026-10-08-survey.md)与[选型预览](http://127.0.0.1:49688/view/skills/dev-architecture/references/technology-stack.md)依赖当前本机服务；以后从运行信息重新生成地址。历史 v0.1 行为证据见[原记录](../evals/dev-architecture/report.md)，不将其覆盖范围延伸为本轮新增选型能力。

## 能力与交付限制

静态元数据与源码只能支持所读配置、依赖声明和相关结构事实，不证明设备、原生库、数据库、媒体、浏览器扩展或部署实际可用。来源快照不是每个项目的持续技术基线，本轮未往样本项目写入 `stack.md`。

新增选型方法仍需后续真实任务验证采用、用户重要选择、研发/测试交接与交付循环；原生职责发现/派发和跨上下文恢复仍需单独证据。News 包管理冲突等发现只登记为待核验输入，没有执行升级、删锁或整改。全局链接若检查成立可反映源码更新，实际新会话加载与专业行为另外验收。
