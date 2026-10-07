import { execFileSync } from 'node:child_process'
import { mkdtempSync, readFileSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const workspace = dirname(dirname(fileURLToPath(import.meta.url)))
const target = mkdtempSync(join(tmpdir(), 'dev-flow-package-check-'))
const metadata = JSON.parse(readFileSync(join(workspace, 'package.json'), 'utf8'))
const app = JSON.parse(readFileSync(join(workspace, 'apps/antd-lab/package.json'), 'utf8'))
const run = (args, cwd = workspace, capture = false) => execFileSync('npm', args, {
  cwd, encoding: 'utf8', stdio: capture ? ['ignore', 'pipe', 'inherit'] : 'inherit',
})

// 使用实际包产物，在工作区外独立安装，避免源码别名掩盖分发问题。
run(['run', 'build'])
const packed = {}
for (const name of ['@dev-flow/ui-antd', '@dev-flow/ui-web']) {
  const result = JSON.parse(run(['pack', '--workspace', name, '--pack-destination', target, '--json'], workspace, true))
  packed[name] = `file:${join(target, result[0].filename)}`
}
const toolNames = ['vite', '@vitejs/plugin-react', 'typescript', '@types/react', '@types/react-dom', '@types/node']
writeFileSync(join(target, 'package.json'), JSON.stringify({
  name: 'dev-flow-package-consumer-check', private: true, type: 'module',
  dependencies: { ...packed, react: app.dependencies.react, 'react-dom': app.dependencies['react-dom'], antd: app.dependencies.antd },
  devDependencies: Object.fromEntries(toolNames.map(name => [name, metadata.devDependencies[name]])),
  scripts: { check: 'tsc --noEmit && vite build' },
}, null, 2))
const html = entry => `<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head><body><div id="root"></div><script type="module" src="/${entry}.tsx"></script></body></html>`
const files = {
  'index.html': html('consumer'),
  'business.html': html('business'),
  'tsconfig.json': JSON.stringify({ compilerOptions: {
    target: 'ES2022', lib: ['ES2022', 'DOM'], module: 'ESNext', moduleResolution: 'Bundler', jsx: 'react-jsx',
    strict: true, skipLibCheck: true, types: ['vite/client', 'node'],
  }, include: ['*.tsx', '*.ts'] }),
  'vite.config.ts': `import { defineConfig } from 'vite'; import react from '@vitejs/plugin-react'; import { resolve } from 'node:path'; export default defineConfig({ plugins: [react()], build: { rolldownOptions: { input: { consumer: resolve('index.html'), business: resolve('business.html') } } } });`,
  'consumer.tsx': `import { createRoot } from 'react-dom/client'; import { ActionCard, Button } from '@dev-flow/ui-web'; import type { ActionCardProps } from '@dev-flow/ui-web'; import '@dev-flow/ui-web/styles.css';
// @ts-expect-error 分发声明必须保留回调类型，不能退化为 any。
const invalid: ActionCardProps['onAction'] = 'callback';
createRoot(document.getElementById('root')!).render(<><ActionCard title="接入检查" description="独立工程" actionLabel="继续" onAction={() => {}} /><Button variant="outline">返回</Button></>);`,
  'business.tsx': `import { createRoot } from 'react-dom/client'; import { ConfigProvider } from 'antd'; import { SelectionSummary } from '@dev-flow/ui-antd'; import type { SelectionSummaryProps } from '@dev-flow/ui-antd';
// @ts-expect-error 分发声明必须保留数量类型，不能退化为 any。
const invalid: SelectionSummaryProps['selectedCount'] = 'two';
createRoot(document.getElementById('root')!).render(<ConfigProvider><SelectionSummary selectedCount={2} scopeLabel="当前页" onClear={() => {}} onConfirm={() => {}} /></ConfigProvider>);`,
}
for (const [name, content] of Object.entries(files)) writeFileSync(join(target, name), content)
run(['install', '--no-audit', '--no-fund'], target)
run(['run', 'check'], target)
console.log(JSON.stringify({ result: 'passed', directory: target, packages: Object.keys(packed), entries: ['consumer', 'business'] }))
