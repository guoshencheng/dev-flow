# 工程资产、集成交付与新上下文

项目文档在 `docs/dev-flow/` 下维护，先复用已有有效权威位置，通过迭代索引映射，不强制迁移或复制。无约定时本轮使用：

| 资产 | 默认位置与维护内容 |
| --- | --- |
| 工程索引 | `engineering/index.md`：真实安装单元、命令、代码映射和权威入口 |
| 研发设计 | `iterations/<迭代ID>/engineering/design.md`：业务链路、架构及实现的统一设计 |
| 独立 Review | `iterations/<迭代ID>/engineering/review.md`：设计、计划、完整实现的对象版本、发现、处理和复核 |
| 实施计划 | `iterations/<迭代ID>/engineering/implementation-plan.md`：步骤、依赖、自测、集成与交付安排 |
| 架构技术收尾 | `iterations/<迭代ID>/architecture/closeout.md`：实际实现与设计差异、验证、资产和遗留 |
| 工程交接 | `iterations/<迭代ID>/engineering/handoff.md` 或现行任务/PR：候选、自测、启动与待验项 |
| 规范、自动化与源码 | 复用项目权威位置，文档引用实际配置和代码 |

模板为[工程索引](../assets/templates/engineering-index.md)、[设计](../assets/templates/technical-delivery-design.md)、[Review](../assets/templates/engineering-review.md)、[计划](../assets/templates/implementation-plan.md)和[交接](../assets/templates/engineering-handoff.md)。正式 Review 的结论及未关闭项持久保存；普通运行日志和重试过程留在项目约定本机目录。总体进度仅由现行 Todo/Progress 维护，各文档引用其阶段与候选状态。

交接声明源码候选、真实命令与结果、配置/身份/数据准备、启动/停止入口、核心任务、已知缺口及适用环境。构建、健康与核心任务分别验证；开发服务可访问不自动等于完整交付。研发自测、正式验收、可运行交付与部署状态分别记录。运维提供实际环境和产物版本，验收执行后置正式用例及交付核验，架构收尾引用原证据。

代码收尾核对完整差异、必要 Review 与验证、相关源码/测试/文档保存，保留无关修改。更新受影响工程索引、有效设计/计划引用及诊断知识；未实现目标或旧候选通过不能覆写当前事实。
