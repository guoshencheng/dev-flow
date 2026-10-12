# 仓库工作约定

设计文档和实现计划都用中文表述。
subagent 的模型与推理强度遵循用户本次要求和宿主配置。专业 Skills 不固定模型与强度，避免将某次会话的选择固化为可复用要求。

本仓库维护研发协作总纲、职责 Agent、专业 Skills 和相关安装工具。共同协议的权威位置是 `skills/dev-flow/references/constitution.md`。

按已确定的顺序逐个建设职责，更新对应能力现状与代表案例。当前已有总纲、全局入口、六职责指导及共享文档预览；状态见 `docs/product-agent.md`、`docs/visual-agent.md`、`docs/architecture-agent.md`、`docs/acceptance-agent.md`、`docs/engineering-agent.md`、`docs/operations-agent.md`。工具检查、专业行为、原生派发与真实项目分别登记，项目事实与长期资产保存在各项目中；下一步按真实任务验证完整协作。

安装脚本只管理本插件的构建与宿主插件来源，不注册 Agent 或改写用户指引。修改脚本后在隔离目录验证打包、缓存/来源核验和用户配置保留，再更新已安装插件。

## 插件迭代与版本升级

后续每次将迭代成果安装或分发到宿主前，必须配合插件版本升级；不得长期覆盖同一版本缓存来交付不同内容。内部草稿可先验证，发布候选确定后再升级版本。

1. 完成相关 Skills、参考、工具与文档修改，核对已有改动和交付范围，并执行对应验证。
2. 按语义化版本升级：兼容修复和文档/方法维护递增 patch，兼容能力新增递增 minor，不兼容变化递增 major；在 0.x 阶段不兼容变化递增 minor，并说明影响。同步修改 `plugin.json` 与 `.codex-plugin/plugin.json` 的版本，运行 `python3 scripts/sync_host_agents.py --write` 生成 Kimi 清单和职责入口，再运行 `--check`；同步 README 等当前版本说明。插件版本与总纲协议版本分别维护。
3. 新文件先纳入 Git 管理，再验证候选。安装脚本变更必须运行 `python3 -m unittest discover -s tests -p 'test_plugin_installation.py'`，在隔离目录覆盖打包、缓存/来源检查和用户配置保留；其他变化执行相关检查。
4. 在本仓库执行 `python3 scripts/manage_plugin.py install`，随后执行 `python3 scripts/manage_plugin.py check`，核对实际启用、安装缓存版本、八个 Skills 及源码指纹一致。Kimi 按 `docs/plugin.md` 的原生安装/重载流程单独处理，不将 Codex 安装结果视为 Kimi 已更新。
5. 交接记录版本、源码候选、产物/缓存位置和验证结果；安装后若再改包内文件，应重新验证、构建和安装，已交付版本的下一次迭代使用新版本。能力发现刷新在新会话核验，必要时重启宿主。

安装只管理本插件来源与产物，不注册个人 Agent、不改写全局用户指引。详细安装命令与限制以 `docs/plugin.md` 为准。

## 文档归类

执行时按需读取的方法、协议和契约放在 `skills/*/references/`；复制到项目的模板、示例与源码放在 `assets/`。本仓库的建设计划放在 `docs/plans/`，职责建设与现状放在 `docs/`，历史配置/接入快照放在 `docs/history/` 或 `docs/integrations/`，审阅与行为证据放在 `reviews/`、`evals/`。混合文档拆分后同步修改引用，业务任务入口不默认路由至规划或历史记录。具体约定见 `docs/document-organization.md`。
