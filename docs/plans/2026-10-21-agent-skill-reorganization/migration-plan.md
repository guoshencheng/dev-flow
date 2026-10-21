# 迁移清单与实施安排

日期：2026-10-21。状态：已按清单形成迁移候选，验收与安装见 Progress.md。上级：[重组规划](../2026-10-21-agent-skill-reorganization.md)。

## 本轮范围与状态

本轮工作是落实边界评审、形成具体目标目录、迁移清单和后续实施安排。规划时基线为0.3.0；用户随后明确“好，那按照这个实施吧”，现已形成迁移与生成器候选。实际版本、验收和安装状态见[总体进度](Progress.md)。

| 阶段 | 状态 | 完成条件 |
| --- | --- | --- |
| 现状与边界收敛 | 已整理，见独立边界评审 | 四类内容及跨层调用有明确判定 |
| 目标结构和迁移安排 | 已整理，待实施中核验 | 57 份参考、8 个入口与已跟踪资产均有去向 |
| 插件源码迁移与生成器适配 | 已集成候选，独立Review与验收中 | 权威源切换、入站引用、生成和打包一致 |
| 行为验证与独立复核 | 未开始 | 角色、操作和完整流程代表案例有真实证据 |
| 升版、安装与宿主发现 | 未开始 | 最终候选升级版本，分别核验 Codex/Kimi 实际支持能力 |

## 目标目录与权威源

```text
agents/
  prompts/                    # 六职责核心责任 + common.md，共同约束由生成器组合
  references/<role>/          # 长篇专业规范、评审清单、案例；不必都包装成 Skill
  assets/<role>/              # 直接由职责使用的设计、计划、Review、收尾模板与配置
  dev_*.toml                  # 生成的 Codex 参考入口，保持现有“不自动注册”事实
adapters/kimi/agents/          # 从同一提示词源生成的原生入口
skills/
  dev-flow/                   # 唯一流程协议和阶段核验器
  git-workflow/
  subagent-coordination/
  document-management/
  product-specification/
  react-prototyping/
  component-reuse/
  visual-verification/
  codebase-mapping/
  regression-verification/
  defect-diagnosis/
  acceptance-case-design/
  acceptance-execution/
  runtime-operations/
  release-and-recovery/
  codex-session-monitor/
```

拟定结构共 16 个 Skill（1 流程 + 3 公共 + 11 专业操作 + 1 监控），是当前设计结果而非必须达到的数量。专业参考不是第五种 Agent，也不是绕过技能发现的隐藏入口：提示词负责其按需路由，生成物和安装包必须携带并能定位这些参考。角色名继续采用六职责现有名称。

不默认让每个 Skill 依赖 dev-flow，也不要求 Agent 执行局部任务时加载完整总纲。Skill 使用通用默认值时引用已安装包中真实可定位的唯一源，独立拷贝 Skill 时须连同必需资源处理，不能引用开发者机器路径。

## 三个公共 Skill 的可观察契约

| Skill | 典型输入 | 具体输出 | 与邻接能力的分界 |
| --- | --- | --- | --- |
| git-workflow | 仓库/工作目录、目标操作、任务基线、相关修改范围、已有授权 | 实际分支/worktree/候选差异/提交或 PR 状态，残留修改与资源交接 | 不要求无关的业务验收；不凭“功能完成”推导外部写入授权 |
| subagent-coordination | 所需职责与任务、输入版本、写入范围、独立性条件、宿主/模型约束 | 实际执行者和任务包、等待状态、返回结果、独立性/资源缺口 | 只收集和核对执行信息；专业正确性由职责判定；代码合并交 Git |
| document-management | 项目权威索引、有效专业结论、需组织的文档/模板/源码引用 | 文件/索引/版本/链接更新、真实预览地址、历史替代和归档记录 | 不自行认定业务规则或技术现状有效，不决定整体结束 |

## 十一个专业操作的触发与产出

| Skill | 何时使用 / 输入 | 输出与相邻边界 |
| --- | --- | --- |
| product-specification | 需要将任务、决定、规则整理为可执行规格；输入用户任务、有效规则及未决问题 | 流程、状态表、RULE/AC 和规格；未知保持待决，不承担用户价值取舍或正式 TC 设计 |
| react-prototyping | 需要构建/修改/启动设计原型；输入有效设计、现有工程和目标场景 | 可运行原型、源码及真实入口、模拟边界；不负责确认体验或生产验收 |
| component-reuse | 需要查选、预览或接入组件/主题；输入需求约束、现有栈和组件目录 | 候选 API/示例、复制文件集、主题接入和来源差异；不设计完整视觉体系 |
| visual-verification | 需要核验当前页面呈现；输入候选、有效规格、窗口/内容/状态 | 可复现的呈现问题和复验记录；不代替产品流程走查或业务 E2E |
| codebase-mapping | 需要理解实际代码业务链或更新地图；输入仓库、范围、真实入口 | 路径/符号支持的模块/调用/数据地图与未解析项；架构合理性由架构角色判断 |
| regression-verification | 需要证明测试能捕获目标变化；输入预期、旧新候选、最小场景 | 目标失败/通过、有效回归和证据边界；不承包整轮实现，不要求低影响改动机械先失败 |
| defect-diagnosis | 需要定位可重复问题；输入现象、候选、环境及预期来源 | 最小复现、假设实验、根因与修复建议；正式 Review 裁定不等于诊断 |
| acceptance-case-design | 需要从有效规则设计或修订正式测试用例；输入 RULE/AC、设计、交付与观察点 | 场景/技术两层 TC、覆盖和数据条件；实现不是正确预期来源，正式时点由流程定 |
| acceptance-execution | 需要验证可运行候选或复验问题；输入用例、候选、环境/数据 | 界面/API/E2E 观察、缺陷和复验记录；总体通过结论由测试职责给出 |
| runtime-operations | 需要准备环境、启动/停止或诊断运行；输入真实工程和配置/依赖 | 当前运行身份、真实入口、启动停止及运行信号；端口可访问不证明核心任务通过 |
| release-and-recovery | 需要发布、回退、恢复或退役；输入已授权操作、候选/产物及运行数据约束 | 实际部署/版本、回退/恢复和核心运行证据；测试仍核验约定业务任务 |

## 现行参考逐文件去向

以下为已实施候选的归属；来源列保留旧名，链接导航到现行文件。`skills/` 下目标省略共同前缀；`agents/` 表示职责源。所有记录均已形成迁移候选，最终验证见本轮验收记录，后续实施须核对具体段落、入站引用和真实证据。

| 当前文件 | 主要目标 | 拆分或保留要求 |
| --- | --- | --- |
| [codex-session-monitor/progress-message-format.md](../../../skills/codex-session-monitor/references/progress-message-format.md) | `codex-session-monitor/references/progress-message-format.md` | 保持独立通知格式、证据和去重边界；实例配置不进入项目资产 |
| [dev-acceptance/backend-and-api.md](../../../skills/acceptance-execution/references/backend-and-api.md) | `acceptance-execution/references/backend-and-api.md` | 真实 HTTP、鉴权、数据不变量与故障验证步骤 |
| [dev-acceptance/end-to-end-and-delivery.md](../../../skills/acceptance-execution/references/end-to-end-and-delivery.md) | `acceptance-execution/references/end-to-end-and-delivery.md` | 当前环境/版本核对、真实业务链与交付行为验证；启动发布操作引用运维技能 |
| [dev-acceptance/execution-and-feedback.md](../../../skills/acceptance-execution/references/execution-and-feedback.md) | `acceptance-execution/references/execution-and-feedback.md` | 固定候选、证据、问题反馈及定向复验；是否整体通过由测试职责判断 |
| [dev-acceptance/frontend-and-ui.md](../../../skills/acceptance-execution/references/frontend-and-ui.md) | `acceptance-execution/references/frontend-and-ui.md` | 界面行为/真实浏览器执行；呈现专项调用视觉检查，设计原型默认归产品/视觉走查 |
| [dev-acceptance/project-assets.md](../../../skills/document-management/references/professional-assets.md#测试验收) | `document-management/references/professional-assets.md#测试验收` | 测试资产目录/索引迁移；预期、用例有效性和报告结论归测试 |
| [dev-acceptance/strategy-and-cases.md](../../../skills/acceptance-case-design/references/strategy-and-cases.md) | `acceptance-case-design/references/strategy-and-cases.md` | 预期来源映射、场景/技术两层用例与覆盖复核；正式用例时点留流程 |
| [dev-architecture/clean-architecture.md](../../../agents/references/architecture/clean-architecture.md) | `agents/references/architecture/clean-architecture.md` | 依赖方向等核心原则内嵌提示词；长篇拆分说明和案例保留引用 |
| [dev-architecture/code-standards.md](../../../agents/references/architecture/code-standards.md) | `agents/references/architecture/code-standards.md` | 通用规范唯一源和可复制配置的使用说明；具体项目规范/例外留项目 |
| [dev-architecture/design-and-contracts.md](../../../agents/references/architecture/design-and-contracts.md) | `agents/references/architecture/design-and-contracts.md` | 模块、契约及技术方案/计划 Review 的专业内容；阶段顺序引用流程 |
| [dev-architecture/project-assets.md](../../../skills/document-management/references/professional-assets.md#架构) | `document-management/references/professional-assets.md#架构` | 目录与归档动作合并；技术事实更新和有效性判断由架构执行 |
| [dev-architecture/retrospective-and-evolution.md](../../../agents/references/architecture/review-and-closeout.md) | `agents/references/architecture/review-and-closeout.md` | 完整变更检查清单、两类结论及技术收尾专业方法保留；差异获取引用 Git、独立执行引用 subagent |
| [dev-architecture/system-and-module-map.md](../../../skills/codebase-mapping/references/system-and-module-map.md) | `codebase-mapping/references/system-and-module-map.md` | 实际入口/符号/数据追踪和来源覆盖；合理性判据引用架构规范，由职责给结论 |
| [dev-architecture/technology-stack.md](../../../agents/references/architecture/technology-stack.md) | `agents/references/architecture/technology-stack.md` | 默认选型与项目基线字段；实际版本/选择留项目，不分散复制到角色身份 |
| [dev-engineering/baseline-and-plan.md](../../../agents/references/engineering/baseline-and-plan.md) | `agents/references/engineering/baseline-and-plan.md` | 影响分析、计划字段和依赖判断；Git 基线获取引用公共 Skill |
| [dev-engineering/compatible-changes.md](../../../agents/references/engineering/compatible-changes.md) | `agents/references/engineering/compatible-changes.md` | 兼容演进专业方法先保留参考；数据恢复操作引用发布恢复 Skill，不删除消费者和迁移检查 |
| [dev-engineering/diagnosis-and-feedback.md](../../../skills/defect-diagnosis/references/diagnosis.md) | `defect-diagnosis/references/diagnosis.md` | 根因假设、最小复现、实验和影响分析；修复由研发承担，正式复验归测试 |
| [dev-engineering/frontend-implementation.md](../../../agents/references/engineering/frontend-implementation.md) | `agents/references/engineering/frontend-implementation.md` | 状态/数据/框架边界专业方法保留；组件接入与视觉检查引用对应 Skill |
| [dev-engineering/project-assets-and-delivery.md](../../../agents/references/engineering/handoff.md) | `document-management/references/professional-assets.md#研发；agents/references/engineering/handoff.md` | 索引/记录归文档；完整候选及工程交接内容归研发，阶段前置引用流程 |
| [dev-engineering/review-feedback.md](../../../agents/references/engineering/review-feedback.md) | `agents/references/engineering/review-feedback.md` | 研发处理意见、证据反驳、修订与交回；关闭由评审/测试实际复核；不归普通缺陷诊断 |
| [dev-engineering/slices-and-integration.md](../../../agents/references/engineering/slices-and-integration.md) | `agents/references/engineering/slices-and-integration.md` | 切片、业务/协议/存储与集成责任保留；Git 合并操作调用公共 Skill |
| [dev-engineering/technical-delivery-design.md](../../../agents/references/engineering/technical-delivery-design.md) | `agents/references/engineering/technical-delivery-design.md` | 真实代码反馈、统一技术设计内容与模板；不另建完整研发设计流程 Skill |
| [dev-engineering/test-first-and-regression.md](../../../skills/regression-verification/references/test-first-and-regression.md) | `regression-verification/references/test-first-and-regression.md` | 目标失败、旧新对照、事后补测与回归证据；不替代正式验收 |
| [dev-flow/codex-agent-configuration.md](../../../skills/subagent-coordination/references/host-execution.md) | `subagent-coordination/references/host-execution.md；docs/plugin.md` | 能力发现、路径传递、真实降级进 Skill；安装和历史事实进维护文档 |
| [dev-flow/constitution.md](../../../skills/dev-flow/references/constitution.md) | `dev-flow/references/constitution.md` | 精简为流程共同协议；专业责任进提示词，操作进三个公共 Skill |
| [dev-flow/design-document-contract.md](../../../skills/document-management/references/document-contract.md) | `document-management/references/document-contract.md` | 目录、索引、链接、版本和落位迁移；总体进度语义留流程 |
| [dev-flow/document-archive.md](../../../skills/document-management/references/archive.md) | `document-management/references/archive.md；dev-flow/references/closeout.md` | 整理/总结保存/归档步骤迁移；收尾时序及完成判断留流程；提交交 Git |
| [dev-flow/document-preview.md](../../../skills/document-management/references/document-preview.md) | `document-management/references/document-preview.md` | 文档阅读器的项目定位、启动和实际 URL 契约迁移 |
| [dev-flow/execution-contract.md](../../../skills/dev-flow/references/execution-contract.md) | `dev-flow/references/execution-contract.md` | 保留阶段依赖、授权、变更及完成规则；具体派发、保存、目录步骤改引用 |
| [dev-flow/git-and-worktree.md](../../../skills/git-workflow/references/git-and-worktree.md) | `git-workflow/references/git-and-worktree.md` | Git 操作迁移；何时允许集成/结束留流程；独立 Git 请求不强制完整验收 |
| [dev-flow/progress-management.md](../../../skills/dev-flow/references/progress-management.md) | `dev-flow/references/progress-management.md` | 保留完整阶段与状态权威语义；目录落位引用文档管理 |
| [dev-flow/project-asset-maintenance.md](../../../skills/document-management/references/asset-maintenance.md) | `document-management/references/asset-maintenance.md；agents/prompts/*.md` | 组织更新和引用复用进 Skill；专业有效性判断归各职责；能力成熟度事实留 docs |
| [dev-flow/role-capabilities.md](../../history/2026-10-21-role-capabilities.md) | `agents/prompts/*.md；docs/agent-development.md` | 能力责任逐职责迁入提示词；能力编号保持稳定；建设成熟度留维护文档；流程仅简要路由 |
| [dev-flow/stage-state.md](../../../skills/dev-flow/references/stage-state.md) | `dev-flow/references/stage-state.md` | 保留状态语义、核验器与示例；模板引用新位置 |
| [dev-flow/subagent-guidance.md](../../../skills/subagent-coordination/references/dispatch-and-lifecycle.md) | `subagent-coordination/references/dispatch-and-lifecycle.md` | 任务包/资源/等待及执行独立性检查迁移；是否必须评审及阶段顺序留流程 |
| [dev-flow/task-routing.md](../../../skills/dev-flow/references/task-routing.md) | `dev-flow/references/task-routing.md` | 保留路径、参与职责、裁剪条件；路由到 Agent 与操作 Skill |
| [dev-operations/artifacts-and-release.md](../../../skills/release-and-recovery/references/artifacts-and-release.md) | `release-and-recovery/references/artifacts-and-release.md` | 候选/产物身份、实际发布和版本核验；Git 集成操作交公共 Skill，阶段条件引用流程 |
| [dev-operations/environment-and-startup.md](../../../skills/runtime-operations/references/environment-and-startup.md) | `runtime-operations/references/environment-and-startup.md` | 真实项目/配置/依赖核验及启动停止步骤 |
| [dev-operations/observation-and-incidents.md](../../../skills/runtime-operations/references/observation-and-incidents.md) | `runtime-operations/references/observation-and-incidents.md` | 当前运行信号与故障定位；回退/恢复引用发布恢复 Skill |
| [dev-operations/project-assets-and-evolution.md](../../../skills/release-and-recovery/references/evolution-and-retirement.md) | `document-management/references/professional-assets.md#运维交付；release-and-recovery/references/evolution-and-retirement.md` | 目录/归档归文档；运行资源演进、退役步骤归发布恢复；是否适合演进归运维判断 |
| [dev-operations/recovery-and-migrations.md](../../../skills/release-and-recovery/references/recovery-and-migrations.md) | `release-and-recovery/references/recovery-and-migrations.md` | 回退、备份、迁移兼容和恢复演练，不将应用回退等同数据恢复 |
| [dev-product/consumer-and-business-design.md](../../../agents/references/product/consumer-and-business-design.md) | `agents/references/product/consumer-and-business-design.md` | 任务/用户类型判断保留为产品参考；核心原则入提示词；UI 默认约定改引用唯一源 |
| [dev-product/flows-and-interactions.md](../../../skills/product-specification/references/flows-and-states.md) | `product-specification/references/flows-and-states.md` | 流程、分支、状态和恢复表达步骤/检查表迁移；行为选择责任进产品提示词 |
| [dev-product/html-prototyping.md](../../../skills/react-prototyping/references/build-and-preview.md) | `react-prototyping/references/build-and-preview.md` | React 工程操作与旧 HTML 支持迁移；方案价值及业务确认归产品 |
| [dev-product/project-assets.md](../../../skills/document-management/references/professional-assets.md#产品) | `document-management/references/professional-assets.md#产品` | 目录/记录/复用动作合并；专业规则有效性归产品；能力建设留 docs |
| [dev-product/reference-research-and-ideation.md](../../../skills/product-specification/references/reference-research.md) | `product-specification/references/reference-research.md` | 按需参考核验与候选对比方法；独立研究请求可由产品直接读取该方法，不要求先写规格 |
| [dev-product/rules-and-acceptance.md](../../../skills/product-specification/references/rules-and-ac.md) | `product-specification/references/rules-and-ac.md` | 将业务来源转换为规则和可观察 AC；不负责正式 TC 或用户确认 |
| [dev-product/specification-contract.md](../../../skills/product-specification/references/specification-contract.md) | `product-specification/references/specification-contract.md` | 规格字段和来源映射；职责保留内容责任；目录规则引用文档管理 |
| [dev-product/validation-and-handoff.md](../../../agents/references/product/usability-and-handoff.md) | `agents/references/product/usability-and-handoff.md` | 原型走查的专业方法与判断保留，不混为实现验收；技术启动引用原型 Skill |
| [dev-visual/ant-design-capabilities.md](../../../skills/component-reuse/references/ant-design-capabilities.md) | `component-reuse/references/ant-design-capabilities.md` | 官方能力发现、API/主题核验与任务所需接入；不把旧外部核验日期改成当前验证 |
| [dev-visual/component-preview-and-reuse.md](../../../skills/component-reuse/references/component-preview-and-reuse.md) | `component-reuse/references/component-preview-and-reuse.md` | 选择、预览、文件集复制及来源差异记录；整套设计工作台引用原型 Skill |
| [dev-visual/project-assets.md](../../../skills/document-management/references/professional-assets.md#视觉) | `document-management/references/professional-assets.md#视觉` | 现行 UI 资产独立维护与迭代增量组织迁移；视觉正确性归职责 |
| [dev-visual/reference-and-direction.md](../../../agents/references/visual/reference-and-direction.md) | `agents/references/visual/reference-and-direction.md` | 视觉方向、参考转化与取舍作为专业方法；核心判断进视觉提示词 |
| [dev-visual/rendered-review.md](../../../skills/visual-verification/references/rendered-review.md) | `visual-verification/references/rendered-review.md` | 固定候选、窗口、主题、数据/状态，实际呈现检查和定向复验 |
| [dev-visual/specification-contract.md](../../../agents/references/visual/specification-contract.md) | `agents/references/visual/specification-contract.md` | 规格字段与专业内容要求；通用文件管理引用文档 Skill |
| [dev-visual/system-and-pages.md](../../../agents/references/visual/system-and-pages.md) | `agents/references/visual/system-and-pages.md；react-prototyping/references/multi-device-preview.md` | 布局/层级/状态专业准则留职责参考；React 拆分、多端容器及工程预览步骤进原型 Skill |
| [dev-visual/ui-stack-and-components.md](../../../agents/references/visual/ui-baseline.md) | `agents/references/visual/ui-baseline.md；component-reuse/references/source-reuse.md` | 通用 UI 基准唯一源归视觉；源码复制/差异回收进组件 Skill；Git 操作引用 Git Skill |

## 八个 Skill 入口与执行提示词

| 现行入口 | 处理 |
| --- | --- |
| dev-flow/SKILL.md | 保留并缩减到流程；操作调用替换为新 Skill |
| dev-product、dev-visual、dev-architecture、dev-engineering、dev-acceptance、dev-operations/SKILL.md | 分别拆到六份提示词、职责参考和操作 Skill；退出旧职责 Skill 结构 |
| codex-session-monitor/SKILL.md | 保持独立，修正确有变化的包内引用；不新增监控任务或发送通知 |

六份现有 TOML、六份 Kimi Markdown、kimi.plugin.json 及生成器同时适配；新提示词是内容权威源，宿主文件为生成物。旧职责入口的过渡说明不复制专业规则；是否暂留由入站兼容检查决定，发现相关引用时不得直接删除。

## 工具、源码与模板去向

以 Git 跟踪文件为基线，排除 node_modules、构建目录、临时运行记录。当前共 138 个被跟踪的 assets/scripts 文件，按目录族整体核对，复制/移动时保留源码、许可、清单、测试及相对路径。

| 当前目录或文件族 | 目标与操作 |
| --- | --- |
| dev-flow/assets/document-workspace/（15） | document-management/assets/document-workspace/，整体迁移共享阅读器，更新预览命令与项目定位 |
| dev-flow/assets/templates/{project-document-index,iteration-index}.md（2） | document-management/assets/templates/，组织规则引用流程状态语义 |
| dev-flow/assets/templates/progress.md（1） | 留 dev-flow，模板直接表达阶段/依赖；文档 Skill 仅引用其落位方法 |
| dev-flow/assets/examples/iteration-state.md 与 scripts/check_iteration.py（2） | 留 dev-flow，修正工具调用/示例引用，不改既有状态语义 |
| dev-product/assets/prototype/ 与 scripts/prototype.py（6） | react-prototyping 对应目录，保留旧 HTML 工具支持，区分默认 React 和可选 HTML |
| dev-product/assets/templates/feature-spec.md（1） | product-specification/assets/templates/，保留产品字段与 RULE/AC 关联 |
| dev-visual/assets/design-workspace/ 与 scripts/design-template*（31） | react-prototyping 对应目录，更新模板测试中的路径，保留内部源码结构 |
| dev-visual/assets/react-workspace/（56） | component-reuse/assets/react-workspace/，保留 catalog、源码文件集、复制工具与许可证 |
| dev-visual/assets/templates/design-spec.md（1） | agents/assets/visual/，由视觉职责直接使用，通用目录规则改引用 |
| dev-architecture/assets/code-standards/（5） | agents/assets/architecture/code-standards/，从架构规范指向唯一可复制配置 |
| dev-architecture/assets/templates/（5） | agents/assets/architecture/，保留设计、Review、现状、基线、技术收尾模板 |
| dev-engineering/assets/templates/（5） | 设计、计划、Review、交接模板到 agents/assets/engineering/（4）；工程索引到 document-management/assets/templates/（1） |
| dev-acceptance/assets/templates/（5） | 策略/用例模板到 acceptance-case-design（2）；检查/缺陷/报告模板到 acceptance-execution（3） |
| dev-operations/assets/templates/（3） | 运维索引到 document-management（1）；交付、事故恢复模板到 release-and-recovery（2），runtime-operations 按需引用 |

数量是现行跟踪文件的盘点，不是未来不允许拆并的约束。未跟踪的依赖与产物不随迁移纳入包。专业模板可由多个职责读取，不因调用者增加而复制多份。

## 需要重点逐节拆分的内容

| 原位置/章节 | 保留责任 | 可复用操作 / 其他归属 |
| --- | --- | --- |
| subagent-guidance：是否委派、按流程安排、主会话保持运行、派发并发交接 | dev-flow 保存必须参与的职责、独立 Review 和主会话完成条件 | subagent Skill 保存执行可行性/隔离、任务包、等待和资源生命周期 |
| document-archive：一条指令收尾、归档条件、执行步骤、技术收尾、总结 | dev-flow 编排；架构/测试/运维给专业结论 | Git 保存代码；文档管理组织总结、遗留及索引并归档 |
| product/flows-and-interactions：流程、状态、异步恢复、可访问性、检查产物 | 产品提示词保存行为语义和真实契约原则 | 规格 Skill 提供流程/状态表及检查步骤；原型操作交原型 Skill |
| visual/system-and-pages：可实现规则、交互语义、原型复用、多端与尺寸容器 | 视觉提示词及职责参考保存层级、Tokens 和状态判断 | 原型 Skill 保存工程拆分/尺寸容器步骤；组件 Skill 负责复用接入 |
| architecture/retrospective-and-evolution：完整变更评审、复盘、发现、写回 | 架构提示词与参考保存检查范围、专业判据、双结论和技术收尾 | Git 获取完整候选差异；subagent 核验执行独立性；文档管理保存结果 |
| engineering/review-feedback：集中评审、核对依据、tracker 闭环 | 研发核验/修复或反驳；评审者复核；测试关闭行为缺陷 | 流程规定阶段；缺陷诊断只处理需根因实验的部分；文档不裁定关闭 |
| operations/project-assets-and-evolution：资产、依赖演进、退役 | 运维判断影响、兼容及实际状态 | 文档组织记录；发布恢复执行切换、资源回收与退役核验 |

## 维护工具与兼容影响

`scripts/sync_host_agents.py` 改为读取 agents/prompts 的真实专业提示词；共用描述/角色标识设唯一维护源，不从已退出职责 Skill 反推。编译时组合公共约束与专业提示词，检查六职责存在及引用有效；六职责数量可作为本插件明确能力范围，操作 Skill 数量不能继续写死八个。

`scripts/manage_plugin.py::validate_bundle` 当前写死八个名称，必须改为候选声明与实际发现的一致性核验：不能仅数文件，也不能只比较两个都可能漏项的动态列表。验证每个角色路由需要的 Skill 和专业参考/资产确实被打包，拒绝缺项、未声明入口及路径越界。候选声明采用单一清单，具体格式在实施设计中确定，不额外维护互相矛盾的列表。

`tests/test_plugin_installation.py` 的隔离夹具和数量断言同步调整；新增缺失提示词/引用资源、错误技能路由的失败场景，沿用缓存篡改、源码指纹与用户配置保留检查。README、docs/plugin.md、文档归类/归属、六职责现状、AGENTS 引用等当前维护入口同步更新；评测和历史快照不伪装成新结构通过。

包内所有 references 与工具/测试路径通过 Git 全量查引用；业务项目已经复制的原型/组件不强制迁移，只更新插件内源及后续命令。旧 Skill 名称和绝对缓存路径的引用要区分当前入口、历史证据和外部项目，不能全局机械替换。

## 后续实施顺序与退出条件

1. 形成六职责提示词和资源路由候选，先检查责任完整且可单独读取；建立公共 Skill，保留旧入口直至新路径可运行。
2. 按清单逐文件迁移，拆混合章节，移动对应工具/模板和入站引用；每一族明确唯一写入者，避免多个执行者同时改生成器和共同入口。
3. 同一候选完成 dev-flow 精简、六职责旧入口退出、生成器/清单/安装检查适配；发布前不留下两个专业权威源。
4. 运行结构与路径核验、受影响工具测试、隔离打包安装测试；再进行真实角色/操作与完整流程案例。
5. 独立 Review 最终完整变更与行为结果，修复并复验；之后再升级 0.4.0、同步生成物、构建安装和分宿主核验。

各步只记录真实状态；开发中间态不安装到用户宿主。没有实际宿主角色发现/派发能力时，记录主 Agent 执行及独立性边界，不将生成入口存在写成原生支持。

## 边界回归场景

| 场景 | 必须观察到的边界 |
| --- | --- |
| 单独提交已验证的局部改动 | Git Skill 可独立完成；不引入完整产品/设计审批；保留无关修改 |
| 派发一次只读架构评审 | 原要求和完整候选进入任务包；subagent 返回不自动通过；评审者实际给专业结论 |
| 整理文档并更新索引 | 仅处理有效来源与组织；不改业务政策，不把未完成迭代标记结束 |
| 将需求整理为规则与状态 | 产品职责决定语义，规格 Skill 形成 RULE/AC；不得从实现反推规则或凭规格登记确认 |
| 从 RULE/AC 形成并执行正式 TC | 用例设计与执行分别有输入输出；测试判断覆盖与结果；不改变设计原型的主责 |
| 建立代码地图并做完整变更评审 | 地图是事实证据，专业评审检查原要求和最终完整差异；地图生成成功不等于架构评审通过 |
| 开始收尾 | 流程编排、专业收尾、Git 保存、文档归档分工可追溯，未关闭必需项阻止整体完成 |
| 完整功能迭代 | 原有设计/授权、实现、自测、Review、正式用例/验收及交付规则不因拆分丢失 |

结构盘点是本轮已做的规划核对；上述工具与行为场景均属于实施后的待验证项。独立意见与本轮处理见[边界评审](../../../reviews/2026-10-21-agent-skill-reorganization-boundaries.md)。
