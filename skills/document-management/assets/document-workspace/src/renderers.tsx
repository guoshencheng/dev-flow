import { useEffect, useId, useRef, useState } from 'react'
import { Alert, Button, Select, Space, Spin, Table } from 'antd'
import DOMPurify from 'dompurify'
import Markdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'
import rehypeSlug from 'rehype-slug'
import mdxLoaders from 'virtual:design-mdx'
import pdfWorker from 'pdfjs-dist/build/pdf.worker.min.mjs?url'
import type { Components } from 'react-markdown'
import type { PDFDocumentProxy } from 'pdfjs-dist'
import type { CellValue } from 'exceljs'

export type DocumentEntry = { path: string; title: string; kind: string; status: string; metadata: Record<string, unknown>; rawPath: string; viewPath: string }
const encoded = (file: string) => file.split('/').map(encodeURIComponent).join('/')
const raw = (file: string) => '/__docs/file/' + encoded(file)
async function request(url: string) {
  const result = await fetch(url)
  if (!result.ok) { const error = await result.json(); throw new Error(error.error || `读取失败 ${result.status}`) }
  return result
}
async function source(file: string) {
  return (await (await request('/__docs/source/' + encoded(file))).json()).content as string
}
function useArtifact<T>(key: string, load: () => Promise<T>) {
  const [value, setValue] = useState<T>()
  const [error, setError] = useState('')
  useEffect(() => {
    let active = true
    setValue(undefined); setError('')
    load().then((next) => { if (active) setValue(() => next) }).catch((issue: unknown) => { if (active) setError(String(issue)) })
    return () => { active = false }
    // 每个格式由路径作为读取版本，服务变化会通过 Vite 刷新页面。
  }, [key])
  return { value, error }
}
function Waiting({ error }: { error: string }) { return error ? <Alert type="error" title="无法展示该文件" description={error} showIcon /> : <Spin aria-label="正在读取文档" /> }

let mermaidReady: ReturnType<typeof importMermaid> | undefined
async function importMermaid() {
  const { default: mermaid } = await import('mermaid')
  mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: 'default', htmlLabels: false })
  return mermaid
}
export function MermaidView({ code }: { code: string }) {
  const id = 'diagram-' + useId().replace(/[^a-zA-Z0-9]/g, '')
  const result = useArtifact(code, async () => {
    mermaidReady ||= importMermaid()
    const mermaid = await mermaidReady
    const rendered = await mermaid.render(id, code)
    return DOMPurify.sanitize(rendered.svg)
  })
  return result.value ? <div className="mermaid" dangerouslySetInnerHTML={{ __html: result.value }} /> : <Waiting error={result.error} />
}

function documentLink(file: string, target: string, image = false) {
  if (/^(https?:|mailto:|tel:|data:|#)/i.test(target)) return target
  const base = new URL(raw(file), location.origin)
  const resolved = new URL(target, base)
  if (!resolved.pathname.startsWith('/__docs/file/')) return resolved.href
  const relative = resolved.pathname.slice('/__docs/file/'.length)
  return (image ? '/__docs/file/' : '/view/') + relative + resolved.search + resolved.hash
}
function components(file: string): Components {
  return {
    a: ({ href, children }) => <a href={documentLink(file, href || '')}>{children}</a>,
    img: ({ src, alt }) => <img src={documentLink(file, typeof src === 'string' ? src : '', true)} alt={alt || ''} />,
    code: ({ className, children }) => className?.split(' ').includes('language-mermaid') ? <MermaidView code={String(children).trim()} /> : <code className={className}>{children}</code>,
  }
}
function MarkdownView({ file }: { file: DocumentEntry }) {
  const result = useArtifact(file.path, () => source(file.path))
  return result.value !== undefined ? <article className="document"><Markdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight, rehypeSlug]} components={components(file.path)}>{result.value}</Markdown></article> : <Waiting error={result.error} />
}
function MdxView({ file }: { file: DocumentEntry }) {
  const result = useArtifact(file.path, async () => {
    const loader = mdxLoaders[file.path]
    if (!loader) throw new Error('MDX 未进入当前编译索引')
    return (await loader()).default
  })
  const Component = result.value
  return Component ? <article className="document"><Component components={{ ...components(file.path), Button, Alert, Space, Table }} /></article> : <Waiting error={result.error} />
}
function WordView({ file }: { file: DocumentEntry }) {
  const result = useArtifact(file.path, async () => {
    const [module, response] = await Promise.all([import('mammoth/mammoth.browser'), request(raw(file.path))])
    const converted = await module.default.convertToHtml({ arrayBuffer: await response.arrayBuffer() })
    return { html: DOMPurify.sanitize(converted.value), messages: converted.messages }
  })
  return result.value ? <><Alert type="info" title="Word 内容预览" description="保留标题、段落与表格等语义；精确版式请查看原文件或有来源的 PDF 导出。" /><article className="document" dangerouslySetInnerHTML={{ __html: result.value.html }} />{result.value.messages.length > 0 && <Alert type="warning" title="转换提示" description={result.value.messages.map((item) => item.message).join('；')} />}</> : <Waiting error={result.error} />
}
const valueText = (value: CellValue): string => {
  if (value === null || value === undefined) return ''
  if (value instanceof Date) return value.toISOString().slice(0, 10)
  if (typeof value !== 'object') return String(value)
  if ('richText' in value) return value.richText.map((part) => part.text).join('')
  if ('text' in value) return value.text
  if ('formula' in value) return value.result === undefined ? '=' + value.formula : String(value.result)
  if ('error' in value) return value.error
  return JSON.stringify(value)
}
function DataGrid({ rows }: { rows: string[][] }) {
  const count = Math.min(30, Math.max(0, ...rows.map((row) => row.length)))
  const columns = Array.from({ length: count }, (_, index) => ({ title: rows[0]?.[index] || `列 ${index + 1}`, dataIndex: String(index), key: String(index), width: 180 }))
  const data = rows.slice(1, 301).map((row, index) => Object.fromEntries([['key', String(index)], ...row.slice(0, 30).map((cell, column) => [String(column), cell])]))
  return <><p>以首行为表头，最多展示前 300 条数据、30 列；公式使用文件内缓存结果，未重新计算。完整内容见原文件。</p><Table size="small" columns={columns} dataSource={data} scroll={{ x: Math.max(600, count * 180) }} pagination={{ pageSize: 20 }} /></>
}
function SheetView({ file }: { file: DocumentEntry }) {
  const [selected, setSelected] = useState(0)
  const result = useArtifact(file.path, async () => {
    const [module, response] = await Promise.all([import('exceljs'), request(raw(file.path))])
    const book = new module.default.Workbook()
    await book.xlsx.load(await response.arrayBuffer() as Parameters<typeof book.xlsx.load>[0])
    return book.worksheets.map((sheet) => ({ name: sheet.name, rows: Array.from({ length: Math.min(sheet.rowCount, 301) }, (_, row) => Array.from({ length: Math.min(sheet.columnCount, 30) }, (_, column) => valueText(sheet.getRow(row + 1).getCell(column + 1).value))) }))
  })
  useEffect(() => setSelected(0), [file.path])
  return result.value ? <><Select aria-label="工作表" value={selected} options={result.value.map((sheet, index) => ({ value: index, label: sheet.name }))} onChange={setSelected} /><DataGrid rows={result.value[selected]?.rows || []} /></> : <Waiting error={result.error} />
}
function CsvView({ file }: { file: DocumentEntry }) {
  const result = useArtifact(file.path, async () => {
    const { default: parser } = await import('papaparse')
    const parsed = parser.parse<string[]>(await source(file.path), { skipEmptyLines: true })
    if (parsed.errors.length) throw new Error(parsed.errors.map((item) => item.message).join('；'))
    return parsed.data
  })
  return result.value ? <DataGrid rows={result.value} /> : <Waiting error={result.error} />
}
function PdfView({ file }: { file: DocumentEntry }) {
  const canvas = useRef<HTMLCanvasElement>(null)
  const [pdf, setPdf] = useState<PDFDocumentProxy>()
  const [page, setPage] = useState(1)
  const [error, setError] = useState('')
  useEffect(() => {
    let active = true; let task: { destroy(): Promise<void> } | undefined
    setPdf(undefined); setPage(1); setError('')
    import('pdfjs-dist').then(async (module) => {
      module.GlobalWorkerOptions.workerSrc = pdfWorker
      const loading = module.getDocument({ data: await (await request(raw(file.path))).arrayBuffer() })
      task = loading
      const document = await loading.promise
      if (active) setPdf(document); else await loading.destroy()
    }).catch((issue: unknown) => { if (active) setError(String(issue)) })
    return () => { active = false; void task?.destroy() }
  }, [file.path])
  useEffect(() => {
    let active = true; let rendering: { cancel(): void } | undefined
    if (!pdf || !canvas.current) return
    pdf.getPage(page).then((entry) => {
      if (!active || !canvas.current) return
      const viewport = entry.getViewport({ scale: 1.3 })
      canvas.current.width = viewport.width; canvas.current.height = viewport.height
      rendering = entry.render({ canvas: canvas.current, viewport })
      return (rendering as ReturnType<typeof entry.render>).promise
    }).catch((issue: unknown) => { if (active) setError(String(issue)) })
    return () => { active = false; rendering?.cancel() }
  }, [pdf, page])
  return <>{error && <Waiting error={error} />}{pdf ? <Space><Button disabled={page === 1} onClick={() => setPage((value) => value - 1)}>上一页</Button><span>{page} / {pdf.numPages}</span><Button disabled={page === pdf.numPages} onClick={() => setPage((value) => value + 1)}>下一页</Button></Space> : !error && <Spin aria-label="正在读取 PDF" />}<canvas className="pdf-page" ref={canvas} role="img" aria-label={`${file.title} 第 ${page} 页`} /></>
}
function SourceView({ file }: { file: DocumentEntry }) {
  const result = useArtifact(file.path, () => source(file.path))
  if (result.value === undefined) return <Waiting error={result.error} />
  if (file.kind === 'mermaid') return <MermaidView code={result.value} />
  let content = result.value
  if (file.path.toLowerCase().endsWith('.json')) { try { content = JSON.stringify(JSON.parse(content), null, 2) } catch { /* 原文保留以便定位格式错误。 */ } }
  return <pre className="source"><code>{content}</code></pre>
}
export function DocumentView({ file }: { file: DocumentEntry }) {
  if (file.kind === 'markdown') return <MarkdownView file={file} />
  if (file.kind === 'mdx') return <MdxView file={file} />
  if (file.kind === 'word') return <WordView file={file} />
  if (file.kind === 'sheet') return <SheetView file={file} />
  if (file.kind === 'csv') return <CsvView file={file} />
  if (file.kind === 'pdf') return <PdfView file={file} />
  if (file.kind === 'image') return <img className="asset-image" src={raw(file.path)} alt={file.title} />
  if (file.kind === 'video') return <video controls src={raw(file.path)} className="asset-media" />
  if (file.kind === 'audio') return <audio controls src={raw(file.path)} />
  if (file.kind === 'html') return <iframe title={file.title} src={raw(file.path) + location.search} sandbox="allow-scripts allow-forms" className="html-preview" />
  if (file.kind === 'download') return <Alert type="info" title="此格式请使用原工具或导出预览" description="例如 PPTX、旧版 Office、设计专用格式：保留原文件，并将同版本 PDF、HTML 或图片导出关联到文档。可通过上方原文件入口下载。" />
  return <SourceView file={file} />
}
