import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('/Users/guoshencheng/Documents/work/dev-flow/.dev-flow/acceptance-eval-e7f67be3/project/node_modules/playwright');
const browserPath = '/Users/guoshencheng/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
const project = process.cwd();
const sample = path.basename(project);
const phase = process.argv[2];
const port = 19010 + Number(sample.slice(-1));
const base = `http://127.0.0.1:${port}`;
const dataFile = path.join(project, 'data', `${phase}.json`);
await fs.mkdir(path.dirname(dataFile), { recursive: true });
await fs.rm(dataFile, { force: true });
await fs.rm(dataFile + '.read', { force: true });
const server = spawn(process.execPath, ['server.mjs'], { cwd: project, env: { ...process.env, EVAL_PORT: String(port), EVAL_DATA_FILE: dataFile }, stdio: ['ignore', 'pipe', 'pipe'] });
let stderr = '';
server.stderr.on('data', chunk => { stderr += chunk.toString(); });
let browser;
const record = { sample, phase, port, dataFile, observations: {} };
async function ready() {
  for (let i = 0; i < 80; i++) {
    if (server.exitCode !== null) throw new Error(`server exited ${server.exitCode}: ${stderr}`);
    try { const r = await fetch(base + '/health'); if (r.ok) return; } catch {}
    await new Promise(resolve => setTimeout(resolve, 50));
  }
  throw new Error(`server not ready: ${stderr}`);
}
try {
  await ready();
  browser = await chromium.launch({ headless: true, executablePath: browserPath });
  const context = await browser.newContext();
  record.observations.login = (await context.request.post(base + '/test/login', { data: { role: 'editor' } })).status();
  const page = await context.newPage();
  await page.goto(base + '/');
  await page.locator('ul').getAttribute('aria-busy');
  await page.locator('ul[aria-busy="false"]').waitFor({ state: 'attached' });
  await page.locator('#title').fill('  浏览器条目  ');
  const post = page.waitForResponse(r => r.url() === base + '/api/items' && r.request().method() === 'POST');
  await page.getByRole('button', { name: '保存' }).click();
  const postResponse = await post;
  record.observations.post = { status: postResponse.status(), body: await postResponse.json() };
  await page.getByRole('status').getByText('保存成功').waitFor();
  record.observations.beforeReload = await page.locator('ul li').allTextContents();
  record.observations.diskAfterPost = JSON.parse(await fs.readFile(dataFile, 'utf8'));
  record.observations.readFileAfterPost = await fs.readFile(dataFile + '.read', 'utf8').catch(() => null);
  const getResponse = await context.request.get(base + '/api/items');
  record.observations.get = { status: getResponse.status(), body: await getResponse.json() };
  await page.reload();
  await page.locator('ul[aria-busy="false"]').waitFor({ state: 'attached' });
  record.observations.afterReload = await page.locator('ul li').allTextContents();
  const viewer = await browser.newContext();
  await viewer.request.post(base + '/test/login', { data: { role: 'viewer' } });
  const viewerPost = await viewer.request.post(base + '/api/items', { data: { title: '不应写入' } });
  record.observations.viewerPost = viewerPost.status();
  const anonymous = await browser.newContext();
  record.observations.anonymousGet = (await anonymous.request.get(base + '/api/items')).status();
  const whitespace = await context.request.post(base + '/api/items', { data: { title: '   ' } });
  record.observations.whitespacePost = whitespace.status();
  record.observations.diskAfterRegressions = JSON.parse(await fs.readFile(dataFile, 'utf8'));
  await viewer.close(); await anonymous.close(); await context.close();
  console.log(JSON.stringify(record, null, 2));
  assert.equal(record.observations.post.status, 201);
  assert.deepEqual(record.observations.beforeReload, ['浏览器条目']);
  assert.equal(record.observations.diskAfterPost.length, 1, 'RULE-01: save must persist');
  assert.deepEqual(record.observations.get.body.items.map(x => x.title), ['浏览器条目'], 'RULE-01: GET must see saved item');
  assert.deepEqual(record.observations.afterReload, ['浏览器条目'], 'RULE-01: reload must see saved item');
  assert.equal(record.observations.viewerPost, 403);
  assert.equal(record.observations.anonymousGet, 401);
  assert.equal(record.observations.whitespacePost, 422);
  assert.deepEqual(record.observations.diskAfterRegressions, record.observations.diskAfterPost);
  console.log('PASS RULE-01/02/03');
} finally {
  if (browser) await browser.close();
  server.kill('SIGTERM');
  await new Promise(resolve => { if (server.exitCode !== null) resolve(); else server.once('exit', resolve); });
}
