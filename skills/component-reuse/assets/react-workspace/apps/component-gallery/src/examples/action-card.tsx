import { useEffect, useRef, useState } from 'react'
import '@dev-flow/ui-web/styles.css'
import { ActionCard, Button } from '@dev-flow/ui-web'

export function ActionCardExample({ scenario = 'idle' }: { scenario?: string }) {
  const [saved, setSaved] = useState(scenario === 'complete')
  const [saving, setSaving] = useState(false)
  const timer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined)
  useEffect(() => () => clearTimeout(timer.current), [])
  const pending = scenario === 'pending' || saving
  function save() {
    setSaving(true)
    timer.current = setTimeout(() => { setSaving(false); setSaved(true) }, 700)
  }
  return (
    <div style={{ display: 'grid', gap: 16 }}>
      <ActionCard title="保存你的选择" description="保存后可以重新查看。本示例使用内存模拟。"
        actionLabel={saved ? '已保存' : '保存选择'} onAction={save} pending={pending} disabled={saved} />
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap' }}>
        <span role="status">{pending ? '处理中（模拟）' : saved ? '已保存（模拟）' : '尚未保存'}</span>
        <Button variant="outline" disabled={!saved || pending} onClick={() => setSaved(false)}>重置示例</Button>
      </div>
    </div>
  )
}
