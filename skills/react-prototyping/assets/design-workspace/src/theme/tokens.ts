import type { ThemeConfig } from 'antd'

// 此模块是示例主题数值的权威来源，规范展示和 antd 同时读取。
export const tokens = {
  color: {
    primary: '#176b52',
    primarySoft: '#eaf3ee',
    text: '#20372e',
    muted: '#738078',
    canvas: '#f4f5f1',
    surface: '#ffffff',
    border: '#e2e7df',
    success: '#267948',
    warning: '#a36519',
    danger: '#bb4944',
  },
  radius: { small: 8, medium: 12, large: 20 },
  space: [4, 8, 12, 16, 24, 32, 48],
  type: { body: 14, small: 12, title: 24, display: 32 },
  fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif',
} as const

export const antdTheme: ThemeConfig = {
  token: {
    colorPrimary: tokens.color.primary,
    colorText: tokens.color.text,
    colorTextSecondary: tokens.color.muted,
    colorBorder: tokens.color.border,
    colorSuccess: tokens.color.success,
    colorWarning: tokens.color.warning,
    colorError: tokens.color.danger,
    fontFamily: tokens.fontFamily,
    fontSize: tokens.type.body,
    borderRadius: tokens.radius.small,
  },
}

export function installTheme() {
  const style = document.documentElement.style
  for (const [name, value] of Object.entries(tokens.color)) style.setProperty(`--color-${name}`, value)
  for (const [name, value] of Object.entries(tokens.radius)) style.setProperty(`--radius-${name}`, `${value}px`)
  for (const [name, value] of Object.entries(tokens.type)) style.setProperty(`--type-${name}`, `${value}px`)
  for (const value of tokens.space) style.setProperty(`--space-${value}`, `${value}px`)
  style.setProperty('--font-family', tokens.fontFamily)
}
