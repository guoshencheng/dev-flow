# Kimi 职责入口与派发

日期：2026-10-21。本文说明本包生成结果与当前维护方式。历史原生接入证据见[0.1.x适配记录](../../reviews/2026-10-09-kimi-agent-adaptation.md)，不能当作0.4.0已安装或原生派发通过。

## 同源专业提示词

Kimi 清单扫描 `adapters/kimi/agents/` 的六个 Markdown 职责入口与 `skills/` 的操作入口。源内容来自 `agents/prompts/common.md` 及六职责提示词，能力路由在 `capabilities.json`；生成器组合完整专业正文，并按生成文件位置重写相对引用。长参考、专业模板和具体操作资源仍只有一份维护源。

六职责为 dev-product、dev-visual、dev-architecture、dev-engineering、dev-acceptance、dev-operations；这些是Agent名，旧同名职责Skill已经退出。操作技能通过各自新名称发现，不再靠读取旧Skill获得专业责任。

## 安装和发现

同步并构建当前Git候选，在Kimi原生会话通过 `/plugins install <实际包目录>`、`/plugins info dev-flow`、`/plugins reload` 核对加载；新会话使用 `/skill:dev-flow`。具体路径及状态按[安装指南](../plugin.md)和本次真实输出，不把Codex安装结果折算成Kimi已更新。

同名用户/项目Agent可能影响选择，派发前检查实际来源。无法提供原生职责发现时由实际可用执行者读取同源提示词，报告真实方式与独立性限制；不猜测开发机或旧缓存路径。

生成入口保留 `${base_prompt}` 及现有禁止继续委派的宿主约束；继承当前可用工具，不宣称这些任务约束构成文件级沙箱。模型和推理强度由本次用户/宿主选择，不能将其他宿主模型别名当作Kimi已生效配置。

## 最小充分任务包

派发应包含职责/目标/阶段，业务项目绝对根路径和工作目录，当前包绝对根路径、有效提示词及按需操作资源，原始要求与有效文件/版本，基线至完整候选及相关未提交内容，确认/动作授权来源，写入范围、共享资源责任、检查/停止和交接条件。

例如只读实现评审提供本包 `agents/prompts/architecture.md` 与公共约束，原要求和有效契约、开始基线至最终候选完整差异；指定只读源码并给报告写入范围，要求分别给需求符合性和实现质量。Git准备差异、subagent协调执行、架构做专业判断，不能只派“看一下最后提交”。

续派显式给新候选和变化，不默认旧输入仍有效；收集返回后核对真实文件与证据，再由主Agent综合。一次超时、配置存在或返回成功不证明任务及专业检查完成。

## 同步和验证

变更职责源、操作路由或插件身份/版本后运行：

```sh
python3 scripts/sync_host_agents.py --write
python3 scripts/sync_host_agents.py --check
```

生成文件不手工编辑专业规则。构建检查源、路由和资源一致性；Kimi原生发现/加载、实际子Agent交接、隔离专业行为和真实项目结果分别报告。当前已安装状态见[本轮进度](../plans/2026-10-21-agent-skill-reorganization/Progress.md)。
