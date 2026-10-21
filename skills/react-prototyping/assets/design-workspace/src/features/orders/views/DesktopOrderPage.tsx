import { useState } from 'react'
import { Button, Input, Select, Table } from 'antd'
import type { Order, OrderStatus as Status, ScenarioId } from '../scenarios'
import { exampleOrders, filterOrders, money, statusLabels } from '../scenarios'
import { OrderSummary } from '../components/OrderSummary'
import { OrderStatus } from '../components/OrderStatus'
import { OrderDetail } from '../components/OrderDetail'
import { OrderContentState } from '../components/OrderContentState'

export function DesktopOrderPage({ scenario }: { scenario: ScenarioId }) {
  const [query, setQuery] = useState('')
  const [status, setStatus] = useState<Status | 'all'>('all')
  const [recovered, setRecovered] = useState(false)
  const [selected, setSelected] = useState<Order | null>(null)
  const current = recovered ? 'normal' : scenario
  const orders = current === 'empty' ? [] : exampleOrders
  const visible = filterOrders(orders, query, status)

  return <div className="desktop-orders">
    <aside className="business-nav">
      <div className="business-brand"><span className="brand-mark">禾</span><strong>禾一工作室</strong></div>
      <span className="nav-caption">工作空间</span>
      <div className="nav-current">订单管理 <span>08</span></div>
      <div className="nav-bottom"><span className="avatar">林</span><div>林小禾<small>工作空间管理员</small></div></div>
    </aside>
    <main className="desktop-main">
      <header className="business-topbar"><span>工作空间 / 订单管理</span><span>秋日计划 · 2026</span></header>
      <div className="desktop-content">
        <div className="page-heading"><div><p className="eyebrow">ORDERS</p><h1>订单管理</h1><p>从这里查看订单进度，安排接下来的工作。</p></div><span className="quiet-label">示例内容</span></div>
        <OrderSummary orders={orders} />
        <section className="order-panel" aria-label="订单列表">
          <div className="order-filters">
            <div><h2>全部订单</h2><span className="secondary">{visible.length} 笔订单</span></div>
            <div className="filter-controls">
              <Input allowClear aria-label="搜索订单" placeholder="搜索客户、商品或订单编号" value={query} onChange={(event) => setQuery(event.target.value)} />
              <Select aria-label="订单状态" value={status} onChange={setStatus} options={[
                { value: 'all', label: '全部状态' }, ...Object.entries(statusLabels).map(([value, label]) => ({ value, label })),
              ]} />
            </div>
          </div>
          {(current === 'normal' && visible.length > 0) ? <Table<Order> rowKey="id" dataSource={visible} pagination={false} columns={[
            { title: '订单 / 商品', dataIndex: 'id', render: (_value, order) => <div className="table-order"><strong>{order.id}</strong><span>{order.item}</span></div> },
            { title: '客户', dataIndex: 'customer' },
            { title: '金额', dataIndex: 'amount', render: money },
            { title: '状态', dataIndex: 'status', render: (value: Status) => <OrderStatus status={value} /> },
            { title: '创建时间', dataIndex: 'date' },
            { title: '操作', key: 'action', render: (_value, order) => <Button type="link" onClick={() => setSelected(order)} aria-label={`查看订单 ${order.id}`}>查看</Button> },
          ]} /> : <OrderContentState scenario={current === 'normal' ? 'empty' : current} onRetry={() => setRecovered(true)} />}
        </section>
      </div>
    </main>
    <OrderDetail order={selected} onClose={() => setSelected(null)} />
  </div>
}
