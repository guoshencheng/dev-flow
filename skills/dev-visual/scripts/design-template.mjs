import { createHash } from 'node:crypto'
import { promises as fs } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const sourceDirectory = fileURLToPath(new URL('../assets/design-workspace/', import.meta.url))
const excluded = new Set(['node_modules', 'dist', '.git', '.dev', '.DS_Store'])

async function exists(file) {
  try { return await fs.lstat(file) } catch (error) { if (error.code === 'ENOENT') return null; throw error }
}

async function listSource(directory, prefix = '') {
  const files = []
  for (const entry of await fs.readdir(directory, { withFileTypes: true })) {
    if (excluded.has(entry.name) || (entry.name.startsWith('.env') && !['.env.example', '.env.sample'].includes(entry.name))) continue
    if (entry.isSymbolicLink()) throw new Error(`模板源码含符号链接，保留并检查：${entry.name}`)
    const relative = path.join(prefix, entry.name)
    if (entry.isDirectory()) files.push(...await listSource(path.join(directory, entry.name), relative))
    else if (entry.isFile()) files.push(relative)
  }
  return files.sort()
}

export async function initDesignTemplate({ project, directory = 'design/prototype' }) {
  if (!project) throw new Error('需要 --project 指定实际项目目录。')
  const projectRoot = await fs.realpath(path.resolve(project))
  if (!(await fs.stat(projectRoot)).isDirectory()) throw new Error('项目路径不是目录。')
  if (path.isAbsolute(directory)) throw new Error('--dir 必须是项目内相对目录。')
  const target = path.resolve(projectRoot, directory)
  const relative = path.relative(projectRoot, target)
  if (!relative || relative === '..' || relative.startsWith(`..${path.sep}`)) throw new Error('目标必须位于项目子目录内。')
  let ancestor = projectRoot
  for (const part of relative.split(path.sep)) {
    ancestor = path.join(ancestor, part)
    const info = await exists(ancestor)
    if (info?.isSymbolicLink()) throw new Error(`目标路径含符号链接，保留已有内容：${ancestor}`)
    if (info && !info.isDirectory()) throw new Error(`目标路径已有文件，保留：${ancestor}`)
  }
  const initial = await exists(target)
  if (initial && (await fs.readdir(target)).length > 0) throw new Error(`目标已有内容，保留项目修改；请继续维护该工程，不重新初始化：${target}`)
  const files = await listSource(sourceDirectory)
  if (!files.includes('package-lock.json')) throw new Error('模板缺少锁文件，先完成模板构建。')
  await fs.mkdir(path.dirname(target), { recursive: true })
  const temporary = await fs.mkdtemp(path.join(path.dirname(target), '.design-template-'))
  try {
    const hashes = {}
    for (const file of files) {
      const content = await fs.readFile(path.join(sourceDirectory, file))
      const destination = path.join(temporary, file)
      await fs.mkdir(path.dirname(destination), { recursive: true })
      await fs.writeFile(destination, content)
      hashes[file] = createHash('sha256').update(content).digest('hex')
    }
    const packageInfo = JSON.parse(await fs.readFile(path.join(sourceDirectory, 'package.json'), 'utf8'))
    await fs.writeFile(path.join(temporary, '.template-source.json'), `${JSON.stringify({
      template: 'dev-flow-design-workspace', version: packageInfo.version, files: hashes,
    }, null, 2)}\n`)
    // rename 遇到非空目标会失败，保留在复制期间新增的项目内容。
    await fs.rename(temporary, target)
    return { target, files: files.length, version: packageInfo.version, next: ['npm ci', 'npm run dev'], overview: '#/overview/pages' }
  } finally {
    await fs.rm(temporary, { recursive: true, force: true })
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const [command, ...args] = process.argv.slice(2)
    if (command !== 'init') throw new Error('用法：node design-template.mjs init --project /项目绝对路径 [--dir design/prototype]')
    const options = {}
    for (let index = 0; index < args.length; index += 2) {
      const name = args[index]
      const value = args[index + 1]
      if (!['--project', '--dir'].includes(name) || !value || value.startsWith('--')) throw new Error(`参数无效：${name}`)
      options[name.slice(2)] = value
    }
    console.log(JSON.stringify(await initDesignTemplate({ project: options.project, directory: options.dir }), null, 2))
  } catch (error) {
    console.error(error.message)
    process.exitCode = 1
  }
}
