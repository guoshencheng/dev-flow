# 阶段推进与完成判断评测

本次用近期真实迭代暴露的失败模式提炼评测，不复制业务源码或整段私有会话。分开登记：

- `tests/test_iteration_checks.py`：核验器的确定性契约测试，使用合成状态/证据；验证所声明字段、依赖、覆盖及候选一致性，不代表 Agent 行为。
- `evals.json`：供后续获准的新上下文评测或真实任务复验的输入与判据。比较是否正确推进/等待/裁剪及诚实汇总，不把提到标题、固定 Agent 数或额外审批作为通过条件。
- `report.md`：本次实际执行记录和未验证边界；没有执行的模型行为不能写 passed。

工具复跑：从仓库根目录执行 `python3 -m unittest discover -s tests -p test_iteration_checks.py -v`。状态示例和占位模板也在测试中实际解析，避免文档格式与脚本漂移。本轮新规则的确定性工具结果见[2026-10-21 记录](2026-10-21-tool-check.md)。

新上下文评测时只给任务、相关项目资产和 Skill，不把 expected_behavior 交给执行者。检查其真实动作、引用版本、确认覆盖、实际 Review/验证及结束行为；评测需要委派时遵守本次用户与宿主权限。工具检查、主 Agent 自查、独立行为与真实项目结果分别记录。首轮至少采用混合请求/局部确认、原生证据边界和合法局部修复，随后按真实失败补用例。

原 13 个输入中涉及实施前完整 TC 的判据已按 2026-10-21 新流程改写，新增完整候选后用例/交付、唯一 Progress 权威和空 cases 场景；当前共 17 个行为输入，本轮执行其中 6 个，并另跑固定 `proposal-cost` 项目场景；七个场景及新会话发现的独立结果见[本轮行为报告](2026-10-21-behavior-report.md)。其余 11 个策略输入未执行，不扩写为全部通过。历史工具结果保留其当时结论。阶段工具测试另验证授权缺失、未关联/不适用、范围与版本失效，以及合并/历史授权合法复用；实际结果见[本轮记录](../../reviews/2026-10-12-implementation-authorization.md)。


## 2026-10-21 固定行为输入

执行者只拿下表项目、任务和已安装 Skill；独立评判者另读 `evals.json` 的 `expected_behavior` 或 `evaluators/`。复制项目到忽略的运行目录再执行，不能原地修正夹具。固定夹具中的确认、Review 与旧运行记录均是明确标注的合成设定，不能当真实业务证据。

| 场景 | 执行输入 | 观察边界 |
| --- | --- | --- |
| proposal-cost | `fixtures/proposal-cost/task.md` 与 `project/` | 真实读取隔离代码、两方案成本、状态价值和进度恢复；不含可运行 UI |
| post-candidate-cases-delivery | `fixtures/post-candidate/task.md` 与 `project/`；这是同名 eval 的固定项目输入增强，只运行一次 | 后置正式用例、独立 Review、CLI 验收和源码目录外 zipapp 启动/保存/回读 |
| valid-quick-fix | 同名 eval 的 prompt 与 `fixtures/quick-fix/project/` | 捕获只读权限失败、局部修复与回归，无委派权限时如实自查 |
| mixed-rename-mobile | 同名 eval 的 prompt 与 `fixtures/mixed-rename/project/` | 已授权 Mac 更名可执行，新增手机支持待设计与授权 |
| evidence-does-not-expand | 同名 eval 的 prompt 与 `fixtures/evidence/project/` | 仅合成证据分类/汇总；没有原生运行环境，不声称完成必需原生验收 |
| single-progress-authority | 同名 eval 的 prompt 与 `fixtures/progress/project/` | 实际唯一 Progress 路径核验与恢复；结构化记录为合成输入 |
| native-subagent-independent-review | 同名 eval 的 prompt，关联实际 `proposal-cost` 设计作者和另一原生 Reviewer | 真实作者/评审分离、窄写入边界；不以静态角色名称代替派发 |

运行原始会话和产物保存在 `.dev/runs/flow-revision/`；正式结论见本轮验收与行为报告。未列入本轮必跑的其余策略输入仍保留未执行，不把七个场景扩写为全部 17 个通过。
