# Codex / Kimi Plugin 安装与维护

当前源码 0.6.1 提供流程入口、三个公共操作 Skill、十一个专业操作 Skill 和会话监控，共 16 个 Skill；六职责本质工作由生成配置内嵌的提示词承载，维护源位于 agents/prompts。长篇专业参考与写作模板在 agents/references、agents/assets，操作工具与模板随相关 Skill。实际安装与验证状态见[本轮 Progress](plans/2026-10-23-service-architecture-template/Progress.md)。

0.6.1 完善架构文档模板与规范：项目总架构作为跨迭代长期基线，所有迭代架构变化（含重大调整）统一放在研发设计，技术收尾依据实际结果回写总架构并记录前后版本和证据。服务端明确分层图、Service/Usecase 操作清单、具体业务时序和 ER 图，现状地图作为总架构的支撑资料；相关 Review、职责、目录及索引同步。属于文档/方法的兼容维护，递增 patch；总纲 0.32、文档协议 0.15、安装机制不变。

0.6.0 新增 Codex 安装命令自动注册六职责原生子 Agent：install 同时写入受管角色、升级同步正文和资源路径，check 核验全部六份配置，remove 清理受管注册。同名外来角色、用户修改和来源冲突会明确报错并保留内容。属于兼容安装能力新增，递增 minor；总纲仍为 0.32，Kimi 安装机制不变。

0.5.2 在六职责提示词正文中直接明确模板使用要求：编写或实质修订前读取对应模板正文，按其章节和字段组织内容；评审时读取被评对象模板，核对结构、必要内容和重要裁剪依据，将遗漏或无依据的裁剪列为修改项。模板仍独立维护，用户指定格式与项目已有有效模板优先，不为填满模板新增无关成果。研发设计/计划及其架构评审有直接模板入口，两端生成配置同步承载要求。本版是既有模板规则的兼容维护，递增 patch；总纲 0.32、能力声明和安装机制不变。

0.5.1 / 总纲 0.32 是对 0.5.0 既有要求的入口和方法澄清：进度规则、模板、状态核验入口及更新责任集中到 Skill 的“从目标推进到完成”；开始执行 Dev Flow 必须先建流程文档、展示路径并取得用户确认，咨询转设计且没有有效确认时首条进度说明先通知。实际已加载角色正文与公共约束时不重读维护源；未加载才补充，长篇专业 reference/模板按需读取。本版不改变角色注册机制、状态 schema 或核验算法。

0.5.0 / 总纲 0.31 要求每轮迭代单独维护 `Progress.md`，开始前主动展示入口和整体路径，取得用户流程确认后进入后续阶段；流程确认、业务设计确认和实施授权分别记录，可明确合并，已有同范围有效确认复用。索引/原生 Todo 不再替代迭代总体进度，旧活动迭代接续时迁入有效状态，已结束历史不追溯改写。这是 0.x 阶段的流程不兼容收紧，因此递增 minor；schema 1 和只读核验代码保持兼容，不能把核验器通过当作已确认流程。Agent 工作交接负责执行者之间移交上下文与责任，面向用户报告成果称完成说明。

0.4.1 将主干既有技术图示规范并入新职责资源与统一研发设计，保留 0.4.0 的能力边界；主干集成与实际交付见[收尾记录](../reviews/2026-10-22-main-integration.md)。

## 0.4.0 的能力组织与迁移

流程只维护阶段、参与职责、依赖、授权、变更及完成条件；Git、subagent、文档操作独立。旧 dev-product/dev-visual/dev-architecture/dev-engineering/dev-acceptance/dev-operations 六个职责 Skill 退出发现，直接任务按同名职责 Agent 提示词执行，并按需调用操作 Skill。现行调用方引用需更新；历史评测与已经复制到业务项目的源码保留原始事实，不强制改写。

agents/prompts 是专业责任唯一维护源，capabilities.json 声明本包 Skill 与角色路由；生成器组合 common.md 与完整专业提示词，并将链接按各宿主入口位置重新定位。生成物不手工编辑；生成一致性不证明原生发现/派发。资源声明及递归引用由打包检查验证，未声明、缺失或越界不能靠简单数量检查通过。

0.4.x–0.5.x 的 Codex agents/*.toml 只作参考入口；自 0.6.0 起安装命令将其转换为内嵌公共约束与职责正文的受管个人角色。优先使用宿主实际已加载的职责 Agent；使用未加载角色的 Harness 通用子 Agent 时才补充缺失正文，并记录真实方式。Kimi 清单声明六个原生职责入口，实际加载后同样不重读同源正文。没有额外 setup，不维护全局 AGENTS.md，不把 Codex 安装视作 Kimi 已安装。

总纲 0.30 是归属调整，保留 0.29 的有效设计/重要取舍、独立设计/计划 Review、明确范围实施授权、连续实现/自测、完整候选后正式 TC/独立 Review/验收及交付关系；状态 schema 仍为 1。旧记录只按真实来源恢复，不倒填执行，也不重新索取已有同范围授权。

## Codex 安装、更新与检查

在 Git 仓库根目录运行：

```sh
python3 scripts/manage_plugin.py install
python3 scripts/manage_plugin.py check
```

新文件先纳入 Git。install 构建 Git 管理的当前源码，排除依赖缓存、构建产物、本机运行数据与真实环境变量文件；注册本地 marketplace，并通过 Codex 安装/更新插件。核验缓存指纹、实际启用及候选声明的 Skills 后，自动注册 `dev_product`、`dev_visual`、`dev_architecture`、`dev_engineering`、`dev_acceptance`、`dev_operations` 六个原生 Agent。不写个人 AGENTS.md、config.toml 或全局 Skill 链接，不固定模型/推理强度。

角色目录为 `$CODEX_HOME/agents/`，未设置时为 `~/.codex/agents/`。归属与指纹保存在同一 Codex 用户根目录的 `dev-flow/native-agents.json`；`native-agents.lock` 串行化本工具操作，卸载后保留锁文件。仓库 `.dev-flow/plugin-install.json` 保存实际缓存路径。角色正文的本地链接绑定已核验缓存，以百分号编码处理空格/括号等字符。

`check` 同时核验实际启用、包/源码一致性、六角色归属及预期正文；缺失时重新 install 可修复。安装前发现非受管同名文件、其他 TOML 声明同名角色、目标链接或用户修改会停止；请先另存个人修改或移开冲突文件再重试，不会静默覆盖。不能可靠识别外来 TOML 顶层 name 时保守拒绝并指出文件。普通文件提交失败会回滚角色和记录字节；外部 CLI 状态及旧缓存不属于文件事务，失败后修复环境并重新 install，不保证原角色资源仍可运行。突然断电或强制终止不保证多文件原子性。

原生角色发现与文件注册分别核验；能力列表未刷新时在新会话检查，必要时重启宿主。项目级 `.codex/agents/` 可能影响当前项目角色选择，使用实际派发元数据确认角色，不以文件存在代替已加载。注册仅支持本轮已验证的 macOS/Unix Python 3.9+ 环境。

### 插件页面安装的边界

截至 2026-10-23，官方 [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) 将独立角色入口定义在个人/项目 agents 目录；[插件打包文档](https://developers.openai.com/plugins/build/plugins) 没有说明包内 agents 自动注册或安装后回调。Hooks 安装后须用户信任，SessionStart 也不等同安装事件；onboardingSkill 须运行 setup。因此不能保证只在插件页面点击安装就自动注册六角色。本轮通过上述现有 install 命令完成注册，不添加 Hooks 或额外 setup。

页面直接禁用/卸载不会触发本工具的角色清理；受管安装应使用 remove 命令完整移除。页面操作后 check 会报告未启用，重新 install 可恢复。PATH CLI 与桌面捆绑版本可能不同，实际版本及原生演练结果见本轮 Progress。

共享文档预览默认不再复制到业务项目。使用已安装 `skills/document-management` 目录中的阅读器脚本，并传入项目目录和文档根目录：

```sh
node "$DOCUMENT_SKILL_DIR/assets/document-workspace/scripts/preview.mjs" \
  serve --project /项目绝对路径 --roots docs/dev-flow,design --port 0
```

脚本首次运行时按锁文件在插件模板目录准备依赖，后续项目共享该依赖；项目只保存文档源文件和 `.dev` 运行记录。需要项目级定制时才使用 `preview.mjs init` 复制兼容工程。

源码远程为 [guoshencheng/dev-flow](https://github.com/guoshencheng/dev-flow)。新环境克隆后执行上述命令即可安装并注册六职责；其他安装入口仅按其宿主能力加载插件，不推定已完成 Codex 角色注册。当前版本没有 MCP 服务、后台常驻进程或生命周期 Hooks。

## Kimi 安装与双端维护

Kimi 原生清单为包根目录 `kimi.plugin.json`，提供同一套 Skills 和 `adapters/kimi/agents/` 的六个 Markdown 职责 Agent。先同步入口，再构建；新文件先纳入 Git：

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

新会话使用 `/skill:dev-flow`。专业职责按需派发，输入包含实际安装包根路径、所需操作资源与业务项目任务包，实际已加载角色时无需重复传提示词，未加载才补充；详见 [Kimi 职责说明](integrations/kimi-agent-configuration.md)。本地插件从受管副本运行，修改源文件后重新构建并在 Kimi 重新安装；只改源码不表示缓存已更新。

Kimi 安装/启用/移除使用其原生 `/plugins` 入口，当前 Python install/check/remove 仍专用于 Codex。Kimi 清单不自动加载流程、不配置额外 MCP/Hooks，不写个人 AGENTS.md 或 SYSTEM.md。解除使用 `/plugins remove dev-flow`。

维护职责改 agents/prompts，长篇标准/模板改 agents/references 与 agents/assets，操作方法改相应 Skills；能力路由改 capabilities.json。职责、路由、插件身份或版本变化后运行同步脚本。生成器统一检查 Kimi 清单与两端职责入口，构建时过期即失败；不手工维护两份专业提示。

## 会话监控 Skill

`skills/codex-session-monitor/SKILL.md` 随插件提供，用于手动检查或在用户授权后跟踪 Codex/ChatGPT 会话的进度、完成、阻塞和待处理事项。它不包含 Lark 凭据、收件人、会话正文或定时器，也不自动创建调度。实例配置可使用本地 `.dev/lark-session-monitor-state.json` 或 Codex Automation；这些内容不进入 Git。发送 Lark 前必须有明确的收件人、发送身份和通知范围授权；会话监控的完成状态不能替代项目架构/测试资产检查或归档协议。

0.1.5 的[富文本进展规范](../skills/codex-session-monitor/references/progress-message-format.md)通过 `--markdown` 发送飞书 `post`：状态分组使用标题，会话原名加粗，四项内容使用列表，用户待办加粗。同一状态只设一个标题，默认按等待你处理、阻塞、执行中、本轮结束、已完成、暂时不可读取排列，空组省略；定期检查没有新增事件时保持安静。

插件更新后，核对已有授权调度的 Skill 引用，避免继续读取历史缓存。优先通过宿主 Skill 发现加载当前启用的 `codex-session-monitor`；实例必须使用绝对路径时，同步为实际安装版本。使用宿主自动化工具更新现有实例，保留频率、收件人、身份、目标会话和通知条件，不将安装操作视为新调度或扩大通知范围的授权。

## 阶段状态核验

Plugin 0.2.0、总纲 v0.25 和执行协议 v0.12 新增[首次实施人工同意](../skills/dev-flow/references/execution-contract.md#首次实施的人工同意)，快速路径也先展示实施摘要并取得同意；已有同一范围明确授权持续有效。核验器要求含正式实现的 scope 关联有效 confirmation，其 `authorizes` 明确覆盖范围。一般设计确认、AI Review、未关联或不适用不能替代开工同意。

这是对旧实施/完成核验条件的不兼容收紧，因此递增 minor。schema 仍为 1，旧记录缺少实施授权会保持未就绪；有真实历史同意时引用其摘要、版本、来源和答复，无需重复询问；没有则保持 pending，禁止倒填授权。只评审/设计等无正式实现范围无需开工同意。完整影响和验证见[调整记录](../reviews/2026-10-12-implementation-authorization.md)。

插件提供[只读核验脚本](../skills/dev-flow/scripts/check_iteration.py)，由主 Agent 按[共同协议](../skills/dev-flow/references/stage-state.md)从本轮独立 Progress 调用。它核验已声明的输入版本、确认覆盖、Review 字段、依赖次序、候选及检查/证据观察范围；不会自动发现遗漏的流程确认，仍须人工核对真实答复。为读取旧记录/夹具仍接受索引或 JSON 路径，不改变当前 Progress 规则。退出码支持区分通过、未完成和格式错误；需要实际可用的 Python 3.9+，无第三方运行依赖。

这项能力不是自动 Hooks 或 MCP 拦截，不会自行调用、不修改项目、不证明真实执行或语义完整。核验器契约测试、新上下文行为及真实项目验收分别登记，见[验证记录](../evals/dev-flow-stages/report.md)。新文件须纳入 Git 管理后才能随现有 install 打包，安装不改变 Agent 或用户指引。

## 使用与解除

使用 `$dev-flow` 或选择插件，按[任务路由](../skills/dev-flow/references/task-routing.md)处理 bugfix 或正常需求。主 Agent 协调范围、依赖、全局进度和集成；标准跨职责任务默认委派实际可用且允许的 Harness subagent，提供所需操作资源、原要求、有效输入/版本和明确写入边界，仅未加载角色时补充缺失提示词，独立评审与作者分离。模型遵循用户及宿主本次约束。

Plugin 0.2.1、总纲 v0.26 明确现有 $dev-flow 的[一条指令收尾](../skills/dev-flow/references/closeout.md)入口：`使用 $dev-flow 收尾当前迭代，把文档和长期资产沉淀好。` 正常交付已包含文档收尾；补做时直接同步相关资产、总结、遗留与项目入口并核验归档条件，不重启实施流程。候选清单声明的 Skills 和状态 schema 保持不变，属于兼容的方法维护，验证见[收尾记录](../reviews/2026-10-12-iteration-closeout.md)。

Plugin 0.2.2、总纲 v0.27 将既有代码/验证/集成方法接入收尾，直接说“开始收尾”默认包含[代码收尾](../skills/git-workflow/references/git-and-worktree.md#代码收尾与资源交接)和文档沉淀。相关成果无其他约定时形成本地提交，保留无关修改；推送/PR/合并/发布沿用已有授权，仅文档任务裁剪代码动作。候选清单声明的 Skills、状态 schema 和安装行为不变，属于兼容方法维护；范围和证据见[代码收尾记录](../reviews/2026-10-12-code-closeout.md)。

```sh
python3 scripts/manage_plugin.py remove
```

remove 先核对归属与用户修改，再解除当前仍属于本仓库来源的插件和 marketplace，并删除六个受管角色、角色归属记录和本地安装路径记录；保留源码、无关用户配置和业务项目资产。受管角色已被修改时整体拒绝卸载，保留资源供用户另存修改后重试。无归属记录时不删除个人角色。外部 CLI 移除成功后若文件清理失败会明确报错，不声称全部已移除；可重试 remove，或 install 恢复安装。

## 历史迁移

2026-10-09 按用户要求删除 dev-flow-setup、Agent 注册脚本及旧源码链接安装入口。本机旧 setup 生成的六个原生角色链接/副本和受管状态已核对归属后清理；已有全局 Dev Flow 流程指引保留为用户既有偏好，后续插件安装不改写它。其他机器曾执行过旧 setup 的残留配置需要按实际归属单独清理，新安装不会产生这些配置。

此前八 Skills/原生角色接入的测试是历史版本证据，见[旧安装验证](../reviews/2026-10-09-plugin-installation.md)，不作为当前版本行为说明。
