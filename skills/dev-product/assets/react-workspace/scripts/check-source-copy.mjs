import assert from 'node:assert/strict'
import { execFileSync } from 'node:child_process'
import { existsSync, mkdtempSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { copyComponent, findComponent, manifest, sourceBundle, workspace } from './source-kit.mjs'

const directory = mkdtempSync(join(tmpdir(), 'dev-flow-source-check-'))
const componentsDir = join(directory, 'src/components/dev-flow')
const metadata = JSON.parse(readFileSync(join(workspace, 'package.json'), 'utf8'))
const antd = JSON.parse(readFileSync(join(workspace, 'apps/antd-lab/package.json'), 'utf8'))
const web = JSON.parse(readFileSync(join(workspace, 'packages/ui-web/package.json'), 'utf8'))
const receipts = manifest.components.map((component) => copyComponent(component.id, componentsDir))
assert.equal(copyComponent('web-action-card', componentsDir).created.length, 0, '重复复制应复用相同源码')

const summaryPath = join(componentsDir, 'business/selection-summary.tsx')
const originalSummary = readFileSync(summaryPath, 'utf8')
const localSummary = originalSummary.replace("confirmLabel = '确认所选项'", "confirmLabel = '确认副本所选项'")
assert.notEqual(localSummary, originalSummary)
writeFileSync(summaryPath, localSummary)
assert.throws(() => copyComponent('antd-selection-summary', componentsDir), /保留项目已有文件/)
assert.equal(readFileSync(summaryPath, 'utf8'), localSummary, '复制不能覆盖项目修改')
assert.equal(sourceBundle(findComponent('antd-selection-summary')).files[0].content, originalSummary, '项目修改不改变仓库来源')

const conflictDir = join(directory, 'conflict')
mkdirSync(join(conflictDir, 'web/lib'), { recursive: true })
writeFileSync(join(conflictDir, 'web/lib/utils.ts'), '// project-owned')
assert.throws(() => copyComponent('web-action-card', conflictDir), /未复制任何源码/)
assert.equal(existsSync(join(conflictDir, 'web/action-card.tsx')), false, '后续文件冲突时不可先复制部分源码')

// 从复制后的本地相对路径导入；没有工作区别名、文件包或 dev-flow 运行时依赖。
const toolNames = ['vite', '@vitejs/plugin-react', 'typescript', '@types/react', '@types/react-dom', '@types/node', 'tailwindcss', '@tailwindcss/vite']
const dependencies = { react: antd.dependencies.react, 'react-dom': antd.dependencies['react-dom'], antd: antd.dependencies.antd, ...web.dependencies }
assert.equal(Object.keys(dependencies).some((name) => name.startsWith('@dev-flow/')), false)
writeFileSync(join(directory, 'package.json'), JSON.stringify({ name: 'dev-flow-source-consumer-check', private: true, type: 'module',
  dependencies, devDependencies: Object.fromEntries(toolNames.map((name) => [name, metadata.devDependencies[name]])),
  scripts: { check: 'tsc --noEmit && vite build', dev: 'vite --host 127.0.0.1' },
}, null, 2))
const html = (entry, title) => `<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title></head><body><div id="root"></div><script type="module" src="/src/${entry}.tsx"></script></body></html>`
writeFileSync(join(directory, 'index.html'), html('business', 'B 端源码副本'))
writeFileSync(join(directory, 'web.html'), html('consumer', 'C 端源码副本'))
writeFileSync(join(directory, 'tsconfig.json'), JSON.stringify({ compilerOptions: {
  target: 'ES2022', lib: ['ES2022', 'DOM'], module: 'ESNext', moduleResolution: 'Bundler', jsx: 'react-jsx',
  strict: true, skipLibCheck: true, types: ['vite/client', 'node'],
}, include: ['src', 'vite.config.ts'] }, null, 2))
writeFileSync(join(directory, 'vite.config.ts'), `import { defineConfig } from 'vite'; import react from '@vitejs/plugin-react'; import tailwindcss from '@tailwindcss/vite'; import { resolve } from 'node:path';
export default defineConfig({ plugins: [react(), tailwindcss()], build: { rolldownOptions: { input: { business: resolve('index.html'), consumer: resolve('web.html') } } } });`)
for (const [id, file] of [['antd-selection-summary', 'ExampleBusiness'], ['web-action-card', 'ExampleConsumer'], ['web-button', 'ExampleButton'], ['web-card', 'ExampleCard']]) {
  writeFileSync(join(directory, `src/${file}.tsx`), sourceBundle(findComponent(id)).code)
}
writeFileSync(join(directory, 'src/business.tsx'), `import { createRoot } from 'react-dom/client'; import { ConfigProvider } from 'antd'; import { SelectionSummaryExample } from './ExampleBusiness';
import type { SelectionSummaryProps } from './components/dev-flow/business/selection-summary';
// @ts-expect-error 源码副本须保留数量契约。
const invalid: SelectionSummaryProps['selectedCount'] = 'two';
createRoot(document.getElementById('root')!).render(<ConfigProvider><main style={{ maxWidth: 800, margin: '40px auto', padding: 24 }}><h1>B 端源码副本</h1><p>所选项栏在本项目直接修改了按钮文案。</p><SelectionSummaryExample scenario="selected" /></main></ConfigProvider>);`)
writeFileSync(join(directory, 'src/consumer.tsx'), `import { createRoot } from 'react-dom/client'; import { ActionCardExample } from './ExampleConsumer'; import { ButtonExample } from './ExampleButton'; import { CardExample } from './ExampleCard';
import type { ActionCardProps } from './components/dev-flow/web/action-card';
// @ts-expect-error 源码副本须保留回调契约。
const invalid: ActionCardProps['onAction'] = 'callback';
createRoot(document.getElementById('root')!).render(<main style={{ maxWidth: 540, margin: '40px auto', padding: 24, display: 'grid', gap: 24 }}><h1>C 端源码副本</h1><ActionCardExample /><ButtonExample scenario="outline" /><CardExample scenario="with-action" /></main>);`)
for (const file of ['ExampleBusiness', 'ExampleConsumer', 'ExampleButton', 'ExampleCard']) assert.equal(readFileSync(join(directory, `src/${file}.tsx`), 'utf8').includes('@dev-flow/'), false)
const run = (args) => execFileSync('npm', args, { cwd: directory, stdio: 'inherit' })
run(['install', '--ignore-scripts', '--no-audit', '--no-fund'])
run(['run', 'check'])
const result = { result: 'passed', directory, adoptionMode: 'copy-source', copiedComponents: receipts.map((receipt) => receipt.componentId),
  checks: ['独立源码导入与严格类型构建', '共享依赖文件重复复制', '保留项目修改', '冲突前完整核验', '副本迭代不改变来源'],
  runtimeDependencies: Object.keys(dependencies),
}
writeFileSync(join(directory, 'source-check.json'), JSON.stringify(result, null, 2) + '\n')
console.log(JSON.stringify(result))
