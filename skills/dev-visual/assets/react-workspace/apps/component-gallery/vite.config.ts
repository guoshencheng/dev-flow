import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: { alias: {
    '@dev-flow/ui-web/styles.css': fileURLToPath(new URL('../../packages/ui-web/src/styles.css', import.meta.url)),
    '@dev-flow/ui-web': fileURLToPath(new URL('../../packages/ui-web/src/index.ts', import.meta.url)),
    '@dev-flow/ui-antd': fileURLToPath(new URL('../../packages/ui-antd/src/index.ts', import.meta.url)),
  } },
  build: { rollupOptions: { input: {
    business: fileURLToPath(new URL('./index.html', import.meta.url)),
    web: fileURLToPath(new URL('./web.html', import.meta.url)),
  } } },
})
