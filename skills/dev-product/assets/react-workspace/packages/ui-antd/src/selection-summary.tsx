import { Button, Flex, Typography } from 'antd'

export interface SelectionSummaryProps {
  selectedCount: number
  scopeLabel: string
  onClear: () => void
  onConfirm: () => void
  confirmLabel?: string
  busy?: boolean
}

/** 展示已选范围，选择与提交状态由调用方控制。 */
export function SelectionSummary({
  selectedCount,
  scopeLabel,
  onClear,
  onConfirm,
  confirmLabel = '确认所选项',
  busy = false,
}: SelectionSummaryProps) {
  return (
    <Flex gap="middle" wrap align="center" justify="space-between">
      <Typography.Text aria-live="polite">
        已选择 {selectedCount} 项 · {scopeLabel}
      </Typography.Text>
      <Flex gap="small" wrap>
        <Button disabled={selectedCount === 0 || busy} onClick={onClear}>清空选择</Button>
        <Button type="primary" disabled={selectedCount === 0 || busy} loading={busy} onClick={onConfirm}>
          {confirmLabel}
        </Button>
      </Flex>
    </Flex>
  )
}
