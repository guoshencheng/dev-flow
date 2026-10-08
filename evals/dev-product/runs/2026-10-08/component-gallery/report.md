# 组件预览与源码复制验证记录

日期：2026-10-08（Asia/Shanghai）。执行者：主 Agent。对应产品职责 v0.6、总纲 v0.4、UI 约定 v0.3。模型与原生职责配置沿用现有设置。

## 成果与复现

Skill 同仓库的 React 工作区提供组件目录和源码索引。SelectionSummary、ActionCard、Button、Card 支持搜索、状态预览、使用示例、源码文件查看、完整文件集复制，以及候选 JSON。使用示例从内部预览源码生成本地相对导入版本，并在独立项目实际编译和操作。

默认采用复制或参考源码：项目直接维护组件；基础依赖按项目现行工程使用；后续比较来源与项目差异，按需合并并回收通用改进。复制工具包含必要组件、支持文件、样式起点和许可，记录来源提交或真实文件哈希；有差异的既有文件留给项目维护。

```sh
cd "$HOME/.agents/skills/dev-product/assets/react-workspace"
npm ci
npm run dev:gallery
npm run --silent catalog -- antd-selection-summary
npm run --silent copy:component -- antd-selection-summary --to /目标项目/src/components/dev-flow
npm run typecheck
npm run build
npm run check:source
```

目录本轮实际地址 `http://127.0.0.1:5177/`，B/C 分别为 index.html、web.html。临时独立源码副本使用 5178 检查，检查后已停止该临时服务；目录服务保留。重新运行按 Vite 实际输出地址访问。

## 已完成检查

- 五个工作区类型检查、构建通过。B/C 构建入口分开，B 端 HTML 不加载 C 端 CSS。依赖安装与锁文件匹配，初次安装报告 0 个已知漏洞。
- B 端目录检查：未选择时动作禁用、选择后数量更新、模拟确认反馈、处理中禁止选择和操作、已选两项状态。C 端目录检查：ActionCard 等待与完成、Enter 重置、固定处理中禁用，Button Enter 计数与禁用，Card Enter 展开并更新 aria-expanded。
- 目录搜索无匹配有反馈，关键词“按钮”只匹配 Button；候选跨 B/C 入口保留，加入、移除、清空和状态 URL 刷新恢复已检查。测试候选已清空，未登记为用户选择。
- 新接入方式检查：B 端使用示例复制后为本地源码导入；单个文件复制得到实际组件实现。B/C 完整文件集 JSON 内容完整，C 端包含七个必要文件与基础/样式依赖说明。候选 JSON schemaVersion 2 使用 copy-source，包含源码路径，未登记自有组件包依赖；复制与实际下载成功，样本为 selection-export.json。
- B/C 窄屏查看代码检查：390×844 下 clientWidth = scrollWidth = 390；新增长路径文件选择器与代码区复验正常。初次目录的代码溢出已修复。截图使用真实浏览器，临时视口已恢复。
- `check:source` 在工作区外的独立 React/Vite 工程复制四类源码，只安装公开基础依赖；没有 @dev-flow 依赖或工作区别名，使用本地相对路径严格类型检查与 B/C 构建通过。类型错误用例证明数量与回调类型仍有约束。
- 复制脚本检查：相同源码重复复制不重写；项目修改后再次复制保留该修改；完整文件集后部发生冲突时，不先复制前部文件。CLI 实际复制通过，含空格目标路径有效，生成来源记录与 SHA-256。
- 独立副本实际操作：B 端在项目副本改为“确认副本所选项”后，浏览器显示该文案并确认两项；仓库原始文案保持“确认所选项”。C 端本地副本保存从等待到完成，Button Enter 计数，Card Enter 展开详情；无 error/warn 日志。
- 两个 Skill 格式与全局链接检查通过。React 代码核验组件结构、受控状态、计时器清理、键盘名称、存储格式、源码文件集和支持依赖。

## 证据与边界

`business-desktop.png`、`web-mobile.png` 是最终目录；`source-copy-business.png`、`source-copy-web.png` 是独立副本。`checks.json` 保存执行范围及当前源文件指纹；`source-copy-check.json` 与 `source-copy-receipts.json` 保存独立检查实际目录和复制时的源文件哈希。

候选状态是 candidate，预览状态不代表项目默认状态；浏览器不能读取 Git，sourceCommit 为 null。复制工具记录基准提交、修改状态和实际文件哈希，允许采用未发布、未提交的当前源码。项目业务状态和接口仍需实际集成、操作和登记验证。

[v0.5 的包接入证据](../../2026-10-07/react-kit/report.md)保留历史含义；当前源码流程不以打包安装作为默认接入方式，旧包检查脚本已从活动工作区移除。

Ant Design 展示构建有大于 500kB 的 JS 分块提示，未做生产性能验收；类型检查沿用 Vite 的 skipLibCheck，不证明全部依赖内部声明一致。当前是隔离源码副本与预览验证，没有真实项目采用、真实用户观察、远程 Git 同步或原生角色派发证据。
