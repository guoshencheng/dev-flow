import http from 'node:http';
import { randomUUID } from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';

const port = Number(process.env.EVAL_PORT);
const dataFile = process.env.EVAL_DATA_FILE;
if (!Number.isInteger(port) || port < 1 || !dataFile) {
  throw new Error('需要 EVAL_PORT 与独立 EVAL_DATA_FILE');
}
await fs.mkdir(path.dirname(dataFile), { recursive: true });
try { await fs.writeFile(dataFile, '[]\n', { flag: 'wx' }); }
catch (error) { if (error.code !== 'EEXIST') throw error; }
const readItems = async () => JSON.parse(await fs.readFile(dataFile, 'utf8'));
const writeItems = async (items) => fs.writeFile(dataFile, JSON.stringify(items) + '\n');
const roleOf = (request) => /(?:^|;\s*)fixture_role=(editor|viewer)(?:;|$)/.exec(request.headers.cookie || '')?.[1];
const json = (response, status, data, headers = {}) => {
  response.writeHead(status, { 'content-type': 'application/json', ...headers });
  response.end(JSON.stringify(data));
};
async function body(request) {
  const chunks = [];
  for await (const chunk of request) chunks.push(chunk);
  return JSON.parse(Buffer.concat(chunks).toString());
}
function page(role) {
  return `<!doctype html><html lang="zh"><meta charset="utf-8"><title>条目保存测试</title>
<h1>条目保存</h1><form><label for="title">标题</label><input id="title" name="title">
<button type="submit" ${role === 'editor' ? '' : 'disabled'}>保存</button></form>
<p role="status"></p><ul aria-label="已保存条目" aria-busy="true"></ul>
<script>
const input = document.querySelector('input');
const button = document.querySelector('button');
const status = document.querySelector('[role="status"]');
const list = document.querySelector('ul');
const show = (item) => { const li = document.createElement('li'); li.textContent = item.title; list.append(li); };
fetch('/api/items').then(r => r.json()).then(data => data.items.forEach(show)).finally(() => list.setAttribute('aria-busy', 'false'));
document.querySelector('form').addEventListener('submit', async (event) => {
  event.preventDefault(); button.disabled = true; status.textContent = '保存中';
  try {
    const response = await fetch('/api/items', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ title: input.value }) });
    if (!response.ok) throw new Error('save failed');
    const item = await response.json(); show(item); status.textContent = '保存成功'; input.value = '';
  } catch { status.textContent = '保存失败，请重试';  }
  finally { button.disabled = false; }
});
</script></html>`;
}
const server = http.createServer(async (request, response) => {
  try {
    if (request.url === '/health') return json(response, 200, { kind: 'acceptance-fixture' });
    if (request.url === '/test/login' && request.method === 'POST') {
      const { role } = await body(request);
      if (!['editor', 'viewer'].includes(role)) return json(response, 400, { error: 'INVALID_ROLE' });
      return json(response, 200, { role }, { 'set-cookie': `fixture_role=${role}; Path=/; HttpOnly; SameSite=Lax` });
    }
    const role = roleOf(request);
    if (!role) return json(response, 401, { error: 'UNAUTHENTICATED' });
    if (request.url === '/' && request.method === 'GET') {
      response.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
      return response.end(page(role));
    }
    if (request.url === '/api/items' && request.method === 'GET') return json(response, 200, { items: await readItems() });
    if (request.url === '/api/items' && request.method === 'POST') {
      if (role !== 'editor') return json(response, 403, { error: 'FORBIDDEN' });
      const { title } = await body(request);
      if (typeof title !== 'string' || !title.trim()) return json(response, 422, { error: 'INVALID_TITLE' });
      const item = { id: randomUUID(), title: title.trim() };
      const items = await readItems();
      await writeItems([...items, item]);
      return json(response, 201, item);
    }
    return json(response, 404, { error: 'NOT_FOUND' });
  } catch { return json(response, 500, { error: 'FIXTURE_ERROR' }); }
});
server.listen(port, '127.0.0.1', () => process.stdout.write(JSON.stringify({ port }) + '\n'));
process.once('SIGTERM', () => server.close());
process.once('SIGINT', () => server.close());
