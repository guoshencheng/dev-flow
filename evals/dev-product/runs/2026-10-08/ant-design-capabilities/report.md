# Ant Design 官方能力接入核验

日期：2026-10-08。执行：主 Agent。对应产品指导 v0.7、UI 约定 v0.4；本轮只调整选型与能力接入指导，历史组件证据保持原版本。详细结果见[检查记录](checks.json)。

## 结论与范围

官方 `ant-design/ant-design-cli` 提供 `@ant-design/cli`、`antd` Skill 和 MCP stdio 服务。通过官方 GitHub 文档与实际 npm 包核对来源，验证 CLI 6.6.5 在临时项目的组件/设计查询、项目 Skill 安装，以及独立协议客户端的 MCP 查询。CLI 需要 Node.js 20 及以上，npm 包采用 MIT 许可。[官方仓库](https://github.com/ant-design/ant-design-cli)

| 检查 | 实际结果 |
| --- | --- |
| 指定项目版本查询 | `info Table --version 6.6.5 --format json --lang zh` 成功，返回 Table 及 33 条 Props；`design.md` 返回设计文档 |
| Codex setup dry-run | 预览 `.agents/skills/antd/` 和 `AGENTS.md` 变更；原文件未变化、未创建 Skill |
| 项目 Skill 安装 | 在临时项目安装；Skill 内容与 npm 包内文件逐字节相同，来源哈希已记录 |
| 检查与重复安装 | `--check` 返回已配置；第二次安装 Skill 与指引均无变化 |
| 既有资产保留 | 临时项目原 `AGENTS.md` 内容与另一份 Skill 保留 |
| MCP stdio | 完成 initialize、tools/list、tools/call 和 prompts/list；Table 查询成功，提供 8 个工具与 2 个提示词 |
| MCP 版本边界 | 目标 antd 版本由服务启动参数指定；本次 `antd_info` schema 没有单次查询版本参数，跨项目版本不匹配时应使用 CLI 或对应项目连接 |

## 采用方式

指导要求先复用项目有效组件并参考官方完整组件体系，现成 antd 直接使用；共享目录提供组合与参考源码，仍有具体缺口才自建。按任务需要联用官方 Skill、CLI 或已连接 MCP，默认项目级或临时安装，记录版本及范围；本仓库维护方法与引用，不复制官方手册或将其标为自建 Skill。

复现时按官方 README 的 setup 命令在临时项目中预览、安装并检查；查询显式提供目标项目 antd 版本。本次 CLI 通过临时工具目录安装，记录 npm 来源与 integrity；使用 `NO_UPDATE_CHECK=1` 关闭查询后的更新检查。记录中的 CLI 版本代表本次工具核验，不是未来项目或 Agent 的固定要求。

## 未执行与限制

没有安装第三方全局 Skill，也没有修改 Codex 全局 MCP 配置；没有核验官方 Skill 在 Codex 新会话中的发现或实际角色行为。MCP 仅通过本地独立协议客户端验证，不能登记为 Codex 宿主接入已通过。没有新增生产项目、用户观察或组件成熟度证据；本轮未改组件实现，未重跑历史构建与浏览器检查。

Skills 搜索 CLI 本次返回的候选与查询不相关，未据此推荐；来源以官方仓库、npm 包与实际工具为准。首次搜索遇到既有 npm cache 权限冲突，改用临时 cache 完成，未修改既有 cache 权限。
