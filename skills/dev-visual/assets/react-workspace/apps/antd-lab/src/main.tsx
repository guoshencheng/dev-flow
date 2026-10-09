import { StrictMode, useState } from 'react'
import type { Key } from 'react'
import { createRoot } from 'react-dom/client'
import { App, Card, ConfigProvider, Space, Table, Typography } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import { SelectionSummary } from '@dev-flow/ui-antd'
import './styles.css'

const rows = [
  { key: 'one', name: '示例对象一', status: '待确认' },
  { key: 'two', name: '示例对象二', status: '待确认' },
  { key: 'three', name: '示例对象三', status: '待确认' },
]

function Example() {
  const [selectedKeys, setSelectedKeys] = useState<Key[]>([])
  const [result, setResult] = useState('尚未确认')
  return (
    <main className="antd-example">
      <Space orientation="vertical" size="large" style={{ width: '100%' }}>
        <header>
          <Typography.Title level={1}>所选项确认</Typography.Title>
          <Typography.Paragraph>组件隔离示例：选择范围为当前页，确认仅更新本页模拟结果。</Typography.Paragraph>
        </header>
        <Card>
          <Space orientation="vertical" size="large" style={{ width: '100%' }}>
            <Table dataSource={rows} pagination={false} rowSelection={{ selectedRowKeys: selectedKeys, onChange: setSelectedKeys }}
              columns={[{ title: '对象', dataIndex: 'name' }, { title: '状态', dataIndex: 'status' }]} />
            <SelectionSummary selectedCount={selectedKeys.length} scopeLabel="当前页" onClear={() => setSelectedKeys([])}
              onConfirm={() => setResult(`已确认 ${selectedKeys.length} 项（模拟）`)} />
            <Typography.Paragraph role="status">{result}</Typography.Paragraph>
          </Space>
        </Card>
      </Space>
    </main>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode><ConfigProvider locale={zhCN}><App><Example /></App></ConfigProvider></StrictMode>,
)
