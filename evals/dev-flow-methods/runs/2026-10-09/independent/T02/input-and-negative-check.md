# T01/T02 评测输入范围与语法负例判读

## 实际读取的输入

本代理在 T01/T02 实施前读取了以下文件内容：

- `skills/dev-engineering/SKILL.md`
- `skills/dev-engineering/references/test-first-and-regression.md`
- `skills/dev-acceptance/references/execution-and-feedback.md`
- `.dev-flow/methods-eval-20261009/T01/project/{docs/product.md,server.mjs,package.json}`
- `.dev-flow/methods-eval-20261009/T02/{always-pass.test.mjs,current/{docs/product.md,server.mjs,package.json},previous/{docs/product.md,server.mjs,package.json}}`
- `evals/dev-flow-methods/run.py`

另执行 `rg --files` 仅列出上述案例与 runner 路径；实施后读取了自己运行生成的 T01/T02 runner `record.json`，用于报告时间、退出码和源文件指纹。此前的任务上下文包括用户提供的仓库 AGENTS.md 指令、环境信息和主 Agent 下达的 T01/T02 评测任务；未获得事先的评测答案、标准补丁或其他案例分析。完成后才收到主 Agent 独立复跑结果一致的反馈。

没有读取 `prepare.py`、`check_controls.py`、建设计划、其他评测/答案、D01/R01 等其他案例内容或标准补丁。本次追加读取了 `.dev-flow/methods-controls-20261009/evidence/syntax-negative/{stdout.txt,stderr.txt,record.json}` 三份原始日志。该 `record.json` 的指纹清单列有 D01/R01/T01/T02 等文件名与 SHA-256；这些是 runner 输出的元数据，不等于读取了所列文件的内容。此处只陈述实际操作边界；环境没有文件级沙箱，不能据此声称技术上无法访问其他文件。

## `syntax-negative` 判读

这次退出码 1 **不足以证明** viewer 权限缺陷被捕获。原始 `record.json` 显示命令是 `node --input-type=module -e 'const = 1'`；`stderr.txt` 显示 `SyntaxError: Unexpected token '='`，`stdout.txt` 为空。Node 在解析无效 JavaScript 时就退出，没有启动案例 HTTP 服务、设置 viewer 身份、执行 POST 或观察 JSON 存储。该失败属于测试/命令语法错误，与 RULE-02 的预期 403 和无写入副作用无关；单看退出码会误判目标红灯。

下一步应排除语法错误后，用有效测试命令实际启动隔离服务，准备 viewer 身份与独立数据文件，执行 POST 并同时断言 403 与文件内容不变；将同一测试用于旧版和新版，保留旧版目标失败及新版通过的原始记录。T02 已有的 `viewer.test.mjs` 及 `evidence/t02-previous-red/`、`evidence/t02-current-green/` 正是这类目标行为证据。这里没有修改案例源码、测试或原报告。
