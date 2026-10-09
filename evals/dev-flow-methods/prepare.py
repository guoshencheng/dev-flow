#!/usr/bin/env python3
"""准备新的隔离方法案例；仅构造输入，不替执行者修复或应用答案。"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


REPO = Path(__file__).resolve().parents[2]


def replace(source, old, new):
    if source.count(old) != 1:
        raise ValueError('样本基线不匹配：' + old)
    return source.replace(old, new)


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def fixed_source():
    source = (REPO / 'evals/dev-acceptance/fixtures/http-ui/server.mjs').read_text()
    source = replace(source, "const variant = process.env.EVAL_VARIANT || 'fixed';\n", '')
    source = replace(source, "!['broken', 'fixed'].includes(variant) || ", '')
    source = replace(source, "${variant === 'broken' ? \"input.value = '';\" : ''}", '')
    source = replace(source, "role !== 'editor' && variant === 'fixed'", "role !== 'editor'")
    source = replace(source, "if (variant === 'fixed' || role === 'viewer') await writeItems([...items, item]);", "await writeItems([...items, item]);")
    source = source.replace(', variant', '').replace('EVAL_VARIANT=broken|fixed、', '')
    return source.replace('      // 缺陷版本只向编辑者返回成功，没有保存；查看者却被允许写入。\n', '')


SPEC = '''# 隔离条目应用契约

RULE-01：fixture editor 可以保存非空标题，成功返回 201，保存后通过 GET /api/items 和刷新页面仍可见。
RULE-02：fixture viewer 可读取、不能写入，POST 返回 403 且没有任何存储写入副作用；未登录返回 401。
RULE-03：标题去除首尾空白，纯空白返回 422 且没有副作用。
身份通过测试 Cookie fixture_role=editor|viewer 指定，不代表生产身份方案。
服务入口为 node server.mjs，需要独立 EVAL_PORT 和 EVAL_DATA_FILE。存储是 JSON 文件，页面为遗留 HTML/JS。
仅隔离案例，沿用既有有效预期；不需要重新要求用户确认用例，也不部署。
'''


def project(root, source):
    write(root / 'server.mjs', source)
    write(root / 'docs/product.md', SPEC)
    write(root / 'package.json', '{"private":true,"type":"module"}\n')


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    root.relative_to(REPO / '.dev-flow')
    if root.exists():
        parser.error('需要尚不存在的路径，保留旧证据')
    root.mkdir(parents=True)
    good = fixed_source()
    no_auth = replace(good, "      if (role !== 'editor') return json(response, 403, { error: 'FORBIDDEN' });\n", '')
    project(root / 'T01/project', no_auth)
    project(root / 'T02/current', good)
    project(root / 'T02/previous', no_auth)
    write(root / 'T02/always-pass.test.mjs', "import assert from 'node:assert/strict';\nassert.ok(true, 'viewer cannot write');\n")
    project(root / 'D01/sample-1', replace(good, '      await writeItems([...items, item]);', '      void items;'))
    wrong_read = replace(good, "const readItems = async () => JSON.parse(await fs.readFile(dataFile, 'utf8'));", "const readItems = async () => JSON.parse(await fs.readFile(dataFile, 'utf8'));\nconst readVisibleItems = async () => JSON.parse(await fs.readFile(dataFile + '.read', 'utf8'));\ntry { await fs.writeFile(dataFile + '.read', '[]\\n', { flag: 'wx' }); } catch (e) { if (e.code !== 'EEXIST') throw e; }")
    wrong_read = replace(wrong_read, '{ items: await readItems() }', '{ items: await readVisibleItems() }')
    project(root / 'D01/sample-2', wrong_read)
    cached = replace(good, "const roleOf =", "const visibleCache = await readItems();\nconst roleOf =")
    project(root / 'D01/sample-3', replace(cached, '{ items: await readItems() }', '{ items: visibleCache }'))
    review = root / 'R01/project'
    project(review, good)
    git(review, 'init', '--quiet')
    git(review, 'config', 'user.name', 'Isolated method fixture')
    git(review, 'config', 'user.email', 'fixture@example.invalid')
    git(review, 'add', '.')
    git(review, 'commit', '--quiet', '-m', 'baseline')
    baseline = git(review, 'rev-parse', 'HEAD')
    write(review / 'server.mjs', no_auth)
    git(review, 'add', 'server.mjs')
    git(review, 'commit', '--quiet', '-m', 'simplify request processing')
    second = replace(no_auth, '<title>条目保存测试</title>', '<title>条目工作台</title>')
    write(review / 'server.mjs', second)
    git(review, 'add', 'server.mjs')
    git(review, 'commit', '--quiet', '-m', 'update page title')
    third = replace(second, "kind: 'acceptance-fixture'", "kind: 'method-fixture'")
    write(review / 'server.mjs', third)
    git(review, 'add', 'server.mjs')
    git(review, 'commit', '--quiet', '-m', 'name health response')
    candidate = git(review, 'rev-parse', 'HEAD')
    write(review / 'server.mjs', replace(third, 'title: title.trim()', 'title'))
    write(review / 'review-input.json', json.dumps({'baseline': baseline, 'candidate': candidate, 'uncommitted': ['server.mjs']}, indent=2) + '\n')
    manifest = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in root.rglob('*') if p.is_file() and '.git' not in p.parts}
    write(root / 'initial-manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'root': str(root), 'review_baseline': baseline, 'review_candidate': candidate}, indent=2))


if __name__ == '__main__':
    main()
