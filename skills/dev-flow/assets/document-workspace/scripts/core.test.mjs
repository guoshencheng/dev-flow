import { test } from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs/promises'
import os from 'node:os'
import path from 'node:path'
import { execFileSync, spawn } from 'node:child_process'
import { once } from 'node:events'
import { setTimeout as delay } from 'node:timers/promises'
import { fileURLToPath } from 'node:url'
import { context, checkedFile, catalog, viewPath } from './core.mjs'

test('中文、空格和特殊字符地址可逆；目录限制、链接与归档状态准确', async () => {
  const project = await fs.mkdtemp(path.join(os.tmpdir(), 'dev-flow-doc-paths-'))
  const outside = await fs.mkdtemp(path.join(os.tmpdir(), 'dev-flow-doc-outside-'))
  try {
    const relative = 'docs/product/含 空格 #问?.md'
    await fs.mkdir(path.join(project, 'docs/product/archive/2026-10-08'), { recursive: true })
    await fs.writeFile(path.join(project, relative), '---\nid: P-1\ntitle: 当前规则\nstatus: current\n---\n# 当前规则\n')
    await fs.writeFile(path.join(project, 'docs/product/archive/2026-10-08/old.md'), '---\nstatus: archived\nsupersededBy: "docs/product/含 空格 #问?.md"\n---\n# 旧规则\n')
    await fs.writeFile(path.join(project, 'docs/product/archive/2026-10-08/old.pdf'), '旧二进制资产的状态测试')
    await fs.writeFile(path.join(outside, 'private.md'), '不属于文档根目录')
    await fs.symlink(path.join(outside, 'private.md'), path.join(project, 'docs/product/escape.md'))
    const ctx = await context(project, ['docs'])
    assert.equal(decodeURIComponent(viewPath(relative).slice('/view/'.length)), relative)
    assert.equal((await checkedFile(ctx, relative)).real, await fs.realpath(path.join(project, relative)))
    await assert.rejects(checkedFile(ctx, 'docs/../../private.md'))
    await assert.rejects(checkedFile(ctx, 'docs/product/escape.md'))
    await assert.rejects(checkedFile(ctx, 'package.json'))
    const index = await catalog(ctx)
    assert.equal(index.files.length, 3)
    assert.equal(index.files.find((file) => file.path === relative).status, 'current')
    assert.equal(index.files.find((file) => file.path.includes('/archive/')).metadata.supersededBy, relative)
    assert.equal(index.files.find((file) => file.path.endsWith('old.pdf')).status, 'archived')
  } finally { await fs.rm(project, { recursive: true, force: true }); await fs.rm(outside, { recursive: true, force: true }) }
})

test('脚手架复制保留项目修改，发生晚文件冲突时不部分写入', async () => {
  const project = await fs.mkdtemp(path.join(os.tmpdir(), 'dev-flow-doc-copy-'))
  const cli = fileURLToPath(new URL('./preview.mjs', import.meta.url))
  try {
    execFileSync(process.execPath, [cli, 'init', '--project', project])
    const destination = path.join(project, 'tools/design-docs')
    await fs.writeFile(path.join(destination, 'src/styles.css'), '/* 项目自定义样式 */')
    await fs.unlink(path.join(destination, 'index.html'))
    assert.throws(() => execFileSync(process.execPath, [cli, 'init', '--project', project], { stdio: 'pipe' }))
    await assert.rejects(fs.stat(path.join(destination, 'index.html')))
    assert.equal(await fs.readFile(path.join(destination, 'src/styles.css'), 'utf8'), '/* 项目自定义样式 */')
  } finally { await fs.rm(project, { recursive: true, force: true }) }
})

test('实际服务地址、MDX 编译、复用、读取范围、正常退出和失效记录', { timeout: 20000 }, async () => {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'dev-flow-doc-runtime-'))
  const project = await fs.realpath(directory)
  const cli = fileURLToPath(new URL('./preview.mjs', import.meta.url))
  const record = path.join(project, '.dev-flow/previews/documents.json')
  const run = (...args) => execFileSync(process.execPath, [cli, ...args, '--project', project], { stdio: 'pipe', encoding: 'utf8' })
  let child
  try {
    await fs.mkdir(path.join(project, 'docs/dev-flow'), { recursive: true })
    await fs.writeFile(path.join(project, 'docs/dev-flow/中文 空格.md'), '# 独立预览\n')
    await fs.writeFile(path.join(project, 'docs/dev-flow/demo.mdx'), "---\nstatus: candidate\n---\n\nimport {Button} from 'antd'\n\n# 可运行 MDX\n\n<Button>本地组件</Button>\n")
    child = spawn(process.execPath, [cli, 'serve', '--project', project, '--port', '0'], { stdio: ['ignore', 'pipe', 'pipe'], env: { ...process.env, CI: 'true' } })
    let output = ''
    child.stdout.on('data', (chunk) => { output += chunk }); child.stderr.on('data', (chunk) => { output += chunk })
    let runtime
    for (let attempt = 0; attempt < 100; attempt++) {
      try { runtime = JSON.parse(await fs.readFile(record, 'utf8')); break } catch { if (child.exitCode !== null) throw new Error(output); await delay(50) }
    }
    assert.ok(runtime, output)
    const url = JSON.parse(run('url', '--file', 'docs/dev-flow/中文 空格.md'))
    assert.equal(url.viewUrl, runtime.origin + viewPath('docs/dev-flow/中文 空格.md'))
    assert.equal(JSON.parse(run('serve', '--port', '0')).reused, true)
    const compiled = await fetch(runtime.origin + '/@fs' + project + '/docs/dev-flow/demo.mdx')
    assert.equal(compiled.status, 200); assert.match(await compiled.text(), /可运行 MDX/)
    for (const route of ['/__docs/file/package.json', '/__docs/file/docs/dev-flow/missing.md', '/__docs/file/docs/dev-flow/%2E%2E%2F%2E%2E%2Fpackage.json', '/@fs/etc/passwd']) {
      assert.ok([400, 403, 404].includes((await fetch(runtime.origin + route)).status), route)
    }
    assert.equal((await fetch(runtime.origin + '/__docs/index', { method: 'POST' })).status, 405)
    const exited = once(child, 'exit'); child.kill('SIGTERM'); await exited
    await assert.rejects(fs.stat(record))
    // 模拟异常退出留下旧记录，不能凭旧端口生成地址。
    await fs.writeFile(record, JSON.stringify(runtime))
    assert.throws(() => run('url', '--file', 'docs/dev-flow/中文 空格.md'))
  } finally {
    if (child && child.exitCode === null && child.signalCode === null) child.kill('SIGTERM')
    await fs.rm(project, { recursive: true, force: true })
  }
})
