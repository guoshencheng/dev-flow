# Dev Flow

面向 Codex 与 Kimi 的六职责研发协作插件。流程、专业职责和操作技能分别维护：`dev-flow` 只安排阶段、依赖、授权和完成条件；六职责 Agent 提示词承担专业判断；操作 Skills 提供具体方法与工具。项目业务事实保存在所属项目。

当前源码版本 **0.9.1**，总纲 **0.35**：提前执行适用真实冒烟，按影响选择用例，区分阻碍测试的缺陷与集中修复项，合并定向 Review、复验及回归；Web 复用项目 Playwright 和脚本，需要视觉判断时实际观察画面。0.9.1 整理本轮交付记录；保留 UI 方案确认、文档审阅效率规则、独立 [iteration-closeout](skills/iteration-closeout/SKILL.md)、文档协议 0.16 和安装机制；状态 schema 1 及核验算法不变。验证和安装状态见[本轮 Progress](docs/plans/2026-10-27-acceptance-efficiency/Progress.md)。

## 能力入口

| 内容 | 唯一维护源 | 作用 |
| --- | --- | --- |
| 流程 | [dev-flow](skills/dev-flow/SKILL.md)、[总纲](skills/dev-flow/references/constitution.md) | 路径、阶段、参与职责、前置依赖、授权、变更、整体完成与收尾 |
| 六职责 | [agents/prompts](agents/prompts/) | 专业目标、判断原则、责任边界及交接标准 |
| 专业参考和写作模板 | [agents/references](agents/references/)、[agents/assets](agents/assets/) | 长篇标准、评审检查表、设计/计划/收尾模板；按需读取 |
| 操作技能 | 下表的 Skills | 独立操作触发、输入、执行方法与可核验输出 |
| 候选能力声明 | [capabilities.json](capabilities.json) | Skill 清单、角色路由与必需资源；生成/打包校验使用 |

六职责分别为[产品](agents/prompts/product.md)、[视觉](agents/prompts/visual.md)、[架构](agents/prompts/architecture.md)、[研发](agents/prompts/engineering.md)、[测试验收](agents/prompts/acceptance.md)、[运维交付](agents/prompts/operations.md)。所有宿主入口从提示词源生成，不反向从 Skill 描述推导职责，不手工维护第二份专业规则。

## 操作 Skills

| Skill | 操作对象 |
| --- | --- |
| [iteration-closeout](skills/iteration-closeout/SKILL.md) | 本轮资料盘点、有效变化提炼、项目长期文档实际回写与收尾结果 |
| [git-workflow](skills/git-workflow/SKILL.md) | 基线、分支/worktree、完整差异、提交、冲突与已授权集成 |
| [subagent-coordination](skills/subagent-coordination/SKILL.md) | 能力发现、任务包、隔离写入、派发/等待与结果收集 |
| [document-management](skills/document-management/SKILL.md) | 文档目录/索引/版本/链接、Web 阅读、总结与逻辑归档 |
| [product-specification](skills/product-specification/SKILL.md) | 将任务与决定表达为流程、状态、RULE/可观察 AC |
| [react-prototyping](skills/react-prototyping/SKILL.md) | 原型构建、设计工作台、多端场景与真实预览 |
| [component-reuse](skills/component-reuse/SKILL.md) | 组件/API发现、示例预览、源码文件集复制与主题接入 |
| [visual-verification](skills/visual-verification/SKILL.md) | 真实页面、内容/状态/窗口的呈现检查与复验 |
| [codebase-mapping](skills/codebase-mapping/SKILL.md) | 代码业务链、模块、调用/依赖、数据与符号现状地图 |
| [regression-verification](skills/regression-verification/SKILL.md) | 目标失败、旧新对照和测试保护有效性 |
| [defect-diagnosis](skills/defect-diagnosis/SKILL.md) | 最小复现、假设实验、未知根因与修复建议 |
| [acceptance-case-design](skills/acceptance-case-design/SKILL.md) | 文字用例列表、增量维护和覆盖核对 |
| [acceptance-execution](skills/acceptance-execution/SKILL.md) | 界面/API/E2E/交付用例执行、缺陷和复验 |
| [runtime-operations](skills/runtime-operations/SKILL.md) | 环境/配置、启动停止、运行版本与信号诊断 |
| [release-and-recovery](skills/release-and-recovery/SKILL.md) | 分别按授权进行发布、回退/恢复及资源退役 |
| [codex-session-monitor](skills/codex-session-monitor/SKILL.md) | 授权范围内的会话状态跟踪、去重和通知 |

加上流程入口共 17 个 Skill。数量是当前清单结果，不作为未来能力建设目标。独立 Git、文档、派发等操作不强制启动完整研发流程；流程可安排对应职责按需调用 Skill。模型与强度遵循本次用户和宿主设置。

## 安装与使用

```sh
python3 scripts/sync_host_agents.py --write
python3 scripts/sync_host_agents.py --check
python3 scripts/manage_plugin.py install
python3 scripts/manage_plugin.py check
```

新文件先纳入 Git，安装只打包受管理源码；同一命令将六职责注册到 `CODEX_HOME/agents/`（默认 `~/.codex/agents/`），无需另行配置。检查实际启用、缓存/源码指纹、Skill、角色及资源；同名冲突或用户修改会报错并保留内容，不改全局指引。插件页面安装目前没有已核实的自动注册入口；采用上述命令完成注册。原生发现/派发需在新会话核验。Kimi 使用独立安装/重载路径，见[安装指南](docs/plugin.md)。

完整任务使用 `$dev-flow`；直接使用 `$iteration-closeout` 或说“开始收尾”进入[独立收尾 Skill](skills/iteration-closeout/SKILL.md)。主 Agent 盘点已有资料，取得相关专业结论，将有效变化实际写回项目长期文档，记录来源、目标、更新或复用依据与遗留；再按[流程门槛](skills/dev-flow/references/closeout.md)核对 Review、验证、技术收尾、交付和保存。必需回写未完成不能只凭总结或归档结束，已有同范围授权复用。仅文档整理按明确范围裁剪。

直接在线阅读项目文档可使用 [document-management](skills/document-management/references/document-preview.md) 中的脚本，显式传项目根路径；文档与独立原型仍由所属项目维护，预览 URL 依赖实际运行服务。

## 维护与证据

- [本轮设计与归纳图](docs/plans/2026-10-21-agent-skill-reorganization.md)、[迁移清单](docs/plans/2026-10-21-agent-skill-reorganization/migration-plan.md)、[总体进度](docs/plans/2026-10-21-agent-skill-reorganization/Progress.md)。
- [边界评审](reviews/2026-10-21-agent-skill-reorganization-boundaries.md)、[职责建设与验证](docs/agent-development.md)、[文档归类](docs/document-organization.md)、[权威归属](docs/document-ownership.md)。
- [阶段状态核验](skills/dev-flow/references/stage-state.md)：检查声明的版本/候选/依赖，不证明真实执行和专业质量。
- [技术图示规范](agents/references/architecture/technical-diagrams.md)统一选图、边界/箭头语义及图示 Review；[可改写示例](agents/assets/architecture/examples/technical-diagrams.md)。
- [技术基线](agents/references/architecture/technology-stack.md)、[代码规范](agents/references/architecture/code-standards.md)、[UI 基准](agents/references/visual/ui-baseline.md)分别维护唯一专业来源，项目具体版本和例外留项目。

历史版本的职责能力编号和验证记录保留原事实：[旧能力目录](docs/history/2026-10-21-role-capabilities.md)、[评测入口](evals/)。导航可更新到现行源，旧结果不能折算成本轮实现、宿主加载或真实业务项目通过。

解除安装使用 `python3 scripts/manage_plugin.py remove`，同时清理归属明确且未被修改的六角色；其他个人配置、源码和业务项目资产保留。Kimi 使用 `/plugins remove dev-flow`。
