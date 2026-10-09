import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:net';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';

const candidate = process.argv[2];
assert.ok(['previous', 'current'].includes(candidate), '用法: node viewer.test.mjs previous|current');
const temp = await fs.mkdtemp(path.join(os.tmpdir(), 'dev-flow-t02-'));
const dataFile = path.join(temp, 'items.json');
const port = await new Promise((resolve, reject) => {
  const socket = createServer();
  socket.once('error', reject);
  socket.listen(0, '127.0.0.1', () => {
    const selected = socket.address().port;
    socket.close(() => resolve(selected));
  });
});
const child = spawn(process.execPath, ['server.mjs'], {
  cwd: path.join(import.meta.dirname, candidate),
  env: { ...process.env, EVAL_PORT: String(port), EVAL_DATA_FILE: dataFile },
  stdio: ['ignore', 'pipe', 'pipe'],
});
let serverOutput = '';
child.stdout.on('data', chunk => { serverOutput += chunk; });
child.stderr.on('data', chunk => { serverOutput += chunk; });
const url = `http://127.0.0.1:${port}`;
async function request(route, options = {}) {
  const response = await fetch(url + route, options);
  return { status: response.status, body: await response.text(), response };
}
async function login(role) {
  const result = await request('/test/login', {
    method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ role }),
  });
  assert.equal(result.status, 200);
  return result.response.headers.get('set-cookie').split(';')[0];
}
async function post(cookie, title) {
  return request('/api/items', {
    method: 'POST', headers: { 'content-type': 'application/json', ...(cookie ? { cookie } : {}) },
    body: JSON.stringify({ title }),
  });
}
try {
  let ready = false;
  for (let i = 0; i < 100; i++) {
    if (child.exitCode !== null) throw new Error(`服务提前退出: ${serverOutput}`);
    try { ready = (await request('/health')).status === 200; } catch {}
    if (ready) break;
    await new Promise(resolve => setTimeout(resolve, 30));
  }
  assert.ok(ready, `服务未启动: ${serverOutput}`);
  const editor = await login('editor');
  const viewer = await login('viewer');
  const save = await post(editor, '  初始条目  ');
  assert.equal(save.status, 201, `editor 保存: ${save.body}`);
  assert.equal(JSON.parse(save.body).title, '初始条目');
  const before = await fs.readFile(dataFile, 'utf8');
  assert.deepEqual(JSON.parse(before).map(item => item.title), ['初始条目']);
  const visible = await request('/api/items', { headers: { cookie: viewer } });
  assert.equal(visible.status, 200);
  assert.deepEqual(JSON.parse(visible.body).items.map(item => item.title), ['初始条目']);
  const denied = await post(viewer, '越权条目');
  const afterDenied = await fs.readFile(dataFile, 'utf8');
  assert.equal(denied.status, 403, `RULE-02 viewer POST 应为 403，实际 ${denied.status}: ${denied.body}; 存储变化=${before !== afterDenied}`);
  assert.equal(afterDenied, before, 'RULE-02 viewer POST 不得写入存储');
  const anonymous = await post(undefined, '匿名条目');
  assert.equal(anonymous.status, 401);
  assert.equal(await fs.readFile(dataFile, 'utf8'), before);
  const blank = await post(editor, '  ');
  assert.equal(blank.status, 422);
  assert.equal(await fs.readFile(dataFile, 'utf8'), before);
  const page = await request('/', { headers: { cookie: editor } });
  assert.equal(page.status, 200);
  assert.match(page.body, /fetch\('\/api\/items'\)/);
  console.log(`${candidate}: RULE-01/02/03 HTTP、读取、权限拒绝、数据文件副作用检查通过`);
} finally {
  child.kill('SIGTERM');
  await new Promise(resolve => { if (child.exitCode !== null) resolve(); else child.once('exit', resolve); });
  await fs.rm(temp, { recursive: true, force: true });
}
