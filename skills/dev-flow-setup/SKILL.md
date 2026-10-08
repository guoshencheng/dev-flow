---
name: dev-flow-setup
description: 初始化、检查或解除 Dev Flow 插件的原生职责 Agent 和全局流程入口；用于插件安装、更新、旧全局链接迁移及接入诊断。
---

# Dev Flow 插件初始化

先定位当前启用的 Dev Flow 插件根目录，读取同包[安装指南](../../docs/plugin.md)。本 Skill 的根目录向上两层是插件根；不要依据历史缓存路径或本机固定用户名定位。

用户要求初始化或修复插件接入时，先核验 `codex plugin list --json` 中 `dev-flow@dev-flow-local` 实际安装并启用，再运行同包 `scripts/setup_plugin.py apply --plugin-root <实际插件根目录>`，随后运行 `check`。若初始化由仓库安装命令完成，直接检查并复用。来自其他 marketplace 的分发按实际插件 ID 核验，不把本地 ID 套用为所有宿主的固定名称。

初始化将六个 TOML 适配到当前插件 Skill 绝对路径，存入个人 Codex 目录的受管区域，再逐个链接至 `agents/`。源码与生成配置均不固定模型或推理强度。配置发现和实际派发分别验证；文件存在不能登记为角色已执行。

旧的本仓库全局链接迁移使用 `--legacy-root <原 dev-flow 仓库根目录>`，只移除确实指向该仓库的同名 Skill 链接，保留其他来源；冲突先报告具体占用，不覆盖。脚本备份原指引和链接信息，更新的只有 Dev Flow 管理区块。用户或宿主当前规则始终优先。

更新本地源码插件从 Git 仓库运行 `scripts/manage_plugin.py install`，它会重建干净包、刷新缓存并重新初始化；安装缓存内不运行源码构建。来源是 Git marketplace 时采用该来源的刷新方式，再运行本包初始化并核验版本。

解除接入先运行同包 `scripts/setup_plugin.py remove`，移除当前仍属于本插件的角色链接和指引区块，再用 Codex 卸载对应插件；保留其他配置及业务项目资产。用户没有要求卸载时，不因排查问题执行移除。

交接报告实际插件 ID、版本/源码指纹、初始化结果、发现与未验证项。通用 Skill 维护使用文件链接，不启动业务项目预览。
