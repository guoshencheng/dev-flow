---
title: 安装插件时自动注册六职责原生子 Agent
status: current
updated: 2026-10-23
workflow_version: 1
---

# 原生子 Agent 自动注册 Progress

本文是本轮唯一总体进度，由主 Agent 维护。用户已确认流程并授权设计/计划独立通过后连续实施、验证、升版及安装；本机六角色已注册，原config与AGENTS未改，全部必需验收与交付核验已通过。

## 流程方案与用户确认

- 用户目标：用户提出“能不能改成安装插件时就自动注册这六个原生 subagent，不需要再手动配置？”
- 目标范围：核实 Codex 的插件安装及原生角色发现能力，使受支持安装入口统一完成六职责注册，并处理重复安装、升级、检查和卸载；同步现行文档与安装规则。
- 路径：采用安装契约系统变更路径。没有界面改动，裁剪原型、视觉设计和浏览器页面验收；保留行为约定、统一技术设计、独立 Review、计划复核、实施授权、实现、完整变更 Review、正式用例及验收、版本升级和交付核验。
- 阶段与职责：主 Agent 维护流程及唯一源码写入；研发主责安装实现，架构独立复核设计、计划及完整候选，测试验收核验安装生命周期，运维交付核验实际产物与本机安装。职责按对象执行，不例行启用全部六角色。
- 子 Agent 如需实际派发，采用用户约定的 sol medium；模型选择仅属于本轮执行记录，不固化进专业职责配置。
- 流程确认：已确认。用户原话：“确认，按这个流程推进，设计和计划独立复核通过后直接实现、验证，升级版本并安装。优先保证现有安装命令自动注册六个原生 subagent，同时核实插件页面安装是否支持。”覆盖本文整体路径及本机交付。
- 业务预期与实施授权：复用上述用户明确授权；优先现有安装命令，设计/计划独立复核通过后直接实施、验证、升级和本机安装。新增重要行为取舍才定向确认。
- 起点仓库规则不注册个人Agent；本轮依据用户明确要求同步修改现行规则，安装只管理本插件六个受管角色，保护用户其他配置。

## 目标与当前状态

- 起点：源码提交 `adb8bed`，分支 `codex/agent-template-contract`，插件 0.5.2，总纲 0.32；本轮开始时工作区干净。该分支来自已结束的模板要求迭代，本轮使用独立进度文件；正式修改前按 Git 工作约定确定工作分支。
- 已知现状：`scripts/manage_plugin.py` 具有 build/install/check/remove；install 只安装插件，未注册个人角色。`scripts/sync_host_agents.py` 生成六份 Codex 参考 TOML 和 Kimi 原生入口，职责正文与公共约束已内嵌。
- 当前阶段：全部必需用例及实际交付已独立通过，技术收尾完成，保存本地成果后最后重建核验。已读取总纲、路由、执行协议、进度模板、文档管理、研发/架构职责及对应模板，核对官方能力。工作分支已建立为 `codex/native-subagent-registration`。
- 下一步：完成状态保存为本地提交，最后重建/install/check并执行验收者提供的只读一致性断言；此后不再修改包内内容。用户新会话可使用原生角色。
- 页面调查已完成：未找到已核实的自动注册入口，采用用户指定优先的现有安装命令；不添加 Hooks/setup，不将脚本结果外推页面。当前无待人工决定。

## 总体里程碑

| 阶段 | 状态 | 负责人 | 依赖/进入条件 | 完成条件与成果 |
| --- | --- | --- | --- | --- |
| 必要只读了解与整体流程展示 | 完成 | 主 Agent | 用户本次要求 | 本文及官方、源码现状依据；未实施 |
| 用户流程确认 | 完成 | 用户、主 Agent 记录 | 展示本文与完整路径 | 用户明确确认覆盖范围 |
| 安装行为与宿主能力核实 | 完成 | 研发，架构按影响参与 | 有效流程确认 | 安装入口、角色归属、冲突、更新、失败恢复、卸载及发现边界明确 |
| 统一研发设计与独立 Review | 完成 | 研发主笔，架构独立评审 | 明确业务预期及实际源码 | 中文设计有效、阻断关闭、与原目标一致 |
| 实施计划复核与授权 | 完成 | 研发、独立评审者、用户 | 设计经 Review | 中文计划经独立复核，业务预期与实施范围获得有效确认/授权 |
| 连续实现、集成与自测 | 完成 | 唯一源码写入者 | 有效设计、计划及授权 | 完整生命周期候选、适用自测通过、现行规则与文档同步 |
| 完整变更 Review、正式用例及独立复核 | 完成 | 架构、测试验收与独立评审者 | 固定完整候选 | 完整差异和正式场景均经独立复核，阻断关闭 |
| 隔离验收与版本候选 | 完成 | 测试验收、研发 | 有效候选及用例 | 隔离安装/升级/重复安装/冲突/失败/卸载与用户配置保留验证通过；双端生成一致 |
| 版本升级、实际安装与交付核验 | 完成 | 主 Agent、运维交付 | 完整验证通过，新文件纳入 Git | 按能力新增升级 minor 版本，实际版本 0.6.0；实际 install/check、角色文件与资源一致性核验；原生发现/派发单独记录 |
| 技术收尾、保存与完成说明 | 完成 | 架构、主 Agent | 当前版本必需检查与交付有效 | 更新长期资产与安装指南，保存授权范围成果，说明版本、缓存路径、真实验证与限制 |

## 验证与整体结束条件

- 安装脚本发生变化时必须执行 `python3 -m unittest discover -s tests -p 'test_plugin_installation.py'`，使用隔离目录验证打包、缓存/来源、角色生命周期和用户配置保留。
- 使用 `python3 scripts/sync_host_agents.py --write` / `--check` 同步并核验双端入口、清单及资源；Codex 安装结果不代表 Kimi 已安装。
- 区分文件注册、宿主实际发现、按角色实际派发和专业行为。若需新会话或重启完成发现，记录可执行验证方法和实际结果，不能以文件存在宣称已派发。
- 避免覆盖非本插件所有的用户角色；同名冲突和用户修改的处理方式需在设计中明确，并以实际场景验证。模型与推理强度沿用用户和宿主策略。
- 发布前同步 `plugin.json`、`.codex-plugin/plugin.json`、生成清单及当前版本说明；新文件先纳入 Git，再构建及安装；不得以同一已交付版本覆盖不同内容。
- 交付核对受支持入口能自动完成六职责注册、更新及检查，卸载只清理属于本插件的资源，源码/产物/安装缓存一致；全部必需 Review 和检查有效后才标记整体完成。
- 不自动扩大至 Kimi 原生安装、远程推送、PR、合并或发布。本机实际安装属于拟交付范围，依有效实施授权执行。

## 派发与工作交接

`host_capabilities`（sol medium）已只读完成插件页面支持核实；输入为用户原始目标、基线 adb8bed、实际仓库与官方入口，未修改文件、安装或注册个人角色。通用执行者补充公共约束和架构提示词。主 Agent 已核验调查结果；后续design_review和acceptance分别交接设计/计划/完整候选及正式验收，真实结果见下文与专业记录。

## 有效依据与恢复提示

- 现行安装指南：[docs/plugin.md](../../plugin.md)。
- 现行宿主约束：[host-execution.md](../../../skills/subagent-coordination/references/host-execution.md)。
- 官方自定义角色文档：[Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)：独立 TOML 可位于个人 `~/.codex/agents/` 或项目 `.codex/agents/`。
- 官方插件文档：[Package your plugin](https://developers.openai.com/plugins/build/plugins)：当前说明 Skills、MCP 和 Hooks 等；安装/启用插件不自动信任 Hooks。尚无证据证明现有清单能自动注册包内角色或提供安装事件回调。
- 当前仅新增本文流程草案，不将过去已结束迭代的授权套用于本轮安装契约变化。

## 设计候选与独立核对

[设计 v3](design.md)、[计划 v1](implementation-plan.md)、[独立 Review](review.md)已形成。design_review 首轮发现 DR1–DR3，作者已修订，原评审者已定向复核并通过设计 v3 与计划 v1，DR1–DR3 关闭。host_capabilities 调查已返回并核验：脚本可承接注册，页面自动注册无已核实入口，两个 CLI 版本和原生派发证据边界分别记录。

## 完整候选与自测

- 0.6.0 候选包含注册模块、既有命令编排、三个清单/双端生成入口、现行安装规则与文档。六职责专业正文未改变。
- 主 Agent 自测：15 项 native 行为测试、17 项安装测试通过；双端同步检查与差异格式检查通过。开始基线原有 14 项安装测试也通过，未以环境失败冒充目标失败。
- 旧新对照：相同隔离源码/模拟 CLI 下，adb8bed 旧 install 后角色数为 0，“应有六角色”断言因目标缺失失败；新 install 后角色数为 6 且 check 核验通过。本机原始记录 `.dev-flow/native-registration-baseline.json`，旧 manager 临时副本不纳入 Git。
- 独立工作交接：design_review 收到基线至完整候选全部差异，仅只读审查/隔离检查；acceptance（sol medium）从原目标与设计 AC1–AC7 后置编写正式用例，只返回内容。该阶段主 Agent 为唯一写入者，当时尚未执行真实本机注册；后续实际结果见下一节。

## 最终验收、技术收尾与交付

- 最终自测与独立执行均为17项native、18项安装测试；acceptance另执行11项补充检查、独立旧新对照及构建/页面调查。IR1、VR1、VR2由原评审者定向关闭；无剩余代码或用例阻断。
- 初次实际install/check和独立读回确认0.6.0启用、六角色及64本地资源有效、原config/AGENTS未改。完成报告提炼后再次安装，acceptance独立核验761个受管源码/缓存文件的全部SHA256、六副本/归属及64引用，TC13/16通过。
- 六次真实原生spawn_agent分别显式选择dev_product/dev_visual/dev_architecture/dev_engineering/dev_acceptance/dev_operations，fork_turns=none、sol medium；子任务自动加载职责与0.6.0缓存资源，全部返回正确职责标题及NATIVE_OK。原始raw事件、工具返回和completed状态由acceptance与架构分别独立核对，TC14通过；不外推为全部专业任务质量验证。
- design_review依据当前源码、Review、正式验收及真实交付独立完成技术收尾核对，无新增阻断；acceptance明确全部必需TC可标记通过。现行安装规则、README/概览/职责现状及宿主指南同步0.6.0，模板/总纲0.32与16Skills保持既有机制。
- 交付源码位于本分支最终本地提交。构建目录为仓库`.dev-flow/plugin-source`；实际缓存`/Users/guoshencheng/.codex/plugins/cache/dev-flow-local/dev-flow/0.6.0`；角色`/Users/guoshencheng/.codex/agents/`及归属`/Users/guoshencheng/.codex/dev-flow/native-agents.json`。
- 完成状态保存后最后执行install/check和验收者提供的只读断言，原始结果使用`.dev-flow/native-install-final.json`、`native-check-final.json`、`native-independent-acceptance/real-postcommit-results.json`，以最后保存候选的产物清单为准，不在版本化文档中嵌入自身指纹。
- 当前没有未完成的必需事项；新会话直接发现原生角色，现有会话未刷新可重开。页面安装没有已核实自动注册入口，采用现有命令；Kimi宿主安装、Windows、断电/强杀事务、远端推送/合并/部署未执行且不在本轮范围。
- 正式结论分别见[验收结果](acceptance-result.md)、[交付记录](delivery.md)、[架构技术收尾](architecture-closeout.md)，原始证据保存在本机忽略目录，不提交运行日志。
