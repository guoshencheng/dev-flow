---

2026-10-09 文档归属调整：视觉维护 UI/组件基准、Ant Design 联用、组件预览与共享 React 工作区，研发协作实现/依赖；新增视觉规格内容协议。目录归属不表示新增真实项目行为已验证，见[职责归属表](document-ownership.md)。

当前接入：通过专业 Skill 承担职责；2026-10-09 已移除 setup，旧 TOML 仅作参考，不参与当前安装。下文历史配置/派发证据保留原验证范围。
id: ROLE-dev-visual
title: 视觉与界面 Agent
status: current
version: 0.1
owner: visual
---

# 视觉与界面 Agent v0.1

更新日期：2026-10-08。原生职责 `dev_visual`；[专业 Skill](../skills/dev-visual/SKILL.md)；[职责配置](../agents/dev_visual.toml)。配置省略模型和推理强度，由用户与宿主选择。

## 已有基础如何复用

产品与视觉共用 Vite/React、Ant Design/shadcn 基准、官方专业能力、组件预览和源码复制。现有组件工程继续位于产品 Skill 的 assets，通过共同协议引用；新的文档预览放在 `dev-flow/assets/document-workspace/`，没有重复建设组件库。

产品维护用户任务、流程、功能使用限制、透出条件、具体逻辑和验收；视觉维护布局、排版、Tokens、组件与状态呈现、响应及实际视觉检查。两者完善同一有效原型，行为与呈现分别写回权威规格。完整 UI 工作通过反馈持续迭代。

## 具体能力

| 能力 | v0.1 指导与项目产物 |
| --- | --- |
| V01 | 视觉方向、品牌/偏好依据、有来源的参考与适用边界 |
| V02 | 可实现的布局、排版、间距、颜色和 Tokens，映射实际主题代码 |
| V03 | 官方/项目组件选择、公开 API/组合、相关状态与实际示例 |
| V04 | 目标窗口、内容长度与数据量变化下的呈现规则和检查 |
| V05 | 有实际触发与退出条件的反馈/动效，保留必要替代 |
| V06 | 与核心任务有关的可读性、焦点/键盘、状态含义和可访问名称 |
| V07 | 有版本、窗口、数据/状态的实际检查、问题和定向复验 |
| V08 | 当前系统、页面、代码映射、归档和影响核验；通用候选经项目验证再回收 |

方法位于 Skill 的四份按需参考。配置存在不表示这些能力在真实项目已成熟；模型执行、原生派发与工具检查分别登记。

## 文档、原型与预览

[共同文档协议](../skills/dev-flow/references/design-document-contract.md)明确产品/视觉目录、规则、原型、证据、当前状态及历史归档。没有既有规范时，本轮规格集中在 `docs/dev-flow/iterations/<迭代ID>/`，产品为 `product/spec.md`、UI 为 `visual/design.md`，原型为 `product/prototypes/<方案>/`；跨迭代设计系统保留在项目长期资产。

产品文档包含原型及使用限制、功能透出、可执行授权、输入校验/计算/动作/保存/输出、异常恢复及 RULE/AC。视觉引用同一功能和规则，记录呈现与实际代码。普通修订由 Git 保存历史，完整已替换方案进入对应职责 archive，索引指向当前资产。

[Vite 文档工程](../skills/dev-flow/assets/document-workspace/README.md)支持 Markdown/MDX/Mermaid、HTML、PDF、图片、Word/表格转换和文本；专用格式有明确原件/导出回退。通过 `preview.mjs url` 核验当前服务和源路径后生成地址，不要求手工记忆端口。详情见[预览协议](../skills/dev-flow/references/document-preview.md)。

## 验证状态与限制

本轮源配置、Skill 方法、目录协议和工具在仓库维护，工具使用隔离虚构项目验证。详细版本、实际检查及范围见[本轮记录](../evals/dev-visual/runs/2026-10-08/visual-and-documents/report.md)。

没有把主 Agent 实施与工具检查登记为 `dev_visual` 原生派发或独立专业行为评测。原生发现/派发、不同模型下的专业行为、新上下文视觉资产复用与真实用户/生产项目仍需实测；产品已有的历史隔离证据保持对应原版本。

后续先在真实 UI 任务按[确认与自主实施协议](../skills/dev-flow/references/execution-contract.md)使用同一规格/原型完成持续交接；[架构首版](architecture-agent.md)已建立，测试验收、研发与[运维交付](operations-agent.md)首版均已建设，下一步真实任务检验全流程。用户确认体验、重要架构取舍与验收预期，AI 复核实现计划并持续修正实现。
