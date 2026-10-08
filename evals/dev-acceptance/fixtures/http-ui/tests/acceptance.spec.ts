import { randomUUID } from 'node:crypto';
import { test, expect, type APIRequestContext } from '@playwright/test';

const titleFor = (id: string) => `${id}-${randomUUID()}`;
async function login(request: APIRequestContext, role = 'editor') {
  expect((await request.post('/test/login', { data: { role } })).status()).toBe(200);
}
async function items(request: APIRequestContext) {
  const response = await request.get('/api/items');
  expect(response.status()).toBe(200);
  return (await response.json()).items as { id: string; title: string }[];
}

test('TC-API-01 编辑者保存后可通过真实接口读回', async ({ request }) => {
  await login(request);
  const title = titleFor('TC-API-01');
  const response = await request.post('/api/items', { data: { title } });
  expect(response.status()).toBe(201);
  const saved = await response.json();
  expect(saved).toEqual({ id: expect.any(String), title });
  expect(await items(request)).toContainEqual(saved);
});

test('TC-API-02 查看者直接请求拒绝且无写入', async ({ request }) => {
  await login(request, 'viewer');
  const title = titleFor('TC-API-02');
  const before = await items(request);
  const response = await request.post('/api/items', { data: { title } });
  // soft 保留状态与副作用两项失败，便于原问题反馈。
  expect.soft(response.status()).toBe(403);
  expect.soft(await items(request)).toEqual(before);
});

test('TC-API-03 无效输入拒绝且没有业务副作用', async ({ request }) => {
  await login(request);
  const before = await items(request);
  const response = await request.post('/api/items', { data: { title: '   ' } });
  expect(response.status()).toBe(422);
  expect(await response.json()).toEqual({ error: 'INVALID_TITLE' });
  expect(await items(request)).toEqual(before);
});

test('TC-E2E-01 界面保存、请求与读回、刷新仍可见', async ({ page }) => {
  await login(page.request);
  await page.goto('/');
  await expect(page.getByRole('list')).toHaveAttribute('aria-busy', 'false');
  const title = titleFor('TC-E2E-01');
  await page.getByLabel('标题').fill(title);
  const responsePromise = page.waitForResponse((response) =>
    new URL(response.url()).pathname === '/api/items' && response.request().method() === 'POST');
  await page.getByRole('button', { name: '保存', exact: true }).click();
  const response = await responsePromise;
  expect(response.request().postDataJSON()).toEqual({ title });
  expect(response.status()).toBe(201);
  const saved = await response.json();
  expect(saved).toEqual({ id: expect.any(String), title });
  await expect(page.getByRole('status')).toHaveText('保存成功');
  await expect(page.getByRole('listitem').filter({ hasText: title })).toHaveText(title);
  expect.soft(await items(page.request)).toContainEqual(saved);
  await page.reload();
  await expect(page.getByRole('listitem').filter({ hasText: title })).toHaveText(title);
});

test('TC-UI-01 ui-isolated 服务失败保留输入且恢复后能重试', async ({ page }) => {
  await login(page.request);
  await page.goto('/');
  await expect(page.getByRole('list')).toHaveAttribute('aria-busy', 'false');
  const title = titleFor('TC-UI-01');
  await page.getByLabel('标题').fill(title);
  const failSave = async (route: import('@playwright/test').Route) => {
    if (route.request().method() === 'POST') await route.fulfill({ status: 500, json: { error: 'SERVICE_FAILURE' } });
    else await route.continue();
  };
  await page.route('**/api/items', failSave);
  await page.getByRole('button', { name: '保存', exact: true }).click();
  await expect(page.getByRole('status')).toHaveText('保存失败，请重试');
  await expect(page.getByLabel('标题')).toHaveValue(title);
  await expect(page.getByRole('button', { name: '保存', exact: true })).toBeEnabled();
  await page.unroute('**/api/items', failSave);
  await page.getByRole('button', { name: '保存', exact: true }).click();
  await expect(page.getByRole('status')).toHaveText('保存成功');
  expect(await items(page.request)).toEqual(expect.arrayContaining([expect.objectContaining({ title })]));
});

test('TC-UI-02 查看者界面透出禁用状态', async ({ page }) => {
  await login(page.request, 'viewer');
  await page.goto('/');
  await expect(page.getByRole('button', { name: '保存', exact: true })).toBeDisabled();
});
