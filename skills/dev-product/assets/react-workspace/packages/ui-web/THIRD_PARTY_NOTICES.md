# 第三方来源与维护边界

Button、Card 系列从 [shadcn/ui](https://github.com/shadcn-ui/ui) 官方 Registry 获取，工具调用为 `shadcn@4.21.4 add button card --yes`，采用日期 2026-10-07，配置 new-york、TypeScript、非 RSC。Registry 内容会变化，工具版本不等于组件源码版本；本仓库提交中的源码与 package-lock.json 构成可复现快照。

上游组件路径：`src/components/ui/button.tsx`、`src/components/ui/card.tsx`。本次将工具函数导入改为公共库的相对路径，补齐代码实际使用的 class-variance-authority 依赖，确保组件不依赖原型项目的路径别名。`src/lib/utils.ts` 按 shadcn 的 clsx/tailwind-merge 方式实现；`src/styles.css` 使用 neutral 主题 Token 并限定类扫描范围。ActionCard 为本仓库在 Card/Button 上形成的组合。

上游采用 MIT 许可，原许可保存在 LICENSE.shadcn，来源 [上游 LICENSE.md](https://github.com/shadcn-ui/ui/blob/main/LICENSE.md)。维护与源码共享保留该许可；当前自有组合与主题未设公开发布许可，包的 UNLICENSED 标识不替代第三方文件的许可。

后续更新记录来源、工具版本、采用日期、源码变化与行为影响；实际复验键盘、焦点、禁用和相关状态，再更新包版本与清单。直接复制到项目时保留本记录和上游许可。
