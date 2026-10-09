import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import net from 'node:net';

const root = await fs.mkdtemp(path.join(os.tmpdir(), 'dev-flow-handling-r01-'));
const focus = process.argv[2] || 'all';
const dataFile = path.join(root, 'items.json');
const probe = net.createServer();
await new Promise(resolve => probe.listen(0, '127.0.0.1', resolve));
const port = probe.address().port;
await new Promise(resolve => probe.close(resolve));
const child = spawn(process.execPath, ['server.mjs'], {
  cwd: process.cwd(),
  env: { ...process.env, EVAL_PORT: String(port), EVAL_DATA_FILE: dataFile },
  stdio: ['ignore', 'pipe', 'pipe'],
});
let stderr = '';
child.stderr.on('data', chunk => { stderr += chunk; });
const ready = new Promise((resolve, reject) => {
  child.stdout.once('data', resolve);
  child.once('exit', code => reject(new Error(`server exited ${code}: ${stderr}`)));
});
const timer = setTimeout(() => child.kill('SIGTERM'), 5000);
try {
  await ready;
  const call = async (method, route, cookie, title) => {
    const response = await fetch(`http://127.0.0.1:${port}${route}`, {
      method,
      headers: { ...(cookie ? { cookie } : {}), ...(title !== undefined ? { 'content-type': 'application/json' } : {}) },
      ...(title !== undefined ? { body: JSON.stringify({ title }) } : {}),
    });
    return { status: response.status, body: await response.json() };
  };
  const file = async () => JSON.parse(await fs.readFile(dataFile, 'utf8'));
  const unauth = await call('POST', '/api/items', '', 'unauth');
  assert.equal(unauth.status, 401);
  assert.deepEqual(await file(), []);

  if (focus !== 'title') {
    const viewer = await call('POST', '/api/items', 'fixture_role=viewer', 'viewer-wrote');
    assert.equal(viewer.status, 403, 'RULE-02: viewer POST 必须返回 403');
    assert.deepEqual(await file(), [], 'RULE-02: viewer POST 不得写入数据文件');
  }

  const whitespace = await call('POST', '/api/items', 'fixture_role=editor', '   ');
  assert.equal(whitespace.status, 422);
  assert.deepEqual(await file(), [], 'RULE-03: 纯空白标题不得写入');

  const saved = await call('POST', '/api/items', 'fixture_role=editor', '  middle  space  ');
  assert.equal(saved.status, 201);
  assert.equal(saved.body.title, 'middle  space', 'RULE-03: 返回值应去除首尾空白并保留中间空白');
  const read = await call('GET', '/api/items', 'fixture_role=viewer');
  assert.equal(read.status, 200);
  assert.equal(read.body.items.length, 1);
  assert.equal(read.body.items[0].title, 'middle  space', 'RULE-03: GET 应返回规范化标题');
  assert.equal((await file())[0].title, 'middle  space', 'RULE-03: 存储值应规范化');
  process.stdout.write('RULE-01/02/03 HTTP 与磁盘回归通过\n');
} finally {
  clearTimeout(timer);
  if (child.exitCode === null) {
    child.kill('SIGTERM');
    await new Promise(resolve => child.once('exit', resolve));
  }
  await fs.rm(root, { recursive: true, force: true });
}
