# 本机启动与交付方式

环境：Python 3.9+，只依赖标准库。项目根目录是包含 `__main__.py` 和 `order_notes/` 的目录。数据文件由调用者用 `--store` 指定；测试时应选临时路径，避免覆盖已有文件。

源码启动：在项目根目录执行 `python3 -m order_notes --store <数据文件> save --order ORD-100 --note 门口放置 --role editor`，再执行 `show --order ORD-100`。

候选交付方式：在项目根目录执行 `python3 -m zipapp . -o <输出目录>/order-notes.pyz`。从项目根目录之外用 `python3 <输出目录>/order-notes.pyz --store <数据文件> ...` 启动；`show` 应在另一次进程调用中从同一文件读回。`--fail-before-commit` 可以模拟提交前失败并检查原文件，随后不带该参数重试。

当前状态：这里只给出启动与产物生成方法；尚未打包并启动交付产物，也没有交付核验结果。无发布或线上环境。
