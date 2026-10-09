import { useState } from 'react'
import type { Key } from 'react'
import { Space, Table, Typography } from 'antd'
import { SelectionSummary } from '@dev-flow/ui-antd'

const rows = [
  { key: 'one', name: '示例对象一', status: '待确认' },
  { key: 'two', name: '示例对象二', status: '待确认' },
  { key: 'three', name: '示例对象三', status: '待确认' },
]

// scenario 用于目录的状态预览；真实项目以自己的选择与请求状态为准。
export function SelectionSummaryExample({ scenario = 'empty' }: { scenario?: string }) {
  const busy = scenario === 'busy'
  const [selectedKeys, setSelectedKeys] = useState<Key[]>(scenario === 'empty' ? [] : ['one', 'two'])
  const [result, setResult] = useState('确认仅更新本页模拟结果。')
  return (
    <Space orientation="vertical" size="large" style={{ width: '100%' }}>
      <Table size="small" dataSource={rows} pagination={false}
        rowSelection={{ selectedRowKeys: selectedKeys, onChange: setSelectedKeys, getCheckboxProps: () => ({ disabled: busy }) }}
        columns={[{ title: '对象', dataIndex: 'name' }, { title: '状态', dataIndex: 'status' }]} />
      <SelectionSummary selectedCount={selectedKeys.length} scopeLabel="当前页" busy={busy}
        onClear={() => setSelectedKeys([])} onConfirm={() => setResult(`已确认 ${selectedKeys.length} 项（模拟）`)} />
      <Typography.Text role="status">{result}</Typography.Text>
    </Space>
  )
}
