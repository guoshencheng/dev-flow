# Codex / Kimi Plugin 安装与维护

当前插件包含一个流程 Skill、六个专业 Skills 和一个跨职责会话监控 Skill，共八个。职责方法通过共用 Skills 提供；Kimi 清单另外声明六个职责 Agent 入口，会话监控不新增 Agent。不需要 setup Agent，也不向个人 Agent 目录写入角色配置或维护全局指引。仓库 `agents/` 的 TOML 由同步脚本生成，仅保留为 Codex 配置参考，不参与当前安装或流程。项目长期资产留在所属项目。

## Codex 安装、更新与检查

在 Git 仓库根目录运行：

```sh
python3 scripts/manage_plugin.py install
python3 scripts/manage_plugin.py check
```

新文件先纳入 Git。install 构建 Git 管理的当前源码，排除依赖缓存、构建产物、本机运行数据与真实环境变量文件；注册本地 marketplace，并通过 Codex 安装/更新插件。它核验安装缓存指纹与八个 Skills，不创建原生 Agent、不写个人 AGENTS.md 或全局 Skill 链接。

本机安装路径保存在源码仓库的 `.dev-flow/plugin-install.json`，只用于只读检查缓存；它不是项目资产或 Agent 初始化状态。`check` 核验实际启用、包内容和源码一致性。能力列表未刷新时在新会话核验发现，必要时重启宿主。

共享文档预览默认不再复制到业务项目。使用已安装 `skills/dev-flow` 目录中的阅读器脚本，并传入项目目录和文档根目录：

```sh
node "$DEV_FLOW_SKILL_DIR/assets/document-workspace/scripts/preview.mjs" \
  serve --project /项目绝对路径 --roots docs/dev-flow,design --port 0
```

脚本首次运行时按锁文件在插件模板目录准备依赖，后续项目共享该依赖；项目只保存文档源文件和 `.dev` 运行记录。需要项目级定制时才使用 `preview.mjs init` 复制兼容工程。

源码远程为 [guoshencheng/dev-flow](https://github.com/guoshencheng/dev-flow)。新环境可克隆后执行上述命令；从其他安装入口使用插件时，按该宿主的安装/更新机制处理，均无需初始化 Agent。当前版本没有 MCP 服务、后台常驻进程或生命周期 Hooks。

## Kimi 安装与双端维护

Kimi 原生清单为包根目录 `kimi.plugin.json`，提供同一套八个 Skills 和 `adapters/kimi/agents/` 的六个 Markdown 职责 Agent。先同步入口，再构建；新文件先纳入 Git：

```sh
python3 scripts/sync_host_agents.py --write
python3 scripts/sync_host_agents.py --check
python3 scripts/manage_plugin.py build
```

在 Kimi 会话中执行（包路径替换为本仓库实际构建结果）：

```text
/plugins install <仓库绝对路径>/.dev-flow/plugin-source
/plugins info dev-flow
/plugins reload
```

新会话使用 `/skill:dev-flow`。专业职责按需派发，输入包含实际安装包 Skill 路径和业务项目上下文，详见 [Kimi 职责说明](integrations/kimi-agent-configuration.md)。本地插件从受管副本运行，修改源文件后重新构建并在 Kimi 重新安装；只改源码不表示缓存已更新。

Kimi 安装/启用/移除使用其原生 `/plugins` 入口，当前 Python install/check/remove 仍专用于 Codex。Kimi 清单不自动加载流程、不配置额外 MCP/Hooks，不写个人 AGENTS.md 或 SYSTEM.md。解除使用 `/plugins remove dev-flow`。

维护专业方法改 Skills/参考；职责名称/说明、插件身份与版本变化后运行同步脚本。生成器统一检查 Kimi 清单与两端职责入口，构建时过期即失败；不手工维护两份专业提示。

## 会话监控 Skill

`skills/codex-session-monitor/SKILL.md` 随插件提供，用于手动检查或在用户授权后跟踪 Codex/ChatGPT 会话的进度、完成、阻塞和待处理事项。它不包含 Lark 凭据、收件人、会话正文或定时器，也不自动创建调度。实例配置可使用本地 `.dev/lark-session-monitor-state.json` 或 Codex Automation；这些内容不进入 Git。发送 Lark 前必须有明确的收件人、发送身份和通知范围授权；会话监控的完成状态不能替代项目架构/测试资产检查或归档协议。

0.1.5 的[富文本进展规范](../skills/codex-session-monitor/references/progress-message-format.md)通过 `--markdown` 发送飞书 `post`：状态分组使用标题，会话原名加粗，四项内容使用列表，用户待办加粗。同一状态只设一个标题，默认按等待你处理、阻塞、执行中、本轮结束、已完成、暂时不可读取排列，空组省略；定期检查没有新增事件时保持安静。

插件更新后，核对已有授权调度的 Skill 引用，避免继续读取历史缓存。优先通过宿主 Skill 发现加载当前启用的 `codex-session-monitor`；实例必须使用绝对路径时，同步为实际安装版本。使用宿主自动化工具更新现有实例，保留频率、收件人、身份、目标会话和通知条件，不将安装操作视为新调度或扩大通知范围的授权。

## 阶段状态核验

Plugin 0.2.0、总纲 v0.25 和执行协议 v0.12 新增[首次实施人工同意](../skills/dev-flow/references/execution-contract.md#首次实施的人工同意)，快速路径也先展示实施摘要并取得同意；已有同一范围明确授权持续有效。核验器要求含正式实现的 scope 关联有效 confirmation，其 `authorizes` 明确覆盖范围。一般设计确认、AI Review、未关联或不适用不能替代开工同意。

这是对旧实施/完成核验条件的不兼容收紧，因此递增 minor。schema 仍为 1，旧记录缺少实施授权会保持未就绪；有真实历史同意时引用其摘要、版本、来源和答复，无需重复询问；没有则保持 pending，禁止倒填授权。只评审/设计等无正式实现范围无需开工同意。完整影响和验证见[调整记录](../reviews/2026-10-12-implementation-authorization.md)。

插件提供[只读核验脚本](../skills/dev-flow/scripts/check_iteration.py)，由主 Agent 按[共同协议](../skills/dev-flow/references/stage-state.md)从已有迭代索引调用。它核验声明的输入版本、确认覆盖、Review 字段、依赖次序、候选及检查/证据观察范围；退出码支持区分通过、未完成和格式错误。需要实际可用的 Python 3.9+，无第三方运行依赖。

这项能力不是自动 Hooks 或 MCP 拦截，不会自行调用、不修改项目、不证明真实执行或语义完整。核验器契约测试、新上下文行为及真实项目验收分别登记，见[验证记录](../evals/dev-flow-stages/report.md)。新文件须纳入 Git 管理后才能随现有 install 打包，安装不改变 Agent 或用户指引。

## 使用与解除

使用 `$dev-flow` 或选择插件，按[任务路由](../skills/dev-flow/references/task-routing.md)处理 bugfix 或正常需求。主 Agent 读取所需专业 Skill；需要且获准委派时，向实际可用子 Agent 提供专业 Skill 路径与明确任务。模型遵循用户及宿主本次约束。

Plugin 0.2.1、总纲 v0.26 明确现有 $dev-flow 的[一条指令收尾](../skills/dev-flow/references/document-archive.md#一条指令收尾当前迭代)入口：`使用 $dev-flow 收尾当前迭代，把文档和长期资产沉淀好。` 正常交付已包含文档收尾；补做时直接同步相关资产、总结、遗留与项目入口并核验归档条件，不重启实施流程。八个 Skills 和状态 schema 保持不变，属于兼容的方法维护，验证见[收尾记录](../reviews/2026-10-12-iteration-closeout.md)。

Plugin 0.2.2、总纲 v0.27 将既有代码/验证/集成方法接入收尾，直接说“开始收尾”默认包含[代码收尾](../skills/dev-flow/references/git-and-worktree.md#代码收尾)和文档沉淀。相关成果无其他约定时形成本地提交，保留无关修改；推送/PR/合并/发布沿用已有授权，仅文档任务裁剪代码动作。八个 Skills、状态 schema 和安装行为不变，属于兼容方法维护；范围和证据见[代码收尾记录](../reviews/2026-10-12-code-closeout.md)。

```sh
python3 scripts/manage_plugin.py remove
```

remove 只解除当前仍属于本仓库构建来源的插件和 marketplace，并删除本地安装路径记录；保留源码、用户配置和业务项目资产。用户在宿主页面关闭或卸载插件无需额外解除 Agent。

## 历史迁移

2026-10-09 按用户要求删除 dev-flow-setup、Agent 注册脚本及旧源码链接安装入口。本机旧 setup 生成的六个原生角色链接/副本和受管状态已核对归属后清理；已有全局 Dev Flow 流程指引保留为用户既有偏好，后续插件安装不改写它。其他机器曾执行过旧 setup 的残留配置需要按实际归属单独清理，新安装不会产生这些配置。

此前八 Skills/原生角色接入的测试是历史版本证据，见[旧安装验证](../reviews/2026-10-09-plugin-installation.md)，不作为当前版本行为说明。
