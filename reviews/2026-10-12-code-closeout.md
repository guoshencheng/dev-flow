# “开始收尾”的代码处理与工程交接

日期：2026-10-12。用户在文档收尾入口确定后，希望同时做好代码收尾。原有[Git 与集成指南](../skills/dev-flow/references/git-and-worktree.md)已规定候选验证、提交建议、合并及资源保留；本轮将其接入“开始收尾”的默认路径，专业内容继续引用现行研发、架构、测试与运维方法。

## 范围与方案

开始提交为 `fbb81fdf0195ef635d71625516a39d0915cde912`，沿用 `codex/implementation-authorization` 原 checkout。输入包含已安装的 0.2.1 候选及本分支尚未提交的实施授权/文档收尾修改。本轮维护收尾方法、职责引用、模板、能力现状和版本，不新增脚本、Agent、状态字段或业务功能；保留原有成果。

主 Agent 顺序承担方法维护和 AI 自查，未委派，不声明独立 Review。实施顺序为恢复总纲与既有代码/资产协议，补齐代码收尾规范及短指令路由，同步研发入口/交接模板和长期说明，核对整体候选与实际验证，按仓库约定保存源码并升级、安装。设计与计划使用中文。

默认“开始收尾”覆盖：

- 本轮完整变更与归属核对、必要代码整理，不扩展为无关重构或删除其他任务内容。
- 完整实现 Review、阻断项修复/复评/复验、当前候选必要测试/构建/启动；有效证据复用，实际修改后定向重验。
- 代码、测试、配置和文档对齐；无其他约定时形成本轮相关本地提交，已有完整提交复用，重复调用不生成空提交。
- 推送/PR/合并/发布按已有授权推进，记录实际状态；工作区剩余内容与服务/worktree 按归属和成果保留条件处理。
- 总结、长期资产和遗留承接；代码交付与文档归档分别判断，缺少必需结果保持真实未完成。

明确仅文档整理或历史归档时裁剪代码动作；用户禁止提交或采用其他交付形式时遵循现行约定。已有暂存/未暂存/未跟踪改动不能被整体卷入，不用清空工作区证明收尾；未确定归属保留原状，待验/WIP 保存不能冒充可合并候选。

## 验证、版本与交接

Plugin 0.2.2、总纲 v0.27；八个 Skills、六职责、执行协议、状态 schema 和安装脚本保持原有接口，属于兼容方法维护。本轮相关规范位于[代码收尾](../skills/dev-flow/references/git-and-worktree.md#代码收尾)，主流程在[收尾入口](../skills/dev-flow/references/document-archive.md#一条指令收尾当前迭代)，研发采用[工程资产](../skills/dev-engineering/references/project-assets-and-delivery.md)和[交接模板](../skills/dev-engineering/assets/templates/engineering-handoff.md)。

主 Agent 自查用户要求、已安装基线及从开始提交到候选的完整相关差异，包括此前实施授权核验器/测试、收尾入口、专业引用和模板。核对了本地保存与远端动作边界、混合暂存内容、失效证据/待验候选、已有提交复用、仅文档范围、资源归属及归档条件；已补齐工程成果保存和交付缺口的归档约束，未发现开放阻断项。这是实际自查，不声明独立评审或新上下文行为通过。

- `python3 -m unittest discover -s tests -v`：38 项通过，包含 32 项阶段状态契约及 6 项隔离打包/安装/配置保留检查；覆盖本次整体插件候选，不将测试数量视为新收尾行为证明。
- Skill Creator `quick_validate.py` 对 `dev-flow` / `dev-engineering` 通过；PyYAML 使用临时目录提供，未改变项目依赖。
- `python3 scripts/sync_host_agents.py --write` / `--check` 通过；两端六职责、八 Skills 同步，三份清单均为 0.2.2。
- 增量 Markdown 相对文件引用/标题锚点及 `git diff --check` 通过。代码收尾方法、主入口、文档归档、职责和模板引用均可达。
- 本机 Codex `install` / `check` 通过：已启用、八 Skills、`source_matches_cache=true`，已实际读取缓存的代码收尾章节。

本分支源码保存覆盖此前实施授权、文档收尾和本轮代码收尾的完整已核验插件候选，只选取清楚归属的相关文件。最终本地提交及工作区状态保存于忽略目录 `.dev-flow/releases/0.2.2-source.json`；推送、PR、合并及远端发布未执行，本轮交付目标为本机插件。没有新增 worktree 或运行服务需清理，本机日志/构建/安装记录按仓库规则保留。

构建目录为 `/Users/guoshencheng/Documents/work/dev-flow/.dev-flow/plugin-source`，缓存为 `/Users/guoshencheng/.codex/plugins/cache/dev-flow-local/dev-flow/0.2.2`，最终包清单及源码指纹见构建目录 `package-files.json`。交接补齐、本地保存后重新构建/安装该尚未交付候选并核验，最终原始结果保存于 `.dev-flow/releases/0.2.2-install.json` 和 `0.2.2-check.json`；提交不改变已验证源码内容，hook 若产生额外变化则补相关验证。

静态检查、工具测试、本仓库保存和安装只证明已执行范围，不能升级为真实业务项目完整代码收尾或新上下文行为已验证。Kimi 清单同步，原生安装/重载另行处理；后续真实任务按该入口验证相关提交、集成交付和下一任务复用。
