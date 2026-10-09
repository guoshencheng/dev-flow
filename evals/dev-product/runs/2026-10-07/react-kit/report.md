# React 组件与预览工作区验证

启动日期：2026-10-07，完成日期：2026-10-08，证据目录沿用启动日期。总纲 v0.3，产品职责 v0.5，组件工作区与包版本 0.1.0。本次由主 Agent 执行，沿用用户指定的 Vite/React、Ant Design、shadcn/ui 方向；没有新增独立职责派发或真实用户研究。

## 成果与环境

源码见[React 工作区](../../../../../skills/dev-visual/assets/react-workspace/README.md)，共同约定见[UI 技术与组件协议](../../../../../skills/dev-visual/references/ui-stack-and-components.md)。Node.js 26.4.0，npm 11.17.0；实际依赖版本由 package-lock.json 固定，源码指纹见 checks.json。

B 端直接使用 antd 6.6.5，SelectionSummary 组合 Flex、Typography、Button。C 端采用 shadcn@4.21.4 从官方 Registry 获取 Button、Card，再形成 ActionCard；来源、修改与 MIT 许可保存到包中。Vite 8.3.3、React 19.3.0 为本次运行版本，其他版本未因此被验收。

## 已执行检查

| 检查 | 实际结果 |
| --- | --- |
| Skills 与接入 | dev-flow、dev-product 的 quick_validate 通过；两 Skill、一职责链接检查通过，未新增固定模型字段 |
| 类型与构建 | 四个工作区 typecheck 通过；两个库、两个应用 build 通过，生成 ESM、声明文件、C 端 CSS 与应用静态产物 |
| B 端操作 | 初始数量 0、动作禁用；选择两行后显示 2 项及当前页范围，确认得到 2 项模拟结果；清空回到 0 并禁用动作；Space 选择第三行，Enter 确认得到 1 项模拟结果 |
| C 端操作 | 初始主行动可用、重置禁用；保存后处理中、两动作禁用；完成后显示模拟结果并允许重置；重置恢复初始状态；Enter 可再次触发行动 |
| 渲染与日志 | B 端桌面、C 端窄屏实际查看；C 端 document contentWidth/clientWidth 均为 390；浏览器收集到的 error/warn 日志为空 |
| 包共享 | 两个 npm pack 产物在工作区外临时工程独立安装；公开导出、C 端 CSS、调用方严格类型、错误类型负例与 B/C 双入口 Vite 构建通过 |
| 原型初始化 | create-vite@9.2.1 的 react-ts 非交互初始化实际执行成功；默认指南采用相同路径 |

截图：[B 端桌面](antd-desktop.png)、[C 端窄屏](web-mobile.png)。本次开发入口：[B 端](http://127.0.0.1:5175/)、[C 端 Web](http://127.0.0.1:5176/)，仅本机进程运行时可用，停止后按工作区命令重启。

## 复现

在工作区执行：

```sh
npm ci
npm run typecheck
npm run check:packages
```

check:packages 重建组件和示例，在系统临时目录打包、安装并编译两个消费入口，不依赖工作区源码别名。成功输出 `{ "result": "passed" }` 与目录；本次成功目录为 `/var/folders/48/cj4jq0s54xdd9c314rgcsv180000gn/T/dev-flow-package-check-S3YI3u`。

浏览器按上表实际步骤复验。两个示例分别运行，源码修改由 Vite 热更新；正式消费导入固定包版本与 CSS。示例为本页内存模拟，刷新清空。

## 修正与验证边界

初次类型检查发现 TypeScript 7 删除 baseUrl、CSS 侧效导入缺少 Vite 类型声明，已修正。实际渲染发现 Tailwind 基础边框规则缺失，已补齐并重新构建和打包。shadcn 获取代码后补齐实际使用依赖，工具函数导入改为相对路径，保留来源记录。

独立工程曾开启 skipLibCheck=false，antd 的 `@rc-component/image/PreviewGroup` 与 `@rc-component/picker/PickerPanel` 内部接口报 TS2430。最终采用与 Vite 模板一致的 skipLibCheck=true：严格检查调用方，负例保证公开数量与回调类型没有退化为 any；不声称依赖声明内部一致性通过，也未修改 antd 实现。

B 端示例构建有单 chunk 超过 500 kB 的提醒；共享包将 React/antd 等作为外部依赖。示例未作生产性能验收，实际项目按目标检查。

浏览器 checkbox 的可访问名称随选择改变，check 操作曾在状态已变化后返回定位超时。DOM 确认第一行已选，再依据当前控件继续操作，最终结果实际核验；不将其写成未发生的用户操作。

当前为隔离组件与示例证据，尚未验证真实项目采用、全部 Props/状态、生产接口、真实用户、远程 Git 获取、包发布或原生角色派发。真实项目经验按组件协议逐步沉淀，模型与强度仍由任务调用方和宿主选择。
