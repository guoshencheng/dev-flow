# D01 独立工程诊断评测

执行者：研发 Skill 子代理；任务类型：既有 RULE-01/02/03 下的 bugfix。三个样例分别作为独立项目处理。产品契约位于各自 `docs/product.md`，入口均为 `server.mjs`。本记录是隔离样例的研发诊断与自测，不是生产证据或独立验收，也未部署。

## 环境与证据边界

- Node.js v26.4.0；复用 Playwright 1.62.1 与 Google Chrome for Testing 153.0.8010.12，未升级依赖。`node test.mjs` 实际启动对应服务，Playwright 操作真实页面，浏览器发送真实 HTTP，测试直接读独立 JSON 文件。服务由脚本在 `finally` 中关闭。
- sample-1/2/3 分别使用 `127.0.0.1:19011/19012/19013` 和各项目的 `data/<phase>.json`。`red2`、`green` 使用不同数据文件；重启实验保留 `red2` 数据，仅改变进程生命周期。
- 每个样例保留 `server.before.mjs`、`server.mjs`、`fix.patch`、`test.mjs`、`probe.mjs`、`data/` 和 `evidence/`。运行记录包含实际命令、退出码、原始 stdout/stderr、前后源码 SHA-256。
- 首轮 `pre-fix` 因测试脚本等待空列表可见而超时，尚未触发保存；它是执行方法错误，不算目标缺陷证据。修正为等待 `aria-busy=false` 属性后，以 `baseline-red` 捕获目标失败。

## sample-1：保存响应先于持久化

候选旧版 `d1722d07a0408332…`，新版 `e528a9cdfe9054e7…`。旧版 `POST` 创建条目后仅 `void items`，未调用已有的 `writeItems`。

| 观察/假设 | 实验与控制条件 | 预期 | 实际/证据 | 判断与下一步 |
| --- | --- | --- | --- | --- |
| 浏览器先显示成功再丢失，可能只是页面刷新未渲染 | 保持旧版和同一 `red2` 文件；比较 POST、磁盘、GET、刷新 | 若仅 UI 错误，磁盘和 GET 应包含条目 | POST 201、刷新前列表有条目；磁盘 `[]`、GET `[]`、刷新后 `[]`，见 `evidence/baseline-red` | 否定 UI 单独故障；检查写入边界 |
| 可能是进程缓存丢失 | 保留旧数据，仅重启服务读取 | 若缓存遮蔽已写数据，重启后 GET 应出现 | 磁盘与重启后 GET 均为空，见 `evidence/restart-probe` | 否定缓存原因；确认无写入 |
| 未调用写入即返回 201 | 仅补 `await writeItems([...items, item])`，其余条件一致，新的 `green` 文件 | 磁盘、GET、刷新均含修剪后的标题 | 均含“浏览器条目”，见 `evidence/fixed-green` | 支持根因，已修复待验 |

## sample-2：GET 读错文件

候选旧版 `dd47ef0a8768a3b4…`，新版 `e528a9cdfe9054e7…`。旧版写 `EVAL_DATA_FILE`，GET 读独立的 `EVAL_DATA_FILE.read`；后者初始化为空且从未更新。

| 观察/假设 | 实验与控制条件 | 预期 | 实际/证据 | 判断与下一步 |
| --- | --- | --- | --- | --- |
| 可能是 POST 未持久化 | 旧版同一次浏览器保存后读主文件和 GET | 若未持久化，主文件为空 | 主文件含条目，但 GET 为空；`.read` 为 `[]`，见 `evidence/baseline-red` | 否定写入失败；定位读取文件 |
| 可能是内存缓存 | 保留旧版和同一文件，仅重启进程 | 若只因进程缓存，重启后 GET 应恢复 | 主文件仍有条目，`.read` 与 GET 仍为空，见 `evidence/restart-probe` | 否定内存缓存；支持文件分叉 |
| GET 指向旁路文件 | 删除旁路文件初始化/读取，GET 改用既有 `readItems()` | GET/刷新读到主文件 | 真实 HTTP 与界面均读到条目，见 `evidence/fixed-green` | 支持根因，已修复待验 |

## sample-3：GET 使用启动时快照

候选旧版 `bf3f5d2abd1f9dec…`，新版 `e528a9cdfe9054e7…`。旧版 `visibleCache = await readItems()` 仅在进程启动时求值，GET 返回该快照。

| 观察/假设 | 实验与控制条件 | 预期 | 实际/证据 | 判断与下一步 |
| --- | --- | --- | --- | --- |
| 可能是 POST 未持久化 | 旧版同一次浏览器保存后读磁盘和 GET | 若未持久化，磁盘为空 | 主文件含条目，GET 和刷新为空，见 `evidence/baseline-red` | 否定写入失败；检查读路径 |
| 可能是读错独立文件 | 保留旧版与磁盘，仅重启进程 | 若读错文件，重启后仍为空 | 重启后 GET 从相同主文件读到条目，见 `evidence/restart-probe` | 否定固定旁路文件；支持启动快照 |
| GET 使用启动时快照 | 删除 `visibleCache`，GET 每次调用 `readItems()` | 不重启即可读到新条目 | GET 与刷新可见，见 `evidence/fixed-green` | 支持根因，已修复待验 |

## 修复与回归

三个 `baseline-red` 都实际走到浏览器保存：POST 201、成功提示、刷新前有条目，随后针对 RULE-01 断言失败；其退出码均为 1。三个 `fixed-green` 均退出 0：浏览器刷新仍有条目、GET 返回修剪标题、磁盘与响应一致；viewer POST 403、匿名 GET 401、纯空白标题 POST 422，拒绝操作后磁盘内容不变。修复没有改产品契约、身份逻辑、测试预期或依赖。测试保留红绿同一脚本，旧版文件可供隔离复跑。

评测命令（在仓库根目录；每次重复运行须换新 `--label`，测试 phase 也宜换名）：

```sh
python3 evals/dev-flow-methods/run.py --project /Users/guoshencheng/Documents/work/dev-flow/.dev-flow/methods-eval-20261009/D01/sample-1 --label fixed-green -- node test.mjs green
python3 evals/dev-flow-methods/run.py --project /Users/guoshencheng/Documents/work/dev-flow/.dev-flow/methods-eval-20261009/D01/sample-2 --label fixed-green -- node test.mjs green
python3 evals/dev-flow-methods/run.py --project /Users/guoshencheng/Documents/work/dev-flow/.dev-flow/methods-eval-20261009/D01/sample-3 --label fixed-green -- node test.mjs green
```

以上命令为本次原始执行形式，已有相同 label 的目录不可重用。若需复验，换用 `--label recheck-<唯一值>` 和 `node test.mjs recheck-<唯一值>`。旧版复验须在隔离副本以 `server.before.mjs` 替换入口，且使用独立端口和数据文件；本次未改动旧版快照。

待独立验收：由测试职责对当前三个候选在独立上下文复验 RULE-01/02/03。此处只登记研发“已修复待验”，不代替测试关闭缺陷。
