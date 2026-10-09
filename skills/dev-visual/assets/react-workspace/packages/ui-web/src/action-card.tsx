import { Button } from './components/ui/button'
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from './components/ui/card'

export interface ActionCardProps {
  title: string
  description: string
  actionLabel: string
  onAction: () => void
  disabled?: boolean
  pending?: boolean
}

/** 单一行动卡片；业务状态与异步结果由调用方负责。 */
export function ActionCard({ title, description, actionLabel, onAction, disabled = false, pending = false }: ActionCardProps) {
  return (
    <Card aria-busy={pending}>
      <CardHeader><CardTitle><h2>{title}</h2></CardTitle></CardHeader>
      <CardContent><p>{description}</p></CardContent>
      <CardFooter>
        <Button type="button" disabled={disabled || pending} onClick={onAction}>
          {pending ? '处理中…' : actionLabel}
        </Button>
      </CardFooter>
    </Card>
  )
}
