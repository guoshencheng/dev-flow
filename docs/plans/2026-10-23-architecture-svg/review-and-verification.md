---
title: SVG结构图独立复核与验证
status: passed
updated: 2026-10-23
---

# SVG 结构图独立复核与验证

总体范围与状态见 [Progress](Progress.md)，设计见[实施计划](implementation-plan.md)。基线 e06ff5e；本轮源码交付，不发行、安装或推送。

## 独立复核

计划已由原 service_architecture_review 只读复核，通过；恢复工作后使用独立 architecture_svg_review（gpt-6-sol / medium），加载公共/架构职责，复核完整候选及真实浏览器截图；作者主 Agent 负责修正，评审者未写入或向其他聊天发消息。

第一轮发现一项阻断：运行示例正文把控制面外框定义为网络区域，图中“公网”包住数据库和内部模块，可能误导公网暴露范围。已将外框改为“云端 · Control Plane（部署范围）”，仅 Web 与 Gateway 明示公网协议；正文和SVG desc说明数据库不表示公网暴露并列出内部网络省略项。

定向复验实看 runtime-1280-r2.png，通过并关闭阻断。其他两张未变截图/源码与Order时序、ER及模板复核结论沿用：分层只表达归属，源码依赖方向正确，外层实现指向内层端口，装配引用与注入分开，Worker主动连接，数据库与网关并列。最终本仓库规范与示例范围无未关闭阻断。模型选择仅记本次执行，不写入可复用规范。

## 实际验证

- 三张SVG均XML可解析，有viewBox、title/desc、可编辑text和稳定且单文件唯一ID；无script、foreignObject、图片/字体外链、事件属性。改动文档相对资源及文档路径存在，Markdown图片和源文件链接均指向同一SVG。
- Codex内嵌浏览器1280×720窗口，HTML img容器宽1280，三张图的实际显示分别约1280×821、1280×939、1280×949；资源complete为true。完整截图逐张查看，中文、对比、边界、标签及箭头落点可读。运行图修正后重载并保存r2截图。源码依赖SVG直接URL打开也成功，浏览器可访问其title/desc。
- 本次以浏览器原生SVG图片嵌入检查图像，不启动共享文档阅读器；Markdown相对引用静态检查，不声称所有Markdown阅读器兼容性。一次可选DOM几何读取因SVG包装接口不提供viewBox.baseVal失败，未作为通过证据；实际图片呈现与XML检查独立完成。
- `python3 scripts/sync_host_agents.py --check`：通过，六职责、十六Skills生成一致；未改提示词或生成配置。
- `git diff --check`与暂存差异检查通过；新SVG和计划记录已纳入Git管理。纯文档/矢量资源修改，无安装工具改动，不增加业务测试，也未重复上一版本完整回归。
- 本机原始记录：`.dev/runs/architecture-svg/source-check.json`、`sync-check.json`；截图`layers-1280.png`、`dependencies-1280.png`、`runtime-1280-r2.png`，另留旧运行图截图用于问题追溯。预览服务和标签页仅用于本次核验，完成后关闭。

## 最终内容候选指纹

SHA256用于对应本轮内容与实际复核；计划/验证记录不属于图示内容候选。

| 文件 | SHA256 |
| --- | --- |
| `agents/references/architecture/technical-diagrams.md` | `f02d1e65acfd3afbca878a5627bf9402a46212a8297c36fdabb6b54817d0d7a7` |
| `agents/assets/architecture/examples/technical-diagrams.md` | `f8b70a8d1bb59fbcca564a19b4554340d14080e86aebbe0057d8471fb5306174` |
| `agents/assets/architecture/templates/architecture-design.md` | `3c83a388e0919d62680b0b9d681f7486c04bd6bbfea19971fd7ab8f245245162` |
| `agents/assets/architecture/templates/current-architecture.md` | `7faab8d4a565c0101288a34a6a11537a7a2dfc5291d12ba630f08e6b9858ab17` |
| `agents/assets/engineering/technical-delivery-design.md` | `57339de59618362f4a8739c262b4acec865c5f54c00b6b64c2c8327e6ac8198f` |
| `agents/assets/architecture/templates/architecture-review.md` | `f42fb4eac6276b667de3d7fdc43d93e0b67de12da8b0e31d06e683f306131d65` |
| `agents/assets/architecture/examples/diagrams/service-clean-layers.svg` | `da14041747a32e1bf3d68bdcaa7dcaa7182cc78721f70741ad968de3b3e21149` |
| `agents/assets/architecture/examples/diagrams/service-module-dependencies.svg` | `09e46a579088acf6119a607347124c37630a458b7e72e90f5b44ad1117135ed8` |
| `agents/assets/architecture/examples/diagrams/system-runtime-overview.svg` | `ca27e05e6922e2215d7d606f73fcfcd38cfce56158d95da1afe9cb0d6138e126` |

## 已授权通知

2026-10-23 通过 send_message_to_thread 向用户指定的本地聊天“整理项目架构与 Service 文档”（01a1677d-d333-7761-b99e-0e69cdcc6f0e）发送调整请求，工具成功返回相同threadId。消息包含规范和三张SVG绝对源路径、money-bird实际总架构文件、源码/运行语义要求、保留函数端口和真实层次、时序/ER沿用要求，以及0.6.1缓存未含本次修正的明确说明。

没有直接修改money-bird，也没有把消息发送成功宣称为该项目已经完成调整或验证；该聊天的后续执行不属于本轮完成条件。插件版本/缓存保持0.6.1，本轮后续若发行安装，必须按仓库约定升版。
