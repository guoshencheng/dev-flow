# R01 实际实现评审

## 结论与版本

- **需求符合性：阻断。** 当前候选违反 RULE-02（viewer 禁止写入且返回 403）和 RULE-03（保存标题去除首尾空白）。RULE-01 的 editor 创建、201、GET 可读在隔离 HTTP 检查中成立；浏览器刷新后的页面呈现未实际执行。
- **实现质量：阻断。** 服务端仅通过角色 Cookie 进行登录判断，POST 分支已失去授权检查，页面按钮禁用不能阻止直接请求。标题校验与持久化使用不同形式，造成输入规范化不变量失效。其余范围内没有证据支持更广泛的质量结论。
- 评审对象是独立临时项目 `/Users/guoshencheng/Documents/work/dev-flow/.dev-flow/methods-eval-20261009/R01/project`。原始契约为 `docs/product.md`，输入为 `review-input.json`。起始基线 `00af7e4421fc54f8e874f5318fe37e199d7ca22a`，最终已提交候选 `79d1cf89f81a0e5be31591239d924c5be659fd31`，另有相关未提交修改 `server.mjs`。HEAD 在 `main`，评审未切换分支、提交或修改生产源码。
- 基线至候选经过 `c4c5ab7`、`0c89846`、`79d1cf8` 三次提交。已核对基线到最终提交以及最终提交到工作树的两个 diff，不以最后一次提交代替完整评审。基线到最终提交：`server.mjs` 5 行变更（2 增、3 删），删除 POST 角色检查；未提交修改将保存值从 `title.trim()` 改成 `title`。其余变动为页面标题及 `/health.kind` 文本。
- 指纹：评审时工作树 `server.mjs` SHA-256 `573b7f1c48e7a9159951b5b86e00c7a08af8994e07d8a017e1b3e970dd1b587e`；基线至工作树的 `git diff ... -- server.mjs` SHA-256 `4628fe59043200ae40e34ccb30d0beb5f7c76a39bde3e5efb8a1912210744a86`；候选至工作树的未提交 diff SHA-256 `186bdae9404bf57435e1d43217ffdc3f915f8bc70f278bd98fd1d143135d97aa`。契约 SHA-256 `053a84a628b6e12640705637c2de46027fc325861c116c37c368b2efad9775b2`。评审时另有原有未跟踪 `review-input.json`；本次增加的检查脚本和结果只位于 `project/evidence/`。

## 意见

| ID / 优先级 | 关联契约与位置 | 证据、影响及处理建议 | 状态 |
| --- | --- | --- | --- |
| R01-01 / P1 | RULE-02；`server.mjs:57-70`，POST 分支第 64 行起 | `c4c5ab7` 所在完整 diff 删除了 `if (role !== 'editor') return ... 403`。实际以 `fixture_role=viewer` POST 非空标题得到 **201**，返回条目，并在隔离 JSON 文件中看到持久化。viewer 本应 403 且无存储写入。应恢复服务端写入授权，在解析/写入前拒绝 viewer，并复验返回码及文件不变。 | 阻断，待研发处理和独立复验 |
| R01-02 / P1 | RULE-03；`server.mjs:65-69` | 未提交 diff 将 `item.title` 从 `title.trim()` 改为原值；当前只用 `title.trim()` 判断非空。实际 editor POST `"  trimmed  "` 得 201，响应、GET 和 JSON 文件均保留两端空白，违反标题规范化规则。应以裁剪后的值校验并持久化，同时复验纯空白 422 无副作用。 | 阻断，待研发处理和独立复验 |

## 实际检查与边界

- 使用 `python3 /Users/guoshencheng/Documents/work/dev-flow/evals/dev-flow-methods/run.py --project /Users/guoshencheng/Documents/work/dev-flow/.dev-flow/methods-eval-20261009/R01/project --label review-http -- node evidence/review-http.mjs` 记录隔离 Node HTTP 检查，runner 返回退出码 0。原始请求结果见 `project/evidence/review-http/stdout.txt`，命令记录见 `project/evidence/review-http/record.json`，脚本见 `project/evidence/review-http.mjs`。脚本动态选择本机端口，在系统临时目录创建独立数据文件，终止服务并清理文件。
- 未登录 POST 得 401，文件保持空；viewer POST 得 201，文件增加条目；editor 纯空白 POST 得 422，文件无新增；editor 非空 POST 得 201，GET 200 可读，但两端空白未去除。这些是当前工作树的实际运行证据，不代表部署环境。
- 沿 `server.mjs` 的登录 Cookie、页面表单、GET/POST、JSON 文件读写链路阅读完整源码。页面只禁用 viewer 的按钮，服务端可直接接受 POST；此问题由实际请求确认。原有异常处理、文件并发与生产认证并非本次契约/变更目标，未进行性能、并发或安全全面审计。未执行浏览器刷新、UI 呈现、跨进程重启、部署验证；GET 与磁盘检查只支持数据持久化和可读结论，不能替代这些未执行项。
- 本阶段仅评审。项目长期架构资产没有修改；当前系统是单个 Node HTTP 服务和 JSON 文件，UI、HTTP 路由、业务校验及存储集中在 `server.mjs`。对本次小型隔离项目，优先修复权限和规范化不变量；无依据推动目录/服务拆分。
