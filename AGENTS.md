# 仓库工作约定

设计文档和实现计划都用中文表述。
subagent 的模型与推理强度遵循用户本次要求和宿主配置。专业 Skills 不固定模型与强度，避免将某次会话的选择固化为可复用要求。

本仓库维护研发协作总纲、职责 Agent、专业 Skills 和相关安装工具。共同协议的权威位置是 `skills/dev-flow/references/constitution.md`。

按已确定的顺序逐个建设职责，更新对应能力现状与代表案例。当前已有总纲、全局入口、六职责指导及共享文档预览；状态见 `docs/product-agent.md`、`docs/visual-agent.md`、`docs/architecture-agent.md`、`docs/acceptance-agent.md`、`docs/engineering-agent.md`、`docs/operations-agent.md`。工具检查、专业行为、原生派发与真实项目分别登记，项目事实与长期资产保存在各项目中；下一步按真实任务验证完整协作。

安装脚本只管理本插件的构建与宿主插件来源，不注册 Agent 或改写用户指引。修改脚本后在隔离目录验证打包、缓存/来源核验和用户配置保留，再更新已安装插件。

## 文档归类

执行时按需读取的方法、协议和契约放在 `skills/*/references/`；复制到项目的模板、示例与源码放在 `assets/`。本仓库的建设计划放在 `docs/plans/`，职责建设与现状放在 `docs/`，历史配置/接入快照放在 `docs/history/` 或 `docs/integrations/`，审阅与行为证据放在 `reviews/`、`evals/`。混合文档拆分后同步修改引用，业务任务入口不默认路由至规划或历史记录。具体约定见 `docs/document-organization.md`。
