---
title: 〈任务名称〉总体进度
status: active
updated: YYYY-MM-DD
workflow_version: 1
---

# 〈任务名称〉Progress

每轮迭代单独保存为 `docs/dev-flow/iterations/<迭代ID>/Progress.md`；项目已有明确迭代目录时沿用。本文由主 Agent 全局维护，索引、设计、计划和 Todo 只引用或投影它。旧活动迭代的总体状态及结构化块迁入本文，原位置改引用，不改写原证据。按任务裁剪阶段；从起点列到用户最终目标，保留尚未开始的工作。`workflow_version` 仅在整体路径实质变化时递增，`updated` 随实际进展更新。

## 流程方案与用户确认

- 流程版本、目标/范围、路径与裁剪依据：
- 阶段、职责与依赖：见下方总体里程碑。
- 验证、交付形态及整体结束条件：
- 向用户实际展示的本文入口与路径摘要、消息来源：
- 流程确认状态（待确认/已确认/受影响部分待重新确认）、用户原话/来源、覆盖范围：
- 业务确认与实施授权的各自来源/范围（未取得写待确认；明确合并才同时记录）：
- UI 分类与依据（新增/改变方案、恢复已确认设计、用户明确指定调整、已确认规范内实现细节、无 UI；明确自主委托另引来源/边界）：
- 涉及 UI 的有效版本/受影响端与状态、实际展示入口、用户答复及覆盖；复用时引用原确认/指令/委托，缺失写待确认，不以功能授权或 AI 走查替代：

先展示本文链接及整体路径，取得明确流程确认后推进后续阶段；只读了解与本草案可先做。没有答复不视为确认，单纯认可流程不等于业务确认或开工同意；同范围有效确认直接复用。

## 目标与当前状态

- 最终目标、完整交付范围、当前有效基线与来源：
- 整体结束条件：
- 当前阶段及阶段目标：
- 当前动作与执行者：
- 下一步及进入条件：
- 依赖、阻塞、待决与需要用户处理的事项：

## 总体里程碑

| 阶段 | 状态（待开始/待确认/进行中/待核验/受阻/完成/不适用） | 负责人 | 依赖/进入条件 | 完成条件与有效成果入口 |
| --- | --- | --- | --- | --- |
| 整体路径展示与用户流程确认 | 待确认 | 主 Agent 展示，用户决定 | 流程草案 | 用户明确确认及来源 |
| 产品/UI 候选、技术反馈与用户确认 | 待开始 |  | 有效流程确认 | 新/变更 UI 已展示并确认，或有效复用/明确委托依据；无 UI 说明裁剪 |
| 研发设计与跨职责 Review | 待开始 |  |  |  |
| 业务预期确认、实施计划/复核及授权 | 待开始 |  | 有效 UI 确认/复用或裁剪及本次范围授权 | 主 Agent 核对对象版本、覆盖与实际来源 |
| 实现、集成与研发自测 | 待开始 |  |  |  |
| 完整实现 Review、正式用例维护与独立 Review | 待开始 |  |  |  |
| 验收执行与交付核验 | 待开始 |  |  |  |
| 架构技术收尾 | 待开始 |  |  |  |
| 已有资料盘点与项目级长期文档回写 | 待开始 |  |  | 来源、权威入口、实际正文更新或复用依据、未回写项与承接；见下方结果入口 |
| 整体保存、结束与完成说明 | 待开始 |  |  |  |

## 文档盘点与回写结果入口

按 [iteration-closeout](../../../iteration-closeout/SKILL.md)执行，关联已有技术收尾或迭代索引中的实际盘点与回写结果；没有合适记录位置时可在此简述。明确源资料、长期权威目标、实际更新或复用依据、待核验及遗留，不另建平行账本。必需正文同步未完成时保持未完成，不能仅以总结或新增迭代链接关闭。无变化须有核对范围和复用依据；未受影响对象不建空文件。

## 派发与 Agent 工作交接

| 移交对象/交出方 → 接收方 | 输入/候选版本、授权与唯一写入边界 | 接收核对及主 Agent 核验状态 | 结果/未完成、证据与下一项责任 |
| --- | --- | --- | --- |
|  |  |  |  |

工作交接在职责衔接、中断或换执行者时记录；派发成功不等于已核验接续。向用户说明实际成果称“完成说明”，不登记为 Agent 工作交接。

## 有效决定、证据与恢复提示

记录接手必须知道的现行决定、候选版本、Review/验收/交付原始结果链接、失效证据和遗留。历史过程通过 Git 与原始记录追溯；不要在这里复制另一份详细设计或用例。

## 结构化状态（按需采用）

不需要脚本核验时删除本节。需要时仅在本文保留一个块，按实际路径和输入填写；以下是未定路线的待确认占位，不能直接作为已完成记录。`workflow` 的版本对应已展示流程方案，普通进度更新不改变它；实施摘要、设计和候选按实际对象另行登记。完整正式用例在完整候选后维护，此处不预造用例。

```dev-flow-state
{
  "schema_version": 1,
  "candidate": "待形成",
  "scopes": [{
    "id": "scope-1", "route": "undecided", "reason": "", "implementation": true,
    "before_implementation": ["workflow-confirm", "implementation-authorize"],
    "before_finish": ["result-check"]
  }],
  "artifacts": [{
    "id": "workflow", "path": "docs/dev-flow/iterations/iteration-id/Progress.md", "version": "1"
  }],
  "gates": [{
    "id": "workflow-confirm", "kind": "confirmation", "stage": "workflow-confirmation",
    "status": "pending", "inputs": {"workflow": "1"},
    "required_coverage": ["scope-1"], "coverage": [], "after": []
  }, {
    "id": "implementation-authorize", "kind": "confirmation", "stage": "implementation-authorization",
    "status": "pending", "authorizes": ["scope-1"], "inputs": {},
    "required_coverage": ["scope-1"], "coverage": [], "after": ["workflow-confirm"]
  }, {
    "id": "result-check", "kind": "check", "stage": "acceptance", "status": "pending",
    "inputs": {}, "required_coverage": ["scope-1"], "coverage": [], "after": ["implementation-authorize"]
  }],
  "cases": []
}
```

按[状态协议](../../references/stage-state.md)补真实来源、时间和覆盖，确认没有遗漏所需前置。脚本只核验已声明依赖，不自动验证真实答复或实际流程质量。
