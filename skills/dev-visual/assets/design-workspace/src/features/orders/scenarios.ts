export type ScenarioId = 'normal' | 'loading' | 'empty' | 'error'
export type OrderStatus = 'pending' | 'active' | 'done'
export interface Order {
  id: string
  customer: string
  item: string
  amount: number
  status: OrderStatus
  date: string
}

export const scenarios: { id: ScenarioId; label: string }[] = [
  { id: 'normal', label: '正常内容' },
  { id: 'loading', label: '加载中' },
  { id: 'empty', label: '空内容' },
  { id: 'error', label: '加载失败' },
]

export const statusLabels: Record<OrderStatus, string> = {
  pending: '待处理', active: '处理中', done: '已完成',
}

export const exampleOrders: Order[] = [
  { id: 'OD-1024', customer: '林木工作室', item: '桌面收纳套装', amount: 268, status: 'pending', date: '2026-10-11 09:42' },
  { id: 'OD-1023', customer: '南山设计', item: '便携笔记本 × 3', amount: 156, status: 'active', date: '2026-10-11 09:18' },
  { id: 'OD-1022', customer: '禾一空间', item: '陶瓷马克杯', amount: 128, status: 'done', date: '2026-10-11 08:56' },
  { id: 'OD-1021', customer: '云间办公室', item: '桌面收纳套装 × 2', amount: 536, status: 'pending', date: '2026-10-10 16:20' },
  { id: 'OD-1020', customer: '长风文化创意工作室', item: '帆布工具袋', amount: 198, status: 'active', date: '2026-10-10 15:40' },
  { id: 'OD-1019', customer: '小岛商店', item: '便携笔记本', amount: 52, status: 'done', date: '2026-10-10 14:32' },
  { id: 'OD-1018', customer: '山海空间', item: '陶瓷马克杯 × 4', amount: 512, status: 'pending', date: '2026-10-10 12:10' },
  { id: 'OD-1017', customer: '一隅工作室', item: '帆布工具袋 × 2', amount: 396, status: 'done', date: '2026-10-10 10:15' },
]

export function parseScenario(value: string | null): ScenarioId {
  return scenarios.find((item) => item.id === value)?.id ?? 'normal'
}

export function filterOrders(orders: Order[], query: string, status: OrderStatus | 'all') {
  const text = query.trim().toLowerCase()
  return orders.filter((order) =>
    (status === 'all' || order.status === status)
    && `${order.id} ${order.customer} ${order.item}`.toLowerCase().includes(text),
  )
}

export const money = (amount: number) => new Intl.NumberFormat('zh-CN', {
  style: 'currency', currency: 'CNY', maximumFractionDigits: 0,
}).format(amount)
