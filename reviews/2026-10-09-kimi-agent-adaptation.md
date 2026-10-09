# Kimi 职责 Agent 适配复核

日期：2026-10-09。范围为用户确认的独立 Kimi Agent 文档与双端同步，方案见 [计划](../docs/plans/2026-10-09-kimi-agent-adaptation.md)。本次由主 Agent 实施和定向自查，未执行独立 AI 实现评审；Kimi 冒烟使用模型替身，不登记为独立专业评审。

## 当前实现

- `kimi.plugin.json` 指定七 Skills 和六个独立 Markdown Agent；Codex 继续通过 Skills 使用职责，不重新引入个人角色注册。
- `scripts/sync_host_agents.py` 从共用 Skill name/description 和插件身份生成 Kimi 清单、Kimi Agent 和历史 Codex TOML 参考。方法只维护于 Skills/参考，双端加载同一份；修改元信息后生成和检查，手工漂移或未知 Kimi Agent 阻断构建。
- Agent 保留宿主基础提示，传入实际 Skill 路径与自包含业务上下文；不猜测固定用户目录或旧缓存。六职责无模型/强度固定值。
- Kimi 类型授权设为空，并显式禁用 Agent/AgentSwarm 工具。测试表明仅配置空 subagents 仍保留工具；修订后原生工具列表无这两项。
- 只读范围是任务约束，不宣称是文件系统沙箱。主 Agent 保留授权确认、共享写入与运行资源、证据核验、用户沟通和最终集成责任。
- 构建前及包内校验同步状态；Codex install/check/remove 的来源保护和用户配置保留语义保持。

## 实际验证与边界

`python3 evals/host-adapters/test_host_adapters.py -v`：六项通过，覆盖元信息/入口/版本漂移、未知入口、包完整性与篡改拒绝、原 Codex 生命周期及用户文件保留。Codex CLI 在该回归中为替身，不冒充真实宿主安装。

`python3 evals/host-adapters/kimi_native_smoke.py .dev-flow/plugin-source`：在 Kimi 2.1.1、隔离数据根和临时业务目录执行；原生安装无 diagnostics，发现七 Skills/六 Agent，六角色依次原生派发、基础提示展开、真实读取包内 Skill/总纲并回收交接。模型接口为本地确定性替身，未读取真实凭据、未调用外部模型；这证明宿主接线，不证明专业判断或完整业务协作。见 [结构化证据](../evals/host-adapters/native-evidence.json)。

本次变更相对开始工作区单独回传，保留开始时已有流程方法修改；工作副本内检查包内相对链接及当前适配差异。源码/包、实际宿主启用与真实业务行为分开记录。

## 主 Agent 实现自查结论

需求符合性：独立 Kimi 文档存在，双端轻量入口可重复生成并阻断漂移，共用方法没有分叉。实现质量：插件路径在受管包内可用，子 Agent 不依赖主会话历史、不带固定模型配置、不继续委派；模型替身/真实宿主/真实业务证据边界明确。当前适配检查无阻断项。真实模型下的职责路由和项目完整循环留待真实任务验证。

## 本机实际安装

隔离回归通过后，将本次入口合并回共享源码；合并时保留工作期间其他任务新增的 README、职责状态与评测记录。Codex 实际执行 `manage_plugin.py install` 和 `check`，七 Skills 已启用且源码/缓存一致。Kimi 通过本机原生插件 API 安装同一构建包，实际启用七 Skills/六 Agent，零 diagnostics，受管副本的包清单与源码构建一致。安装前后核对两宿主个人配置和 AGENTS/SYSTEM 文件指纹，均保持；无原生 Codex 角色注册或全局指引改写。

本机安装记录保存在忽略目录 `.dev-flow/plugin-install.json` 和 `.dev-flow/kimi-plugin-install.json`，仅为当前环境状态。新会话使用对应宿主入口；真实业务职责能力仍以真实任务执行证据判断。
