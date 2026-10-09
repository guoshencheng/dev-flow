# 隔离条目应用契约

RULE-01：fixture editor 可以保存非空标题，成功返回 201，保存后通过 GET /api/items 和刷新页面仍可见。
RULE-02：fixture viewer 可读取、不能写入，POST 返回 403 且没有任何存储写入副作用；未登录返回 401。
RULE-03：标题去除首尾空白，纯空白返回 422 且没有副作用。
身份通过测试 Cookie fixture_role=editor|viewer 指定，不代表生产身份方案。
服务入口为 node server.mjs，需要独立 EVAL_PORT 和 EVAL_DATA_FILE。存储是 JSON 文件，页面为遗留 HTML/JS。
仅隔离案例，沿用既有有效预期；不需要重新要求用户确认用例，也不部署。
