#!/usr/bin/env node
import fs from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { randomUUID } from 'node:crypto'

const workspace = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const args = process.argv.slice(2)
const command = args.shift()
const options = {}
while (args.length) {
  const key = args.shift()
  if (!['--project', '--roots', '--port', '--file', '--to'].includes(key) || !args.length) throw new Error('用法：preview.mjs init|serve|url --project <项目> [--roots docs/dev-flow,design] [--port 0] [--file 项目相对路径]')
  options[key.slice(2)] = args.shift()
}

async function readRuntime(project) {
  const runtime = JSON.parse(await fs.readFile(path.join(project, '.dev-flow/previews/documents.json'), 'utf8'))
  const response = await fetch(new URL('/__docs/health', runtime.origin), { signal: AbortSignal.timeout(2000) })
  const health = await response.json()
  if (!response.ok || health.kind !== 'dev-flow-documents' || health.project !== project || runtime.project !== project) throw new Error('文档预览进程与当前项目不匹配')
  return runtime
}

async function init(project) {
  const relative = options.to || 'tools/design-docs'
  if (path.isAbsolute(relative) || relative.split(/[\\/]/).includes('..')) throw new Error('目标目录必须位于项目内')
  const destination = path.resolve(project, relative)
  const files = []
  async function collect(directory, prefix = '') {
    for (const entry of await fs.readdir(directory, { withFileTypes: true })) {
      if (['node_modules', 'dist'].includes(entry.name)) continue
      const next = path.join(prefix, entry.name)
      if (entry.isDirectory()) await collect(path.join(directory, entry.name), next)
      else if (entry.isFile()) files.push(next)
    }
  }
  await collect(workspace)
  for (const file of files) {
    const target = path.join(destination, file)
    let ancestor = path.dirname(target)
    while (ancestor !== path.dirname(ancestor)) {
      try {
        const real = await fs.realpath(ancestor)
        if (real !== project && !real.startsWith(project + path.sep)) throw new Error('目标链接超出项目范围')
        break
      } catch (error) { if (error.code !== 'ENOENT') throw error }
      ancestor = path.dirname(ancestor)
    }
    try {
      if ((await fs.lstat(target)).isSymbolicLink()) throw new Error('目标文件是链接：' + target)
      const existing = await fs.readFile(target)
      if (!existing.equals(await fs.readFile(path.join(workspace, file)))) throw new Error('保留项目修改，请比较后合并：' + target)
    } catch (error) { if (error.code !== 'ENOENT') throw error }
  }
  for (const file of files) {
    const target = path.join(destination, file)
    await fs.mkdir(path.dirname(target), { recursive: true })
    try { await fs.writeFile(target, await fs.readFile(path.join(workspace, file)), { flag: 'wx' }) }
    catch (error) { if (error.code !== 'EEXIST') throw error }
  }
  console.log(JSON.stringify({ directory: destination, files: files.length, next: '在该目录 npm ci；npm run dev -- --project <项目绝对路径>' }, null, 2))
}

async function main() {
  if (!options.project) throw new Error('请显式指定 --project，避免将工具目录误当作项目')
  const project = await fs.realpath(path.resolve(options.project))
  if (command === 'init') return init(project)
  if (command === 'url') {
    if (!options.file) throw new Error('url 需要 --file 项目相对路径')
    const runtime = await readRuntime(project)
    const { context, checkedFile, viewPath, rawPath } = await import('./core.mjs')
    const ctx = await context(project, runtime.roots)
    await checkedFile(ctx, options.file)
    const indexResponse = await fetch(new URL('/__docs/index', runtime.origin), { signal: AbortSignal.timeout(5000) })
    if (!indexResponse.ok) throw new Error('文档索引无法读取')
    const index = await indexResponse.json()
    const file = index.files.find((entry) => entry.path === options.file)
    if (!file) throw new Error('文档没有进入当前索引，请检查路径或索引上限')
    console.log(JSON.stringify({ file: options.file, kind: file.kind, status: file.status, viewUrl: runtime.origin + viewPath(options.file), rawUrl: runtime.origin + rawPath(options.file), pid: runtime.pid }, null, 2))
    return
  }
  if (command !== 'serve') throw new Error('支持 init、serve、url')
  let active
  try { active = await readRuntime(project) } catch { /* 失效记录不作为可用服务。 */ }
  if (active) {
    const { context } = await import('./core.mjs')
    const requestedRoots = (await context(project, (options.roots || 'docs/dev-flow,design').split(','))).roots.map((root) => root.name)
    if (JSON.stringify(active.roots) !== JSON.stringify(requestedRoots)) throw new Error('已有文档服务使用不同根目录，请复用其入口或停止旧服务后重启')
    console.log(JSON.stringify({ reused: true, origin: active.origin, project, pid: active.pid }, null, 2))
    return
  }
  process.env.DEV_FLOW_DOC_PROJECT = project
  process.env.DEV_FLOW_DOC_ROOTS = options.roots || 'docs/dev-flow,design'
  const { context } = await import('./core.mjs')
  const ctx = await context(project, process.env.DEV_FLOW_DOC_ROOTS.split(','))
  if (!ctx.roots.length) throw new Error('指定文档根目录均不存在；先创建本次文档或通过 --roots 指定已有目录')
  const port = Number(options.port || 0)
  if (!Number.isInteger(port) || port < 0 || port > 65535) throw new Error('端口必须在 0—65535 之间')
  const runtimeFile = path.join(project, '.dev-flow/previews/documents.json')
  const instance = randomUUID()
  const cleanup = async () => {
    try {
      const current = JSON.parse(await fs.readFile(runtimeFile, 'utf8'))
      if (current.instance === instance) await fs.unlink(runtimeFile)
    } catch { /* 清理仅针对本进程的运行记录。 */ }
  }
  const { createServer } = await import('vite')
  const server = await createServer({ configFile: path.join(workspace, 'vite.config.mjs'), plugins: [{ name: 'dev-flow-runtime-cleanup', async closeServer({ reason }) { if (reason === 'close') await cleanup() } }], server: { host: '127.0.0.1', port, strictPort: true } })
  await server.listen()
  const origin = server.resolvedUrls?.local?.[0]?.replace(/\/$/, '')
  if (!origin) { await server.close(); throw new Error('无法获取 Vite 实际地址') }
  const runtime = { schemaVersion: 1, kind: 'dev-flow-documents', instance, project, roots: ctx.roots.map((root) => root.name), origin, pid: process.pid, startedAt: new Date().toISOString() }
  await fs.mkdir(path.dirname(runtimeFile), { recursive: true })
  await fs.writeFile(runtimeFile, JSON.stringify(runtime, null, 2) + '\n')
  const stop = async () => {
    await server.close()
    process.exit(0)
  }
  process.once('SIGINT', stop); process.once('SIGTERM', stop)
  console.log(JSON.stringify({ origin, project, roots: runtime.roots, pid: runtime.pid, runtimeFile }, null, 2))
  server.printUrls()
}
main().catch((error) => { console.error(error.message); process.exitCode = 1 })
