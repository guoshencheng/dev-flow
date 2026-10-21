import fs from 'node:fs/promises'
import path from 'node:path'
import matter from 'gray-matter'

const ignored = new Set(['node_modules', 'dist', '.git', '.dev', '.dev-flow'])
export const encodePath = (value) => value.split('/').map(encodeURIComponent).join('/')
export const viewPath = (value) => '/view/' + encodePath(value)
export const rawPath = (value) => '/__docs/file/' + encodePath(value)
const inside = (base, file) => file === base || file.startsWith(base + path.sep)
export const kindOf = (file) => {
  const ext = path.extname(file).toLowerCase()
  if (['.md', '.markdown'].includes(ext)) return 'markdown'
  if (ext === '.mdx') return 'mdx'
  if (['.html', '.htm'].includes(ext)) return 'html'
  if (['.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp', '.avif'].includes(ext)) return 'image'
  if (ext === '.pdf') return 'pdf'
  if (ext === '.docx') return 'word'
  if (ext === '.xlsx') return 'sheet'
  if (ext === '.csv') return 'csv'
  if (['.mp4', '.webm', '.mov'].includes(ext)) return 'video'
  if (['.mp3', '.wav', '.ogg', '.m4a'].includes(ext)) return 'audio'
  if (ext === '.mmd' || ext === '.mermaid') return 'mermaid'
  if (['.json', '.yaml', '.yml', '.txt', '.js', '.jsx', '.ts', '.tsx', '.css', '.scss', '.xml', '.toml', '.py', '.sh', '.sql', '.log'].includes(ext)) return 'source'
  return 'download'
}

export async function context(project, rootNames) {
  const projectRoot = await fs.realpath(path.resolve(project))
  const roots = []
  for (const name of rootNames) {
    if (path.isAbsolute(name) || name.split(/[\\/]/).includes('..')) throw new Error('文档根目录必须是项目内相对路径')
    const directory = path.resolve(projectRoot, name)
    try {
      const real = await fs.realpath(directory)
      if (!inside(projectRoot, real)) throw new Error('文档根目录超出项目范围')
      if (!(await fs.stat(real)).isDirectory()) throw new Error('文档根目录不是目录')
      roots.push({ name: path.relative(projectRoot, directory).split(path.sep).join('/'), real })
    } catch (error) { if (error.code !== 'ENOENT') throw error }
  }
  return { project: projectRoot, roots }
}

export async function checkedFile(ctx, relative) {
  if (!relative || path.isAbsolute(relative) || relative.includes('\\')) throw new Error('文件路径必须是项目内相对路径')
  const segments = relative.split('/')
  if (segments.some((part) => !part || part === '..' || part.startsWith('.') || ignored.has(part))) throw new Error('文件路径不在文档读取范围')
  const lexical = path.resolve(ctx.project, relative)
  const root = ctx.roots.find((entry) => inside(path.resolve(ctx.project, entry.name), lexical))
  if (!root) throw new Error('文件不在已指定的文档根目录')
  const real = await fs.realpath(lexical)
  if (!inside(root.real, real) || !inside(ctx.project, real)) throw new Error('链接目标超出文档根目录')
  const stat = await fs.stat(real)
  if (!stat.isFile()) throw new Error('目标不是文件')
  return { real, stat }
}

export async function catalog(ctx) {
  const files = []; const seen = new Set(); let truncated = false
  async function visit(directory) {
    const entries = await fs.readdir(directory, { withFileTypes: true })
    for (const entry of entries) {
      if (entry.name.startsWith('.') || ignored.has(entry.name)) continue
      if (files.length >= 2500) { truncated = true; return }
      const full = path.join(directory, entry.name)
      if (entry.isDirectory()) { await visit(full); continue }
      if (!entry.isFile() && !entry.isSymbolicLink()) continue
      const relative = path.relative(ctx.project, full).split(path.sep).join('/')
      if (seen.has(relative)) continue
      let checked
      try { checked = await checkedFile(ctx, relative) } catch { continue }
      const kind = kindOf(relative)
      let title = entry.name; let status = '未标状态'; let metadata = {}
      if (['markdown', 'mdx'].includes(kind) && checked.stat.size < 2 * 1024 * 1024) {
        try {
          const parsed = matter(await fs.readFile(checked.real, 'utf8'))
          metadata = parsed.data
          title = String(parsed.data.title || parsed.content.match(/^#\s+(.+)$/m)?.[1] || title)
          status = String(parsed.data.status || status)
        } catch { status = '元信息需检查' }
      }
      if (relative.split('/').includes('archive')) status = 'archived'
      seen.add(relative)
      files.push({ path: relative, title, kind, status, metadata, size: checked.stat.size, modified: checked.stat.mtime.toISOString(), viewPath: viewPath(relative), rawPath: rawPath(relative) })
    }
  }
  for (const root of ctx.roots) await visit(path.resolve(ctx.project, root.name))
  files.sort((a, b) => a.path.localeCompare(b.path, 'zh-CN'))
  return { project: ctx.project, roots: ctx.roots.map((r) => r.name), files, truncated }
}

export function contentType(file) {
  const ext = path.extname(file).toLowerCase()
  const types = { '.html': 'text/html', '.htm': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif', '.avif': 'image/avif', '.pdf': 'application/pdf', '.mp4': 'video/mp4', '.webm': 'video/webm', '.mp3': 'audio/mpeg', '.wav': 'audio/wav', '.ogg': 'audio/ogg' }
  return types[ext] || (kindOf(file) === 'source' || ['markdown', 'mdx', 'mermaid', 'csv'].includes(kindOf(file)) ? 'text/plain; charset=utf-8' : 'application/octet-stream')
}
