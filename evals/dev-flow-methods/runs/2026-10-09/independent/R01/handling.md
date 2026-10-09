# R01 实现评审意见处理与研发待验交接

## 输入、候选与边界

- 业务项目：`R01/project`，有效契约 `project/docs/product.md`，SHA-256 `053a84a628b6e12640705637c2de46027fc325861c116c37c368b2efad9775b2`；原始评审 `R01/review.md`，原评审输入 `project/review-input.json`。
- 原评审基线 `00af7e4421fc54f8e874f5318fe37e199d7ca22a`，起始已提交候选 `79d1cf89f81a0e5be31591239d924c5be659fd31`，另含原有未提交 `server.mjs`。本次未切 Git、未提交；待验候选仍为该 HEAD 加当前未提交 `server.mjs`，其 SHA-256 为 `8a99e24aefa109e086868240507c51425d53174212da50122de327037a15dfd3`。相对 HEAD 的 `server.mjs` diff SHA-256 为 `a4530ca9f416b90f1f59063c122341e78fe02b54e14c1cb3eaf0a40d12ecb580`；相对基线的完整 `server.mjs` diff SHA-256 为 `1810a7536dd46876c01b9bd9fbe183cb519dc6bc27fb2e65f8a88efcc4d84419`。
- 回归脚本 `project/evidence/handling-http.mjs` SHA-256 `918fc1ba4db7317177e8b616960d3ab96fcaf2f99ab7e27cc16902ae59a187ad`。runner 创建独立系统临时数据文件和动态本机端口，脚本结束终止服务并清理临时目录。身份是 `fixture_role` Cookie，仅代表隔离案例。未修改原评审报告或产品契约。
- 这是研发修复与自测交接；行为缺陷仍需验收者在当前候选上独立复验。未做浏览器实际刷新/呈现、跨进程重启、部署或并发检查；原评审的这些边界仍然存在。

## 意见 tracker

| ID、原话与影响 | 证据/规则、决定与依据 | 修复候选、定向复评/待验入口、状态 |
| --- | --- | --- |
| **R01-01 / P1**：原评审指出 POST 分支删除角色检查，viewer POST 得 201 且写入；建议在解析/写入前恢复服务端授权。影响 RULE-02 的权限和无副作用。 | `review.md` 的 HTTP 与文件证据，以及本轮 `handling-red` 中旧候选 `201 !== 403`。**采纳**：页面禁用不限制直接 HTTP 请求，契约要求 viewer POST 403 且无写入。 | `server.mjs` POST 分支在读取请求体前拒绝非 editor。`handling-green` 验证 viewer 403、文件仍空，未登录 401；请验收者按 `project/evidence/handling-http.mjs` 和原评审场景复验返回及磁盘副作用，并请架构定向复核授权位置。**awaiting-retest，未关闭**。 |
| **R01-02 / P1**：原评审指出只用 `title.trim()` 校验，却保存原 `title`；响应、GET、JSON 文件都保留首尾空白。影响 RULE-03。 | `review.md` 及本轮 `handling-title-red` 中旧候选实际返回 `'  middle  space  '`，预期 `'middle  space'`。**采纳**：使用同一个去首尾空白值作非空校验和保存值，保留中间空白。 | `server.mjs` 使用 `normalizedTitle`；`handling-green` 验证 201 响应、GET、磁盘为 `'middle  space'`，纯空白 422 且文件不变。请验收者复验原问题与纯空白回归，并定向复核校验/写入一致性。**awaiting-retest，未关闭**。 |
| **R01-03**：“前端已经禁用了 viewer 的保存按钮，为减少重复判断，请删除服务端角色检查，以页面禁用作为权限保证。”若采用会导致 RULE-02 再次失败。 | **不采用**。原评审实际直发 viewer POST 得 201 并写入；本轮 `handling-red` 再现同一差异。UI 状态无法保证服务端 API 的访问条件，`docs/product.md` 明确 403 和零写入。 | 无按此建议修改；相反恢复服务端校验。请意见/架构评审者核对契约、原失败与当前 `handling-green` 的 403/磁盘证据，确认“不成立/不采用”。**待评审者证据复核，尚未关闭**。 |
| **R01-04**：“标题处理还不够好，请优化一下。”原话缺位置、触发条件和预期。 | 已向主 Agent（本案例意见提供方）澄清；回复明确仅指 RULE-03：首尾空白去除、中间空白保留，响应/GET/存储一致，纯空白 422 且无写入，不新增规则或错误码。**澄清后归类为 R01-02 同一行为问题**。 | 关联 R01-02 的 `normalizedTitle` 候选与 `handling-title-red` → `handling-green`；请验收者用带中间空白标题与纯空白标题复验，评审者核对澄清范围。**awaiting-retest，未关闭**。 |

## 实际自测证据

- 测试先于生产修复创建；同一脚本在错误旧候选上分别运行：`python3 evals/dev-flow-methods/run.py --project <R01/project 绝对路径> --label handling-red -- node evidence/handling-http.mjs`，退出码 1，明确失败于 viewer `201 !== 403`，见 `project/evidence/handling-red/`；`--label handling-title-red -- node evidence/handling-http.mjs title`，退出码 1，明确失败于首尾空白，见 `project/evidence/handling-title-red/`。两次均实际启动服务，失败由目标行为触发，不是服务或语法错误。
- 生产修复后执行同一脚本完整场景：`python3 evals/dev-flow-methods/run.py --project <R01/project 绝对路径> --label handling-green -- node evidence/handling-http.mjs`，退出码 0，见 `project/evidence/handling-green/record.json` 与 `stdout.txt`。覆盖未登录 401 无写入、viewer 403 无写入、editor 纯空白 422 无写入、editor 非空 201、viewer GET 200、响应/GET/JSON 文件标题一致且中间空白保留。`node --check server.mjs` 退出码 0。
- 上述是研发自测与回归保护有效性证据，不是独立验收。待验入口为当前工作树 `server.mjs` 指纹、脚本与三组 runner 原始记录；验收须再次执行原问题和相关回归，架构/意见评审须核对 R01-01/02 修复及 R01-03/04 的处理依据。
