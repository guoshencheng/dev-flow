import { useState } from 'react'
import { Button, Input } from 'antd'
import type { Order, ScenarioId } from '../scenarios'
import { exampleOrders, filterOrders, money } from '../scenarios'
import { OrderStatus } from '../components/OrderStatus'
import { OrderDetail } from '../components/OrderDetail'
import { OrderContentState } from '../components/OrderContentState'

export function MobileOrderPage({ scenario }: { scenario: ScenarioId }) {
  const [query, setQuery] = useState('')
  const [pendingOnly, setPendingOnly] = useState(false)
  const [selected, setSelected] = useState<Order | null>(null)
  const [recovered, setRecovered] = useState(false)
  const current = recovered ? 'normal' : scenario
  const orders = current === 'empty' ? [] : exampleOrders
  const visible = filterOrders(orders, query, pendingOnly ? 'pending' : 'all')

  return <main className="mobile-orders">
    <header className="mobile-header"><div className="business-brand"><span className="brand-mark">禾</span><strong>禾一工作室</strong></div><span className="avatar">林</span></header>
    <div className="mobile-intro"><p className="eyebrow">YOUR WORK, AT A GLANCE</p><h1>订单管理</h1><p>今天，也把每一件小事安排妥当。</p></div>
    <div className="mobile-stats"><div><span>待处理订单</span><strong>{orders.filter((order) => order.status === 'pending').length}<small> 笔</small></strong></div><span className="stats-decoration" aria-hidden="true">↗</span></div>
    <section className="mobile-list" aria-label="移动端订单列表">
      <Input allowClear aria-label="搜索订单" placeholder="搜索客户、商品或订单编号" value={query} onChange={(event) => setQuery(event.target.value)} />
      <div className="mobile-list-heading"><h2>{pendingOnly ? '待处理订单' : '全部订单'}</h2><span>{visible.length} 笔</span></div>
      {current === 'normal' && visible.length > 0 ? visible.map((order) => <article className="mobile-order-card" key={order.id}>
        <div className="mobile-card-top"><strong>{order.customer}</strong><OrderStatus status={order.status} /></div>
        <p>{order.item}</p><span className="secondary">{order.id} · {order.date.slice(5, 16)}</span>
        <div className="mobile-card-bottom"><strong>{money(order.amount)}</strong><Button size="small" onClick={() => setSelected(order)} aria-label={`查看订单 ${order.id}`}>查看订单</Button></div>
      </article>) : <OrderContentState scenario={current === 'normal' ? 'empty' : current} onRetry={() => setRecovered(true)} />}
    </section>
    <nav className="mobile-bottom-nav" aria-label="订单分类">
      <button aria-pressed={!pendingOnly} onClick={() => setPendingOnly(false)}><span aria-hidden="true">▦</span>全部订单</button>
      <button aria-pressed={pendingOnly} onClick={() => setPendingOnly(true)}><span aria-hidden="true">◷</span>待处理</button>
    </nav>
    <OrderDetail order={selected} onClose={() => setSelected(null)} />
  </main>
}
