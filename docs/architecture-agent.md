---

当前接入：通过专业 Skill 承担职责；2026-10-09 已移除 setup，旧 TOML 仅作参考，不参与当前安装。下文历史配置/派发证据保留原验证范围。
id: ROLE-dev-architecture
title: 架构设计与演进 Agent
status: current
version: 0.3
owner: architecture
---

# 架构设计与演进 Agent v0.3

更新日期：2026-10-08。原生职责 `dev_architecture`；[专业 Skill](../skills/dev-architecture/SKILL.md)；[职责配置](../agents/dev_architecture.toml)。配置省略模型与推理强度，由本次用户和宿主设置选择。

## 当前做什么

以整洁架构为基础，先按业务能力细分域、用例、模块职责、公开契约和数据所有权，再说明策略/机制层次与真实目录。业务域、架构层、模块、目录和运行服务分别映射；不靠目录名或层数判断合规。源码依赖朝向业务策略，React/antd、HTTP/ORM 和 SDK 通过外层适配。

架构同时参与设计、实现计划 AI 复核、相关实施变化、交付符合性核验和研发结束后的代码业务复盘。用户确认重要架构选择及测试预期，实现计划由 AI 复核后自主实施，继续遵守[执行协议](../skills/dev-flow/references/execution-contract.md)。

v0.3 按用户要求收敛技术 Guide：Web 使用 React（新建 Vite + React + TS），全栈使用 Next.js，纯静态使用 Astro；其他类型暂不建设通用技术 Guide，历史调查保留为资料。已定选择直接沿用，并新增 EditorConfig/Prettier、ESLint、类型与依赖规则的[代码规范](../skills/dev-architecture/references/code-standards.md)及可复制格式配置。

研发前按[架构基线表](../skills/dev-architecture/references/design-and-contracts.md#研发前应明确的架构基线)确定本次模块/依赖、接口/数据、权限/失败恢复、质量、运行交付和维护事项。已有有效决定直接复用，具体规范由工具执行，不增加人工计划审批。

## 具体能力与产物

| 能力 | 当前指导与项目产物 |
| --- | --- |
| A01 系统理解 | 从真实入口追踪业务、数据与运行组成，输出有源码依据和覆盖边界的系统地图 |
| A02 模块划分 | 细化业务域/层次、目录映射、分工与不负责事项、允许依赖、数据所有权及公开契约；结合代码规范检查真实边界 |
| A03 接口契约 | 用例/API/事件、错误、兼容与必要幂等语义，关联权威接口定义和消费方 |
| A04 数据与不变量 | 数据语义、状态/规则、读写责任、事务/并发与适用迁移，关联真实验证 |
| A05 技术与质量取舍 | 复用已定技术约定，核对规范、入口、代码工具链与交付并维护基线；根据实际目标确定性能/可靠性/容量/成本假设和测量证据 |
| A06 信任与权限 | 身份/租户、数据访问、可信执行边界和对应正向/拒绝检查 |
| A07 演进与恢复 | 分阶段变化、兼容期、数据检查、切换/恢复条件，避免将代码回滚当成数据恢复 |
| A08 复盘与维护 | 研发后的实际代码业务 Review、架构合理性评价、现状/模块地图更新与有证据的改动建议 |

首版重点 A01/A02/A03/A08，涉及数据时同时落实 A04；当前 A05 保留三类技术约定和持续基线，代码规范支撑 A02/A05。指导覆盖与实际验证分开，配置存在不表示全部能力已经成熟。

## 专业内容如何拆分

- [整洁架构](../skills/dev-architecture/references/clean-architecture.md)：领域、应用、适配、基础设施和装配的职责，跨域边界、React/后端/CLI/库、轻量和遗留工程。
- [系统与模块地图](../skills/dev-architecture/references/system-and-module-map.md)：从业务链路读真实代码，目录 ↔ 模块 ↔ 域/层次，实际依赖、合理性和证据覆盖。
- [设计与契约](../skills/dev-architecture/references/design-and-contracts.md)：重要选择、可执行 ARC 约束、接口/数据/权限/运行，以及 AI 计划复核和研发测试对焦。
- [复盘与演进](../skills/dev-architecture/references/retrospective-and-evolution.md)：参与时机、代码业务 Review、优先级、具体建议与改进关闭。
- [项目资产](../skills/dev-architecture/references/project-assets.md)：现状、目标、决策、复盘、债务的目录和归档、版本核验及下一任务复用。
- [技术栈约定](../skills/dev-architecture/references/technology-stack.md)：React Web、Next.js 全栈、Astro 纯静态的已定选择及项目有效基线。
- [代码规范](../skills/dev-architecture/references/code-standards.md)：成熟格式/lint/类型方案、命名与依赖、配置源码复用、研发/CI 检查和项目规范维护。

## 研发结束后如何参与

实质研发完成后，基于最终候选、有效设计和验收证据复核相关代码业务，更新当前系统和模块分工，评价依赖、数据与业务规则的合理性。首次接入、跨域变化、迁移和重复缺陷扩大到相应影响；局部修复定向核验，无变化时记录复用。交付前必需约束与复盘可合并检查。

每条建议给出代码/运行证据、业务影响、优先级、具体模块/目录/契约改动、收益与代价、实施依赖及验证/恢复方式。当前事实、有效目标、偏差和待验证风险分别记录。违反本次必需条件的问题回到修复循环；可选演进入待办。仅 Review 时不自动修改生产代码。

“实时总结”采用变更触发的持续更新：相关规则、模块、接口、数据或运行变化后重核受影响资产，并在交付复盘写回当前版本；此首版没有独立后台监听器。

## 项目文档与共享

优先沿用项目权威目录，无规范时使用 `docs/dev-flow/architecture/`：index/system/modules 保存当前事实，stack 保存技术/工具链和交付基线，changes 保存目标设计和确认，decisions 保存重要取舍，reviews 保存实际代码复盘，debt 关联改进。代码规范使用 `docs/dev-flow/engineering/code-standards.md` 并链接实际配置与命令。小工程允许合并，复杂业务域按需拆分。普通历史由 Git 保存，完整替换方案按协议归档。

随包提供[当前地图](../skills/dev-architecture/assets/templates/current-architecture.md)、[技术基线](../skills/dev-architecture/assets/templates/technology-baseline.md)、[变化设计](../skills/dev-architecture/assets/templates/architecture-design.md)、[代码复盘](../skills/dev-architecture/assets/templates/architecture-review.md)四个模板，复用共享 Vite 文档预览。项目事实留在项目，经过验证的通用方法再沉淀到本 Skill。

## 验证状态

源配置、专业指导、项目资产和代表案例分别登记；本次检查与限制见[验证记录](../evals/dev-architecture/report.md)。原生发现/派发、不同模型和真实项目复用需要对应实际证据，隔离评测不能代替生产验收。

v0.1 的四个 Skill、三个 TOML 与全局链接检查通过。Sol medium 通用子 Agent 在隔离案例实际完成代码业务复盘和模块变化后的资产复用，主 Agent 核验源码/证据并复跑一致。已证明该案例中的现状恢复、域/模块地图、业务/架构偏差识别和持续更新；尚未验证 `dev_architecture` 原生派发、全新上下文与真实项目，也未将全部能力登记为成熟。

v0.2 技术选型新增指导基于只读项目调查与官方平台资料，结构、引用、职责配置和全局链接的实际检查见[本轮记录](../reviews/2026-10-08-architecture-stack-check.md)。现有隔离案例不证明新增选型能力；尚未实际运行样本项目或验证新项目采用和端到端交付。

v0.3 技术约定、代码规范与格式配置的检查见[本轮记录](../reviews/2026-10-08-architecture-code-standards-check.md)。格式工具的实际案例与其他静态/行为/真实项目检查分别登记，不将格式通过延伸为端到端验收。

已建设[测试验收职责](acceptance-agent.md)，与架构使用同一 ARC/RULE/AC 和版本化证据推进完整交付。已建设[研发职责](engineering-agent.md)与[运维交付职责](operations-agent.md)，以实际实现/环境同步运行边界和恢复条件；下一步用真实任务检验完整协作。

## Kimi 宿主接入（2026-10-09）

本职责已提供独立 Kimi Markdown Agent 入口，与 Codex 角色参考从共用 Skill 元信息生成；专业方法仍只在 Skill/参考维护。Kimi 2.1.1 已通过原生发现、派发、包内文件读取和交接的模型替身冒烟；真实模型的专业行为及项目结果尚未验证，不能将接入检查登记为专业验收。见 [适配记录](../reviews/2026-10-09-kimi-agent-adaptation.md)及 [执行说明](../skills/dev-flow/references/kimi-agent-configuration.md)。
