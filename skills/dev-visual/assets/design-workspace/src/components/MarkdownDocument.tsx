import ReactMarkdown, { defaultUrlTransform } from 'react-markdown'
import remarkGfm from 'remark-gfm'

export function MarkdownDocument({ source, links = {} }: { source: string; links?: Record<string, string> }) {
  return <article className="markdown-document"><ReactMarkdown remarkPlugins={[remarkGfm]}
    urlTransform={(url) => defaultUrlTransform(links[url] ?? url)}>{source}</ReactMarkdown></article>
}
