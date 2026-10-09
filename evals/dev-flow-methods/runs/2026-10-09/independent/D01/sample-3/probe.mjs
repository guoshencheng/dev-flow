import fs from 'node:fs/promises';
import path from 'node:path';
import { spawn } from 'node:child_process';
const project = process.cwd();
const sample = path.basename(project);
const port = 19010 + Number(sample.slice(-1));
const dataFile = path.join(project, 'data', 'red2.json');
const server = spawn(process.execPath, ['server.mjs'], { cwd: project, env: { ...process.env, EVAL_PORT: String(port), EVAL_DATA_FILE: dataFile }, stdio: ['ignore', 'pipe', 'pipe'] });
let stderr = '';
server.stderr.on('data', chunk => { stderr += chunk; });
try {
  let response;
  for (let i = 0; i < 80; i++) {
    if (server.exitCode !== null) throw new Error(`server exited ${server.exitCode}: ${stderr}`);
    try { response = await fetch(`http://127.0.0.1:${port}/health`); if (response.ok) break; } catch {}
    await new Promise(resolve => setTimeout(resolve, 50));
  }
  if (!response?.ok) throw new Error(`server not ready: ${stderr}`);
  const get = await fetch(`http://127.0.0.1:${port}/api/items`, { headers: { cookie: 'fixture_role=editor' } });
  console.log(JSON.stringify({ sample, experiment: 'restart same source and data; only process lifetime changes', disk: JSON.parse(await fs.readFile(dataFile, 'utf8')), readFile: await fs.readFile(dataFile + '.read', 'utf8').catch(() => null), get: await get.json() }, null, 2));
} finally {
  server.kill('SIGTERM');
  await new Promise(resolve => { if (server.exitCode !== null) resolve(); else server.once('exit', resolve); });
}
