import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import '@dev-flow/ui-web/styles.css'
import { Button, Card, CardContent, CardHeader, CardTitle } from '@dev-flow/ui-web'
import { Gallery } from './gallery'
import type { Controls } from './gallery'
import { ActionCardExample } from './examples/action-card'
import { ButtonExample } from './examples/button'
import { CardExample } from './examples/card'

const controls: Controls = {
  Button: ({ children, onClick, disabled, primary }) => <Button variant={primary ? 'default' : 'outline'} disabled={disabled} onClick={onClick}>{children}</Button>,
  Input: ({ value, onChange, label }) => <input className="native-control" aria-label={label} placeholder="搜索名称、任务或关键词" value={value} onChange={(event) => onChange(event.target.value)} />,
  Select: ({ value, onChange, options, label }) => <select className="native-control" aria-label={label} value={value} onChange={(event) => onChange(event.target.value)}>
    {options.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
  </select>,
  Panel: ({ title, children }) => <Card><CardHeader><CardTitle><h3>{title}</h3></CardTitle></CardHeader><CardContent>{children}</CardContent></Card>,
}

createRoot(document.getElementById('root')!).render(
  <StrictMode><Gallery platform="consumer-web" controls={controls} preview={(component, scenario) => {
    if (component.id === 'web-action-card') return <ActionCardExample scenario={scenario} />
    if (component.id === 'web-button') return <ButtonExample scenario={scenario} />
    return <CardExample scenario={scenario} />
  }} /></StrictMode>,
)
