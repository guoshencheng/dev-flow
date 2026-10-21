---
name: release-and-recovery
description: 执行已授权的产物发布、应用回退、数据恢复和运行资源退役，核验实际版本及恢复结果。
---

# 发布与恢复操作

明确本次模式和具体授权：发布输入是候选/产物与目标，恢复输入是受影响版本、状态/数据、备份和兼容条件。两种模式分别核验，发布授权不自动覆盖破坏性数据恢复或资源删除。

发布模式按版本身份、目标配置和项目已有入口操作并核验；恢复模式先判断应用回退与数据恢复的不同前置，按 runbook/演练执行。结果未知先查询实际状态，不盲目重复发布或迁移。

交接源/产物/部署映射、实际运行或恢复证据、回退限制和未执行项。命令成功不证明业务任务通过；运维给运行事实，测试核验约定行为。

## 按需读取

- [发布模式：候选、产物与目标版本](references/artifacts-and-release.md)。
- [恢复模式：应用/数据、备份与演练](references/recovery-and-migrations.md)。
- [资源演进与退役](references/evolution-and-retirement.md)。
- [交付记录](assets/templates/delivery-record.md)。
- [事故与恢复记录](assets/templates/incident-and-recovery.md)。
