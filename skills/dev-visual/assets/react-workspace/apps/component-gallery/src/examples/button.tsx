import { useState } from 'react'
import '@dev-flow/ui-web/styles.css'
import { Button } from '@dev-flow/ui-web'

export function ButtonExample({ scenario = 'default' }: { scenario?: string }) {
  const [count, setCount] = useState(0)
  const variant = scenario === 'outline' || scenario === 'secondary' ? scenario : 'default'
  return (
    <div style={{ display: 'grid', gap: 16, justifyItems: 'start' }}>
      <Button variant={variant} disabled={scenario === 'disabled'} onClick={() => setCount((value) => value + 1)}>示例行动</Button>
      <p role="status">已触发 {count} 次（模拟）</p>
    </div>
  )
}
