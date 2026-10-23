---
title: 六职责原生子 Agent 自动注册实施计划
status: current
version: 1
owner: engineering
---

# 六职责原生子 Agent 自动注册实施计划

| 项目 | 内容 |
| --- | --- |
| 关联设计 | [design.md](design.md)，v3，AC1–AC7 |
| 方案 Review | [Review](review.md)：design_review 独立通过设计 v3 与计划 v1 |
| 业务完成标准 | 用户本次确认及设计第一节；脚本安装优先，页面入口如实核实 |
| 现有测试保护 | tests/test_plugin_installation.py 的打包、来源、缓存和配置保留测试 |
| 总体进度 | [Progress](Progress.md) |
| 计划版本 | 1，2026-10-23 |
| 负责人 | 主 Agent，唯一源码写入者 |
| 执行位置 | 仓库 /Users/guoshencheng/Documents/work/dev-flow，基线 adb8bed，分支 codex/native-subagent-registration；既有修改仅本轮流程草案 |
| 执行状态引用 | 以 Progress 为唯一权威 |

## 一、实施目标与前置条件

使现有 install/check/remove 命令完整管理六职责注册，保留模型选择、个人指引和其他角色。设计与计划独立复核通过后直接实施，源自用户明确授权；不重复索取同范围许可。

**实施授权：**用户原话见 Progress。设计/计划通过是进入实现的条件；目前设计 v3 与计划 v1 均已独立通过。页面无自动入口的调查结论只影响说明，不替换脚本优先目标。

## 二、实施步骤与依赖

| 步骤 | 内容与依赖 | 变更及唯一负责人 | 可验证结果 |
| --- | --- | --- | --- |
| 1 | 设计/计划独立复核与必要修订 | 主 Agent 写入文档，独立 sol medium 只读评审 | 需求、模板、生命周期与失败边界无阻断 |
| 2 | 实现注册模块，再接入既有编排 | 主 Agent：scripts/native_agents.py、manage_plugin.py、sync_host_agents.py | 六角色有受管副本和绝对资源引用，预检/检查/清理及普通异常回滚成立 |
| 3 | 补充并运行行为检查 | 主 Agent：tests/test_native_agents.py、test_plugin_installation.py | 临时 CODEX_HOME 和模拟 CLI 覆盖 AC1–AC7；与旧安装行为对照能检出缺失角色 |
| 4 | 同步现行规则、版本和生成物 | 主 Agent：AGENTS.md、README、docs/plugin、overview、agent-development、host-execution、双清单和生成入口 | 0.6.0、16 Skills/6 职责、总纲 0.32，历史记录不追溯改写 |
| 5 | 固定完整候选，完整 Review、正式用例与独立 Review | 只读架构和验收执行者提供结论，主 Agent 整合 | 完整差异、原始要求和用例均覆盖，问题定向复评 |
| 6 | 隔离验收、实际安装及交付 | 主 Agent 唯一操作真实用户目录，独立执行者核验 | install/check 通过、六文件和全部资源有效；原生发现/派发按可用接口实证，限制如实保留 |
| 7 | 技术收尾、保存、最终构建安装核验 | 主 Agent 写入，独立架构核对 | 本地提交、源码/产物/缓存/注册一致、最终记录及完成说明 |

子 Agent 只读取明确候选和对应职责，不与主 Agent 竞争文件写入或本机安装。设计/计划可由同一未主笔架构执行者分别复核；正式用例作者与用例评审者分离；代码作者不作独立验收结论。共享 CLI、个人目录、构建输出及状态均由主 Agent 唯一写入。

## 三、测试保护与持续集成

使用系统 Python 3.9 标准库，避免安装解析依赖。新增测试以临时 Codex 用户目录验证 name 扫描、路径转换、归属、缺失/修改/链接/冲突、回滚和重试；集成测试模拟 CLI 并检查插件副作用发生顺序。必要的新文件先精确纳入 Git，再运行现有打包测试，否则受管文件夹具不会包含新增模块。

命令为 `python3 -m unittest discover -s tests -p 'test_native_agents.py'`、`python3 -m unittest discover -s tests -p 'test_plugin_installation.py'`、`python3 scripts/sync_host_agents.py --write` / `--check`、`git diff --check`、`python3 scripts/manage_plugin.py build`。按变化选择其他回归，不为无关源码重复完整测试。

同一六角色存在断言在旧 manager 的隔离安装后应失败，失败点必须是缺失角色，而不是环境或导入错误；新候选应通过。普通异常回滚仅证明文件状态恢复，不推定外部 CLI 事务或旧缓存存在。

## 四、完整候选与验收安排

完整模块、编排、版本、说明和隔离自测全部可运行后形成候选。架构对 adb8bed 至候选全部提交及未提交内容做独立 Review；测试依据原用户要求和设计 AC 后置维护正式用例，另一独立执行者复核用例覆盖与预期，再执行正式验收。

实际安装前保存本机既有六目标及状态是否存在的只读结果；冲突按既定规则报告，不强制接管。用户授权涵盖安装，验证后执行 install/check。角色目录文件、正文资源、注册记录、缓存版本和源码指纹逐项核验。可用新进程按角色发现/演练；若当前宿主不支持显式角色选择，区分实际发现与未执行派发，不能以通用 spawn 代替原生角色证明。

正式问题由主 Agent 修复，原评审者定向复评，测试复验原问题和受影响场景；最终文档修订后重新 build/install/check，使缓存包含最终源码。

## 五、计划 AI 复核引用

design_review（sol medium）对本计划 v1 独立复核通过，真实对象、范围和指纹见 [Review](review.md#三实施计划复核)。已有用户授权有效，开始实施；完整代码和验收仍须独立执行。

## 六、执行与重要调整

**当前进展引用：**[Progress](Progress.md)。

**重要调整：**设计 v3 明确不假定旧缓存保留；普通文件回滚不等同跨 CLI 的完整恢复。顶层 name 扫描采取保守失败方式，避免 Python 3.9 下新增解析依赖。进一步重要行为变化先同步设计并定向复核。

**交接：**研发提供完整候选、命令与实际结果给测试验收和架构收尾，未执行项保留真实状态。本轮不包含 Kimi 安装、推送、PR 或合并。

## 七、引用与关联文档

- [研发设计](design.md)：v3，独立通过；引用状态更新不改变已审技术范围。
- [独立 Review](review.md)：设计、计划、完整实现与用例分别通过，IR1/VR1/VR2关闭，主 Agent 只整合记录。
- [架构技术收尾](architecture-closeout.md)：已依据正式验收与实际交付独立核对通过，最终一致性独立核验完成。

模板裁剪：无 UI、服务或数据库，无需相关专项；其余章节按实际文件生命周期保留。
