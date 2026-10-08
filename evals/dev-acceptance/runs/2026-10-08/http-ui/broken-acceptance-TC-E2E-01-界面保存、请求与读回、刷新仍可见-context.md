# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: acceptance.spec.ts >> TC-E2E-01 界面保存、请求与读回、刷新仍可见
- Location: tests/acceptance.spec.ts:43:1

# Error details

```
Error: expect(received).toContainEqual(expected) // deep equality

Expected value: {"id": "37a70be2-06ea-4dcc-874a-d0d86aa8184d", "title": "TC-E2E-01-4358211f-8c0b-4812-ab31-98f686acb756"}
Received array: [{"id": "7a3d9dba-0de6-47ae-a6ce-3745c91b3a45", "title": "TC-API-02-1607b700-082e-4b71-a1eb-5855cfd2e278"}]
```

```
Error: expect(locator).toHaveText(expected) failed

Locator: getByRole('listitem').filter({ hasText: 'TC-E2E-01-4358211f-8c0b-4812-ab31-98f686acb756' })
Expected: "TC-E2E-01-4358211f-8c0b-4812-ab31-98f686acb756"
Timeout: 4000ms
Error: element(s) not found

Call log:
  - Expect "toHaveText" with timeout 4000ms
  - waiting for getByRole('listitem').filter({ hasText: 'TC-E2E-01-4358211f-8c0b-4812-ab31-98f686acb756' })

```

```yaml
- heading "条目保存" [level=1]
- text: 标题
- textbox "标题"
- button "保存"
- status
- list "已保存条目":
  - listitem: TC-API-02-1607b700-082e-4b71-a1eb-5855cfd2e278
```

# Test source

```ts
  1  | import { randomUUID } from 'node:crypto';
  2  | import { test, expect, type APIRequestContext } from '@playwright/test';
  3  |
  4  | const titleFor = (id: string) => `${id}-${randomUUID()}`;
  5  | async function login(request: APIRequestContext, role = 'editor') {
  6  |   expect((await request.post('/test/login', { data: { role } })).status()).toBe(200);
  7  | }
  8  | async function items(request: APIRequestContext) {
  9  |   const response = await request.get('/api/items');
  10 |   expect(response.status()).toBe(200);
  11 |   return (await response.json()).items as { id: string; title: string }[];
  12 | }
  13 |
  14 | test('TC-API-01 编辑者保存后可通过真实接口读回', async ({ request }) => {
  15 |   await login(request);
  16 |   const title = titleFor('TC-API-01');
  17 |   const response = await request.post('/api/items', { data: { title } });
  18 |   expect(response.status()).toBe(201);
  19 |   const saved = await response.json();
  20 |   expect(saved).toEqual({ id: expect.any(String), title });
  21 |   expect(await items(request)).toContainEqual(saved);
  22 | });
  23 |
  24 | test('TC-API-02 查看者直接请求拒绝且无写入', async ({ request }) => {
  25 |   await login(request, 'viewer');
  26 |   const title = titleFor('TC-API-02');
  27 |   const before = await items(request);
  28 |   const response = await request.post('/api/items', { data: { title } });
  29 |   // soft 保留状态与副作用两项失败，便于原问题反馈。
  30 |   expect.soft(response.status()).toBe(403);
  31 |   expect.soft(await items(request)).toEqual(before);
  32 | });
  33 |
  34 | test('TC-API-03 无效输入拒绝且没有业务副作用', async ({ request }) => {
  35 |   await login(request);
  36 |   const before = await items(request);
  37 |   const response = await request.post('/api/items', { data: { title: '   ' } });
  38 |   expect(response.status()).toBe(422);
  39 |   expect(await response.json()).toEqual({ error: 'INVALID_TITLE' });
  40 |   expect(await items(request)).toEqual(before);
  41 | });
  42 |
  43 | test('TC-E2E-01 界面保存、请求与读回、刷新仍可见', async ({ page }) => {
  44 |   await login(page.request);
  45 |   await page.goto('/');
  46 |   await expect(page.getByRole('list')).toHaveAttribute('aria-busy', 'false');
  47 |   const title = titleFor('TC-E2E-01');
  48 |   await page.getByLabel('标题').fill(title);
  49 |   const responsePromise = page.waitForResponse((response) =>
  50 |     new URL(response.url()).pathname === '/api/items' && response.request().method() === 'POST');
  51 |   await page.getByRole('button', { name: '保存', exact: true }).click();
  52 |   const response = await responsePromise;
  53 |   expect(response.request().postDataJSON()).toEqual({ title });
  54 |   expect(response.status()).toBe(201);
  55 |   const saved = await response.json();
  56 |   expect(saved).toEqual({ id: expect.any(String), title });
  57 |   await expect(page.getByRole('status')).toHaveText('保存成功');
  58 |   await expect(page.getByRole('listitem').filter({ hasText: title })).toHaveText(title);
  59 |   expect.soft(await items(page.request)).toContainEqual(saved);
  60 |   await page.reload();
> 61 |   await expect(page.getByRole('listitem').filter({ hasText: title })).toHaveText(title);
     |                                                                       ^ Error: expect(locator).toHaveText(expected) failed
  62 | });
  63 |
  64 | test('TC-UI-01 ui-isolated 服务失败保留输入且恢复后能重试', async ({ page }) => {
  65 |   await login(page.request);
  66 |   await page.goto('/');
  67 |   await expect(page.getByRole('list')).toHaveAttribute('aria-busy', 'false');
  68 |   const title = titleFor('TC-UI-01');
  69 |   await page.getByLabel('标题').fill(title);
  70 |   const failSave = async (route: import('@playwright/test').Route) => {
  71 |     if (route.request().method() === 'POST') await route.fulfill({ status: 500, json: { error: 'SERVICE_FAILURE' } });
  72 |     else await route.continue();
  73 |   };
  74 |   await page.route('**/api/items', failSave);
  75 |   await page.getByRole('button', { name: '保存', exact: true }).click();
  76 |   await expect(page.getByRole('status')).toHaveText('保存失败，请重试');
  77 |   await expect(page.getByLabel('标题')).toHaveValue(title);
  78 |   await expect(page.getByRole('button', { name: '保存', exact: true })).toBeEnabled();
  79 |   await page.unroute('**/api/items', failSave);
  80 |   await page.getByRole('button', { name: '保存', exact: true }).click();
  81 |   await expect(page.getByRole('status')).toHaveText('保存成功');
  82 |   expect(await items(page.request)).toEqual(expect.arrayContaining([expect.objectContaining({ title })]));
  83 | });
  84 |
  85 | test('TC-UI-02 查看者界面透出禁用状态', async ({ page }) => {
  86 |   await login(page.request, 'viewer');
  87 |   await page.goto('/');
  88 |   await expect(page.getByRole('button', { name: '保存', exact: true })).toBeDisabled();
  89 | });
  90 |
```
