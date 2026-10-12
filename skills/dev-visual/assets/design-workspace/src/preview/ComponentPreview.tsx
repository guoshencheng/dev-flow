import { App, Button, Space } from 'antd'
import { MarkdownDocument } from '../components/MarkdownDocument'
import { OrderSummary } from '../features/orders/components/OrderSummary'
import { OrderStatus } from '../features/orders/components/OrderStatus'
import { exampleOrders } from '../features/orders/scenarios'
import contract from '../../docs/visual/components/order-summary.md?raw'

export function ComponentPreview() {
  const { message } = App.useApp()
  return <section className="showcase-content">
    <div className="section-heading"><p className="eyebrow">COMPONENTS</p><h1>组件与状态</h1><p>页面里的真实组件，在这里独立查看。</p></div>
    <section className="showcase-card"><h2>订单摘要</h2><p className="secondary">有内容 / 零内容，使用同一个 OrderSummary。</p>
      <OrderSummary orders={exampleOrders} /><OrderSummary orders={[]} /></section>
    <div className="showcase-columns">
      <section className="showcase-card"><h2>状态标签</h2><Space wrap><OrderStatus status="pending" /><OrderStatus status="active" /><OrderStatus status="done" /></Space></section>
      <section className="showcase-card"><h2>基础操作</h2><Space wrap>
        <Button type="primary" onClick={() => void message.success('操作反馈示例')}>主要操作</Button>
        <Button onClick={() => void message.info('次要操作反馈示例')}>次要操作</Button><Button disabled>不可操作</Button><Button loading>处理中</Button>
      </Space></section>
    </div>
    <section className="showcase-card"><MarkdownDocument source={contract} links={{ '../system.md': '#/overview/system' }} /></section>
  </section>
}
