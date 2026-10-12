import { useEffect, useState } from 'react'
import { Button, Result } from 'antd'
import { DesignOverview } from '../preview/DesignOverview'
import { pageRegistry, sectionRegistry } from '../preview/registry'
import { parseScenario } from '../features/orders/scenarios'

export function App() {
  const [hash, setHash] = useState(window.location.hash)
  useEffect(() => {
    const update = () => setHash(window.location.hash)
    window.addEventListener('hashchange', update)
    return () => window.removeEventListener('hashchange', update)
  }, [])
  const route = new URL(hash.slice(1) || '/overview/pages', 'https://design.local')
  const parts = route.pathname.split('/').filter(Boolean)
  if (parts[0] === 'page') {
    const entry = pageRegistry.find((item) => item.id === parts[1])
    if (entry) {
      const Page = entry.component
      const scenario = parseScenario(route.searchParams.get('scenario'))
      return <Page key={`${entry.id}-${scenario}`} scenario={scenario} />
    }
  } else if (parts[0] === 'overview') {
    const section = sectionRegistry.find((item) => item.id === (parts[1] || 'pages'))
    if (section) return <DesignOverview section={section.id} />
  } else if (parts[0] === 'components' || parts[0] === 'system') {
    const entry = sectionRegistry.find((item) => item.id === parts[0])
    if (entry && 'component' in entry) { const Showcase = entry.component; return <Showcase /> }
  }
  return <Result status="404" title="找不到这个设计入口" subTitle="请检查页面注册表或返回设计总览。" extra={<Button href="#/overview/pages">返回总览</Button>} />
}
