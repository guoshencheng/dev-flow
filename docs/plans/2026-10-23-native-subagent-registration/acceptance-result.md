---
id: TEST-native-subagent-result
title: 原生子 Agent 注册验收结果
status: current
owner: acceptance
---

# 原生子 Agent 注册验收结果

## 当前结论与范围

全部必需TC通过：隔离验收、本机最终安装独立读回及六角色原生派发均通过。验收执行者 acceptance（sol medium）未主笔实现、未改真实个人配置；主 Agent 只整合结论并唯一执行本机安装。正式用例由 acceptance 编写、design_review 独立复核通过，作者自查未冒充独立 Review。

## 完成门槛状态

| 门槛 | 状态 | 当前证据与限制 |
| --- | --- | --- |
| 正式用例与技术验证独立 Review | 通过 | v1，VR1/VR2独立关闭，见 [Review](review.md) |
| 完整实现 Review、研发自测/构建 | 通过 | IR1关闭，17 native/18安装，生成/构建有效 |
| 必需真实主链路及回归 | 通过 | 隔离生命周期、实际初次install/check、六角色真实原生调用均有独立核验 |
| 实际安装与约定交付 | 通过 | 最终0.6.0启用，761文件源码/缓存一致、六角色/64引用及原config/AGENTS独立核验通过 |

## 输入、候选与环境

用户确认及授权见 [Progress](Progress.md)，有效输入为设计 v3、计划 v1、验收用例/技术验证 v1，基线 adb8bed，分支 codex/native-subagent-registration，候选0.6.0。环境 macOS26.6.2 arm64、Python3.9.6；PATH CLI0.156.1，桌面捆绑0.163.0-alpha.11.1。

代码候选：manage_plugin SHA-256 6902179c1a5fd41134bb17d52b27f7a084a485abd7e3d6ddae2c7be67db0b4ab；native_agents 为 cc1b0aa3f289a3b82492c53d1cf18d7df4d6171a99629f09fcbf88c22f1bd367；native测试为9afd495f1c4e80a5ca9f31d9c58f3277f8a56cc224b12ce1d7f956e970aa946d。后续仅提炼文档不改变代码证据，包内容变化须重建。

## 整体候选与复验范围

完整实现和用例 Review 独立通过后执行。IR1实际启用版本错配已修并复验；VR2升级回滚检查已改为不同新缓存且故障4/7/8，独立无回滚替身产生1个断言失败、0个运行错误。正式验收从原目标推导，未从实现反推预期。

## 实际执行与证据

| 检查 | 操作与退出码 | 实际结果与范围 |
| --- | --- | --- |
| 独立自动化 | `python3 -m unittest discover -s tests -p 'test_native_agents.py' -v`、`test_plugin_installation.py -v`；0 | 17与18项通过，临时用户目录/模拟CLI，非真实宿主 |
| 独立补充 | `.dev-flow/native-independent-acceptance/supplement.py`；0 | 11项：state字段变异/缺失、目标目录CLI零调用、无归属保护、禁用检查、临时HOME与独立CODEX_HOME六哨兵生命周期 |
| 独立候选 | 同目录 `candidate.py`；0 | 旧install0角色断言因目标缺失失败，新install6角色并check通过；三清单0.6.0，6角色/16Skills，隔离build758文件 |
| 本机初次安装 | `python3 scripts/manage_plugin.py install` / `check`；0 | 0.6.0实际启用，六角色写入实际用户目录 |
| 本机独立读回 | 同目录 `real-initial-readback.py`；0 | 源码/缓存758文件逐字节一致，六副本与归属一致，64本地链接有效，原config/AGENTS快照不变 |
| 页面调查 | 官方文档与两CLI版本只读核验 | 调查通过；未实施页面安装，不宣称其自动注册 |
| 原生派发 | 桌面捆绑CLI app-server临时会话，独立native-raw-readback.py；0 | 六次显式agent_type、fork_turns=none、sol medium，工具成功返回且子任务自动加载职责/缓存资源，返回正确标题+NATIVE_OK |

原始证据位于本机忽略目录 `.dev-flow/native-independent-acceptance/`，包括逐测试日志、补充脚本/结果、候选旧新对照、环境/指纹、页面调查和真实读回。主 Agent 安装原始输出为 `.dev-flow/native-install-initial.json`、`native-check-initial.json`；安装前快照为 `native-preinstall-snapshot.json`。

## 按用户用例汇总

| TC | 检查映射 | 当前结果 | 实际依据 |
| --- | --- | --- | --- |
| TC-01 | CHK-01 | 通过 | 首装六角色及归属 |
| TC-02 | CHK-01/13 | 通过 | 重复安装、旧无注册迁移 |
| TC-03 | CHK-02 | 通过 | 特殊路径实际解码，升级正文更新 |
| TC-04 | CHK-03 | 通过 | 逐项异常拒绝，缺失修复，版本/来源错配拒绝 |
| TC-05 | CHK-04 | 通过 | 文件/链接/目录/不同名文件同名角色预检 |
| TC-06 | CHK-04 | 通过 | 顶层名称词法样本与保守拒绝 |
| TC-07 | CHK-05 | 通过 | 首装和实变升级4/7/8故障、回滚重试 |
| TC-08 | CHK-06 | 通过 | 期间修改不覆盖，独立进程锁报忙/重试 |
| TC-09 | CHK-07 | 通过 | 正常/缺失/重复卸载，无归属不删个人同名 |
| TC-10 | CHK-07 | 通过 | 修改在CLI前拒绝、链接与外来来源拒绝 |
| TC-11 | CHK-08 | 通过 | 删除3/7/8故障字节回滚、重装 |
| TC-12 | CHK-09 | 通过 | 双用户目录六哨兵原字节保留 |
| TC-13 | CHK-10 | 通过 | 最终0.6.0真实安装，独立761文件/六角色/64引用及个人配置快照一致 |
| TC-14 | CHK-11 | 通过 | 独立从原始raw事件关联六次实际角色选择、子任务developer正文、final及completed状态 |
| TC-15 | CHK-12 | 通过（调查范围） | 未核实页面自动注册入口，准确说明脚本边界 |
| TC-16 | CHK-13/14 | 通过 | 独立旧新/版本/生成/构建和最终实际源码缓存一致 |

## 缺陷、修复与复验

IR1、VR1、VR2均由原独立评审者关闭，正式隔离验收无新增缺陷。首次验收证据脚本误写 Kimi 清单路径，修正为实际 kimi.plugin.json 后完整重跑通过，属于证据脚本修正，不是产品缺陷。未隐藏该次夹具失败。

首次CLI原生探针遇WebSocket连接重试，HTTPS回退后普通JSON只记录等待及父自述，不足以验收；该进程已停止。随后使用系统已配置代理的本进程环境，桌面app-server临时会话开启原始事件，捕获六个具名调用、自动加载和完成；未改系统代理/用户配置。acceptance 独立从 rawResponseItem/completed 关联调用、返回及子任务正文，结果为 native-raw-results.json。此演练只证明原生最小执行链路，不证明专业任务质量。

## 资产、恢复与后续

保留稳定用例与技术映射、行为测试及安装指南；临时数据只位于本轮临时/忽略目录。验收者已执行最终只读核验，TC-13/16通过、全部必需TC可标记通过。完成状态文档保存后再次重建安装，复用验收者提供的相同断言记录real-postcommit-results.json；仅文档状态变化，不失效生命周期或原生调用证据。无UI/服务/数据库，相关专项不适用；Windows、断电/强杀事务、Kimi安装未覆盖。
