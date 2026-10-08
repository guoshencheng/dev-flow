---
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

[共同文档协议](../skills/dev-flow/references/design-document-contract.md)明确产品/视觉目录、规则、原型、证据、当前状态及历史归档。没有既有规范时，产品规格放在 `docs/dev-flow/product/features/<功能ID>/spec.md`，视觉规格在对应 `visual/features/<功能ID>/design.md`，可运行原型在 `design/prototypes/`。

产品文档包含原型及使用限制、功能透出、可执行授权、输入校验/计算/动作/保存/输出、异常恢复及 RULE/AC。视觉引用同一功能和规则，记录呈现与实际代码。普通修订由 Git 保存历史，完整已替换方案进入对应职责 archive，索引指向当前资产。

[Vite 文档工程](../skills/dev-flow/assets/document-workspace/README.md)支持 Markdown/MDX/Mermaid、HTML、PDF、图片、Word/表格转换和文本；专用格式有明确原件/导出回退。通过 `preview.mjs url` 核验当前服务和源路径后生成地址，不要求手工记忆端口。详情见[预览协议](../skills/dev-flow/references/document-preview.md)。

## 验证状态与限制

本轮源配置、Skill 方法、目录协议和工具在仓库维护，工具使用隔离虚构项目验证。详细版本、实际检查及范围见[本轮记录](../evals/dev-visual/runs/2026-10-08/visual-and-documents/report.md)。

没有把主 Agent 实施与工具检查登记为 `dev_visual` 原生派发或独立专业行为评测。原生发现/派发、不同模型下的专业行为、新上下文视觉资产复用与真实用户/生产项目仍需实测；产品已有的历史隔离证据保持对应原版本。

后续先在真实 UI 任务使用同一规格/原型完成产品、视觉、研发和验收交接；下一项职责为测试验收，重点持续对焦和真实端到端交付。
