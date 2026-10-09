# 可执行研发方法评测

对应[改造计划](../../docs/plans/2026-10-09-executable-engineering-methods.md)。跨研发、架构和验收复用六职责，不新增 Agent。新方法见[测试保护](../../skills/dev-engineering/references/test-first-and-regression.md)、[实验诊断](../../skills/dev-engineering/references/diagnosis-and-feedback.md)、[完整实现评审](../../skills/dev-architecture/references/retrospective-and-evolution.md)和[意见处理](../../skills/dev-engineering/references/review-feedback.md)。

## 输入与运行

`prepare.py` 从既有 HTTP/UI 样本构造新的隔离输入：T01 缺失行为、T02 旧/新候选和无效测试、D01 三个同症状项目、R01 三次提交及相关未提交内容。固定契约保存在各工程 `docs/product.md`，样本采用 Node HTTP、JSON 文件及遗留 HTML/JS，不代表生产身份或数据库能力。

```sh
python3 evals/dev-flow-methods/prepare.py --root .dev-flow/methods-new-run
python3 evals/dev-flow-methods/check_controls.py --root .dev-flow/methods-new-run --report .dev-flow/methods-new-run/control-results.json
```

准备目录必须尚不存在，报告不覆盖。工具对照与模型行为使用不同副本；上面第二条命令用于构造者核验输入，不交给被评测执行者。`prepare.py` 和 `check_controls.py` 包含注入/判据，不在盲测输入范围内。

向独立执行者提供专业 Skill、角色任务、原始契约、指定案例工程、可写范围和证据要求。D01 不告知变体原因，R01 先要求独立只读评审，再向另一个研发执行者交评审报告和意见；澄清由意见提供方答复。不得提供标准答案补丁或用 runner 自动修复来代替执行者。

记录真实命令：

```sh
python3 evals/dev-flow-methods/run.py --project .dev-flow/methods-new-run/T01/project --label red -- node behavior.test.mjs
```

测试由执行者编写，上例不是预置答案。runner 保存命令、时间、退出码、原始输出和前后文件指纹，证据目录 label 必须唯一。目标失败、准备/语法失败及未执行由证据核验者分类，退出码本身不证明检出；超时终止本次进程组并记未完成。服务/端口/数据由测试隔离与清理。

## 成功判据与证明边界

| 案例 | 成功判据 |
| --- | --- |
| T01 | 同一测试先因目标行为失败，生产修改后通过，顺序与指纹可核验 |
| T02 | 同一有效测试旧失败/新通过，拒绝无写入；识别始终通过测试的无效性，不能凭新版本一次通过声称保护 |
| D01 | 实际浏览器保存/刷新、HTTP/存储取证与必要控制实验区分三个根因，再最小修复并回归；准备错误不算目标失败 |
| R01 | 评审覆盖开始基线至最终候选全部提交与未提交内容；正确意见修复，错误意见以证据反驳，模糊意见先澄清；修复后定向复评和实际复验 |

本轮结果与版本见[报告](report.md)。保留历史失败与后续运行，不覆盖原证据。记录独立评审、研发自测、主 Agent 复跑和最终验收的实际执行方式；隔离案例不替代真实项目完整协作、生产部署或新机器交付。
