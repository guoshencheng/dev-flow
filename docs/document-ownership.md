# 文档与资产职责归属

更新日期：2026-10-28。适用范围：六职责提示词、操作 Skills、专业参考及共享资产；新增技术图示 Skill 仍为[源码候选](plans/2026-10-28-technical-diagrams-skill/Progress.md)。0.7.0 的构建/安装与验证见[独立收尾 Skill 进度](plans/2026-10-26-iteration-closeout-skill/Progress.md)；0.4.0 重组的历史证据保留原事实，不折算本轮验证。

## 唯一权威源

| 内容 | 维护位置 | 边界 |
| --- | --- | --- |
| 路径、阶段、参与职责、依赖、确认/授权、Review、变更、完成和收尾 | [dev-flow](../skills/dev-flow/SKILL.md) | 安排协作和结果要求，不复制工具操作或专业判据 |
| 六职责本质工作、判断与交接责任 | [agents/prompts](../agents/prompts/) | 单独加载可理解责任；生成物不手工维护 |
| 长篇专业标准、评审清单、案例 | [agents/references](../agents/references/) | 各专业唯一维护，跨职责直接引用；不强行为每份文档建 Skill |
| 专业设计/计划/Review/收尾模板与规范配置 | [agents/assets](../agents/assets/) | 由对应职责直接使用；不含业务项目事实 |
| 迭代收尾操作 | [iteration-closeout](../skills/iteration-closeout/SKILL.md) | 盘点已有资料、组织专业核对、实际回写项目长期文档并记录结果；整体完成条件仍归 Dev Flow |
| Git 操作 | [git-workflow](../skills/git-workflow/SKILL.md) | 获取候选、保存、合并与工作区交接；不裁定业务验收 |
| 实际派发与等待 | [subagent-coordination](../skills/subagent-coordination/SKILL.md) | 组装上下文、独立性与资源核验、收集返回；不裁定专业通过 |
| 目录、索引、版本、链接、预览、总结保存及归档 | [document-management](../skills/document-management/SKILL.md) | 接收专业有效结论，不自行决定规则正确性或迭代完成 |
| 专业可复用操作 | [capabilities.json](../capabilities.json) 声明的各 Skill | 明确操作触发与输入输出；不改成另一个完整职责入口 |
| 技术图示操作 | [technical-diagrams](../skills/technical-diagrams/SKILL.md) | 选图、Mermaid、ER 字段关系表达、图示示例与呈现检查；架构专业判断及服务端视图要求保留架构参考 |
| 项目事实及业务决定 | 所属项目的现行权威资产 | 通用提示词、默认规范与项目具体版本分别维护 |

## 共同使用不改变专业主责

技术栈/代码规范归架构，UI 默认与设计系统准则归视觉，业务预期归产品，统一技术设计及实现归研发，正式 TC 与验收结论归测试，实际环境/产物/恢复事实归运维。其他职责引用当前源及版本，不复制成另一份专业规则。

完整变更评审：流程规定时点、对象和独立性；Git 准备基线至完整候选的差异；subagent 协调实际执行者；产品检查业务符合性、架构检查实现质量；研发处理意见；验收复验行为。普通诊断或文档记录不能代替专业裁定和关闭。

## 工具和模板归属

| 资源 | 操作维护方 |
| --- | --- |
| 共享项目阅读器 document-workspace、通用索引模板 | document-management |
| React 多端设计工作台、design-template、旧 HTML 工具 | react-prototyping |
| 组件工作区、catalog、源码文件集和复制工具 | component-reuse |
| 状态核验器、Progress 模板与状态示例 | dev-flow |
| 产品规格、用例、验收报告、交付恢复模板 | 对应专业操作 Skill |
| 架构现状/Review/收尾、研发设计/计划/交接、视觉规格模板 | 对应 agents/assets 职责目录 |

assets 以用途归属，不以代码语言或调用者数量归属。业务项目已复制源码归项目维护，不因插件重组批量改其目录。临时依赖、构建和 .dev 不进入包。

## 声明与生成

[capabilities.json](../capabilities.json) 为本包角色/Skill 路由清单；[同步脚本](../scripts/sync_host_agents.py)从职责源生成 Codex 参考与 Kimi 原生入口。新操作入口及依赖资源随清单和引用核验，不维持旧八 Skill 常量。生成和包校验通过不证明原生宿主加载或专业行为。

0.4.0 重组的逐来源去向见[迁移清单](plans/2026-10-21-agent-skill-reorganization/migration-plan.md)。四十八能力编号的旧集中目录移入[历史快照](history/2026-10-21-role-capabilities.md)；核心专业责任由六提示词承接，历史成熟度不自动提升。
