---
title: 原生子 Agent 注册交付记录
status: current
owner: operations
---

# 交付与发布记录

2026-10-23，主 Agent 在本仓库唯一执行本机安装；独立 acceptance 只读核验。交付模式为 Codex 本地插件与六职责受管注册，用户确认/授权见 [Progress](Progress.md)。按交付模板裁剪，无线上服务、数据库或远端部署。

## 候选与目标

源码基线 adb8bed，任务分支 codex/native-subagent-registration，0.6.0候选。Python3.9标准库与本机CodexCLI，未新增依赖。构建根为仓库 `.dev-flow/plugin-source`，目标缓存 `/Users/guoshencheng/.codex/plugins/cache/dev-flow-local/dev-flow/0.6.0`，六角色位于 `/Users/guoshencheng/.codex/agents/`，归属为同一用户根 `dev-flow/native-agents.json`。

实际入口为仓库根 `python3 scripts/manage_plugin.py install` / `check` / `remove`。CODEX_HOME优先于默认个人目录，角色不固定模型/推理强度。旧无注册安装重跑同一命令即可迁移。

## 实际执行与证据

| 步骤 | 对象/操作 | 实际结果 | 限制 |
| --- | --- | --- | --- |
| 候选准备 | 设计/计划/完整实现和正式用例独立Review | 通过，IR1/VR1/VR2关闭 | 不替代真实交付 |
| 隔离验收 | 35自动化、11补充检查、独立旧新对照与build | 通过 | 模拟CLI不替代实际安装 |
| 本机初次install/check | 0.6.0；native-install-initial.json / native-check-initial.json | 返回16Skills、六角色，已启用 | 后续文档固定后重建 |
| 独立读回 | real-initial-readback.py | 758文件源码/缓存一致、64链接有效、config/AGENTS未改 | 初次候选 |
| 原生演练 | 桌面捆绑CLI临时会话原始事件 | 六角色显式agent_type成功，独立核验自动加载职责/缓存资源与NATIVE_OK完成 | 最小身份执行，非专业任务质量 |
| 最终内容重建与独立读回 | 0.6.0，761文件 | 全部源/缓存SHA256、六副本/归属、64引用、config/AGENTS快照一致 | 完成状态保存后同断言再次复跑，结果存real-postcommit-results.json |

普通文件失败回滚字节，外部CLI及旧缓存不属于文件事务；修复后install恢复，已移除插件的文件清理失败可重试remove或install。该限制有隔离故障证据，不承诺断电/强杀原子性。

## 交付结论

目前已构建、隔离验收通过、本机初次可安装且六角色齐全，六个原生角色逐一派发通过并获独立核验；最终内容重建及独立读回均通过，全部必需TC闭合。页面没有已核实的无操作自动注册入口，需采用现有安装命令；不添加需要额外信任的Hooks。

安装/升级复用install，核验使用check，完整清理使用remove；页面禁用/卸载不触发本工具清理。专业结果见[验收报告](acceptance-result.md)，长期方法见[安装指南](../../plugin.md)。源码候选为本分支最终本地提交，状态保存后再运行install/check和验收者相同只读断言，保留最终输出；未向远端推送或部署。
