# 可执行研发方法的插件接入核验

日期：2026-10-09。执行者：主 Agent。范围为本次方法改造的已有安装工具接入，不修改安装脚本、Agent 注册或用户指引。

方法/行为结论由[独立复核](2026-10-09-executable-methods-review.md)提供，本记录补齐该复评时尚未执行完成的 P5 接入检查。新增文件纳入 Git 后，使用 `python3 scripts/manage_plugin.py install` 重建并更新插件，再执行 `python3 scripts/manage_plugin.py check`。

首次安装成功，但独立复评记录随后写入，源码指纹变化；首次 check 明确提示重新构建，未将其登记为通过。待复评记录稳定后重新 install/check，实际结果为：

```json
{"plugin_id":"dev-flow@dev-flow-local","enabled":true,"source_matches_cache":true,"skills":7}
```

当次命令/退出码与原始输出保存于 `evals/dev-flow-methods/runs/2026-10-09/install-check.json`。它对应记录归档前的收尾候选；归档并更新本计划状态后，必须再次 install/check 核对最终源码，最终执行记录保存在本机忽略目录 `.dev-flow/methods-baseline/final-install-check.json`，不把较早缓存通过直接移植到新源码。

共同总纲、方法、模板与评测链接检查通过，四个改动 Skills 的 quick_validate 通过。安装工具核验来源、包指纹与七个 Skills；当前会话的已加载能力不自动刷新，宿主发现新内容需按既有安装指南在新会话核验。没有登记真实项目采用、生产部署或全新机器验证。
