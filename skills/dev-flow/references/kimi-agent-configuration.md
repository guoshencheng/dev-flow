# Kimi 职责 Agent 与派发

Kimi 插件入口为包根目录 `kimi.plugin.json`，明确扫描 `adapters/kimi/agents/` 的六个 Markdown Agent，并复用 `skills/` 的七个 Skills。Codex 安装仍只启用 Skills；`agents/*.toml` 是历史配置参考，不注册个人 Agent。双端职责入口由 `scripts/sync_host_agents.py` 从共用 Skill 元信息生成；专业规则只在 Skills/参考中维护。

## 发现与选择

在 Kimi 会话安装构建包后使用 `/plugins info dev-flow` 核验诊断，重载或在新会话检查实际发现。流程入口为 `/skill:dev-flow`；按阶段需要且获准委派时选择 `dev-product`、`dev-visual`、`dev-architecture`、`dev-engineering`、`dev-acceptance` 或 `dev-operations`。同名项目/用户 Agent 可能覆盖插件 Agent，派发前核验实际来源；未发现或不允许委派时，主 Agent 读取共用 Skill 承担职责，独立 Review 缺口如实记录。

六份 Agent 保留 `${base_prompt}`，继承宿主基础工作规则、工具/Skills 说明；`subagents: []` 关闭类型授权，并用 `disallowedTools: [Agent, AgentSwarm]` 禁用委派工具，禁止继续派发，不要求六个角色同时常驻。不声明固定 tools 清单，继承宿主实际工具；任务中的只读/写入范围是执行约束，不宣称它构成文件系统沙箱。确需工具级只读时另用宿主的权限/工具配置，工具不够则报告相应验证缺口。模型与推理强度沿用用户与宿主本次执行配置，不能将 Codex 的模型别名或其他工具的 `model` 字段当作 Kimi 已生效设置。

## 自包含派发

Kimi 子 Agent 不继承主会话聊天历史。主 Agent 将以下内容明确放入原生 Agent 派发任务，不使用“按前文”“继续刚才”代替输入：

- 职责、目标、当前阶段与任务范围。
- 业务项目绝对根路径、工作目录、分支/候选版本和相关未提交差异。
- 共用专业 Skill 的实际绝对路径；从当前宿主发现的 Skill 位置取得，同包路径计算参考位置，不能使用源码仓库或旧安装缓存的固定路径。
- 有效需求/设计/契约/用例及版本、确认和授权来源；内容过长时给可访问文件的绝对路径。
- 可写范围、共享文件/接口与运行资源负责人、依赖和停止条件。
- 必需验收、成果位置和完整交接要求。

示例派发内容（路径和版本由当前任务替换）：

```text
职责：dev-architecture；阶段：最终实现评审。
项目/工作目录：<业务项目绝对路径>。
Skill：<本次实际安装包绝对路径>/skills/dev-architecture/SKILL.md。
输入：<原要求与有效契约绝对路径/版本>；基线 <提交> 至候选 <提交及未提交差异>。
授权/写入：只读源码，仅可写 <评审报告绝对路径>；不修改实现或验收预期。
验收：对完整变更给需求符合性与实现质量结论，问题须有路径/位置/证据。
交接：最终回复包含结论、版本、成果、实际检查、问题、未覆盖和依赖。
```

这是任务内容模板，不是固定的 Agent 工具 JSON schema；实际参数和完成/续派机制遵循当前 Kimi 工具说明。后台结果通过原生机制回收，任务未完成、失败或仍有背景进程时不能登记完成。续派显式提供新增差异和新候选，不假定旧输入仍有效。主 Agent 核验关键事实、差异与证据后集成并定向重验。

## 双端同步和验证

专业规则改在对应 Skill 或 references 中，双端入口均读取同一份方法；职责名称/description、插件身份/版本变化后运行：

```sh
python3 scripts/sync_host_agents.py --write
python3 scripts/sync_host_agents.py --check
```

生成文件不手工补专业方法；新增职责或修改宿主行为时修改生成器，同时更新本说明和验证记录。构建包自动检查生成结果，过期入口阻断构建。宿主工具/上下文行为差异留在适配说明，避免复制整套专业规则。

验证分为：清单和生成一致性、Kimi 原生发现/加载、实际子 Agent 派发与交接、真实项目职责行为。分别报告实际达到的层级，静态检查或成功加载不代表独立评审/验收已执行。

来源：[Kimi Agents](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/agents)、[Plugins](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/plugins.html)、[Skills](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html)。2026-10-09 对照本机 Kimi 2.1.1；后续升级按真实发现和派发重新核验。
