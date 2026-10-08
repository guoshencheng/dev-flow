# 架构 Agent v0.1 验证记录

日期：2026-10-08。候选基于仓库 `f69fe6b`，对应架构 Skill v0.1、总纲 v0.7、执行协议 v0.2。代表案例与完整原始输入见[案例说明](cases.md)和[虚构项目](fixtures/retrospective/docs/product.md)。本记录区分专业指导、工具检查、原生角色派发和真实项目。

## 结构与接入

主 Agent 实际执行并通过：四个 Skill 的结构校验、三个 TOML 解析/必需字段核对、无职责级模型或推理强度覆盖、临时安装目标/重复执行/原规则备份保留/冲突前置保护、真实全局安装及 `--check`。当前四个 Skill 和三个职责配置链接到本仓库；未修改安装脚本或全局模型设置。来源指纹与结构化检查见[checks.json](checks.json)，引用和格式检查按最后候选登记。

文档预览工具核验存活服务、项目根和源文件后返回 `http://127.0.0.1:49688/view/docs/architecture-agent.md`。这证明地址生成和来源核验，不登记为新 UI 渲染评测。通用文档 Viewer 沿用已有工具证据。

## 独立专业行为：研发复盘

按 skill-creator 的复杂 Skill 行为指导，在隔离临时工程派发通用子 Agent，参数为 `gpt-6.1-sol` / `medium`。评估者读取 dev-architecture Skill、原始代码/产品/设计与真实请求；未提供预期发现、修复答案或主 Agent 结论。此模型参数只属于本次评测，不进入职责配置。

源版本 `734473c138fe669e33d627bfac6472dda6d81e59`。实际成果：

- [当前架构](runs/retrospective/project/docs/dev-flow/architecture/index.md)纠正了原文中未实现的双服务/HTTP/Repository 描述，确认当前单进程内存源码演示；保留已确认目标和未落实约束。
- [模块地图](runs/retrospective/project/docs/dev-flow/architecture/modules.md)把实际目录/符号映射到预约/结算域、层次和分工，列出真实依赖、数据所有权、公开入口及覆盖。
- [代码业务复盘](runs/retrospective/project/docs/dev-flow/architecture/reviews/2026-10-08/cancel.md)发现重复取消登记两笔退款，以及领域写存储和跨域私有存储调用；关联原始 RULE/AC/ARC，给出限定模块范围的修复、收益/代价与复验。区分演示退款数据与真实支付，不扩展到网络服务或整仓重写。
- [改进状态](runs/retrospective/project/docs/dev-flow/architecture/debt.md)保留两项 P1、已纠正文档和可选 P3，未以文档更新关闭代码问题。

评估者实际执行已有测试 2/2 通过、`npm start` 成功；新增七项定向检查中五项通过、两项失败，证明现有测试未覆盖的重复退款和领域 IO 偏差。[检查脚本](runs/retrospective/project/evidence/runtime/cancel-architecture/check.mjs)和[原始结果](runs/retrospective/project/evidence/runtime/cancel-architecture/check-output.txt)可重跑。这里的失败是虚构项目中的预置缺陷被检出，评测目的不是修复该源码。

主 Agent 逐项阅读成果，核对 10 个文件的来源指纹、确认 src/test/package 原样，独立复跑现有测试/启动和定向检查，得到相同两项失败。结果支持 A01/A02/A08，以及本场景相关的 A03/A04；不证明所有语言/规模和其他能力均已成熟。

## 持续复用案例

主 Agent 在原隔离项目新增只读摘要导出能力及装配入口，源版本 `992d110be38c5c8e2ae834bc9561b23111682927`；变更见[evolution.patch](evolution.patch)。同一评估者读取既有资产完成本次复核，实际结果见[当前地图](runs/evolution/project/docs/dev-flow/architecture/modules.md)与[续轮报告](runs/evolution/project/docs/dev-flow/architecture/reviews/2026-10-08/export.md)：

- 更新摘要查询、预约公开边界、报表导出与装配的职责/域/层次，正确区分源码依赖与回调运行方向，保持轻量单体；没有将新目录直接推断为成熟业务域或独立服务。
- 明确本轮重读变化链路，旧模块按指纹与重跑检查复用；原 `734473c` 报告/日志保留原版本，当前 `992d110` 另记来源与覆盖。
- 导出定向检查 5/5 通过，正式测试 2/2 通过、启动新增摘要正确；旧取消检查在新版仍两项失败，P1 保持开放。建议将导出场景与同步摘要/null 契约纳入正式回归，不扩大到无业务依据的异步/网络场景。

主 Agent 核对 14 个文件的来源指纹、当前源码与提交一致、旧报告和原始日志未变，并在持久快照复跑上述检查得到相同结果。续轮验证持续资产复用，不宣称全新上下文；这仍是通用子 Agent 读取 Skill。

## 保存与复跑

长期快照把原临时 `.dev-flow/evidence/` 搬到同层数的 `evidence/runtime/`，改写架构文档中的对应链接/复跑命令；续轮 debt 表格还移除了插入新行前的多余空行，属于展示修复。结论、问题状态、源码与原始日志保持不变。真实项目证据优先遵循专业 Skill 的长期项目位置，此搬移是评测结果归档。原隔离 Git 版本在来源清单保留，快照无需原 `.git/` 即可复跑。

```sh
cd evals/dev-architecture/runs/retrospective/project
npm test
npm start
node evidence/runtime/cancel-architecture/check.mjs
```

最后一条当前预期退出 1，摘要为 7 项、5 通过、2 失败。该结果用于展示缺陷识别，不代表已完成该虚构功能的修复/验收。

续轮快照在 `runs/evolution/project/`，相同命令可复跑既有检查；新增 `node evidence/runtime/export-architecture/check.mjs` 预期退出 0、5/5 通过。

## 未验证范围

未执行 `dev_architecture` 原生角色发现/派发及实际模型继承，没有把普通子 Agent 读 Skill 登记为原生执行。没有真实生产项目、真实支付/持久化/并发/网络权限/性能/部署或 UI 验收证据；A05/A06/A07 的指导仍待相应专业场景实测。新上下文恢复、跨项目复用与整个研发生命周期需要后续真实任务验证。
