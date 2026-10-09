# 移除 setup 与任务路由检查

日期：2026-10-09。执行方式：主 Agent 接续共享工作区，按 Dev Flow 总纲进行 AI 自查与工具验证，未派发子 Agent，不属于独立复核。

## 范围与结果

删除 `dev-flow-setup`、`setup_plugin.py`、`install_global.py` 和两份插件清单中的初始化入口。安装工具独立完成构建、安装、来源/缓存核验与卸载，仅提供流程及六职责共七个 Skills；不注册个人 Agent 或改写全局指引。`agents/` 旧 TOML 保留为历史配置参考。

新增[任务路由](../skills/dev-flow/references/task-routing.md)，并同步总纲、执行协议、研发/验收入口与当前安装说明。bugfix 恢复有效预期，采用复现、根因、简短计划/AI 复核、修复、自测/复验、必要回归与交付；不新增整套设计或人工用例审批。正常需求保留设计/重要架构确认、研发技术方案及符合性 AI Review、用例 AI Review/用户确认、实施计划 AI 复核、持续研发测试和交付/架构复盘。变更确认基线只确认受影响部分，技术方案及实施计划不增加人工审批。

阶段产物继续按 `docs/dev-flow/iterations/<迭代ID>/` 集中，跨迭代基线保存在项目级职责资产中；本次不迁移既有业务项目文档。

## 实际验证

- `python3 -m unittest discover -s tests -v`：五项隔离测试通过，覆盖无 setup 打包/更新、缓存损坏拒绝、目录外路径拒绝、install/check/remove 保留用户配置、同名外部 marketplace 保护。
- 七个 Skills 的 `quick_validate.py` 校验通过。
- 本地 Markdown 引用检查无断链，`git diff --check` 通过。
- 本机新版 `manage_plugin.py install` 成功，`check` 确认启用、源码与缓存一致、七个 Skills；实际缓存不存在 setup Skill、注册脚本和 onboardingSkill。
- 旧 setup 受管状态已清理，六个个人角色链接/生成副本清理沿用接续前记录；备份为 `/Users/guoshencheng/.codex/backups/dev-flow/remove-setup-20261009-101059-944683`。保留其他角色和已有全局指引，没有重复运行旧 setup。

## 证据边界

本次验证安装工具与指导内容，未执行完整真实业务迭代或重新验证历史专业行为；没有启动浏览器或项目文档预览。当前会话初始 Skill 目录属于刷新前快照，后续新会话的发现以宿主加载结果为准。旧[八 Skills 安装记录](2026-10-09-plugin-installation.md)保持历史版本，不作为当前行为说明。
