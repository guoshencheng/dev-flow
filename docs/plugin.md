# Codex / Kimi Plugin 安装与维护

当前插件包含一个流程 Skill 和六个专业 Skills，共七个。职责方法通过共用 Skills 提供；Kimi 清单另外声明六个职责 Agent 入口。不需要 setup Agent，也不向个人 Agent 目录写入角色配置或维护全局指引。仓库 `agents/` 的 TOML 由同步脚本生成，仅保留为 Codex 配置参考，不参与当前安装或流程。项目长期资产留在所属项目。

## Codex 安装、更新与检查

在 Git 仓库根目录运行：

```sh
python3 scripts/manage_plugin.py install
python3 scripts/manage_plugin.py check
```

新文件先纳入 Git。install 构建 Git 管理的当前源码，排除依赖缓存、构建产物、本机运行数据与真实环境变量文件；注册本地 marketplace，并通过 Codex 安装/更新插件。它核验安装缓存指纹与七个 Skills，不创建原生 Agent、不写个人 AGENTS.md 或全局 Skill 链接。

本机安装路径保存在源码仓库的 `.dev-flow/plugin-install.json`，只用于只读检查缓存；它不是项目资产或 Agent 初始化状态。`check` 核验实际启用、包内容和源码一致性。能力列表未刷新时在新会话核验发现，必要时重启宿主。

源码远程为 [guoshencheng/dev-flow](https://github.com/guoshencheng/dev-flow)。新环境可克隆后执行上述命令；从其他安装入口使用插件时，按该宿主的安装/更新机制处理，均无需初始化 Agent。当前版本没有 MCP 服务、后台常驻进程或生命周期 Hooks。

## Kimi 安装与双端维护

Kimi 原生清单为包根目录 `kimi.plugin.json`，提供同一套七 Skills 和 `adapters/kimi/agents/` 的六个 Markdown 职责 Agent。先同步入口，再构建；新文件先纳入 Git：

```sh
python3 scripts/sync_host_agents.py --write
python3 scripts/sync_host_agents.py --check
python3 scripts/manage_plugin.py build
```

在 Kimi 会话中执行（包路径替换为本仓库实际构建结果）：

```text
/plugins install <仓库绝对路径>/.dev-flow/plugin-source
/plugins info dev-flow
/plugins reload
```

新会话使用 `/skill:dev-flow`。专业职责按需派发，输入包含实际安装包 Skill 路径和业务项目上下文，详见 [Kimi 职责说明](../skills/dev-flow/references/kimi-agent-configuration.md)。本地插件从受管副本运行，修改源文件后重新构建并在 Kimi 重新安装；只改源码不表示缓存已更新。

Kimi 安装/启用/移除使用其原生 `/plugins` 入口，当前 Python install/check/remove 仍专用于 Codex。Kimi 清单不自动加载流程、不配置额外 MCP/Hooks，不写个人 AGENTS.md 或 SYSTEM.md。解除使用 `/plugins remove dev-flow`。

维护专业方法改 Skills/参考；职责名称/说明、插件身份与版本变化后运行同步脚本。生成器统一检查 Kimi 清单与两端职责入口，构建时过期即失败；不手工维护两份专业提示。

## 使用与解除

使用 `$dev-flow` 或选择插件，按[任务路由](../skills/dev-flow/references/task-routing.md)处理 bugfix 或正常需求。主 Agent 读取所需专业 Skill；需要且获准委派时，向实际可用子 Agent 提供专业 Skill 路径与明确任务。模型遵循用户及宿主本次约束。

```sh
python3 scripts/manage_plugin.py remove
```

remove 只解除当前仍属于本仓库构建来源的插件和 marketplace，并删除本地安装路径记录；保留源码、用户配置和业务项目资产。用户在宿主页面关闭或卸载插件无需额外解除 Agent。

## 历史迁移

2026-10-09 按用户要求删除 dev-flow-setup、Agent 注册脚本及旧源码链接安装入口。本机旧 setup 生成的六个原生角色链接/副本和受管状态已核对归属后清理；已有全局 Dev Flow 流程指引保留为用户既有偏好，后续插件安装不改写它。其他机器曾执行过旧 setup 的残留配置需要按实际归属单独清理，新安装不会产生这些配置。

此前八 Skills/原生角色接入的测试是历史版本证据，见[旧安装验证](../reviews/2026-10-09-plugin-installation.md)，不作为当前版本行为说明。
