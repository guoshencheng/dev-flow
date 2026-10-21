import { Button, Empty, Result, Skeleton } from 'antd'
import type { ScenarioId } from '../scenarios'

export function OrderContentState({ scenario, onRetry }: { scenario: ScenarioId; onRetry: () => void }) {
  if (scenario === 'loading') return <div className="content-state" aria-label="订单加载中"><Skeleton active paragraph={{ rows: 5 }} /></div>
  if (scenario === 'error') return <Result status="warning" title="暂时无法加载订单" subTitle="请稍后重试，已输入的筛选条件会保留。"
    extra={<Button onClick={onRetry}>重新加载</Button>} />
  return <div className="content-state"><Empty description="暂无符合条件的订单" /></div>
}
