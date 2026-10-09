import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import fs from 'node:fs/promises';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';

const root = await fs.mkdtemp(path.join(os.tmpdir(), 'r01-re-review-'));
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
  child.once('exit', code => reject(new Error(`server exit ${code}: ${stderr}`)));
});
const timeout = setTimeout(() => child.kill('SIGTERM'), 5000);
const results = [];
try {
  await ready;
  const request = async (method, cookie, title) => {
    const response = await fetch(`http://127.0.0.1:${port}/api/items`, {
      method,
      headers: { ...(cookie ? { cookie } : {}), ...(title !== undefined ? { 'content-type': 'application/json' } : {}) },
      ...(title !== undefined ? { body: JSON.stringify({ title }) } : {}),
    });
    return { status: response.status, body: await response.json() };
  };
  const bytes = () => fs.readFile(dataFile, 'utf8');
  let before = await bytes();
  let got = await request('POST', '', 'anonymous');
  assert.equal(got.status, 401);
  assert.equal(await bytes(), before);
  results.push({ case: 'anonymous POST', result: got, unchanged: true });

  before = await bytes();
  got = await request('POST', 'fixture_role=viewer', 'viewer denied');
  assert.equal(got.status, 403);
  assert.equal(await bytes(), before);
  results.push({ case: 'viewer POST', result: got, unchanged: true });

  before = await bytes();
  got = await request('POST', 'fixture_role=editor', ' \t ');
  assert.equal(got.status, 422);
  assert.equal(await bytes(), before);
  results.push({ case: 'blank editor POST', result: got, unchanged: true });

  got = await request('POST', 'fixture_role=editor', '  middle  space  ');
  assert.equal(got.status, 201);
  assert.equal(got.body.title, 'middle  space');
  assert.equal(typeof got.body.id, 'string');
  results.push({ case: 'editor POST normalized', result: got });

  const editorGet = await request('GET', 'fixture_role=editor');
  const viewerGet = await request('GET', 'fixture_role=viewer');
  const stored = JSON.parse(await bytes());
  assert.equal(editorGet.status, 200);
  assert.equal(viewerGet.status, 200);
  assert.deepEqual(editorGet.body.items, [got.body]);
  assert.deepEqual(viewerGet.body.items, [got.body]);
  assert.deepEqual(stored, [got.body]);
  results.push({ case: 'editor/viewer GET and disk', editorGet, viewerGet, stored });

  process.stdout.write(JSON.stringify({ passed: results.length, port, cases: results }, null, 2) + '\n');
} finally {
  clearTimeout(timeout);
  child.kill('SIGTERM');
  await new Promise(resolve => child.once('exit', resolve));
  await fs.rm(root, { recursive: true, force: true });
}
