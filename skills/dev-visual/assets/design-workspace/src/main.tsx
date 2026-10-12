import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { App as AntdApp, ConfigProvider } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import { App } from './app/App'
import { antdTheme, installTheme } from './theme/tokens'
import './styles.css'

installTheme()
createRoot(document.getElementById('root')!).render(
  <StrictMode><ConfigProvider locale={zhCN} theme={antdTheme}><AntdApp><App /></AntdApp></ConfigProvider></StrictMode>,
)
