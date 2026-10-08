# 仓库工作约定

设计文档和实现计划都用中文表述。
subagent 的模型与推理强度遵循用户本次要求和宿主配置。职责配置默认省略模型与强度，避免将某次会话的选择固化为可复用要求。

本仓库维护研发协作总纲、职责 Agent、专业 Skills 和相关安装工具。共同协议的权威位置是 `skills/dev-flow/references/constitution.md`。

按已确定的顺序逐个建设职责，更新对应能力现状与代表案例。当前已有总纲、全局入口、六职责指导及共享文档预览；状态见 `docs/product-agent.md`、`docs/visual-agent.md`、`docs/architecture-agent.md`、`docs/acceptance-agent.md`、`docs/engineering-agent.md`、`docs/operations-agent.md`。工具检查、专业行为、原生派发与真实项目分别登记，项目事实与长期资产保存在各项目中；下一步按真实任务验证完整协作。

安装脚本只管理本仓库的链接和全局指引区块，保留其他设置。修改脚本后在临时目录验证链接目标、重复执行、冲突保护和既有指引保留，再应用到全局。
