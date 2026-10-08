# 代码规范与可执行检查

版本：0.1。更新日期：2026-10-08。适用于本体系的 React Web、Next.js 全栈与 Astro 静态工程。架构维护规范及模块边界，研发落实配置并修复检查，测试使用相同候选和命令核验；模型设置继续交给宿主。

## 采用成熟方案

统一采用 **EditorConfig + Prettier + ESLint + TypeScript**。配置、必要插件和版本锁保存在项目 Git 中，可复制随包源码；共享规范不依赖内部 npm 包发布。已有项目先核对有效格式器、lint 和 CI，复用能覆盖要求的工具；局部任务不同时引入第二套格式器或全仓改风格。

| 约束 | 工具与责任 |
| --- | --- |
| 编辑器一致性 | EditorConfig：UTF-8、LF、缩进与文件末尾换行 |
| 格式 | Prettier：引号、分号、空格、换行与文档格式；CLI 和编辑器使用项目同一配置/版本 |
| 代码问题 | ESLint flat config：基础推荐规则 + 相应框架/TS 推荐规则，按任务补充实际需要的规则 |
| 类型 | 新 TS 工程采用 strict 与框架适配的 tsconfig；使用实际类型检查入口 |
| 架构 | 模块允许依赖/公开入口等 ARC：按实际路径配置 import 限制或已有架构检查，再结合代码业务 Review |

Prettier 与 ESLint 分别运行，使用 `eslint-config-prettier` 在 flat config 末尾关闭冲突的风格规则；格式检查通过不证明类型、模块边界或业务成立。[Prettier 与 Linters](https://prettier.io/docs/integrating-with-linters)、[Prettier 项目配置](https://prettier.io/docs/configuration)

## 新工程格式基线

使用随包[格式配置](../assets/code-standards/base/prettierrc.json)与[EditorConfig](../assets/code-standards/base/editorconfig.txt)：2 空格、单引号、JSX 双引号、分号、尾逗号、LF；参考排版宽度 100，Markdown 段落保持原换行。这是本体系的新工程风格，已有有效项目风格可以沿用；不靠人工 Review 空格和引号。

复制[忽略配置](../assets/code-standards/base/prettierignore.txt)后按项目路径补充：生成目录、锁文件、工具生成类型、缓存和固定证据不参与重排；业务源码、测试和当前规格仍在适用检查范围。原型源码同样格式化，不能把整个 HTML/文档目录默认忽略。Astro 使用带官方插件的[Astro 格式配置](../assets/code-standards/astro/prettierrc.json)，代替通用 `.prettierrc.json`。[Astro 官方编辑器/Prettier 配置](https://docs.astro.build/en/editor-setup/)

模板使用普通文件名，复制到项目根目录时分别保存为 `.prettierrc.json`、`.editorconfig` 和 `.prettierignore`；已有文件按本次需要合并。忽略模板默认覆盖根构建目录，多包工程须添加实际各包的生成路径，不能通过忽略业务源码目录缩小检查。

## 框架与类型检查

优先采用当前版本官方初始化工程提供的配置，再合并项目实际规则；已有配置保留并核验，避免直接覆盖。按 runtime 与 peerDependencies 选兼容版本并维护锁文件，不把文档里的最新配置套入不支持的旧工具。

| 工程 | ESLint 方案 | 类型检查 |
| --- | --- | --- |
| React + Vite | `@eslint/js`、`typescript-eslint` 推荐配置，React Hooks 推荐规则；沿用 Vite 的有效框架配置 | 项目 tsconfig/引用结构对应命令，通常为 `tsc --noEmit` 或已有 `tsc -b` 检查链 |
| Next.js | 当前 Next 版本匹配的 `eslint-config-next/core-web-vitals` 与 TS 配置；使用 ESLint CLI | 使用项目入口；需要生成路由类型时先执行支持版本的 `next typegen`，再检查 TS |
| Astro | `eslint-plugin-astro` 推荐配置；按所用版本为 TS/frontmatter 配置正确解析器与相关 JS/TS 规则 | `astro check` 与需要的 `@astrojs/check`/TypeScript；覆盖 `.astro` 与项目 TS |

Next.js 16 已移除 `next lint`，不能照抄旧命令；Astro 组件检查需要 `astro check`，普通 tsc 不覆盖 `.astro`。[Next ESLint](https://nextjs.org/docs/app/api-reference/config/eslint)、[Next 类型生成](https://nextjs.org/docs/app/api-reference/config/typescript)、[Astro 类型检查](https://docs.astro.build/en/guides/typescript/)

推荐规则起步，不一次打开插件的全部规则。需要类型信息的 TS lint 规则再配置相应 projectService/项目范围，避免虚拟文件、配置和测试错误套用。strict 属于 TS 新工程基线，ESLint 更严格规则按收益选用。[typescript-eslint 配置](https://typescript-eslint.io/getting-started/)、[React Hooks 官方规则](https://react.dev/reference/eslint-plugin-react-hooks)、[Astro ESLint 配置](https://ota-meshi.github.io/eslint-plugin-astro/user-guide/)、[TypeScript strict](https://www.typescriptlang.org/tsconfig/strict.html)

## 命名、职责与依赖

- React 组件/类型采用 PascalCase，变量/函数采用 camelCase，Hook 使用 `use` 前缀；框架规定的 `page.tsx`、`layout.tsx`、Astro 路由等文件名服从框架约定。既有目录命名风格保持一致，注释解释规则、边界与取舍。
- 领域/用例与展示、协议、存储适配的职责依[整洁架构](clean-architecture.md)细分。统一模块公开入口，跨域通过明确契约；共享目录只放有实际消费和稳定职责的能力，不用 `utils` 承载隐藏的业务核心。
- 按真实模块路径约束禁止 import：例如内层禁止 ORM/HTTP/React 依赖，跨域禁止引用私有实现；考虑别名和 type-only 依赖。路径限制检查是辅助，仍沿业务链路验证数据所有权和副作用。
- 外部输入在相应边界解析/校验，类型断言不代替运行时校验；错误与恢复遵循用例契约。Next 的 Server/Client 依赖和配置边界写入模块地图。
- 文件和函数按职责与变化原因拆分；不设置全体系统一的行数上限。规则禁用/检查例外说明原因和作用范围，不通过忽略当前必需源码或降低验收使实现通过。

## Agent 接入与研发循环

首次建立工程规范时核对现有配置、源码风格和安装链，在项目内复制/合并上述配置，并按框架接入兼容的成熟工具。将[脚本片段](../assets/code-standards/package-scripts.json)合并进现有 package.json，保留 dev/build/test 等实际入口。片段只提供 format、format:check、lint；typecheck/test/build/架构检查必须取项目实际命令。

| 入口 | 用途 |
| --- | --- |
| `format` | 显式格式化本次相关文件；首次接入先确定范围，再安排必要的完整格式基线 |
| `format:check` | 在当前声明范围内只读检查格式，失败后修复并复查 |
| `lint` | 检查代码规则；在框架有效配置基础上执行，不只检查配置文件 |
| `typecheck`、测试、build、架构检查 | 使用项目实际入口分别证明对应结果，按既有依赖和并发要求运行 |

用项目包管理器安装兼容依赖并锁定版本；无需为了规范切换管理器。新工程示例调用 `npm run format -- src/Feature.tsx` 只修改指定文件。`format` 必须显式传入目标，完整格式基线使用 `npm run format -- .`；已有工程局部修复传入本次路径，脚本不隐式追加全仓目标。

本地修改后执行对应格式/静态/类型及必要行为检查，失败回到研发修复。CI 使用只读检查和适用测试/build，不在 CI 自动修改源文件。编辑器保存格式化与 lint-staged/Husky 可以按项目需要配置，CI 是可复现的共同入口，不要求每个项目增加 Git hook。

首次接入有大量历史问题时登记具体基线、覆盖和遗留范围，逐步收敛；本次新问题需处理，不能把“历史有问题”写成整体通过。格式统一与业务变更分开组织，复盘按配置/源码变化更新规则与证据。

## 项目维护

沿用现有工程规范，无规范时保存 `docs/dev-flow/engineering/code-standards.md`；架构入口和 `architecture/stack.md` 链接它。保存采用工具/版本、权威配置、适用范围、检查命令、规则理由/例外及源码版本。配置或框架升级后实际验证相关语言/文件、故意格式错误与修复后的只读检查；真实业务验证另行执行。
