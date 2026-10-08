# Codex Plugin 安装与维护

首版本地 Plugin，版本 0.1.0。一个流程 Skill、六个专业 Skills 和一个初始化 Skill，共八个；六个原生职责配置由初始化脚本接入。插件没有 MCP 服务、后台常驻进程或生命周期 Hooks。业务项目的长期资产继续留在各项目中。

## 安装与更新

在本 Git 仓库根目录运行：

```sh
python3 scripts/manage_plugin.py install
python3 scripts/manage_plugin.py check
```

安装前先将新文件纳入 Git；脚本使用 Git 管理的当前文件内容，包含已跟踪文件的未提交修改，记录提交及工作区变化。忽略 node_modules、dist、本机运行数据和实际环境变量文件。依赖在使用原型或文档工程时按该工程锁文件安装；共享组件按源码复制或参考到项目，不发布内部 npm 包。

`install` 同时用于更新：构建 `.dev-flow/plugin-source/` 的干净包，注册本地 `dev-flow-local` marketplace，经 Codex CLI 安装 `dev-flow@dev-flow-local`，核验安装缓存指纹，再初始化角色并迁移旧入口。`check` 只读检查实际启用、源码与缓存一致、六角色与指引和重复 Skill 入口。插件加载安装缓存，修改源码后应重新运行 install，当前会话的能力列表不一定热更新；新会话核验发现，桌面尚未刷新时重启应用。

源码仓库已有根 `plugin.json` 和兼容 `.codex-plugin/plugin.json`。根清单是便携入口，兼容清单保持身份一致。源码 repo marketplace 指向 `./`；本机采用干净包目录作为注册来源，避免把已有依赖缓存复制进插件。源码远程为 [guoshencheng/dev-flow](https://github.com/guoshencheng/dev-flow)，发布分支 main；新环境推荐克隆后运行上述安装命令，保留统一的构建、迁移和更新行为。直接从 Git marketplace 安装时仍需执行原生 Agent 初始化，实际发现与派发独立核验。

## 原生 Agent 初始化与迁移

安装命令自动完成初始化；从插件目录单独安装后也可使用 `dev-flow-setup`，按它的实际路径运行：

```sh
python3 <插件根目录>/scripts/setup_plugin.py apply --plugin-root <插件根目录>
python3 <插件根目录>/scripts/setup_plugin.py check --plugin-root <插件根目录>
```

首次从旧 Skill Set 迁移增加 `--legacy-root <原 dev-flow 仓库>`。只移除指向该仓库的同名 Skill 链接，并把原来六个角色链接改接到 `~/.codex/dev-flow/plugin/agents/` 中的适配副本。角色指令读取实际安装插件的 Skills；生成副本及源配置都省略 model 和 model_reasoning_effort。非本包角色、其他 Skill 和全局指引原文保留；链接冲突、受管副本被修改、有效 AGENTS.override.md 会在写入前报告。备份在 `~/.codex/backups/dev-flow/`，包括原指引和链接信息。

状态文件 `~/.codex/dev-flow/plugin/state.json` 记录实际插件根、版本、包指纹、六角色摘要和备份位置。它用于本机安装恢复，不替代项目资产。Plugin 的启用状态与原生角色配置分别管理；仅在插件页面关闭插件不会自动移除已初始化角色和指引。完整解除采用下面的命令。

## 使用与解除

新会话使用 `$dev-flow` 或选择 Dev Flow 插件，按总纲裁剪当前任务。`dev-flow-setup` 用于安装维护，不参与日常业务阶段。自定义角色的文件发现与真实派发分别记录；发现 TOML 或解析成功不能登记为已执行六角色协作。模型遵循本次用户要求及宿主默认。

```sh
python3 scripts/manage_plugin.py remove
```

先解除仍由本插件管理的角色链接和全局区块，再通过 Codex 移除本插件和本地来源；保留 Git 源码、备份及业务项目资产。已由其他来源接管的入口保留。旧全局 Skill 链接不会自动恢复；如需回到源码链接模式，解除后运行 `python3 scripts/install_global.py`。两种接入方式择一，避免重复加载。

直接在 Codex 页面卸载插件时，也应先运行安装包里的 setup remove；若已经卸载，可从 Git 仓库运行 manage remove 清理仍在的受管状态。不得据插件缓存存在登记部署、运行内核或真实项目交付已完成。

## 格式依据与验证

- [官方插件打包与本地 marketplace](https://developers.openai.com/plugins/build/plugins)。
- [官方 CLI 插件管理](https://learn.chatgpt.com/docs/cli/reference)。
- [官方自定义 Agent](https://learn.chatgpt.com/docs/agent-configuration/subagents)。

本次验证在[安装验证记录](../reviews/2026-10-09-plugin-installation.md)登记。插件包装和全局接入可验证；实际专业行为继续引用各职责已有证据，原生派发与真实项目完整循环单独验收。
