# 研发 Agent v0.1 验证记录

日期：2026-10-08。执行方式为主 Agent AI 自查与隔离研发自执行/复验，没有子 Agent、独立专业评测或原生 `dev_engineering` 派发。角色方法、工具检查、原生发现与真实项目成熟度分别登记。

## 已定义与接入

[职责说明](../../docs/engineering-agent.md)、[Skill](../../skills/dev-engineering/SKILL.md)与[原生配置](../../agents/dev_engineering.toml)细化 E01–E08：工程基线与代码映射、实现计划/AI 复核、纵向切片、前端/业务接口实现、证据诊断、兼容变更、工程检查及集成交付；六份按需参考与三个项目模板支持持续维护。

沿用已确认产品/UI、重要架构和可读用例，实施计划由 AI 复核通过后自主实现，不新增人工计划审批。真实接口/数据、UI/错误恢复、待验交接和项目工程资产分别落实；共享代码复制/参考并记录 Git 来源，没有新增内部 npm 发布依赖。

新 Skill/共同入口结构检查通过，五个 TOML 可解析且没有固定模型/强度，新 UI YAML 合法且保留默认自动发现。既有安装脚本实际新增全局 Skill 和职责链接，`--check` 验证六个 Skills/五个职责配置；安装脚本、业务项目与文档阅读器没有修改。引用/差异和最终检查见[建设检查](../../reviews/2026-10-08-engineering-agent-check.md)。

## 实际诊断修复与复验

输入及实施前 AI 自查见[案例记录](case.md)。从原测试样本构造[单一缺陷源码](fixtures/http-ui/server.before.mjs)，移除 broken/fixed 开关；在隔离副本实际安装依赖、运行原测试、读取失败证据，修复三处实现并复验，不是仅切换版本标志。

| 原用例 | 修改前 | 修改后 |
| --- | --- | --- |
| TC-API-01 编辑者保存/真实读回 | 失败，返回成功但没有保存 | 通过 |
| TC-API-02 查看者直接请求/无副作用 | 失败，201 且有写入 | 通过，403 且无副作用 |
| TC-API-03 无效输入/无副作用 | 通过 | 通过 |
| TC-E2E-01 实际操作/请求响应/读回/刷新 | 失败，查询与刷新缺失 | 通过 |
| TC-UI-01 故障保留输入/恢复重试 | 失败，输入被清空 | 通过 |
| TC-UI-02 查看者界面禁用 | 通过 | 通过 |

实际补丁为[repair.patch](fixtures/http-ui/repair.patch)：服务端先检查 editor 权限，完成真实写入再返回成功，UI catch 保留输入而只在成功时清空。原产品、测试、配置、依赖/锁文件指纹保持，没有更改预期、timeout、重试或 Mock 范围。错误注入一例仍为明确 route mock，其他 API/E2E 使用真实样本 HTTP 服务。

两轮各 6 项/单 worker/无重试，修改前退出 1（4 失败/2 通过），修改后退出 0（6 通过），没有 skipped/flaky；两次自管服务端口均已关闭。[原始失败报告](runs/2026-10-08/http-ui/before-report.json)、[原始复验报告](runs/2026-10-08/http-ui/after-report.json)、[命令/版本/指纹与结果](runs/2026-10-08/http-ui/checks.json)持久保留。trace/截图仍是本地诊断资料，没有登记视觉回归通过。

环境为 Node v26.4.0、Playwright 1.62.1 和经同一 Playwright 启动读取版本的已有 Chrome for Testing 153.0.8010.12，浏览器通过显式可执行路径使用。独立源码副本执行 `npm ci --ignore-scripts --no-audit --no-fund` 后可运行核心链路，沿用了宿主已装 runtime/浏览器；不声称全新机器、框架构建产物或目标部署交付。

## 重复运行与工程接手

从仓库根目录为另一轮选择尚不存在的忽略目录。先准备兼容的 Playwright 浏览器，或将已实际核验浏览器的绝对路径设为 `EVAL_BROWSER_EXECUTABLE`。示例：

```sh
python3 evals/dev-engineering/run.py --prepare --project .dev-flow/engineering-replay/project
cd .dev-flow/engineering-replay/project
npm ci --ignore-scripts --no-audit --no-fund
cd ../../..
python3 evals/dev-engineering/run.py --project .dev-flow/engineering-replay/project --phase before
patch -d .dev-flow/engineering-replay/project -p1 < evals/dev-engineering/fixtures/http-ui/repair.patch
python3 evals/dev-engineering/run.py --project .dev-flow/engineering-replay/project --phase after
```

`run.py` 只准备/执行固定案例，不实施修复或调用模型；分别判定原问题检出与相同用例复验，保存实际报告。阶段目录已存在会停止，保留原记录。准备分支和补丁应用另在新副本验证，重建源码指纹等于实际修复候选，没有再次重复已通过的浏览器测试。

工程接手以缺陷源码＋补丁、输入/候选指纹和原用例为依据；当前实际修复副本与数据/报告位置在检查记录中。启动采用样本 `node server.mjs`，显式提供本次独立 `EVAL_PORT`/`EVAL_DATA_FILE`，测试 runner 分配端口和文件并通过 Playwright webServer 管理启动/停止。健康入口与核心业务分别核验，生产环境的身份/数据/运行方案不由该测试样本替代。

## 准确边界与后续

案例中的实际 UI 是遗留 HTML/JS、后端为 Node HTTP＋JSON 文件，局部修复保留其基线。它检验的是本例证据诊断、实际修复、用例保持、原问题与正常/拒绝回归，不证明 React/Next/Astro 工程实现、整洁架构重构、数据库并发事务、兼容迁移、性能、跨域或生产部署。

本轮没有独立测试角色关闭缺陷、原生角色发现/派发、新上下文复用或真实项目完整协作。专业方法是首版指导；后续在真实项目依据有效设计与已确认用例验证计划复核、实现/测试来回对焦、交付与工程资产复用，再提高成熟度。
