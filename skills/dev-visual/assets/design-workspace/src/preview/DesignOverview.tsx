import { useState } from 'react'
import { Button, InputNumber, Segmented, Select, Tag } from 'antd'
import { scenarios } from '../features/orders/scenarios'
import type { ScenarioId } from '../features/orders/scenarios'
import { DeviceViewport } from './DeviceViewport'
import { pageHref, pageRegistry, sectionRegistry } from './registry'
import type { SectionId } from './registry'

const sizes = [
  { value: '375x812', label: '375 × 812' }, { value: '390x844', label: '390 × 844' }, { value: '430x932', label: '430 × 932' },
]

export function DesignOverview({ section }: { section: SectionId }) {
  const [scenario, setScenario] = useState<ScenarioId>('normal')
  const [layout, setLayout] = useState('compare')
  const [width, setWidth] = useState(390)
  const [height, setHeight] = useState(844)
  const current = sectionRegistry.find((entry) => entry.id === section)!
  const showcase = 'component' in current ? current.component : null
  const visible = pageRegistry.filter((entry) => layout === 'compare' || entry.kind === layout)
  return <div className="design-workbench">
    <aside className="workbench-sidebar">
      <a className="workbench-brand" href="#/overview/pages"><span className="brand-mark">D</span><div><strong>设计工作台</strong><small>DEV FLOW / STARTER</small></div></a>
      <div className="workspace-label"><span className="live-dot" /> 禾一 · 示例工作空间</div>
      <nav aria-label="设计工作台导航">{sectionRegistry.map((entry) => <a href={`#/overview/${entry.id}`} key={entry.id} aria-current={section === entry.id ? 'page' : undefined}>
        <span className="nav-number">{entry.mark}</span><div>{entry.title}<small>{entry.subtitle}</small></div>
      </a>)}</nav>
      <div className="sidebar-note"><strong>分开维护，一起查看。</strong><p>页面、组件与规范保持独立，总览只组合它们。</p><span>模板 v0.1 · 设计候选</span></div>
    </aside>
    <main className="workbench-main">
      <header className="workbench-topbar"><span>设计资产 / {current.title}</span><Tag color="green">可复用 React 模板</Tag></header>
      {showcase ? (() => { const Showcase = showcase; return <Showcase /> })() : <>
        <div className="overview-heading"><div><p className="eyebrow">DESIGN, IN ONE PLACE</p><h1>把每一端，放在一起看。</h1><p>独立页面，共享组件。这里是同一份设计的不同视角。</p></div><span className="quiet-label">{pageRegistry.length} 个页面 / {scenarios.length} 种状态</span></div>
        <div className="overview-controls">
          <Segmented aria-label="展示方式" value={layout} onChange={setLayout} options={[
            { value: 'compare', label: '多端对照' }, { value: 'desktop', label: '桌面端' }, { value: 'mobile', label: '移动端' },
          ]} />
          <div className="scenario-control"><label htmlFor="scenario">展示状态</label><Select id="scenario" aria-label="展示状态" value={scenario} onChange={setScenario} options={scenarios.map((item) => ({ value: item.id, label: item.label }))} /></div>
        </div>
        <div className={`page-previews ${layout === 'compare' ? 'compare' : 'single'}`}>
          {visible.map((entry) => <section className="preview-panel" key={entry.id}>
            <header className="preview-panel-heading"><div><span className="eyebrow">{entry.kind.toUpperCase()}</span><h2>{entry.title} <span>{entry.platform}</span></h2></div>
              <Button href={pageHref(entry.id, scenario)} target="_blank" rel="noopener noreferrer" size="small">独立打开 ↗</Button></header>
            {entry.kind === 'mobile' && <div className="device-controls">
              <Select aria-label="屏幕尺寸预设" placeholder="尺寸预设" value={sizes.find((item) => item.value === `${width}x${height}`)?.value}
                onChange={(value) => { const [nextWidth, nextHeight] = value.split('x').map(Number); setWidth(nextWidth); setHeight(nextHeight) }} options={sizes} />
              <InputNumber aria-label="屏幕宽度" min={240} max={1920} value={width} onChange={(value) => value !== null && setWidth(Math.round(value))} />
              <span>×</span><InputNumber aria-label="屏幕高度" min={320} max={1600} value={height} onChange={(value) => value !== null && setHeight(Math.round(value))} />
            </div>}
            <DeviceViewport title={`${entry.title} · ${entry.platform}`} src={pageHref(entry.id, scenario)}
              width={entry.kind === 'mobile' ? width : entry.width} height={entry.kind === 'mobile' ? height : entry.height}
              kind={entry.kind} />
            <footer className="preview-caption">{entry.kind === 'mobile' ? '仅模拟屏幕尺寸，内容在屏幕内部滚动。' : '独立视图与总览使用同一页面组件。'}</footer>
          </section>)}
        </div>
        <footer className="overview-footnote"><span>示例数据 · 不连接真实业务接口</span><a href="#/overview/system">查看独立设计规范 ↗</a></footer>
      </>}
    </main>
  </div>
}
