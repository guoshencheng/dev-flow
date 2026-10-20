import test from 'node:test'
import assert from 'node:assert/strict'
import { promises as fs } from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { initDesignTemplate } from './design-template.mjs'

async function isolated(run) {
  const project = await fs.mkdtemp(path.join(os.tmpdir(), 'dev-flow-design-test-'))
  try { await run(project) } finally { await fs.rm(project, { recursive: true, force: true }) }
}

test('复制自包含工程、独立规范与锁文件，排除运行产物', () => isolated(async (project) => {
  const { target } = await initDesignTemplate({ project })
  assert.equal(target, path.join(await fs.realpath(project), 'docs/dev-flow/visual/prototype'))
  assert.ok(await fs.stat(path.join(target, 'src/features/orders/views/MobileOrderPage.tsx')))
  assert.ok(await fs.stat(path.join(target, 'docs/visual/system.md')))
  assert.ok(await fs.stat(path.join(target, 'package-lock.json')))
  await assert.rejects(fs.stat(path.join(target, 'node_modules')), { code: 'ENOENT' })
  await assert.rejects(fs.stat(path.join(target, 'dist')), { code: 'ENOENT' })
  const manifest = JSON.parse(await fs.readFile(path.join(target, '.template-source.json'), 'utf8'))
  assert.equal(manifest.template, 'dev-flow-design-workspace')
  assert.match(manifest.files['src/preview/DeviceViewport.tsx'], /^[a-f0-9]{64}$/)
}))

test('重复初始化保留项目定制与其他文件', () => isolated(async (project) => {
  const { target } = await initDesignTemplate({ project })
  const custom = path.join(target, 'docs/visual/system.md')
  await fs.writeFile(custom, '项目自己的设计规范')
  await assert.rejects(initDesignTemplate({ project }), /已有内容/)
  assert.equal(await fs.readFile(custom, 'utf8'), '项目自己的设计规范')
}))

test('已有非模板目录也不会部分覆盖', () => isolated(async (project) => {
  const target = path.join(project, 'docs/dev-flow/visual/prototype')
  await fs.mkdir(target, { recursive: true })
  await fs.writeFile(path.join(target, 'existing.txt'), '保留')
  await assert.rejects(initDesignTemplate({ project }), /已有内容/)
  assert.deepEqual(await fs.readdir(target), ['existing.txt'])
}))

test('拒绝项目外路径与指向其他目录的符号链接', () => isolated(async (project) => {
  await assert.rejects(initDesignTemplate({ project, directory: '../escape' }), /子目录/)
  await assert.rejects(initDesignTemplate({ project, directory: project }), /相对目录/)
  await fs.symlink(os.tmpdir(), path.join(project, 'linked'))
  await assert.rejects(initDesignTemplate({ project, directory: 'linked/prototype' }), /符号链接/)
}))

test('支持既有空目录与包含空格的项目相对路径', () => isolated(async (project) => {
  const directory = 'design/订单 设计稿'
  await fs.mkdir(path.join(project, directory), { recursive: true })
  const { target } = await initDesignTemplate({ project, directory })
  assert.ok(await fs.stat(path.join(target, 'package.json')))
}))
