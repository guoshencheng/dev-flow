import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { '@dev-flow/ui-antd': fileURLToPath(new URL('../../packages/ui-antd/src/index.ts', import.meta.url)) } },
})
