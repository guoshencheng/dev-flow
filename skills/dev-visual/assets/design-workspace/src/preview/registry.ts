import type { ComponentType } from 'react'
import { DesktopOrderPage } from '../features/orders/views/DesktopOrderPage'
import { MobileOrderPage } from '../features/orders/views/MobileOrderPage'
import { ComponentPreview } from './ComponentPreview'
import { DesignSystemPreview } from './DesignSystemPreview'
import type { ScenarioId } from '../features/orders/scenarios'

export const pageRegistry = [
  { id: 'orders-desktop', title: '订单管理', platform: '桌面端', kind: 'desktop', width: 1280, height: 800,
    component: DesktopOrderPage as ComponentType<{ scenario: ScenarioId }>, source: 'src/features/orders/views/DesktopOrderPage.tsx', specification: 'docs/visual/pages/orders.md' },
  { id: 'orders-mobile', title: '订单管理', platform: '移动端', kind: 'mobile', width: 390, height: 844,
    component: MobileOrderPage as ComponentType<{ scenario: ScenarioId }>, source: 'src/features/orders/views/MobileOrderPage.tsx', specification: 'docs/visual/pages/orders.md' },
] as const

export const sectionRegistry = [
  { id: 'pages', title: '页面设计', subtitle: '各端页面 · 同一组业务组件', mark: '01' },
  { id: 'components', title: '组件展示', subtitle: '真实组件 · 完整状态', mark: '02', component: ComponentPreview },
  { id: 'system', title: '设计规范', subtitle: '规范源文档 · 实际主题', mark: '03', component: DesignSystemPreview },
] as const

export type SectionId = (typeof sectionRegistry)[number]['id']
export const pageHref = (id: string, scenario: ScenarioId = 'normal') => `#/page/${encodeURIComponent(id)}?scenario=${scenario}`
