import manifest from '../../../catalog.json'
import { sources } from './source-files'
import selectionCode from './examples/selection-summary.tsx?raw'
import actionCode from './examples/action-card.tsx?raw'
import buttonCode from './examples/button.tsx?raw'
import cardCode from './examples/card.tsx?raw'

export type Platform = 'business' | 'consumer-web'
const examples: Record<string, string> = {
  'antd-selection-summary': selectionCode,
  'web-action-card': actionCode,
  'web-button': buttonCode,
  'web-card': cardCode,
}
export const components = manifest.components.map((item) => ({
  ...item,
  code: item.usageReplacements.reduce((text, [from, to]) => text.replaceAll(from, to), examples[item.id]),
  sourceFiles: item.files.map((file) => ({ ...file, content: sources[file.source] })),
}))
export type CatalogComponent = typeof components[number]
export interface Selection { id: string; scenario: string }

const storageKey = 'dev-flow:component-candidates:v1'
export function loadSelections(): Selection[] {
  try {
    const stored: unknown = JSON.parse(sessionStorage.getItem(storageKey) || '[]')
    if (!Array.isArray(stored)) return []
    const valid = stored.filter((item): item is Selection => {
      if (!item || typeof item !== 'object' || typeof item.id !== 'string' || typeof item.scenario !== 'string') return false
      return components.some((component) => component.id === item.id && component.scenarios.some((scenario) => scenario.id === item.scenario))
    })
    return valid.filter((item, index) => valid.findIndex((other) => other.id === item.id) === index)
  } catch { return [] }
}
export function saveSelections(items: Selection[]): boolean {
  try { sessionStorage.setItem(storageKey, JSON.stringify(items)); return true }
  catch { return false }
}
export function selectionRecord(items: Selection[]) {
  return JSON.stringify({
    schemaVersion: 2,
    status: 'candidate',
    sourceRepository: 'dev-flow',
    sourceCommit: null,
    components: items.map((item) => {
      const component = components.find((entry) => entry.id === item.id)!
      return {
        id: component.id, name: component.name, platform: component.platform,
        adoptionMode: component.adoptionMode, library: component.library,
        files: component.files,
        source: component.source, example: component.example,
        previewScenario: item.scenario,
      }
    }),
  }, null, 2)
}
