import { Tag } from 'antd'
import { statusLabels } from '../scenarios'
import type { OrderStatus as Status } from '../scenarios'

export function OrderStatus({ status }: { status: Status }) {
  const colors = { pending: 'gold', active: 'processing', done: 'success' } as const
  return <Tag color={colors[status]}>{statusLabels[status]}</Tag>
}
