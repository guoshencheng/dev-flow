# T01 研发自测与待验交接

执行者：本次独立 Skill 行为评测代理，按 `skills/dev-engineering/SKILL.md`、`references/test-first-and-regression.md` 及验收 `references/execution-and-feedback.md` 裁剪执行；未发生原生职责派发或独立验收。项目基线为 `project/docs/product.md` RULE-01/02/03。隔离案例直接实施，不涉及部署。

## 候选、修改与先后证据

1. 编写 `project/behavior.test.mjs`，SHA-256 `0478b46094d94ca196be4772d7b76c2625d0c45e55e0be28dc05bbe57f6adb39`。Node 启动真实 HTTP 服务，自动分配端口、独立系统临时 JSON 文件，结束时关闭服务并删除临时数据。先由 editor 存入一条记录，再以 viewer 读取和尝试 POST；核对返回码与数据文件原始内容，并检查匿名及空白标题。
2. 修改前运行 `python3 /Users/guoshencheng/Documents/work/dev-flow/evals/dev-flow-methods/run.py --project /Users/guoshencheng/Documents/work/dev-flow/.dev-flow/methods-eval-20261009/T01/project --label t01-red -- node behavior.test.mjs`，退出码 1。原始证据：`project/evidence/t01-red/{record.json,stdout.txt,stderr.txt}`。失败确实到达 viewer POST：预期 403，实际 201，返回了“越权条目”，数据文件同时变化。旧 `server.mjs` SHA-256 `01c90bc01cb4c550b4b708249aea29d394df74e1b1b5d19b728c198918b0571e`。
3. 生产源码只增加一处权限门禁：在 POST `/api/items` 分支读取 body 和写入之前，`if (role !== 'editor') return json(response, 403, { error: 'FORBIDDEN' });`。新 `server.mjs` SHA-256 `e528a9cdfe9054e7e207b1d32dfbf35f29d0de1212b2a59cb054fc36eb206fe5`。原测试未修改。
4. 修改后运行同一命令（label `t01-green`），退出码 0；原始证据：`project/evidence/t01-green/{record.json,stdout.txt,stderr.txt}`。RULE-01 editor 保存/去空格、viewer GET，RULE-02 viewer 403 且存储字节不变、匿名 401，RULE-03 空白 422 且存储字节不变均通过。两次 runner 记录包含各自命令与执行前后文件指纹。

## 范围与待验

这是研发自测通过的待验候选；独立验收未执行。测试检查页面返回 HTML 含列表读取脚本，但没有浏览器刷新和 UI 交互验收；没有覆盖并发写入、异常 JSON、生产身份机制。复跑时采用新的唯一 label，执行 `node behavior.test.mjs` 或上述 runner 命令。无需依赖安装。
