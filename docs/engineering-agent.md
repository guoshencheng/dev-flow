---

当前接入：通过专业 Skill 承担职责；2026-10-09 已移除 setup，旧 TOML 仅作参考，不参与当前安装。下文历史配置/派发证据保留原验证范围。
id: ROLE-dev-engineering
title: 研发实现与修复 Agent
status: current
version: 0.2
owner: engineering
---

# 研发 Agent v0.2

更新日期：2026-10-08。原生职责 `dev_engineering`，配置见[dev_engineering.toml](../agents/dev_engineering.toml)，专业入口为[dev-engineering](../skills/dev-engineering/SKILL.md)。不固定模型/强度，宿主不可派发时当前执行者按 Skill 承担职责并如实记录。

## 从有效设计到可运行成果

研发先读取有效产品/交互/UI、架构与工程入口，在架构设计/重要确认后形成端到端技术实现方案：拟交付的页面/入口、功能、OUT/链路、接口/模块/数据/权限/恢复及实际交付产出。产品复核需求符合性，视觉/架构按影响参与 AI Review；通过后交测试综合原产品设计用例。

用例 AI Review/人工确认后，研发关联方案/OUT 与 TC 产出实施计划并实际 AI 复核，通过后自主编码；技术方案和计划不另加人工审批。已有有效 Review/确认复用，局部任务按变化裁剪，重要假设失效定向重审，改变确认基线只请求受影响部分决定。

以用户/接口行为形成纵向可运行切片，按整洁架构落实域、用例和适配职责，实际集成界面、接口与数据。测试带候选和证据反馈，研发复现/诊断/修复、自测原问题及相关回归并交回待验版本，测试实际复验后关闭。自测、兼任执行与独立验收分别登记。

工程采用已定 React Web、Next.js 全栈、Astro 纯静态，既有工程局部工作沿用有效基线。B 端优先 antd，C Web 优先 shadcn/ui；自有共享组件复制/参考源码，在项目直接维护 Git 来源、差异与验证。代码规范、类型/行为/集成/构建和启动按实际工程入口落实。

## 八项能力如何落实

| 能力 | 具体判断与项目产物 | 验证方式 |
| --- | --- | --- |
| E01 工程理解 | 真实入口、代码功能映射、依赖/消费者、有效规范和候选 | 对照实际源码与命令，识别过期资产和他人修改 |
| E02 方案、计划与切片 | 架构后端到端技术方案/OUT/符合性 Review；用例确认后切片/依赖/实施计划/AI 复核 | 方案忠于产品/UI/ARC，TC 与 OUT/原规则关联，实施计划覆盖完整链路及交付 |
| E03 前端实现 | 组件、真实数据、状态/恢复、设计和规则映射 | 实际操作及相关渲染/目标设备符合基线 |
| E04 业务与接口 | 用例、输入/权限/错误、持久化与适用副作用 | 真实接口/数据结果、拒绝场景和相关不变量 |
| E05 诊断修复 | 最小复现、原因证据、实现补丁与待验候选 | 原场景与受影响回归，不能放宽验收关闭 |
| E06 兼容演进 | 重构/升级/迁移的消费者、阶段与恢复安排 | 原行为或已确认新契约成立，集成重新取证 |
| E07 工程工具 | 适用自动化、格式/lint/类型、行为与构建入口 | 实际执行并证明目标，不以实现镜像测试代替 |
| E08 集成交付 | 集成版本/锁文件、配置样例、真实运行支持和交接 | 声明环境按说明准备/启动并完成核心任务 |

专业方法分为[技术方案与符合性 Review](../skills/dev-engineering/references/technical-delivery-design.md)、[基线与计划](../skills/dev-engineering/references/baseline-and-plan.md)、[切片与集成](../skills/dev-engineering/references/slices-and-integration.md)、[前端](../skills/dev-engineering/references/frontend-implementation.md)、[诊断与反馈](../skills/dev-engineering/references/diagnosis-and-feedback.md)、[兼容变更](../skills/dev-engineering/references/compatible-changes.md)、[工程资产与交付](../skills/dev-engineering/references/project-assets-and-delivery.md)，入口按需读取。

## 职责边界与项目持续维护

研发拥有生产实现和必要工程/测试工具修改，保留他人工作。产品/视觉拥有有效语义与呈现，架构拥有边界/契约与重要取舍，测试拥有实际验收和缺陷复验，运维拥有目标环境/运行。研发可以调整内部实现和测试执行方法，不能将实现偏差改写为产品预期或更换 Mock 掩盖失败。

已有工程规范优先，没有时使用 `docs/dev-flow/engineering/index.md`、`changes/<任务ID>/technical-solution.md`、`plans/<任务ID>.md` 与按需待验交接，复杂诊断关联既有缺陷记录。四个随包模板对应入口、技术方案/符合性 Review、计划/AI 复核及交接；自动化和实现保留实际源码位置。技术方案方法见[专业参考](../skills/dev-engineering/references/technical-delivery-design.md)。

项目索引关联工程、产品/UI、架构、测试及运行；每轮更新受影响技术方案/OUT/Review、代码映射、规范、计划、诊断/回归和交付知识，新任务读取并核验有效性。讨论/确认预览业务项目成果，Skill 方法文件使用源文件。研发结束向架构交接实际模块/契约/业务变化与证据，参与现状同步和有范围的复盘。

## 验证与后续

首版方法、配置、全局接入和隔离诊断修复记录见[验证记录](../evals/dev-engineering/report.md)。主 Agent 自查/自执行案例不代表独立角色行为；原生发现/派发、框架工程、真实项目协作和新上下文复用需要对应实测。

v0.2 增加架构后技术方案和产品符合性 Review、给测试的 OUT/链路映射；本次内容/协议检查与主 Agent 推演见[调整记录](../reviews/2026-10-08-technical-delivery-stage.md)。历史修复案例不证明新增阶段已在真实项目执行。

已建设[运维与交付职责](operations-agent.md)，研发移交实际工程候选、配置/产物与诊断入口，运维维护目标环境和运行证据。下一步用真实任务验证完整协作，再按重复操作与实际失败建设运行内核和 Plugin。

## Kimi 宿主接入（2026-10-09）

本职责已提供独立 Kimi Markdown Agent 入口，与 Codex 角色参考从共用 Skill 元信息生成；专业方法仍只在 Skill/参考维护。Kimi 2.1.1 已通过原生发现、派发、包内文件读取和交接的模型替身冒烟；真实模型的专业行为及项目结果尚未验证，不能将接入检查登记为专业验收。见 [适配记录](../reviews/2026-10-09-kimi-agent-adaptation.md)及 [执行说明](../skills/dev-flow/references/kimi-agent-configuration.md)。
