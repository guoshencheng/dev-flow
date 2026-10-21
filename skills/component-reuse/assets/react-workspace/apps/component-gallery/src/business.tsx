import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { App, Button, Card, ConfigProvider, Input, Select } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import { Gallery } from './gallery'
import type { Controls } from './gallery'
import { SelectionSummaryExample } from './examples/selection-summary'

// 仅目录应用的控件适配；基础组件仍直接来自 antd。
const controls: Controls = {
  Button: ({ children, onClick, disabled, primary }) => <Button type={primary ? 'primary' : 'default'} disabled={disabled} onClick={onClick}>{children}</Button>,
  Input: ({ value, onChange, label }) => <Input aria-label={label} placeholder="搜索名称、任务或关键词" value={value} onChange={(event) => onChange(event.target.value)} allowClear />,
  Select: ({ value, onChange, options, label }) => <Select aria-label={label} value={value} onChange={onChange} options={options} style={{ minWidth: 150 }} />,
  Panel: ({ title, children }) => <Card title={title}>{children}</Card>,
}

createRoot(document.getElementById('root')!).render(
  <StrictMode><ConfigProvider locale={zhCN}><App><Gallery platform="business" controls={controls}
    preview={(_, scenario) => <SelectionSummaryExample scenario={scenario} />} /></App></ConfigProvider></StrictMode>,
)
