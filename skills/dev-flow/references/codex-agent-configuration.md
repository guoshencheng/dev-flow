# 职责 Skills 与执行者

本插件通过流程 Skill 和六个专业 Skills 提供能力，Codex 不要求注册原生职责 Agent，也不需要 setup。Kimi 通过同包清单发现六个独立职责入口，派发和双端同步见 [Kimi 职责说明](kimi-agent-configuration.md)。安装、更新与解除见[插件维护指南](../../../docs/plugin.md)。

主 Agent 按[任务路由](task-routing.md)选择产品、视觉、架构、研发、测试或运维方法，读取对应专业 Skill 承担工作。专业职责是分工，不自动表示存在独立执行者。

需要且获准委派时，使用宿主实际可用的子 Agent，提供对应 Skill 的绝对路径、目标、输入及版本、可写范围、产物位置、验收与交接要求。模型和推理强度遵循用户及宿主本次约束，不写死在插件中。不能委派时由主 Agent 执行并记录实际方式；自查与独立 Review 分别表达。

是否委派、各流程的默认安排、并发边界与交接见[subagent 使用建议](subagent-guidance.md)；工作目录、分支和隔离安排见[Git/worktree 建议](git-and-worktree.md)。只读 Review 不默认建立 worktree，实施并发有明确写入者，集成后重新验证。

插件安装检查、专业行为和项目资产复用分别验证。Skill 能被发现不表示已完成某项任务，执行结果必须有对应成果和证据。
