import { Descriptions, Drawer } from 'antd'
import type { Order } from '../scenarios'
import { money } from '../scenarios'
import { OrderStatus } from './OrderStatus'

export function OrderDetail({ order, onClose }: { order: Order | null; onClose: () => void }) {
  return <Drawer title="订单详情" open={Boolean(order)} onClose={onClose} size="medium">
    {order && <Descriptions column={1} items={[
      { key: 'id', label: '订单编号', children: order.id },
      { key: 'customer', label: '客户', children: order.customer },
      { key: 'item', label: '商品', children: order.item },
      { key: 'amount', label: '金额', children: money(order.amount) },
      { key: 'status', label: '状态', children: <OrderStatus status={order.status} /> },
      { key: 'date', label: '创建时间', children: order.date },
    ]} />}
  </Drawer>
}
