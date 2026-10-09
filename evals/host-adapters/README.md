# 宿主适配验证

范围：双端职责入口一致性、Kimi 原生插件/Agent 接入和原 Codex 安装边界。专业方法共用 Skills，宿主入口从元信息生成；不把适配成功登记为真实业务能力成熟。

## 可重复检查

```sh
python3 scripts/sync_host_agents.py --check
python3 evals/host-adapters/test_host_adapters.py -v
python3 scripts/manage_plugin.py build
python3 evals/host-adapters/kimi_native_smoke.py .dev-flow/plugin-source
```

新文件先纳入 Git。原生冒烟依赖本机 `kimi`，使用隔离 `KIMI_CODE_HOME`、临时业务目录和只在回环地址运行的确定性 OpenAI 协议模型替身，不读取/复制真实凭据，不调用付费模型。Kimi 原生安装、发现、派发、文件 Read 和结果回收实际执行；模型的角色选择和最终文字是替身产生，不能据此证明专业判断、实际任务路由、独立 AI Review、修复能力或真实项目验收。

## 2026-10-09 结果

- 六项隔离回归通过：Skill description 漂移、手工 Agent 漂移、清单版本漂移、未知 Kimi Agent 拒绝；打包含七 Skills/六 Agent、缓存篡改拒绝；Codex CLI 替身验证安装/检查/移除以及配置保留/异来源拒绝。
- Kimi 2.1.1 原生清单安装无诊断错误，发现七 Skills 和六个指定 Agent。
- 六个 Agent 的基础提示成功展开，各通过真实 Read 读取本次受管安装包的 Skill 和总纲，结果返回主 Agent。
- `subagents: []` 本身没有从模型工具列表隐藏 Agent；增加 `disallowedTools: [Agent, AgentSwarm]` 后六角色委派工具均不可见。
- 实际证据见 [native-evidence.json](native-evidence.json)，适配复核见 [报告](../../reviews/2026-10-09-kimi-agent-adaptation.md)。真实模型/真实业务职责行为尚未执行。
