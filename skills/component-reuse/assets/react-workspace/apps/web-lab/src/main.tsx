import { StrictMode, useEffect, useRef, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { ActionCard, Button } from '@dev-flow/ui-web'
import '@dev-flow/ui-web/styles.css'
import './styles.css'

function Example() {
  const [pending, setPending] = useState(false)
  const [saved, setSaved] = useState(false)
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null)
  useEffect(() => () => { if (timer.current) clearTimeout(timer.current) }, [])

  function save() {
    setPending(true)
    timer.current = setTimeout(() => { setPending(false); setSaved(true) }, 700)
  }

  return (
    <main className="web-example">
      <header className="web-header"><p>组件隔离示例</p><h1>一个清楚的行动</h1><p>基于 shadcn/ui 的卡片与按钮，保存结果仅为本页模拟。</p></header>
      <ActionCard title="保存这次选择" description="将当前选择留在本次演示中；刷新页面后会清空。"
        actionLabel="保存选择" onAction={save} pending={pending} disabled={saved} />
      <p role="status" className="web-result">{saved ? '选择已保存（模拟）' : pending ? '正在保存（模拟）' : '尚未保存'}</p>
      <Button variant="outline" disabled={!saved || pending} onClick={() => setSaved(false)}>重新选择</Button>
    </main>
  )
}

createRoot(document.getElementById('root')!).render(<StrictMode><Example /></StrictMode>)
