import { MarkdownDocument } from '../components/MarkdownDocument'
import { tokens } from '../theme/tokens'
import specification from '../../docs/visual/system.md?raw'

export function DesignSystemPreview() {
  return <section className="showcase-content">
    <div className="section-heading"><p className="eyebrow">DESIGN SYSTEM</p><h1>设计规范</h1><p>规范单独维护，展示与页面共用实际主题。</p></div>
    <section className="showcase-card"><h2>语义颜色</h2><div className="swatch-grid">
      {Object.entries(tokens.color).map(([name, value]) => <div className="swatch" key={name}><div style={{ background: value }} /><strong>{name}</strong><code>{value}</code></div>)}
    </div></section>
    <div className="showcase-columns">
      <section className="showcase-card"><h2>文字层级</h2><div className="type-samples">
        {Object.entries(tokens.type).map(([name, value]) => <div key={name} style={{ fontSize: value }}>禾一，让工作有序 <span>{name} · {value}px</span></div>)}
      </div></section>
      <section className="showcase-card"><h2>间距节奏</h2><div className="spacing-samples">
        {tokens.space.map((value) => <div key={value}><code>{value}px</code><span style={{ width: value * 3 }} /></div>)}
      </div></section>
    </div>
    <section className="showcase-card"><MarkdownDocument source={specification} /></section>
  </section>
}
