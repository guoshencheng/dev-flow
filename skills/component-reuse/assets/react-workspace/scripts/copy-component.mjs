import { copyComponent } from './source-kit.mjs'

const [id, option, destination, ...extra] = process.argv.slice(2)
if (!id || option !== '--to' || !destination || extra.length) {
  console.error('用法：npm run --silent copy:component -- <组件 ID> --to /目标项目/src/components/dev-flow')
  process.exitCode = 1
} else {
  try { console.log(JSON.stringify(copyComponent(id, destination), null, 2)) }
  catch (error) { console.error(error.message); process.exitCode = 1 }
}
