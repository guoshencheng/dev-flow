---
title: 独立收尾 Skill 实施计划
status: current
version: 2
---

# 独立收尾 Skill 实施计划

有效输入为[设计 v1](design.md)和 [Progress](../Progress.md) 中用户确认及实施授权。主 Agent 是本轮实现唯一写入者，独立执行者只写其 Review/隔离验证范围；设计 v1、计划 v2 及完整实现 C1 静态 Review 均已通过，见 [Review](review.md)。

## 一、实施目标与前置条件

交付可发现、可直接调用且实际引导长期文档回写的收尾 Skill，保留原流程门槛及文档/Git 权威边界。执行目录为本仓库 `/Users/guoshencheng/Documents/work/dev-flow`，复用 `main` checkout，开始提交 `10c6e124447c6c8013935ece937221f269f074c6`；初始工作树干净，本轮已有改动仅为本计划目录及独立 Review，源码由主 Agent 唯一写入，无需另建 worktree。无业务服务、数据或生产发布要求。

## 二、实施步骤与依赖

| 顺序 | 工作与唯一写入者 | 完成结果 |
| --- | --- | --- |
| 1 | 主 Agent 新建 `skills/iteration-closeout/SKILL.md` 及必要发现元数据 | 触发、盘点、有效性判断、回写、保存及实际输出要求明确 |
| 2 | 主 Agent 接通 dev-flow、文档管理及直接有关的职责/模板/能力声明 | 唯一操作入口与权威来源不冲突；Progress 可单独看到文档回写条件 |
| 3 | 主 Agent 更新长期 README/安装指南/权威归属，升级 0.7.0 并生成入口 | 17 Skills、双插件版本及 Codex/Kimi 生成一致 |
| 4 | 主 Agent 修正安装测试的两处固定 16 预期并纳管新增文件 | 从夹具 `capabilities.json` 取得完整预期 Skill 清单，包校验比对完整列表、安装结果比对清单长度；断言新 Skill 已声明且正文按字节入包 |
| 5 | 独立执行者 Review 完整候选并进行隔离行为验证，主 Agent 修复 | 发现有处理和定向复核；真实文件回写与保留边界有结果 |
| 6 | 主 Agent 执行候选检查、源码保存、本机 install/check 和本轮收尾 | 实际启用、缓存/源码指纹一致，长期入口已同步，遗留如实交接 |

不涉及数据库或 UI 对接，裁剪对应计划小节。共享文件及生成操作始终由主 Agent 维护。

## 三、测试保护与持续集成

- `quick_validate.py` 校验新 Skill；`sync_host_agents.py --write`/`--check` 核对完整包引用与宿主入口。
- 对完整变更检查 Markdown 文件链接、JSON 解析和 `git diff --check`。
- 因调整安装测试预期，执行 `python3 -m unittest discover -s tests -p 'test_plugin_installation.py'`；保留隔离打包、来源缓存和用户配置保护覆盖。
- 独立行为执行使用临时项目及本地忽略目录，检查实际正文结果，禁止操作真实业务项目、推送或发送消息。

## 四、完整候选与验收安排

完整候选包含 Skill、原入口接通、权威边界和长期说明、能力声明/生成入口及版本。独立候选 Review 覆盖开始基线至最终实现和相关未提交内容；行为验证在固定包内容上执行。源码变化后只针对受影响部分复核，不以静态检查代替实际文档回写。

## 五、计划 AI 复核引用

[独立 Review](review.md#plan-r2) 的计划 v2 通过；计划 v1 的 P1-1 执行基线和 P1-2 动态清单与新 Skill 入包验证均已在 v2 明确，由原评审者定向复核关闭后开始实现。已确认授权继续有效，不新增人工逐文件批准。

## 六、执行与重要调整

实时进展统一见 [Progress](../Progress.md)。实际发现、修订与复核记录到 Review，行为原始执行记录留本地忽略目录；本篇只记录安排与重要调整。

初次源码提交和安装完成后发现其他会话修改共享工作区。最终操作改为只提交本轮记录，并在该提交的隔离Git副本构建、核验并安装；保留原来源目录及角色归属，不改管理脚本、不纳入或回退他人未完成修改。最终核验缓存与本轮提交候选，全工作区差异另行如实说明。此项是输入隔离调整，原Skill语义及C1 Review范围不变。

## 七、引用与关联文档

- [设计](design.md)、[唯一 Progress](../Progress.md)。
- [总纲](../../../../skills/dev-flow/references/constitution.md)、[文档管理](../../../../skills/document-management/SKILL.md)、[Git 工作流](../../../../skills/git-workflow/SKILL.md)。
- [Review](review.md)、[独立技术收尾](../architecture/closeout.md)；技术收尾绑定提交afca71a和初次安装，最终记录候选的命令结果由Progress及完成说明交接。
