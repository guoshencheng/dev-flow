import { findComponent, gitSource, manifest, sourceBundle } from './source-kit.mjs'

const id = process.argv[2]
try {
  const result = id ? sourceBundle(findComponent(id)) : { schemaVersion: manifest.schemaVersion, ...gitSource(), components: manifest.components }
  console.log(JSON.stringify(result, null, 2))
} catch (error) { console.error(error.message); process.exitCode = 1 }
