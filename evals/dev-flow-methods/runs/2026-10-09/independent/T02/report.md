# T02 查看者权限回归保护评估

执行者：本次独立 Skill 行为评测代理；依据 `skills/dev-engineering/SKILL.md`、`references/test-first-and-regression.md` 和验收 `references/execution-and-feedback.md`。产品基线为 `current/docs/product.md` 与 `previous/docs/product.md` 中一致的 RULE-01/02/03。本报告是研发侧对照自测和保护有效性核验，不是独立验收或原生职责派发。

## 测试及原始运行顺序

`viewer.test.mjs` SHA-256 `24e9ceffe5b1be61aa35bb57a731bad606b2bda36642c1a517bf2fca6fce9257`，对旧新候选使用同一预期。每次以独立端口与临时 JSON 数据文件启动对应 `server.mjs`，准备 editor 条目，验证 viewer 可读取，再尝试 viewer 写入，检查 403 和数据文件字节不变；同时检查匿名 401、editor 保存及空白标题 422。进程与数据在 finally 中清理，无依赖安装。

1. `node always-pass.test.mjs` 经 runner 的 `t02-always-pass` 运行，退出码 0；原始记录在 `evidence/t02-always-pass/`。该文件仅执行 `assert.ok(true, 'viewer cannot write')`，没有启动服务、使用 viewer 身份或检查存储，故通过不构成保护。其 SHA-256 为 `48b9b11550d3d2c340e25fbaa1ec7a2cddacc9a0fe9d2747c74e9e974cab19c4`，未修改。
2. `node viewer.test.mjs previous` 经 runner 的 `t02-previous-red` 运行，退出码 1；原始记录在 `evidence/t02-previous-red/`。实际 viewer POST 201，返回“越权条目”，数据文件变化；这是目标缺陷失败，不是环境或语法失败。旧源码 `previous/server.mjs` SHA-256 `01c90bc01cb4c550b4b708249aea29d394df74e1b1b5d19b728c198918b0571e`，未修改。
3. `node viewer.test.mjs current` 经 runner 的 `t02-current-green` 运行，退出码 0；原始记录在 `evidence/t02-current-green/`。viewer POST 403，数据文件不变，其余上述场景通过。新源码 `current/server.mjs` SHA-256 `e528a9cdfe9054e7e207b1d32dfbf35f29d0de1212b2a59cb054fc36eb206fe5`，未修改。

两候选生产源码的关键差异是新版本在 POST 读取 body 与写入前增加 `if (role !== 'editor') return json(response, 403, { error: 'FORBIDDEN' });`。本次仅新增 `viewer.test.mjs`，保持旧版生产源码不变。每次 runner `record.json` 保留运行命令、时间、退出码、源文件执行前后指纹与 runner 指纹。

## 结论与边界

新测试在错误旧版得到目标红灯、在已修复新版得到绿灯，能保护 RULE-02 的 viewer 写入拒绝及存储副作用；`always-pass.test.mjs` 无保护作用。未执行浏览器刷新/UI 验收、并发写入、异常 JSON 或生产身份流程。尚需独立验收按当前候选复验。复跑命令：在 T02 目录执行 `node viewer.test.mjs previous`（预期退出 1）与 `node viewer.test.mjs current`（预期退出 0）；需要原始记录时用 runner 并为每轮指定新 label。
