# Agent / Skill 重组实施进度

最终目标：按已确认规划交付职责提示词、流程与操作 Skills 分离的新插件，验证并升级安装。唯一总体进度为本文。

- 基线：`0d3514852cce337d6d56737c6995f69c1548bb5f`，插件 0.3.0，总纲 0.29。
- 工作分支：`codex/agent-skill-reorganization`，复用当前工作目录；开始时仅本轮规划/评审文件未跟踪。
- 实施依据：主规划、迁移清单、独立边界 Review；用户明确答复“好，那按照这个实施吧”，覆盖本轮源码迁移、验证、升版和安装。
- 执行：主 Agent 迁移文件与工具、公共技能/流程及引用集成；实际 sol medium subagent 分别主笔职责提示词、宿主生成/打包及隔离测试；作者与后续评审分离。

| 阶段 | 状态 | 完成条件与下一步 |
| --- | --- | --- |
| 边界/迁移规划与计划复核 | 已完成 | 用户确认、独立边界Review与逐文件清单 |
| 迁移长参考/资产，建立职责与操作技能 | 已完成 | 六职责提示词、16入口与138资源已形成并独立Review |
| 生成器、候选清单及打包适配 | 已完成 | 同源生成、精确资源/路由/链接、负例与用户配置保留 |
| 完整候选Review与正式验收 | 已完成 | 独立双结论通过，58项Python回归及原型/阅读器/组件和代表行为核验 |
| 版本升级和安装核验 | 已完成（Codex范围） | 0.4.0已启用、16Skill、源码/缓存一致；Kimi按用户明确选择延期 |
| 技术收尾和交接 | 已完成 | 独立技术收尾、现行入口同步、本地源码保存；最终文档随最后包核对 |

当前结果：本轮已按五项方向完成并交付Codex0.4.0；流程总纲0.30，六职责提示词与16操作/流程入口。源码实现提交 `2a2c32b`，后续文档交接由当前分支最终提交保存。本轮总体完成结论限于用户确认的Codex交付范围。

实际完整候选安装/check：enabled=true、source_matches_cache=true、16Skill；包737文件，源实现提交2a2c32b的包指纹 `029f64e47d75e8ae938869dd331919e343f7be09e124ce0a02bd2eabb9b98690`。最后文档入Git后再做一次包/缓存核对，实际安装记录保存在忽略的 `.dev-flow/plugin-install.json` 与包的 `package-files.json`，交接以最终源码/缓存一致检查为准。

源码/产物：分支 `codex/agent-skill-reorganization`；构建 `.dev-flow/plugin-source/`；缓存 `/Users/guoshencheng/.codex/plugins/cache/dev-flow-local/dev-flow/0.4.0`。未推送、未创建PR，不修改全局用户指引；仅本轮相关成果纳入本地提交，工作树最终核对后交接。

成果入口：[现行概览](../../overview.md)、[迁移清单](migration-plan.md)、[正式用例](acceptance-cases.md)、[验收记录](verification.md)、[独立最终Review](../../../reviews/2026-10-21-agent-skill-reorganization-final.md)、[技术收尾](architecture-closeout.md)。

Kimi：用户明确选择“先完成Codex，Kimi留待原生会话更新”。本轮仅同步生成入口与产物，未改变目录信任/MCP设置，不执行其原生安装/重载。Codex新会话能力刷新留宿主实际发现，不把当前会话冻结的技能列表视为新版未安装。真实业务/生产环境未纳入本轮。

文档Web入口保持运行：`http://127.0.0.1:49947/view/docs/overview.md`，已实际打开正文及规划归纳图。服务来自本轮新document-management路径；用户仍需阅读故保持运行，可在所属启动终端Ctrl+C停止。
