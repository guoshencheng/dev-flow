---
name: dev-engineering
description: 研发设计、实现与修复：设计期基于真实代码反馈产品/UI，主笔合并架构与实现的设计，经独立跨职责 Review 后编写实施计划，连续实现、自测与集成，交完整候选进行实现 Review、正式验收及交付核验。
---

# 研发实现与修复

先读共同[总纲](../dev-flow/references/constitution.md)，按用户本次目标裁剪。设计、计划、Review 和交接使用中文。模型与强度遵循用户和宿主本次设置，不写入专业方法。

## 恢复与设计期反馈

从项目唯一进度入口恢复范围、阶段、有效产品规则与业务完成标准、UI、架构约束、实施授权和候选版本；核对真实代码、工程入口、已有修改与权威资产。旧项目的有效权威文件可通过索引映射复用，不强制迁移或复制。局部缺陷在有效预期内按根因、简短计划、修复和定向验证裁剪。

产品/UI 设计期间，研发沿真实入口读取受影响组件、接口、状态与数据链路，比较功能放在不同位置或采用不同交互形式所需的模块、共享状态和维护成本。对有争议的状态说明真实触发、用户价值、操作差异和实现代价；提出满足原业务目标的替代方式。重要取舍由产品/UI 及用户按影响确认，技术不能单方缩减已确认需求。

## 设计、Review 与计划

研发主笔 `docs/dev-flow/iterations/<迭代ID>/engineering/design.md`，把本轮架构与实现设计合并，讲清目标、核心业务链路、模块/数据/接口/权限、异常恢复、代码位置、验证和交付。方法见[研发设计](references/technical-delivery-design.md)，模板见[设计模板](assets/templates/technical-delivery-design.md)。重大系统专题可另建架构设计，但每轮默认不另产一份架构方案。

独立架构执行者 Review 设计，产品/UI 核对业务目标、行为与实际呈现承接；各自依据真实对象版本提出发现。意见、作者处理及定向复核写入[独立 Review](assets/templates/engineering-review.md)，设计只引用有效链接、版本、状态和简短结论。作者自查须如实标记，不冒充独立 Review。

设计 Review 通过、业务预期及重要取舍有效后，研发按[工程基线与计划](references/baseline-and-plan.md)编写[实施计划](assets/templates/implementation-plan.md)，由独立执行者复核依赖、变更范围、测试保护、集成和交付。实施前核对已明确的同范围授权；已有授权直接复用。完整正式 TC 在完整功能实现后维护、独立 Review 并执行，不作为实施前置；研发局部测试、缺陷复现和必要回归随实现进行。

## 连续实现与完整候选

按[切片与集成](references/slices-and-integration.md)沿稳定契约分派可独立实现的工作，持续集成和自测，不设逐片正式验收门槛。前端按[前端实现](references/frontend-implementation.md)落实真实数据和必要状态；按[测试保护](references/test-first-and-regression.md)验证目标行为；缺陷按[诊断](references/diagnosis-and-feedback.md)复现、修复和回归；兼容变化按[兼容方法](references/compatible-changes.md)核对消费者及恢复。

完整功能和核心任务可运行后交完整候选。独立架构执行者 Review 任务开始基线至候选的完整代码变化，产品/UI 检查真实流程与呈现；测试以原要求、有效设计及实现入口维护正式验收用例，经独立 Review 后执行功能和交付核验。研发按[意见处理](references/review-feedback.md)修复关联问题，提交新候选并配合定向复评/复验。不能修改预期迁就实现，不能把局部自测报告成正式验收。

标准领域任务在 Harness 可用且允许委派时默认交专业 subagent。派发给出原目标、权威输入版本、成果位置、写入边界、验收条件和共享资源负责人；设计、计划、代码作者与独立评审分离。主会话持续协调、集成和维护唯一 Todo/Progress；设计和计划只引用整体进度，不另设状态权威。无法独立委派时如实记录执行方式与独立性缺口。

## 交付与沉淀

按[工程资产与交付](references/project-assets-and-delivery.md)交接候选、实际命令/结果、失败与待复验、配置/启动入口和限制。向架构技术收尾提供实际模块/契约变化、设计差异、源码版本及自测证据；验收和运维的真实结果分别引用原记录。架构形成 `architecture/closeout.md` 后，设计引用其有效结论。项目长期工程索引保留在 `docs/dev-flow/engineering/`，迭代文档由索引映射；普通运行日志留在项目约定本机目录。

代码收尾遵守[共同协议](../dev-flow/references/git-and-worktree.md#代码收尾)，保留无关修改。需要细化职责能力时读[能力目录](../dev-flow/references/role-capabilities.md)；方法变更和真实项目验证分别登记。
