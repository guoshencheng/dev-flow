# Codex Plugin 安装与维护

当前插件包含一个流程 Skill 和六个专业 Skills，共七个。职责通过 Skills 提供，不需要 setup Agent，也不向个人 Agent 目录写入角色配置或维护全局指引。仓库 `agents/` 的旧 TOML 仅保留为配置参考，不参与当前安装或流程。项目长期资产留在所属项目。

## 安装、更新与检查

在 Git 仓库根目录运行：

```sh
python3 scripts/manage_plugin.py install
python3 scripts/manage_plugin.py check
```

新文件先纳入 Git。install 构建 Git 管理的当前源码，排除依赖缓存、构建产物、本机运行数据与真实环境变量文件；注册本地 marketplace，并通过 Codex 安装/更新插件。它核验安装缓存指纹与七个 Skills，不创建原生 Agent、不写个人 AGENTS.md 或全局 Skill 链接。

本机安装路径保存在源码仓库的 `.dev-flow/plugin-install.json`，只用于只读检查缓存；它不是项目资产或 Agent 初始化状态。`check` 核验实际启用、包内容和源码一致性。能力列表未刷新时在新会话核验发现，必要时重启宿主。

源码远程为 [guoshencheng/dev-flow](https://github.com/guoshencheng/dev-flow)。新环境可克隆后执行上述命令；从其他安装入口使用插件时，按该宿主的安装/更新机制处理，均无需初始化 Agent。当前版本没有 MCP 服务、后台常驻进程或生命周期 Hooks。

## 使用与解除

使用 `$dev-flow` 或选择插件，按[任务路由](../skills/dev-flow/references/task-routing.md)处理 bugfix 或正常需求。主 Agent 读取所需专业 Skill；需要且获准委派时，向实际可用子 Agent 提供专业 Skill 路径与明确任务。模型遵循用户及宿主本次约束。

```sh
python3 scripts/manage_plugin.py remove
```

remove 只解除当前仍属于本仓库构建来源的插件和 marketplace，并删除本地安装路径记录；保留源码、用户配置和业务项目资产。用户在宿主页面关闭或卸载插件无需额外解除 Agent。

## 历史迁移

2026-10-09 按用户要求删除 dev-flow-setup、Agent 注册脚本及旧源码链接安装入口。本机旧 setup 生成的六个原生角色链接/副本和受管状态已核对归属后清理；已有全局 Dev Flow 流程指引保留为用户既有偏好，后续插件安装不改写它。其他机器曾执行过旧 setup 的残留配置需要按实际归属单独清理，新安装不会产生这些配置。

此前八 Skills/原生角色接入的测试是历史版本证据，见[旧安装验证](../reviews/2026-10-09-plugin-installation.md)，不作为当前版本行为说明。
