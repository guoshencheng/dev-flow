import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import mdx from '@mdx-js/rollup'
import remarkGfm from 'remark-gfm'
import remarkFrontmatter from 'remark-frontmatter'
import rehypeSlug from 'rehype-slug'
import { context } from './scripts/core.mjs'
import { documentPlugin } from './scripts/doc-server.mjs'

const workspace = path.dirname(fileURLToPath(import.meta.url))
export default defineConfig(async () => {
  const ctx = await context(process.env.DEV_FLOW_DOC_PROJECT || workspace, (process.env.DEV_FLOW_DOC_ROOTS || 'docs/dev-flow,design').split(','))
  return {
    root: workspace,
    publicDir: false,
    plugins: [{ ...mdx({ include: /\.mdx$/, remarkPlugins: [remarkGfm, remarkFrontmatter], rehypePlugins: [rehypeSlug] }), enforce: 'pre' }, react({ include: /\.[jt]sx?$|\.mdx$/ }), documentPlugin(ctx)],
    resolve: {
      dedupe: ['react', 'react-dom'],
      alias: { react: path.join(workspace, 'node_modules/react'), 'react-dom': path.join(workspace, 'node_modules/react-dom'), antd: path.join(workspace, 'node_modules/antd') },
    },
    server: { host: '127.0.0.1', fs: { strict: true, allow: [workspace, ...ctx.roots.map((root) => root.real)] }, watch: { ignored: ['**/node_modules/**', '**/.dev/**'] } },
  }
})
