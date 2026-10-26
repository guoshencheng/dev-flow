---
title: 文档审阅与呈现检查效率优化实施计划
status: implemented-source
version: 3
---

# 文档审阅与呈现检查效率优化实施计划

有效输入：[设计 v1](design.md)、用户“按照这个方向做优化”及接续指令“另一个已经好了，你这边推进吧”；进度见 [Progress](../Progress.md)，独立复核见 [Review](review.md)。计划 v2 补充独立评审指出的写入范围、共享生成与安装条件；v3 按接续授权落实 0.7.1 本机交付。执行位置为 `/Users/guoshencheng/Documents/work/dev-flow` 的 `main`，最初 Git 起点为 `10c6e124447c6c8013935ece937221f269f074c6`，交付接续基线为另一迭代完成的 `daab711`。本轮相关初始内容快照及指纹为 `.dev/document-review-efficiency/baseline/`；既有暂存范围以该目录 `initial-status.txt` 为准。

## 一、实施目标与前置条件

落实已授权的局部规则维护；先取得独立设计/计划结论，再连续修改。保留其他活动迭代的全部已暂存及未跟踪内容。本轮无运行服务、业务 UI 或数据迁移。

## 二、实施步骤与依赖

主 Agent 唯一写入本轮规则、模板、进度及验证记录；独立执行者只读审阅。先保存相关初始文件快照，再按下列顺序推进：

| 本轮源文件 | 唯一允许修改的内容 |
| --- | --- |
| `skills/document-management/SKILL.md` | 默认检查原则、按需预览及交接 URL 边界；保留既有收尾 Skill 引用 |
| `skills/document-management/references/document-preview.md` | 新增检查选择方法；阅读入口与 Agent 自查分开 |
| `skills/document-management/references/document-contract.md` | 将启动 Vite 限定到实际需要阅读入口的任务 |
| `agents/prompts/common.md` | 一段跨职责默认原则和操作权威引用 |
| `agents/prompts/architecture.md`、`engineering.md` | 替换无条件“核对实际渲染”的句子；保留架构职责中其他迭代已新增的收尾内容 |
| `agents/prompts/visual.md` | 模板核对按内容、实际页面呈现按影响，避免文字 Review 无条件触发渲染 |
| `agents/references/architecture/technical-diagrams.md` | 新图/变化的呈现检查、证据复用与工具选择引用 |
| `agents/references/engineering/technical-delivery-design.md` | 方案/实现 Review 默认源内容，必要呈现按图示规范 |
| `agents/assets/engineering/technical-delivery-design.md` | 第六章检查方式与未覆盖的记录要求 |
| `agents/assets/architecture/templates/architecture-review.md`、`current-architecture.md` | 检查呈现的触发与证据复用引用 |

生成范围为 `agents/dev_*.toml`、`adapters/kimi/agents/dev-*.md` 以及生成器依据现行双清单维护的 `kimi.plugin.json`；不手工编辑生成正文。主 Agent 在生成前保存六职责维护源、能力声明和双清单的同一候选指纹，执行 write 后立即 check 并比对源指纹，保证源与生成物一致。若源发生并发变化，暂停该轮候选结论，回读差异、确认其归属后再生成和验证；其他迭代的内容始终保留，不宣称全局写入已冻结。

1. 文档管理 Skill 入口和预览参考明确内容优先、呈现触发、工具选择及有效证据复用；无预览需求时交接源路径，不强制 Web URL。共同文档协议中的启动阅读器表述限定到需要提供阅读入口时。
2. 公共约束及架构/研发/视觉职责统一检查边界；技术图示规范、研发设计参考和受影响模板消除无条件渲染要求，使用现有权威方法。保留新图、呈现变化及交互目标的真实观察。
3. 使用生成脚本同步六职责的 Codex/Kimi 入口；验证资源和引用，核对源指纹后固定本轮完整差异及生成入口，再交独立候选 Review 和代表场景决策验证。发现问题修订后重新生成并定向复核。
4. 首阶段因另一迭代正在交付而只保留源码。现在该迭代已完成，24 个 C2 文件无漂移，按用户接续授权升级 0.7.1 patch；新增写入范围仅 `plugin.json`、`.codex-plugin/plugin.json`、随脚本生成的 `kimi.plugin.json`、README 当前版本说明及 `docs/plugin.md`，以及本轮四份进度/设计/计划/Review 记录。新文件先纳管，验证固定候选并独立核对接续范围；本地保存后在本仓库执行 install/check，核对实际启用、17 Skills、六职责及全包源码指纹。未跟踪 UI 确认草案不纳管、不纳包；不推送远端或执行 Kimi 原生安装。

## 三、测试保护与持续集成

- 内容检查：本轮差异、引用、各入口对文本/图示/交互的适用边界；不新增逐字匹配文案的测试。
- 代表场景：独立执行者面对真实任务描述与候选规则，说明检查入口、实际观察需求及复用/限制。此验证证明指令选择，不声称执行了未实际运行的 GUI。
- 机械检查：`python3 /Users/guoshencheng/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/document-management`、`python3 scripts/sync_host_agents.py --check`、`git diff --check`；运行现有 `test_native_agents.py` 和 `test_plugin_installation.py` 的隔离测试验证生成资源与打包。安装脚本不修改。

## 四、完整候选与验收安排

完整候选包含本轮源文件差异及生成入口；独立 Review 检查默认行为、必要视觉观察、证据复用和用户限定范围是否一致。代表场景覆盖内容、图示、渲染条件、链接、交互与明确用户要求，发现问题修改后定向复核。

## 五、计划 AI 复核引用

独立执行者已定向复核 v2 的明确文件/hunk、生成入口与共享候选边界，通过并要求将完整候选 Review 放在生成/check 之后；本页已调整该顺序，实际轮次见 [Review](review.md)。本页编写者不登记自身独立通过。

## 六、执行与重要调整

当前状态由唯一 Progress 维护。本轮不调整其他迭代的业务规则、授权及收尾状态。接续授权解除并发交付限制后，只升级本轮独立 patch；安装结果未核验前不将源码通过写成本机已生效。

基线检查：本轮包内文件修改前，生成 `--check` 已通过（六职责、17 Skills）；本机 `manage_plugin.py check` 已报“安装包文件与指纹清单不一致”，对应记录仍指向 0.6.7 缓存。这是既有安装状态，本轮不归因或自行修复未核清的缓存差异。

## 七、引用与关联文档

- [设计](design.md)、[Progress](../Progress.md)、[Review](review.md)。
- 操作权威：`skills/document-management/references/document-preview.md`。
- 专业规范：`agents/references/architecture/technical-diagrams.md`。
- 生成与交付：`scripts/sync_host_agents.py`、`scripts/manage_plugin.py`、`docs/plugin.md`。
