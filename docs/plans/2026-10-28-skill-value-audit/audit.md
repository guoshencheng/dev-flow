# Skill 业务价值盘点

对象是当前工作区 `capabilities.json` 中的 18 项，包含尚未安装的技术图示候选；不是已安装宿主能力清单。2026-10-28 由架构职责执行者及两个读取当前职责指导的通用执行者分组只读盘点，主 Agent 归纳。证据以当前源码、工具和历史记录为准；历史评测不自动证明当前入口有效，更不证明优于无 Skill。

判定看独立任务触发、输入/输出、用户明确约定、可复用资产/操作和已有行为证据。常识与职责描述重叠是精简或撤销入口的线索；无专用代码不自动代表没有价值。单项缺少对照时不推断无价值。真实项目采用、模型独立行为与格式/工具存在分别说明。

| Skill | 实际任务及具体价值 / 证据 | 当前判断 |
| --- | --- | --- |
| `dev-flow` | 本仓库明确指定阶段、确认、单一 Progress 和完成规则；[总纲](../../../skills/dev-flow/references/constitution.md)、状态核验器；[旧行为记录](../../../evals/dev-flow-stages/2026-10-21-behavior-report.md)只覆盖当时场景 | 保留用户明确指定的流程协议；非普通职责描述 |
| `iteration-closeout` | “开始收尾”触发跨专业盘点及长期正文回写；[收尾进度](../2026-10-26-iteration-closeout-skill/Progress.md)记录合成项目验证 | 保留；与文档管理和流程的重复表述可后续精简，真实项目效果未证实 |
| `git-workflow` | 保存/集成时处理混合暂存、worktree 和完整差异；[具体方法](../../../skills/git-workflow/references/git-and-worktree.md) | 合并候选：混合暂存单次有无对照两者均正确，复杂 worktree/多提交未对照，暂保留入口 |
| `subagent-coordination` | 当前宿主职责加载、写入隔离及独立 Review 任务包；[宿主执行](../../../skills/subagent-coordination/references/host-execution.md) | 精简/合并候选；独立委派发现入口及跨宿主操作未作无 Skill 对照，暂保留 |
| `document-management` | 文档权威、路径、归档和 [Vite 阅读器](../../../skills/document-management/assets/document-workspace/README.md) | 保留：实际工具和项目文档协议；可减少与收尾重复 |
| `codex-session-monitor` | 用户授权的会话状态变化、去重与 Lark 通知；[场景入口](../../../evals/codex-session-monitor/README.md) | 保留：独立业务操作；历史场景未连接真实会话/Lark，效果待验证 |
| `product-specification` | 用户功能规则、流程、状态和可观察预期，[规格模板](../../../skills/product-specification/assets/templates/feature-spec.md)与用户确认语义 | 入口合并候选，但模板、项目规则及跨职责单独编写场景需保护；暂保留，尚无有无 Skill 对照 |
| `react-prototyping` | React 原型/多端工作台、初始化与预览脚本；[隔离验证](../../../evals/dev-visual/runs/2026-10-12/react-design-template/report.md) | 保留实际工具入口；旧验证不代表真实项目采用 |
| `component-reuse` | 组件目录、预览、源码文件集、复制与来源核验；[工作区](../../../skills/component-reuse/assets/react-workspace/README.md) | 保留实际资产与工具；第三方 API 需按使用版本核对 |
| `visual-verification` | 真实候选、窗口、状态与溢出检查；[检查方法](../../../skills/visual-verification/references/rendered-review.md) | 可移入视觉职责参考的候选；真机/模拟边界保留；尚无对照，暂保留入口 |
| `codebase-mapping` | 项目入口、规则、动态调用与数据链追踪；[地图方法](../../../skills/codebase-mapping/references/system-and-module-map.md) | 可移入架构职责参考的候选；通用代码探索能力与跨职责调用均需对照，暂保留 |
| `regression-verification` | 修复前目标失败、旧新同测和权限副作用；[研发参考](../../../agents/references/engineering/test-first-and-regression.md)，[旧场景](../../../evals/dev-flow-methods/report.md) | 已撤销独立入口；保留项目特有证据标准和按需低影响裁剪，旧名称调用不再发现 |
| `defect-diagnosis` | 复现、假设与控制变量、根因和修复复验；[研发参考](../../../agents/references/engineering/diagnosis.md)，[旧诊断案例](../../../evals/dev-flow-methods/runs/2026-10-09/independent/D01/report.md) | 已撤销独立入口；保留缺陷记录约定和证据边界，旧名称调用不再发现 |
| `acceptance-case-design` | 维护可提交文字用例、编号和原始预期；[用例模板](../../../skills/acceptance-case-design/assets/templates/acceptance-cases.md) | 与验收执行合并候选；用例与执行的时点、权威和模板不同，不贸然删除 |
| `acceptance-execution` | 按实际用例执行并使用独立 runID 本地执行表，保留未执行/待人工；[执行方法](../../../skills/acceptance-execution/references/execution-and-feedback.md) | 保留操作及模板；是否与用例设计合并需验证完整路径 |
| `runtime-operations` | 准备实际运行环境、识别进程、版本与健康/业务信号；[操作方法](../../../skills/runtime-operations/references/environment-and-startup.md) | 与交付恢复合并候选，暂保留；本地工具记录不代表云环境 |
| `release-and-recovery` | 产物、回滚、数据恢复与退役的区别及模板；[恢复方法](../../../skills/release-and-recovery/references/recovery-and-migrations.md) | 保留实际操作与授权边界；与运行入口合并前须覆盖不同触发和恢复语义 |
| `technical-diagrams` | 独立 Mermaid 技术图、图文和 ER 字段映射；[验证](../2026-10-28-technical-diagrams-skill/verification.md) | 保留，用户刚明确要求独立 Skill；有无对照各一次不足以证明统计优势 |

## 初步清理范围

针对 `defect-diagnosis`、`regression-verification` 的独立入口完成有/无对照和依赖核验后，已将项目特有操作与证据约束迁入研发职责参考，取消单独触发入口并同步引用；历史证据保留。不将少量对照推广为任何任务必然等价。其他候选暂无足够证据判断入口撤销后的实际影响，本轮先保留及如实列出。候选方案和实现均经独立架构评审。

## 定向有无 Skill 对照

均为 2026-10-28 的隔离夹具、同模型 gpt-6.1-terra/xhigh、独立上下文各一次；样例及结果在 `.dev/skill-value-audit/`，不访问生产数据，不代表统计意义或真实项目表现。

| 对照 | 核对对象 | 实际结果及局限 |
| --- | --- | --- |
| Git 混合暂存 | 仅提交 `app.py`，保留他人已暂存 `notes.md` 和未跟踪文件 | 双方均正确只提交目标并保留其他改动。Skill 版本额外记录哈希；未比较多提交、worktree 与冲突，所以暂不移除 Git Skill |
| 缺陷诊断 | 保存与读取不同文件导致结果丢失 | 双方均复现并定位不同文件路径，提出按实际权威数据契约修复并标未验证；Skill 版本在副本上增加控制实验。该例不能证明复杂问题等价 |
| 权限回归 | 同一 viewer 检查对比修复前后 | 双方均在旧版捕获成功写入、新版验证拒绝且数据不变；Skill 版本未把未提供的 403 固定成唯一预期，基线版本将其列为来自实现的附加假设。该例只测内存函数，不能推断真实 HTTP/数据行为 |
| 回归边界 | 恒绿测试、旧版语法错误、未规定拒绝码及写入副作用 | 双方都识别恒绿测试未运行候选、旧版语法失败不是目标失败、旧新对照未成立；都观察新版未写入且未把 403 作为既定契约。任务明确提示这些判断，不能证明模型会无提示自动检查 |
| 诊断边界 | 两种工作目录导致相对路径读取不同数据 | 双方都区分环境路径与数据问题；基线在隔离副本真实保存并用新进程读取，Skill 版本仅以 mock 观察写入目标，明确未真实复现保存。两者均不推断业务权威位置；只覆盖小型脚本 |

迁移路由补充模拟：在 `.dev/skill-value-audit/routing-candidate/` 制作无两个 Skill 入口的局部文件候选；通用执行者显式读取该候选公共/研发职责后，面对自然语言诊断与回归问题找到并读取两个迁入参考，以及验收侧互链。它此前参与过相关盘点与基线，不能算空白上下文；隔离候选不是完整包，未携带 dev-flow 和研发模板，故其下游引用不完整。这里只证明明确加载职责后的局部定位，不证明新会话宿主自动派发或完全无角色指导时自动找到参考。
