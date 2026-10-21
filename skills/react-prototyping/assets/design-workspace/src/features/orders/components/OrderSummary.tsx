import type { Order } from '../scenarios'
import { money } from '../scenarios'

export function OrderSummary({ orders }: { orders: Order[] }) {
  const pending = orders.filter((order) => order.status === 'pending').length
  const total = orders.reduce((sum, order) => sum + order.amount, 0)
  return <section className="order-summary" aria-label="订单摘要">
    <div><span>全部订单</span><strong>{orders.length}<small> 笔</small></strong></div>
    <div><span>待处理</span><strong>{pending}<small> 笔</small></strong></div>
    <div><span>订单金额</span><strong>{money(total)}</strong></div>
  </section>
}
