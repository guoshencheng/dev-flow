import { useEffect, useState } from 'react'
import type { ComponentType, ReactNode } from 'react'
import { components, loadSelections, saveSelections, selectionRecord } from './catalog'
import type { CatalogComponent, Platform } from './catalog'
import './gallery.css'

export interface Controls {
  Button: ComponentType<{ children: ReactNode; onClick: () => void; disabled?: boolean; primary?: boolean }>
  Input: ComponentType<{ value: string; onChange: (value: string) => void; label: string }>
  Select: ComponentType<{ value: string; onChange: (value: string) => void; options: { value: string; label: string }[]; label: string }>
  Panel: ComponentType<{ title: string; children: ReactNode }>
}

export function Gallery({ platform, controls, preview }: {
  platform: Platform; controls: Controls; preview: (component: CatalogComponent, scenario: string) => ReactNode
}) {
  const available = components.filter((component) => component.platform === platform)
  const query = new URLSearchParams(location.search)
  const initial = available.find((component) => component.id === query.get('component')) || available[0]
  const [currentId, setCurrentId] = useState(initial.id)
  const [scenario, setScenario] = useState(initial.scenarios.find((item) => item.id === query.get('state'))?.id || initial.scenarios[0].id)
  const [search, setSearch] = useState('')
  const [selections, setSelections] = useState(loadSelections)
  const [notice, setNotice] = useState('')
  const [showCode, setShowCode] = useState(false)
  const [codeFile, setCodeFile] = useState('usage')
  const current = available.find((component) => component.id === currentId)!
  const matching = available.filter((component) => [component.name, component.title, ...component.keywords].join(' ').toLowerCase().includes(search.trim().toLowerCase()))
  const selected = selections.find((item) => item.id === current.id)
  const record = selectionRecord(selections)
  const currentCode = codeFile === 'usage' ? current.code : current.sourceFiles.find((file) => file.target === codeFile)?.content || ''
  const sourceRecord = JSON.stringify({ adoptionMode: 'copy-source', destinationBase: 'src/components/dev-flow',
    componentId: current.id, files: current.sourceFiles.map(({ target, content }) => ({ path: target, content })),
    usage: { path: 'src/Example.tsx', content: current.code },
    verifiedDependencies: current.verifiedDependencies, styleDependencies: current.styleDependencies || {}, setup: current.setup,
  }, null, 2)
  const { Button, Input, Select, Panel } = controls

  useEffect(() => {
    const params = new URLSearchParams({ component: currentId, state: scenario })
    history.replaceState(null, '', `${location.pathname}?${params}`)
  }, [currentId, scenario])

  function choose(component: CatalogComponent) {
    setCurrentId(component.id); setScenario(component.scenarios[0].id); setShowCode(false); setCodeFile('usage'); setNotice('')
  }
  function updateSelections(next: typeof selections, message: string) {
    setSelections(next)
    setNotice(saveSelections(next) ? message : `${message} 当前浏览器无法保存，切换入口前请复制记录。`)
  }
  async function copy(text: string, success: string) {
    try { await navigator.clipboard.writeText(text); setNotice(success) }
    catch { setNotice('无法自动复制，请从下方代码或选择记录中选取文本。') }
  }
  function download() {
    const blob = new Blob([record + '\n'], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url; link.download = 'component-candidates.json'; link.click()
    setTimeout(() => URL.revokeObjectURL(url), 1000)
    setNotice('已生成选择记录下载。接入时由 Agent 登记来源哈希与项目用途。')
  }

  return (
    <div className={`gallery ${platform}`}>
      <a className="skip-link" href="#component-detail">跳到组件详情</a>
      <header className="gallery-header">
        <div><p className="eyebrow">DEV FLOW / REACT</p><h1>组件目录</h1><p className="lead">选用已有组件，让设计讨论直接连到可运行的实现。</p></div>
        <nav aria-label="设计体系" className="platform-nav">
          <a href="/index.html" aria-current={platform === 'business' ? 'page' : undefined}>B 端 · Ant Design</a>
          <a href="/web.html" aria-current={platform === 'consumer-web' ? 'page' : undefined}>C 端 Web · shadcn/ui</a>
        </nav>
      </header>
      <div className="gallery-layout">
        <aside className="component-nav" aria-label="组件列表">
          <Input label="搜索当前体系组件" value={search} onChange={setSearch} />
          <p className="muted search-count">{matching.length} 个组件 · {platform === 'business' ? 'Ant Design' : 'shadcn/ui'}</p>
          <div className="component-list">
            {matching.map((component) => <Button key={component.id} primary={current.id === component.id} onClick={() => choose(component)}>
              <span className="component-label"><strong>{component.title}</strong><small>{component.name}</small></span>
            </Button>)}
          </div>
          {matching.length === 0 && <p role="status">没有匹配组件。可以清空搜索，或直接采用基础库已有组件。</p>}
          <p className="sidebar-note">{platform === 'business' ? '基础控件优先直接使用 antd。共享库补充有价值的组合。' : '源码组件来自 shadcn/ui。按项目主题和任务调整组合。'}</p>
        </aside>
        <main id="component-detail" tabIndex={-1} className="component-detail">
          <div className="detail-heading"><div><p className="eyebrow">{current.kind}</p><h2>{current.title}</h2><p className="lead">{current.summary}</p></div>
            <span className="version">源码复用</span>
          </div>
          <Panel title="可操作预览">
            <div className="preview-toolbar"><Select label="预览状态" value={scenario} onChange={setScenario}
              options={current.scenarios.map((item) => ({ value: item.id, label: item.label }))} />
              <span className="muted">模拟数据与动作</span>
            </div>
            <div className="preview-stage" key={`${current.id}:${scenario}`}>{preview(current, scenario)}</div>
          </Panel>
          <div className="contract-grid"><section><h3>适用场景</h3><p>{current.useWhen}</p></section><section><h3>由项目负责</h3><p>{current.boundary}</p></section></div>
          <Panel title="接入项目">
            <p>复制源码到项目 · 由项目直接维护</p>
            <p className="muted">查看使用示例或所需源码文件。使用示例以 src/Example.tsx 为基准，替换模拟状态和回调。</p>
            <div className="source-picker"><Select label="代码文件" value={codeFile} onChange={setCodeFile}
              options={[{ value: 'usage', label: '使用示例（本地导入）' }, ...current.sourceFiles.map((file) => ({ value: file.target, label: file.target }))]} /></div>
            <div className="actions"><Button onClick={() => setShowCode(!showCode)}>{showCode ? '收起代码' : '查看代码'}</Button>
              <Button onClick={() => { setShowCode(true); void copy(currentCode, '已复制当前代码；在项目中维护并按实际路径导入。') }}>复制当前代码</Button>
              <Button onClick={() => { void copy(sourceRecord, '已复制源码文件集 JSON，可交给 Agent 写入项目并适配。') }}>复制源码文件集</Button>
              <Button primary onClick={() => updateSelections([...selections.filter((item) => item.id !== current.id), { id: current.id, scenario }], '已加入候选，可在右侧复制或下载选择记录。')}>
                {selected ? '更新候选状态' : '加入候选'}
              </Button>
            </div>
            {showCode && <pre className="code-block" tabIndex={0} aria-label={`${current.name} 接入代码`}><code>{currentCode}</code></pre>}
            <details className="installation"><summary>源码复制与来源</summary>
              <p>在随包 React 工作区运行以下命令；替换目标路径。源码连同依赖文件、样式起点和许可一并复制，记录来源哈希。已有不同内容的文件留给 Agent 比较合并。</p>
              <pre className="code-block"><code>{`npm run --silent copy:component -- ${current.id} --to /目标项目/src/components/dev-flow`}</code></pre>
              <p>{current.setup}</p>
              <p>目录验证过的基础依赖：<code>{Object.keys({ ...current.verifiedDependencies, ...current.styleDependencies }).join('、')}</code>。接入前核对项目现有版本。</p>
              <p>源码：<code>{current.source}</code></p><p>示例：<code>{current.example}</code></p>
              <p>验证状态：{current.maturity}。</p>
            </details>
          </Panel>
        </main>
        <aside className="selection-panel" aria-label="候选记录">
          <Panel title={`候选组件 · ${selections.length}`}>
            <p className="muted">供讨论与接入使用。记录包含源码文件和预览状态，接入时补齐项目用途与来源哈希。</p>
            {selections.length === 0 && <p>还没有候选。查看组件后点击“加入候选”。</p>}
            <ul className="selection-list">{selections.map((item) => {
              const component = components.find((entry) => entry.id === item.id)!
              return <li key={item.id}><div><strong>{component.name}</strong><small>{component.scenarios.find((entry) => entry.id === item.scenario)!.label}</small></div>
                <Button onClick={() => updateSelections(selections.filter((entry) => entry.id !== item.id), `已移除 ${component.name}。`)}>移除 {component.name}</Button>
              </li>
            })}</ul>
            <div className="actions"><Button primary disabled={selections.length === 0} onClick={() => { void copy(record, '已复制选择记录，可发送给 Agent。') }}>复制选择记录</Button>
              <Button disabled={selections.length === 0} onClick={download}>下载 JSON</Button>
              <Button disabled={selections.length === 0} onClick={() => updateSelections([], '已清空候选。')}>清空候选</Button>
            </div>
            <details className="record-details"><summary>查看选择记录</summary>
              <textarea aria-label="选择记录 JSON" readOnly value={record} rows={12} />
            </details>
            <p className="persistence-note">候选仅保存在当前浏览器会话，可跨这两个入口使用；留存到项目请复制或下载。</p>
          </Panel>
        </aside>
      </div>
      <p role="status" className="notice">{notice || '所有预览均为隔离示例。选择组件后，在任务页面中接入并验证。'}</p>
      <footer className="gallery-footer">源码、契约、来源与验证记录随 dev-product Skill 在同一 Git 仓库维护。</footer>
    </div>
  )
}
