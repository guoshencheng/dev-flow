# 文档与资产职责归属

日期：2026-10-09。适用范围：本插件的七个 Skills、专业参考、共享资产及维护资料。目录用途遵守[文档归类约定](document-organization.md)，业务项目资料仍保存在所属项目。本表是仓库维护入口，不是业务任务必读资料。

## 如何判断归属

以文档回答的问题、权威产物与主要维护者判断，不能因为多个职责调用就全部放入 `dev-flow`。专业方法由一个主责维护，其他职责直接引用；确有跨职责依赖、确认、交接或共同工具契约时才保留在流程层。共同规则可以简短列出责任与完成条件，不复制专业执行步骤、数值参数或 API。

| 主责 | 应回答的问题与现行入口 | 与其他职责的边界 |
| --- | --- | --- |
| 流程 `dev-flow` | [总纲](../skills/dev-flow/references/constitution.md)、[任务路由](../skills/dev-flow/references/task-routing.md)、[确认/实施协议](../skills/dev-flow/references/execution-contract.md)、[Git/worktree](../skills/dev-flow/references/git-and-worktree.md)、[subagent](../skills/dev-flow/references/subagent-guidance.md)、[执行者说明](../skills/dev-flow/references/codex-agent-configuration.md)：做什么流程、谁在何时参与、依赖/确认/集成与结束 | 路由到专业 Skill，不定义产品规则写法、UI Tokens、架构拆分或具体测试/发布操作 |
| 产品 `dev-product` | [规格内容](../skills/dev-product/references/specification-contract.md)、用户类型/任务、参考研究、流程/状态、业务规则/AC、原型、可用性与下游交接 | 主责行为与交互语义；视觉呈现引用视觉规范，组件工具跨包使用；AC 表达产品预期，TC/运行报告归验收 |
| 视觉 `dev-visual` | [规格内容](../skills/dev-visual/references/specification-contract.md)、方向/参考、设计系统/页面、渲染复核、[UI/组件指南](../skills/dev-visual/references/ui-stack-and-components.md)、[Ant Design 联用](../skills/dev-visual/references/ant-design-capabilities.md)、[组件预览/源码接入](../skills/dev-visual/references/component-preview-and-reuse.md) | 主责呈现、Tokens、组件契约与目录；产品维护任务/规则，架构维护技术基线，研发协作实现/依赖 |
| 架构 `dev-architecture` | 整洁架构、系统/模块地图、设计/契约、技术栈、代码规范、实际代码复盘与演进 | 主责技术边界及合理性；研发技术方案与实施计划归研发，实际测试执行归验收 |
| 研发 `dev-engineering` | 工程基线/计划、技术方案/OUT、切片/集成、前端实现、诊断/修复、兼容变化与可运行交接 | 主责实现及自测，引用产品/UI/架构基线；不从当前实现反推正确预期，不代替测试复验或目标发布核验 |
| 测试验收 `dev-acceptance` | 策略/TC、前端行为、后端/API、真实链路/交付、执行/反馈/复验与回归 | 主责可运行候选验收；设计文档/原型走查由产品/视觉，研发主责修复，运维提供运行环境证据 |
| 运维 `dev-operations` | 环境/启动、产物/发布、观测/事故、恢复/迁移、运行资产/演进/退役 | 主责实际环境及运行结果；Git 集成时序引用共同协议，测试对约定行为作验收结论 |

各职责的 `project-assets*.md` 分别维护自己的长期基线、阶段记录与有效性；共同目录只提供位置、状态与互相关联，专业内容不在流程层再维护一份。四十八项能力及 P/V/A/E/T/O 编号继续由[能力目录](../skills/dev-flow/references/role-capabilities.md)集中索引，它是跨职责能力地图，具体方法仍路由到专业 Skills。

## 共享协议与工具为什么保留

| 对象 | 主责与保留理由 |
| --- | --- |
| [迭代/文档目录、索引、状态与归档](../skills/dev-flow/references/design-document-contract.md)及项目/迭代索引模板 | 流程维护共同位置与交接，不属于单一产品或视觉职责；专业规格细节已提取到产品/视觉 |
| [项目资产持续沉淀](../skills/dev-flow/references/project-asset-maintenance.md) | 流程维护有效性、证据、成熟度与跨迭代复用；各职责维护实际专业资产 |
| [项目文档预览](../skills/dev-flow/references/document-preview.md)与 `dev-flow/assets/document-workspace/` | 所有职责共用同一业务项目阅读入口，覆盖技术、验收和交付；维护者负责通用预览/路径契约，不决定业务规则或视觉方向 |
| [原型指南](../skills/dev-product/references/html-prototyping.md)、HTML 示例及 `prototype.py` | 产品主责原型要验证的任务、状态、讨论与模拟边界，视觉协作呈现，研发协作工程；原型不等于生产实现 |
| [React 组件工作区](../skills/dev-visual/assets/react-workspace/README.md) | 视觉主责组件契约/目录及呈现，研发协作源码/依赖与构建，产品/测试跨包引用；只维护一份源码，不因调用者多而归流程 |
| 技术栈与 UI 基准 | 架构维护工程技术基线，视觉维护设计体系/组件选择；相互引用，新建原型的工程默认可供产品采用，不在总纲复制选型表 |

`assets/` 归属由模板/工具所承载的专业能力确定，不由代码语言判断：产品原型工具仍归产品，共享组件归视觉，共同阅读器归流程。源码移动不要求改变工作区包名、项目运行目录或已有业务项目副本。

## 维护资料与历史证据

`docs/` 保存插件安装、职责建设与现状；`docs/plans/` 保存建设计划；配置历史、工具观察归 `docs/history/`、`docs/integrations/`；实际 Review、行为/工具证据归 `reviews/`、`evals/`。历史源码路径与当时能力结论保留为证据，导航链接可修正到当前文件；不把旧验证描述改成新目录已通过的新验证。

2026-10-09 本轮迁移：两份 UI/Ant Design 参考从流程移入视觉，组件预览指南及 React 工作区从产品移入视觉；产品/视觉规格内容从共同目录协议提取；总纲及入口缩短为共同要求和专业路由。没有迁移业务项目文档，也未改共享组件逻辑。本轮范围与验证见[整理检查记录](../reviews/2026-10-09-document-ownership.md)。

以后新增文档先明确主要问题和主责；混合文档拆分专业方法与共同协议；修改权威位置时同步 Skill、模板、维护入口及入站链接。新增跨职责引用并不改变维护主责。当前未提交/正在建设的其他方法以对应建设任务结果为准，不由本表宣称已完成。
