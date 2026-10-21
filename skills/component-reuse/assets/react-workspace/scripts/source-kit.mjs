import { execFileSync } from 'node:child_process'
import { createHash } from 'node:crypto'
import { existsSync, lstatSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { dirname, relative, resolve, sep } from 'node:path'
import { fileURLToPath } from 'node:url'

export const workspace = resolve(fileURLToPath(new URL('../', import.meta.url)))
export const manifest = JSON.parse(readFileSync(resolve(workspace, 'catalog.json'), 'utf8'))
const hash = (content) => createHash('sha256').update(content).digest('hex')
function inside(root, path) {
  const result = resolve(root, path)
  if (!result.startsWith(root + sep)) throw new Error(`路径超出目标目录：${path}`)
  return result
}
function noSymlinkBelow(root, path) {
  let current = root
  for (const part of relative(root, path).split(sep)) {
    current = resolve(current, part)
    if (existsSync(current) && lstatSync(current).isSymbolicLink()) throw new Error(`目标包含符号链接，请指定实际目录：${current}`)
  }
}
export function findComponent(id) {
  const component = manifest.components.find((item) => item.id === id)
  if (!component) throw new Error(`没有组件 ${id}。可用 ID：${manifest.components.map((item) => item.id).join(', ')}`)
  return component
}
export function gitSource() {
  try {
    const baseCommit = execFileSync('git', ['rev-parse', 'HEAD'], { cwd: workspace, encoding: 'utf8' }).trim()
    const modified = execFileSync('git', ['status', '--porcelain', '--', '.'], { cwd: workspace, encoding: 'utf8' }).trim().length > 0
    return { sourceCommit: modified ? null : baseCommit, sourceBaseCommit: baseCommit, sourceWorkingTreeModified: modified }
  } catch { return { sourceCommit: null, sourceBaseCommit: null, sourceWorkingTreeModified: null } }
}
export function sourceBundle(component) {
  const raw = readFileSync(inside(workspace, component.example), 'utf8')
  const code = component.usageReplacements.reduce((text, [from, to]) => text.replaceAll(from, to), raw)
  if (code.includes('@dev-flow/')) throw new Error(`使用示例仍依赖内部工作区：${component.id}`)
  const files = component.files.map((file) => {
    const content = readFileSync(inside(workspace, file.source), 'utf8')
    return { ...file, content, sha256: hash(content) }
  })
  return { ...component, ...gitSource(), usageBase: 'src/Example.tsx', destinationBase: 'src/components/dev-flow', code, files }
}
export function copyComponent(id, destination) {
  const bundle = sourceBundle(findComponent(id))
  const target = resolve(destination)
  const plan = bundle.files.map((file) => ({ ...file, path: inside(target, file.target) }))
  const recordPath = inside(target, `.component-sources/${id}.json`)
  let previous = {}
  // 先核对完整文件集，再写入；保留项目已经修改过的实现。
  for (const file of [...plan, { path: recordPath }]) noSymlinkBelow(target, file.path)
  for (const file of plan) {
    if (existsSync(file.path) && readFileSync(file.path, 'utf8') !== file.content) {
      throw new Error(`保留项目已有文件：${file.path}。请比较差异后合并，或选一个新的目标目录；未复制任何源码。`)
    }
  }
  if (existsSync(recordPath)) {
    previous = JSON.parse(readFileSync(recordPath, 'utf8'))
    if (previous.componentId !== id || previous.adoptionMode !== 'copy-source') throw new Error(`来源记录已被其他内容占用：${recordPath}`)
  }
  const created = []
  const reused = []
  for (const file of plan) {
    if (existsSync(file.path)) { reused.push(file.target); continue }
    mkdirSync(dirname(file.path), { recursive: true })
    writeFileSync(file.path, file.content, { flag: 'wx' })
    created.push(file.target)
  }
  const record = { ...previous, schemaVersion: 1, componentId: id, adoptionMode: 'copy-source', sourceRepository: 'dev-flow',
    ...gitSource(), copiedAt: new Date().toISOString(),
    files: bundle.files.map(({ source, target: fileTarget, sha256 }) => ({ source, target: fileTarget, sourceSha256: sha256 })),
    verifiedDependencies: bundle.verifiedDependencies, styleDependencies: bundle.styleDependencies || {}, setup: bundle.setup,
  }
  mkdirSync(dirname(recordPath), { recursive: true })
  writeFileSync(recordPath, JSON.stringify(record, null, 2) + '\n')
  return { componentId: id, adoptionMode: 'copy-source', destination: target, created, reused, recordPath,
    verifiedDependencies: bundle.verifiedDependencies, styleDependencies: bundle.styleDependencies || {}, setup: bundle.setup,
    note: '源码由项目直接维护；未修改项目依赖、入口或主题。示例以 src/Example.tsx 和 src/components/dev-flow 为基准，其他位置调整相对导入。',
  }
}
