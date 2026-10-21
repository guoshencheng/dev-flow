# 订单备注 CLI（合成项目）

这是只使用 Python 3 标准库的隔离小项目。业务入口是 `python3 -m order_notes`，源码运行时在本目录执行；不需要网络、数据库或第三方依赖。项目进度和有效资料见 [文档入口](docs/dev-flow/index.md)。

启动示例（`--store` 指向调用者指定的 JSON 文件）：

```sh
python3 -m order_notes --store /tmp/order-notes.json save --order ORD-100 --note '门口放置' --role editor
python3 -m order_notes --store /tmp/order-notes.json show --order ORD-100
```

源码研发自测：`python3 -m unittest discover -s tests -v`。

交付方式：在本目录执行 `python3 -m zipapp . -o /tmp/order-notes.pyz`；随后可以从别的工作目录运行 `python3 /tmp/order-notes.pyz --store /tmp/order-notes.json ...`。具体产物启动和任务验证状态以本轮运行记录为准；当前尚无已验证的交付产物。
