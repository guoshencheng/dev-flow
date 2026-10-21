# 架构与技术方案图示规范检查

日期：2026-10-21。状态：源码候选，未安装/分发。基线：`503fcb4`。执行方式：主 Agent 依据 Dev Flow、架构和研发 Skill 顺序承担编写与自查；未使用 subagent，未声称独立 Review。文档方法维护，裁剪功能编码、TDD 和正式功能验收。

## 范围与成果

用户指出架构/技术文档缺少选图标准，并提供分区、分层的架构参考图。本次新增架构主责维护的[技术图示规范](../skills/dev-architecture/references/technical-diagrams.md)及[六类可改写示例](../skills/dev-architecture/assets/examples/technical-diagrams.md)，接入架构/研发 Skill、设计/模块地图/技术方案方法、四份设计/现状/Review 模板、共同文档协议与 README。规范同时适用于拆分文档与合并研发设计文档，不改变现行阶段和确认关系。

新增内容覆盖：按问题选择架构总览、模块依赖、部署拓扑、时序、流程/泳道、状态、ER 和数据流图；按实际变化补图，局部线性修改可裁剪；明确现状/目标、边界/包含/连线语义、失败恢复、依据与读图结论；并入已有 Review，要求实际渲染、图文/契约一致性及后续维护。示例为虚构目标方案，不代表本插件实际运行架构。

## 工作位置与并行修改保护

原工作区 `codex/engineering-document-template-preview` 已有流程与模板讨论稿，调查期间又发生共享 Skill/模板写入。为避免覆盖，后续改动隔离在附属工作区 `technical-diagram-standard/dev-flow`，分支 `codex/technical-diagram-standard`，从明确基线建立；原工作区其他修改没有带入、覆盖或提交。

本候选尚未合入原工作区。合并时尤其核对 `skills/dev-engineering/SKILL.md` 与 `assets/templates/technical-delivery-design.md` 的并行重写：将选图要求落入新合并设计模板的“核心业务链路”和“架构与模块设计”，Review 模板承接图示检查，保留新流程的其他有效决定。不得以本候选旧模板覆盖并行新模板。

## 实际检查与修正

- `python3 scripts/sync_host_agents.py --write`、`--check`：通过，六职责、八个 Skills 同步一致，无生成文件差异。
- Markdown 相对文件链接：13 份新增/修改文档共检查 162 个引用，目标均存在；不宣称已验证所有锚点或外部网址。
- 使用现有依赖 Mermaid 12.1.0，浏览器按阅读器相同的 `securityLevel: strict`、`theme: default`、`htmlLabels: false` 渲染六图：全部成功。浏览器截图抽查架构区域/中文、依赖方向、时序分支、流程判断、状态终态与 ER 图；无渲染器实现改动。
- 初次纯 Node 解析中，两图通过，其他图因缺少浏览器 DOM 的 `DOMPurify.addHook` 报错，属于检查环境限制；随后以上述实际浏览器渲染核验，未将 Node 环境失败当成图语法失败或通过证据。
- 自查发现时序图未显式记录 `queued → running`，与状态图不完整对应；补入 Worker 领取、原子条件更新、拒绝重复/已取消领取和成功后执行。流程/状态/时序中取消仅允许从 queued 生效，重试另建任务。
- 架构图初版内部节点外连导致布局过长；改由编排进程边界承接外部通信，进程内按横向展示模块关系，再次实际渲染通过。
- `git diff --check`：通过。未修改运行代码，不制造功能测试通过结论。

## 交付边界

这是可合并的文档方法候选，未执行插件打包、版本升级、宿主安装、Kimi 重载或真实项目行为评测。发布前与其他已确认成果合并，按仓库约定确定新插件版本，重新验证候选并安装/检查；不覆盖已交付的 0.2.2 缓存。实际项目是否能据此稳定产出合适图示，仍需真实任务验证。
