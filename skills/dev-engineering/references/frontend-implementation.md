# 前端工程与交互落实

用于实际页面、组件和前端数据行为。有效产品/交互与设计/UI 是实现依据；采用[技术栈基线](../../dev-architecture/references/technology-stack.md)和[代码规范](../../dev-architecture/references/code-standards.md)，已有工程局部工作保留有效基线。

## 组件与设计复用

新交互型 Web 使用 Vite + React + TypeScript，全栈用 Next.js，纯静态用 Astro。B 端按 Ant Design 规范优先使用 antd 的现有组件/行为，C Web 优先 shadcn/ui；其他 C 端先按共同约定完成网上参考。现成能力不足再做明确业务组合，不重新自建已有通用控件。

复用项目 Tokens、组件和路由模式，落实目标密度、内容、设备与状态。自有共享库按[源码复用约定](../../dev-visual/references/ui-stack-and-components.md)复制/参考到项目，记录源路径与 Git 提交/哈希、修改和验证；不转为内部 npm 包依赖。公开第三方依赖按项目正常锁定，不能把“复制自有源码”误解为复制全部第三方库。

## 状态与数据

把产品定义的加载、空、编辑、提交、成功、失败、禁用和权限状态转为可观察行为；正常和恢复状态使用真实契约与文案。React 状态保留必要来源，能派生的值在渲染中计算；避免互相矛盾、重复和脱离来源的状态。[React 状态结构](https://react.dev/learn/choosing-the-state-structure)

用户事件在相应事件处理器中触发；Effect 处理必要外部同步，不用 Effect 绕行派生状态和事件逻辑。数据获取沿用项目/框架已有能力；手动异步调用需处理清理、旧响应覆盖和任务切换，取消浏览器请求不表示服务端撤销业务。[React Effect 与事件/数据获取](https://react.dev/learn/you-might-not-need-an-effect)

提交反馈与服务端状态一致。防止本次交互重复提交，服务端重复语义仍依契约；失败保留约定输入/上下文并提供重试，成功后的列表/缓存更新与重新读取一致。不要用 Toast 成功、乐观更新或 localStorage 掩盖服务端未写入；采用乐观更新时按设计处理失败回退与读回。

表单限制、功能透出和错误展示关联 RULE，前端校验与后端拒绝都需落实。异步时是否允许编辑、取消、离开及结果恢复依已确认设计，不能临时猜测并静默丢失用户数据。

## 框架边界与呈现验证

Next.js 按实际运行职责选择 Server/Client 边界；浏览器交互与客户端能力进入相应边界，服务端依赖/秘密不进入浏览器包，传递数据符合框架约束。不要为解决局部问题把全部页面改为客户端渲染。[Next Server 与 Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components)

Astro 纯静态沿用静态内容/脚本能力，只在确有需求时引入交互组件；新增服务端业务改变工程形态时回到架构决定。[Astro 脚本与事件](https://docs.astro.build/en/guides/client-side-scripts/)

使用语义化标签、可关联表单标签、稳定对象 key 与项目焦点/键盘规范；组件库使用方式遵循其现有行为。核对实际页面的导航、焦点、输入、边界内容、目标尺寸及加载/异常状态；视觉由相关规格对照实际渲染，操作与截图分别取证。原型代码进入实际工程需替换假数据/临时路由并重新验证，不以原型可点证明功能已交付。
