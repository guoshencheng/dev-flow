import { useEffect, useRef, useState } from 'react'

interface Props {
  title: string
  src: string
  width: number
  height: number
  kind?: 'desktop' | 'mobile'
}

// iframe 的内部视口由实际 width/height 决定，缩放只作用于外部展示。
export function DeviceViewport({ title, src, width, height, kind = 'mobile' }: Props) {
  const host = useRef<HTMLDivElement>(null)
  const [available, setAvailable] = useState(width + 24)
  const [fit, setFit] = useState(true)
  useEffect(() => {
    const node = host.current
    if (!node) return
    const observer = new ResizeObserver(([entry]) => setAvailable(entry.contentRect.width))
    observer.observe(node)
    return () => observer.disconnect()
  }, [])
  const scale = fit ? Math.min(1, Math.max(0.1, (available - 24) / (width + 16))) : 1
  return <div className={`viewport-host viewport-${kind}`} ref={host}>
    <div className="viewport-meta"><span>{width} × {height} px · {Math.round(scale * 100)}%</span>
      <button onClick={() => setFit((value) => !value)}>{fit ? '查看 1:1' : '适应宽度'}</button></div>
    <div className="viewport-scroller"><div className="viewport-footprint" style={{ width: (width + 16) * scale, height: (height + 16) * scale }}>
      <div className="device-shell" style={{ width: width + 16, height: height + 16, transform: `scale(${scale})` }}>
        <iframe title={title} src={src} width={width} height={height} style={{ width, height }} />
      </div>
    </div></div>
  </div>
}
