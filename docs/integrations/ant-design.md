# Ant Design 接入核验记录

核验时间：2026-10-08。此处保留当时的安装与工具观察，当前任务使用[能力联用指南](../../skills/dev-flow/references/ant-design-capabilities.md)并核对实际版本。

当时 CLI 6.6.5 的目标版本由服务启动参数 `--version` 选定，`antd_info` 没有单次查询版本参数。该观察不作为后续版本的永久约束。

当时在临时项目核验官方文档、npm 来源与接入；长期全局接入仍为源码链接模式，随后已迁移 Plugin。CLI、Skill、MCP 启动和宿主工具调用分别登记，详见[原始核验报告](../../evals/dev-product/runs/2026-10-08/ant-design-capabilities/report.md)。当前插件接入见[安装指南](../plugin.md)。
