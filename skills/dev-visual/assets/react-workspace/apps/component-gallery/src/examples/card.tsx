import { useState } from 'react'
import '@dev-flow/ui-web/styles.css'
import { Button, Card, CardContent, CardFooter, CardHeader, CardTitle } from '@dev-flow/ui-web'

export function CardExample({ scenario = 'simple' }: { scenario?: string }) {
  const [expanded, setExpanded] = useState(false)
  return (
    <Card>
      <CardHeader><CardTitle><h2>一个主题的信息</h2></CardTitle></CardHeader>
      <CardContent><p>将相关内容放在一起，让用户快速理解。</p>
        {expanded && <p role="status">这里展示详细信息（模拟）。</p>}
      </CardContent>
      {scenario === 'with-action' && <CardFooter>
        <Button variant="outline" aria-expanded={expanded} onClick={() => setExpanded((value) => !value)}>
          {expanded ? '收起详情' : '查看详情'}
        </Button>
      </CardFooter>}
    </Card>
  )
}
