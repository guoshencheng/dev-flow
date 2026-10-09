# Ant Design 能力联用

核验日期：2026-10-08。适用于 B 端组件选型、原型、主题和相关实现。产品、视觉、研发和测试按职责读取；仅讨论业务流程时按需查阅。

本指南由视觉主责维护组件/主题选型入口，研发协作 CLI/MCP 接入；产品/测试按需引用。2026-10-09 仅调整归属，外部工具的版本观察仍为上述核验日期，不视为重新验证。

## 官方能力与职责分工

Ant Design 官方维护 [ant-design/ant-design-cli](https://github.com/ant-design/ant-design-cli)，提供 `@ant-design/cli`、[antd Skill](https://github.com/ant-design/ant-design-cli/blob/main/skills/antd/SKILL.md) 和 MCP stdio 服务。[官方接入说明](https://github.com/ant-design/ant-design-cli/blob/main/README.zh-CN.md#-agent-集成)

| 能力 | 本体系如何使用 |
| --- | --- |
| `antd` React 依赖 | 在任务页面中直接使用官方基础控件；复用项目主题与 ConfigProvider |
| 官方 `antd` Skill | 指导组件 API、示例、Tokens、调试与版本查询，按当前任务联合读取 |
| 官方 CLI | 通过 shell 查询组件、文档、示例和主题；支持按项目 antd 版本查询 |
| 官方 MCP | 已连接时通过工具查询相同知识，适合频繁选型和设计实现；不作为所有任务的必装前置 |
| 我们的共享源码 | 补充经验证的组件组合与交互模式，复制或参考到项目直接维护 |

`dev-product` 定义任务、交互和验收，官方能力提供组件知识；业务规则、最终设计选择及真实页面验收仍按本体系完成。第三方 Skill 保留上游身份和来源，通过联用或安装接入，不改名登记成自建能力。

## 如何选型与核验

核对项目有效组件、设计资产与锁文件中的实际 antd 版本。先查官方组件和示例，现成能力满足时直接使用；必要时通过公开属性、主题 Tokens 和组件组合扩展。共享源码只是候选补充，自建前说明尚未满足的具体需求。

按问题调用：选型看组件列表和设计规范；实现查 API 与示例；定制看 Tokens 与公开样式接口。查询针对相关组件，不要求每个任务跑全套命令。CLI 的 `--version` 表示目标 antd 版本，CLI 自身版本另行记录；已有项目不自动升级到新大版本。查询快照缺少目标版本时，核验对应官方版本文档、源码及差异，并说明覆盖边界。

设计语言命令 `antd design.md` 当前只支持 antd v6。v4/v5 项目参考适用版本的规范与主题文档，不能因查询缺失而迁移项目。[官方命令与版本说明](https://github.com/ant-design/ant-design-cli/blob/main/README.zh-CN.md)

项目采用记录关联组件选择、来源、实际项目版本、定制原因和页面验证。CLI lint 可辅助检查废弃用法；类型检查、运行操作和视觉验收仍验证最终项目行为。

## 发现与自主安装

先检查当前可用 Skills、`antd` CLI 和实际连接的 MCP，复用已验证接入。能力缺失且有助于当前任务时，Agent 可在当前授权与宿主权限范围内自主安装官方能力。默认采用项目级 Skill 和项目开发工具或临时 CLI；用户要求全局共享时再采用用户级安装。读取来源与实际安装行为，保留项目既有配置及其他 Skills；遇到文件冲突先比较合并。

CLI 支持 Node.js 20 及以上。Codex 的官方 `setup` 当前只安装项目 Skill，并维护项目 `AGENTS.md` 的指引区块；不会为 Codex 配置 MCP。下面是官方项目接入入口，实际使用时确认并记录所采用的 CLI 版本，可将包名限定为该版本以复现：[官方 setup 说明](https://github.com/ant-design/ant-design-cli/blob/main/README.zh-CN.md#antd-setup)

```sh
# 在目标项目中预览将要写入的 Skill 和指引
npx --yes @ant-design/cli setup --client codex --mode skill --project . --dry-run --format json
# 核对变更后，完成当前任务所需的项目接入
npx --yes @ant-design/cli setup --client codex --mode skill --project . --format json
npx --yes @ant-design/cli setup --client codex --mode skill --project . --check --format json
```

也可按官方说明通过 `skills` CLI 选择 `ant-design/ant-design-cli` 的 `antd` Skill；采用哪种入口取决于既有工具和安装范围，无需两套重复安装。新装 Skill 先读取其实际内容；宿主未刷新发现时可以从文件读取，不声称新会话发现已通过。

官方 Skill 包含全局安装及自动更新示例。本体系联用时以本次用户要求、安装范围和可复现版本约定为准：按既定入口调用 CLI，更新提示按实际需要处理，不自动改动项目 antd 版本或锁文件。能力不可安装或暂不可用时继续以对应官方文档/源码核验，明确工具缺口即可。

MCP 的启动入口为 `antd mcp`，由宿主可用的 MCP 配置入口接入，保留其他连接。根据所采用 CLI 的实际启动参数和工具 schema 核对目标版本。项目级连接采用该项目版本；多项目共享连接遇到版本不匹配时改用版本匹配的 CLI 查询。接入或升级时根据实际工具 schema 核验版本支持，避免把某个项目版本固定为所有项目默认。无需为了联用 Skill 同时安装 MCP。

安装记录保存官方来源、CLI/Skill 实际版本或哈希、安装范围、验证结果及适用项目；复用前核验当前有效性。工具不指定 Agent 模型或推理强度。公开查询与本地接入不包含向外提交 Issue 等额外外部操作的授权。
