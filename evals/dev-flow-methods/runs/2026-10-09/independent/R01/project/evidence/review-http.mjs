import { spawn } from 'node:child_process';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import net from 'node:net';

const root = await fs.mkdtemp(path.join(os.tmpdir(), 'dev-flow-review-r01-'));
const dataFile = path.join(root, 'items.json');
const probe = net.createServer();
await new Promise((resolve) => probe.listen(0, '127.0.0.1', resolve));
const port = probe.address().port;
await new Promise((resolve) => probe.close(resolve));
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
  const observations = {};
  observations.unauthPost = await call('POST', '/api/items', '', 'unauth');
  observations.afterUnauth = await file();
  observations.viewerPost = await call('POST', '/api/items', 'fixture_role=viewer', 'viewer-wrote');
  observations.afterViewer = await file();
  observations.whitespacePost = await call('POST', '/api/items', 'fixture_role=editor', '   ');
  observations.afterWhitespace = await file();
  observations.editorPost = await call('POST', '/api/items', 'fixture_role=editor', '  trimmed  ');
  observations.editorGet = await call('GET', '/api/items', 'fixture_role=editor');
  observations.finalFile = await file();
  process.stdout.write(JSON.stringify({ port, dataFile, observations }, null, 2) + '\n');
} finally {
  clearTimeout(timer);
  child.kill('SIGTERM');
  await new Promise(resolve => child.once('exit', resolve));
  await fs.rm(root, { recursive: true, force: true });
}
