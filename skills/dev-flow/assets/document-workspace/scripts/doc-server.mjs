import fs from 'node:fs/promises'
import path from 'node:path'
import matter from 'gray-matter'
import { catalog, checkedFile, contentType } from './core.mjs'

export function documentPlugin(ctx) {
  const virtual = '\0virtual:design-mdx'
  return {
    name: 'dev-flow-documents',
    resolveId(id) { if (id === 'virtual:design-mdx') return virtual },
    async load(id) {
      if (id !== virtual) return
      const index = await catalog(ctx)
      const imports = index.files.filter((file) => file.kind === 'mdx').map((file) => `${JSON.stringify(file.path)}:()=>import(${JSON.stringify(path.join(ctx.project, file.path))})`)
      return `export default {${imports.join(',')}}`
    },
    configureServer(server) {
      server.watcher.add(ctx.roots.map((root) => path.resolve(ctx.project, root.name)))
      let timer
      const onChange = (file) => {
        if (!ctx.roots.some((root) => file.startsWith(path.resolve(ctx.project, root.name) + path.sep))) return
        const module = server.moduleGraph.getModuleById(virtual)
        if (module) server.moduleGraph.invalidateModule(module)
        clearTimeout(timer)
        timer = setTimeout(() => server.ws.send({ type: 'full-reload', path: '*' }), 120)
      }
      server.watcher.on('add', onChange).on('change', onChange).on('unlink', onChange)
      server.httpServer?.once('close', () => {
        clearTimeout(timer)
        server.watcher.off('add', onChange).off('change', onChange).off('unlink', onChange)
      })
      server.middlewares.use(async (req, res, next) => {
        const request = new URL(req.url || '/', 'http://127.0.0.1')
        if (!request.pathname.startsWith('/__docs/')) return next()
        res.setHeader('Cache-Control', 'no-store')
        const json = (value, status = 200) => {
          res.statusCode = status; res.setHeader('Content-Type', 'application/json; charset=utf-8'); res.end(JSON.stringify(value))
        }
        if (req.method !== 'GET' && req.method !== 'HEAD') return json({ error: '只接受文档读取' }, 405)
        try {
          if (request.pathname === '/__docs/index') return json(await catalog(ctx))
          if (request.pathname === '/__docs/health') return json({ kind: 'dev-flow-documents', project: ctx.project })
          const match = request.pathname.match(/^\/__docs\/(file|source)\/(.+)$/)
          if (!match) return json({ error: '文档入口不存在' }, 404)
          const relative = decodeURIComponent(match[2])
          const { real, stat } = await checkedFile(ctx, relative)
          if (stat.size > 50 * 1024 * 1024) return json({ error: '文件超过 50 MiB，请用原工具查看或提供较小导出' }, 413)
          if (match[1] === 'source') {
            if (stat.size > 2 * 1024 * 1024) return json({ error: '文本超过 2 MiB，请查看原文件或拆分文档' }, 413)
            const text = await fs.readFile(real, 'utf8')
            const parsed = ['.md', '.markdown', '.mdx'].includes(path.extname(real).toLowerCase()) ? matter(text) : { data: {}, content: text }
            return json({ path: relative, content: parsed.content, metadata: parsed.data })
          }
          res.setHeader('Content-Type', contentType(relative))
          res.setHeader('X-Content-Type-Options', 'nosniff')
          if (request.searchParams.has('download')) res.setHeader('Content-Disposition', `attachment; filename*=UTF-8''${encodeURIComponent(path.basename(relative))}`)
          res.setHeader('Content-Length', stat.size)
          if (req.method === 'HEAD') return res.end()
          res.end(await fs.readFile(real))
        } catch (error) { json({ error: error.message }, error.code === 'ENOENT' ? 404 : 400) }
      })
    },
  }
}
