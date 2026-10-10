import React, { Component, useEffect, useMemo, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { Alert, Button, ConfigProvider, Drawer, Empty, Input, Select, Space, Spin, Switch, Tag, Tree, Typography, message } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import { DocumentView } from './renderers'
import type { DocumentEntry } from './renderers'
import 'highlight.js/styles/github.css'
import './styles.css'

type Index = { project: string; roots: string[]; files: DocumentEntry[]; truncated: boolean }
type DocumentTreeNode = {
  key: string
  title: React.ReactNode
  isLeaf?: boolean
  selectable?: boolean
  nodeType: 'directory' | 'file'
  path: string
  name: string
  children?: DocumentTreeNode[]
}

function buildDocumentTree(files: DocumentEntry[]) {
  const roots: DocumentTreeNode[] = []
  const nodes = new Map<string, DocumentTreeNode>()

  for (const file of files) {
    const segments = file.path.split('/')
    let children = roots
    let parentPath = ''

    segments.forEach((segment, index) => {
      const currentPath = parentPath ? `${parentPath}/${segment}` : segment
      const isFile = index === segments.length - 1
      const key = isFile ? file.path : `directory:${currentPath}`
      let node = nodes.get(key)

      if (!node) {
        node = isFile
          ? {
              key,
              title: <span className="document-tree-file" title={file.path}><span>{file.title}</span><small>{segment} · {file.kind}</small></span>,
              isLeaf: true,
              nodeType: 'file',
              path: file.path,
              name: file.title,
            }
          : {
              key,
              title: <span className="document-tree-directory">{segment}</span>,
              children: [],
              selectable: false,
              nodeType: 'directory',
              path: currentPath,
              name: segment,
            }
        nodes.set(key, node)
        children.push(node)
      }

      if (!isFile) {
        children = node.children!
        parentPath = currentPath
      }
    })
  }

  const sortNodes = (items: DocumentTreeNode[]) => {
    items.sort((left, right) => {
      if (left.nodeType !== right.nodeType) return left.nodeType === 'directory' ? -1 : 1
      return left.name.localeCompare(right.name, 'zh-CN')
    })
    items.forEach((item) => { if (item.children) sortNodes(item.children) })
  }
  sortNodes(roots)

  const directoryKeys = Array.from(nodes.values())
    .filter((node) => node.nodeType === 'directory')
    .map((node) => String(node.key))
  const rootDirectoryKeys = roots
    .filter((node) => node.nodeType === 'directory')
    .map((node) => String(node.key))

  return { treeData: roots, directoryKeys, rootDirectoryKeys }
}

function selectedPath() { return location.pathname.startsWith('/view/') ? decodeURIComponent(location.pathname.slice('/view/'.length)) : '' }
class PreviewBoundary extends Component<{ children: React.ReactNode }, { error: string }> {
  state = { error: '' }
  static getDerivedStateFromError(error: unknown) { return { error: String(error) } }
  render() { return this.state.error ? <Alert type="error" title="文档组件执行失败" description={this.state.error} /> : this.props.children }
}
function App() {
  const [index, setIndex] = useState<Index>()
  const [error, setError] = useState('')
  const [selected, setSelected] = useState(selectedPath)
  const [query, setQuery] = useState('')
  const [kind, setKind] = useState('all')
  const [archives, setArchives] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)
  const [expandedKeys, setExpandedKeys] = useState<React.Key[]>([])
  const [expandedInitialized, setExpandedInitialized] = useState(false)
  const [api, holder] = message.useMessage()
  useEffect(() => {
    const controller = new AbortController()
    fetch('/__docs/index', { signal: controller.signal }).then(async (response) => {
      if (!response.ok) throw new Error(`目录读取失败 ${response.status}`)
      const value = await response.json() as Index
      setIndex(value)
      if (!selectedPath() && value.files.length) {
        const first = value.files.find((file) => /(^|\/)index\.md$/.test(file.path)) || value.files[0]
        history.replaceState(null, '', first.viewPath); setSelected(first.path)
      }
    }).catch((issue: unknown) => { if (!controller.signal.aborted) setError(String(issue)) })
    const pop = () => setSelected(selectedPath())
    window.addEventListener('popstate', pop)
    return () => { controller.abort(); window.removeEventListener('popstate', pop) }
  }, [])
  const file = index?.files.find((entry) => entry.path === selected)
  const replacement = typeof file?.metadata.supersededBy === 'string' ? index?.files.find((entry) => entry.path === file.metadata.supersededBy) : undefined
  const visible = useMemo(() => index?.files.filter((entry) => (archives || !entry.path.includes('/archive/')) && (kind === 'all' || entry.kind === kind) && (entry.title + ' ' + entry.path).toLowerCase().includes(query.toLowerCase())) || [], [archives, index, kind, query])
  const documentTree = useMemo(() => buildDocumentTree(visible.slice(0, 120)), [visible])

  useEffect(() => {
    if (index && !expandedInitialized) {
      setExpandedKeys(documentTree.rootDirectoryKeys)
      setExpandedInitialized(true)
    }
  }, [documentTree.rootDirectoryKeys, expandedInitialized, index])

  useEffect(() => {
    if (!query.trim()) return
    setExpandedKeys((current) => Array.from(new Set([...current, ...documentTree.directoryKeys])))
  }, [documentTree.directoryKeys, query])

  const navigate = (next: string) => {
    const entry = index?.files.find((item) => item.path === next)
    if (!entry) return
    history.pushState(null, '', entry.viewPath); setSelected(next); setMenuOpen(false); window.scrollTo(0, 0)
  }
  const navigation = <nav aria-label="设计文档目录">
    <Input.Search aria-label="查找文档" placeholder="查找标题或文件路径" value={query} onChange={(event) => setQuery(event.target.value)} allowClear />
    <Select aria-label="文档格式" value={kind} onChange={setKind} options={[{ value: 'all', label: '全部格式' }, ...Array.from(new Set(index?.files.map((item) => item.kind))).map((value) => ({ value, label: value }))]} />
    <Space className="archive-option"><Switch checked={archives} onChange={setArchives} size="small" aria-label="显示归档" /><span>显示归档</span></Space>
    <p className="muted">{visible.length} 份资料{visible.length > 120 ? ' · 目录展示前 120 份，请搜索' : ''}</p>
    {index && (visible.length ? <Tree
      aria-label="文档目录"
      className="document-tree"
      treeData={documentTree.treeData}
      blockNode
      showLine
      selectedKeys={selected ? [selected] : []}
      expandedKeys={expandedKeys.filter((key) => documentTree.directoryKeys.includes(String(key)))}
      autoExpandParent={Boolean(query.trim())}
      onExpand={(keys) => setExpandedKeys(keys)}
      onSelect={(keys) => {
        const next = keys[0]
        if (typeof next === 'string' && visible.some((item) => item.path === next)) navigate(next)
      }}
    /> : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description="没有匹配的资料" />)}
  </nav>
  return <>{holder}<div className="reader">
    <aside className="sidebar"><Typography.Title level={4}>项目设计资料</Typography.Title><p className="muted">产品规则 · 视觉规格 · 原型</p>{navigation}</aside>
    <main className="content">
      <header className="document-header">
        <Button className="mobile-menu" onClick={() => setMenuOpen(true)}>文档目录</Button>
        <div className="document-identity"><Typography.Title level={3}>{file?.title || '项目设计资料'}</Typography.Title><Typography.Text type="secondary" className="file-path">{file?.path || index?.project}</Typography.Text></div>
        {file && <Space wrap><Tag>{file.status}</Tag><Tag>{file.kind}</Tag><Button onClick={async () => { try { await navigator.clipboard.writeText(location.href); api.success('已复制当前预览地址') } catch { api.error('复制失败，可使用浏览器地址') } }}>复制地址</Button><Button href={file.rawPath} target="_blank" rel="noreferrer">原文件</Button><Button href={file.rawPath + '?download=1'}>下载</Button></Space>}
      </header>
      <section className="document-body" aria-label="文档内容">
        {file && (file.metadata.id || file.metadata.version) ? <div className="document-metadata"><Space wrap>{file.metadata.id ? <Tag>{String(file.metadata.id)}</Tag> : null}{file.metadata.version ? <Typography.Text type="secondary">版本 {String(file.metadata.version)}</Typography.Text> : null}{file.metadata.owner ? <Typography.Text type="secondary">主责 {String(file.metadata.owner)}</Typography.Text> : null}</Space></div> : null}
        {file && ['archived', 'superseded'].includes(file.status) && <Alert type="warning" title="历史资料，不能作为当前规则" description={replacement ? <a href={replacement.viewPath}>查看现行版本：{replacement.title}</a> : '现行入口以项目索引为准。'} />}
        {error && <Alert type="error" title="无法加载设计资料" description={error} />}
        {index?.truncated && <Alert type="warning" title="目录达到 2500 文件上限" description="通过 --roots 缩小文档范围后重启。" />}
        {!index && !error && <Spin aria-label="正在加载目录" />}
        {index && !file && <Empty description={selected ? '当前文档不存在，请核对地址或从目录选择' : '指定目录内暂无资料'} />}
        {file && <PreviewBoundary key={file.path}><DocumentView file={file} /></PreviewBoundary>}
      </section>
      <footer>文档源码由项目维护 · 地址依赖当前本机预览服务</footer>
    </main>
    <Drawer title="设计文档目录" open={menuOpen} onClose={() => setMenuOpen(false)} placement="left" size={320}>{navigation}</Drawer>
  </div></>
}
const root = createRoot(document.getElementById('root')!)
root.render(<React.StrictMode><ConfigProvider locale={zhCN} theme={{ token: { colorPrimary: '#315bd6', borderRadius: 8, fontSize: 14, colorBgLayout: '#f5f7fb' } }}><App /></ConfigProvider></React.StrictMode>)
if (import.meta.hot) import.meta.hot.dispose(() => root.unmount())
