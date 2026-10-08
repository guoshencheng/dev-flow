# 本地 Plugin 接入验证

日期：2026-10-09。Plugin 0.1.0；本次由主 Agent 执行工具与文件系统验证，实施计划经过主 Agent AI 自查，没有声称独立复核。范围见[实施计划](../docs/plans/2026-10-08-plugin-packaging.md)。

## 实际完成

- Codex CLI 0.156.1 已通过 marketplace add 和 plugin add 安装并启用 `dev-flow@dev-flow-local`；安装根为 `~/.codex/plugins/cache/dev-flow-local/dev-flow/0.1.0/`。
- 干净包约 2.9 MB，仅复制 Git 管理的文件，排除原目录约 858 MB 的 node_modules 等本机缓存。包含共同流程、六专业职责与安装初始化，共八个 Skills；本次包内检查 672 个 Markdown 本地引用均有效，包括 URL 编码文件名。
- 原七个 `~/.agents/skills/dev-*` 仓库链接已迁移；六个个人角色入口指向受管适配副本。实际插件 Skill 路径写入角色指令，源/生成 TOML 均未固定 model 或 model_reasoning_effort。
- 全局 AGENTS.md 仅更新 Dev Flow 区块，原文和旧链接信息已备份；新用户上下文也已提供实际插件入口。
- 在仓库外的新临时目录执行 `codex debug prompt-input`，模型输入实际出现八个 `dev-flow:<skill-name>` Skills，来源是安装缓存，没有同名源码 Skill 重复项。
- 同一 0.1.0 版本实际重装已刷新包指纹并重新初始化，源码与缓存一致检查通过。此结果适用于本机当前 CLI，不把所有客户端的自动热更新登记为通过。

## 隔离验证

使用 Python 3.11+ 对 `tests/test_plugin_installation.py` 的 14 项测试全部通过：首次/重复初始化、自己的旧链接迁移、外部角色/Skill 冲突保护、更新路径、同版本内容指纹更新、修改副本/指引保护、override/损坏区块阻断、解除保留已接管入口、包损坏识别、六 TOML 实际解析、源码链接模式回退及模式冲突、注入写入失败后恢复原状态/内容/链接。Python 3.9 的文件操作检查也已通过，TOML 解析单独使用 3.11+。

测试发现同版本内容刷新时，旧的重复初始化分支会保留旧指纹；已将当前包摘要和版本纳入重复判定，并通过实际重装和专门用例复验。初始化写入发生异常时恢复修改前文件与链接；无法恢复则报告具体缺口和备份，不声称安装完成。

新初始化 Skill 与修改后的 dev-flow 入口结构校验通过；Git diff 空白检查通过。旧专业行为/原型/API/运行恢复案例保留原版本，本次未将这些案例重复登记为 Plugin 的原生角色运行。

## 证据边界

八 Skills 的模型输入发现、六 TOML 的语法/路径/接入和实际插件安装启用已经验证。只读 app-server 初始化及 config/read 成功，但该响应的 agents 没有枚举角色名，因此不将其当作原生角色发现或派发证据。尚未执行原生六角色实际派发、用户默认模型下的专业协作、桌面插件设置页 UI 核验、远程 Git 安装或真实业务项目完整生命周期。

本次没有 MCP 服务、生命周期 Hooks、独立运行内核、常驻调度或远程发布。用户已授权的本地 Plugin 安装与更新能力已交付；下一阶段的真实项目和原生派发单独验证。

## 使用与复验

在源码仓库执行 `python3 scripts/manage_plugin.py install` 更新，执行 `check` 核验当前实际启用/源码指纹/角色与指引；源码有新文件时先纳入 Git。安装包的 `package-files.json` 记录每个文件摘要、源码提交和工作区变化，本机受管 state 记录当前缓存摘要与备份位置。安装与解除方法见[插件指南](../docs/plugin.md)。
