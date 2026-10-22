# Agent / Skill 重组主干集成收尾

日期：2026-10-22。用户明确要求“收尾一下，并合并主干、推送到远端”。输入为重组候选 `46db236` 和已 fetch 的 `origin/main` `a90ba56`；工作区开始时干净。此前完整重组的独立 Review、正式验收与 Codex 0.4.0 交付见[原验收记录](../docs/plans/2026-10-21-agent-skill-reorganization/verification.md)。本文仅记录后续集成变化，不改写原结果。

## 组合候选与冲突处理

主干的 `a25ad16`、`a90ba56` 增加技术图示规范及其收尾证据；当前分支同时包含尚未入主干的研发流程调整与 Agent/Skill 重组。集成保留双方成果：六个旧职责 Skill 继续退役，图示规范迁至 `agents/references/architecture/technical-diagrams.md`，六类示例迁至 `agents/assets/architecture/examples/technical-diagrams.md`。架构/研发提示词承接专业判据，研发统一设计参考、统一模板、架构模板、代码地图和文档协议引用同一规范。

README 保留新能力组织并增加图示规范入口；自动合并留下的旧相对链接逐项修正。`capabilities.json` 增加示例的精确必需资源，当前 16 个 Skill、六职责及 139 项必需资源；宿主入口重新同源生成。版本按兼容文档/方法维护升至 **0.4.1**，总纲协议仍为 **0.30**。

## 实际验证与交付边界

- `python3 -m unittest discover -s tests`：58 项通过，含 14 项安装隔离回归和 44 项阶段回归。
- 原型脚手架测试：5 项通过；文档阅读器 `npm run check`：3 项通过。
- `sync_host_agents.py --check`：六职责、16 Skill、两个宿主入口同步；暂存差异检查无空白错误、无未解决冲突。变化 Markdown 的实际链接逐项核对。
- 浏览器从新路径打开六类图示示例：总览、模块、时序、流程、状态与 ER 均生成 SVG，无 Parse error；页面正文和首图实际可读。图示源码沿用主干内容，仅调整引用路径；不将示例当作生产系统事实。

独立架构执行者（sol medium，未主笔本次冲突处理）对照 `a25ad16` 和本次完整暂存候选，结论为需求符合性通过、文档实现质量通过，无阻断项。规范与六类示例正文完整保留，仅各一条链接适配迁移；旧入口未复活，195 条本地 Markdown 相对文件引用缺失为 0，三份版本清单及 139 项资源同步。检查仅覆盖静态集成，运行测试由主 Agent 实际执行；历史图示 Review 的旧路径叙述与旧测试数量保留当时事实。独立技术收尾确认可进入提交和集成交付，实际安装与推送另行核验。

最终提交后按本仓库流程安装 Codex 0.4.1 并执行 `manage_plugin.py check`，产物在 `.dev-flow/plugin-source/`，缓存为 `/Users/guoshencheng/.codex/plugins/cache/dev-flow-local/dev-flow/0.4.1`；实际候选、指纹和远端推送结果以本次交接及忽略的安装记录为准。主干与远端确认成功后再声明集成完成，不从静态版本号推定交付。

Kimi 原生更新仍按用户既有选择延期；本轮只同步生成入口。文档 Web 预览继续保留在原端口 49947。旧 Skill 本地残余及个人重复监控入口已移出发现目录，保留恢复备份，监控自动化仅迁移 Skill 引用并保持暂停；这些本机状态不打入插件包。
