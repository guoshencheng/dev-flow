#!/usr/bin/env python3
"""隔离验证源码包启动、健康/业务分离、应用回退与一致文件恢复。"""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import shutil
import socket
import subprocess
import tarfile
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import os

REPO = Path(__file__).resolve().parents[2]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def port_closed(port):
    with socket.socket() as sock:
        return sock.connect_ex(('127.0.0.1', port)) != 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    runtime = REPO / '.dev-flow'
    runtime.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix='operations-eval-', dir=runtime))
    output = args.output.resolve() if args.output else work / 'results'
    output.mkdir(parents=True, exist_ok=True)
    evidence = {'executor': '主 Agent 按 Skill 自执行；工具案例，未委派',
                'workspace': str(work), 'inputs': {}, 'commands': [],
                'artifacts': {}, 'processes': [], 'requests': [], 'checks': []}
    running = []

    def check(name, actual):
        evidence['checks'].append({'name': name, 'passed': bool(actual)})
        if not actual:
            raise AssertionError(name)

    def command(argv, cwd, env=None, timeout=30):
        result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True,
                                text=True, timeout=timeout)
        evidence['commands'].append({'argv': argv, 'cwd': str(cwd),
                                     'exit_code': result.returncode,
                                     'stdout': result.stdout, 'stderr': result.stderr})
        return result

    def request(port, route, payload=None, cookie=None):
        headers = {'content-type': 'application/json'}
        if cookie:
            headers['cookie'] = cookie
        req = Request('http://127.0.0.1:%s%s' % (port, route),
                      data=json.dumps(payload).encode() if payload is not None else None,
                      headers=headers)
        try:
            response = urlopen(req, timeout=3)
        except HTTPError as error:
            response = error
        with response:
            status = response.status
            data = json.loads(response.read())
            set_cookie = response.headers.get('set-cookie', '').split(';')[0]
        evidence['requests'].append({'port': port, 'route': route,
                                     'method': 'POST' if payload is not None else 'GET',
                                     'payload': payload, 'status': status, 'response': data})
        return status, data, set_cookie

    def start(directory, data_file):
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        env = {**os.environ, 'EVAL_PORT': str(port), 'EVAL_DATA_FILE': str(data_file)}
        log = (work / ('server-%s.log' % len(running))).open('w')
        proc = subprocess.Popen(['node', 'server.mjs'], cwd=directory, env=env,
                                stdout=log, stderr=subprocess.STDOUT)
        record = {'pid': proc.pid, 'port': port, 'cwd': str(directory),
                  'argv': ['node', 'server.mjs'],
                  'env': {'EVAL_PORT': str(port), 'EVAL_DATA_FILE': str(data_file)},
                  'stop': 'SIGTERM 自管 PID 后 wait，核对端口关闭'}
        evidence['processes'].append(record)
        entry = (proc, log, record)
        running.append(entry)
        for _ in range(50):
            if proc.poll() is not None:
                raise RuntimeError('自管服务启动失败：' + str(record))
            try:
                status, identity, _ = request(port, '/health')
                if status == 200:
                    manifest = json.loads((directory / 'version.json').read_text())
                    check('启动身份 ' + manifest['release_id'],
                          identity == {**manifest, 'kind': 'operations-fixture'})
                    check('运行源码指纹 ' + manifest['release_id'],
                          sha((directory / 'server.mjs').read_bytes()) == manifest['source_sha256'])
                    return entry
            except (URLError, OSError):
                time.sleep(0.1)
        raise RuntimeError('自管服务未就绪')

    def stop(entry):
        proc, log, record = entry
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)
        log.close()
        record['exit_code'] = proc.returncode
        record['port_closed'] = port_closed(record['port'])
        check('停止后入口关闭 PID %s' % proc.pid, record['port_closed'])

    def login(entry, role):
        status, _, cookie = request(entry[2]['port'], '/test/login', {'role': role})
        check('实际登录 ' + role, status == 200 and bool(cookie))
        return cookie

    def items(entry, cookie):
        status, data, _ = request(entry[2]['port'], '/api/items', cookie=cookie)
        check('真实读回', status == 200)
        return data['items']

    def save(entry, title, expected):
        cookie = login(entry, 'editor')
        before = items(entry, cookie)
        status, item, _ = request(entry[2]['port'], '/api/items', {'title': title}, cookie)
        check('保存响应', status == 201)
        after = items(entry, cookie)
        result = after == before + [item]
        check('保存与服务端读回 ' + title, result == expected)
        return cookie, after

    try:
        check('Node 可用', command(['node', '--version'], REPO).returncode == 0)
        source = REPO / 'evals/dev-engineering/fixtures/http-ui/server.before.mjs'
        patch = REPO / 'evals/dev-engineering/fixtures/http-ui/repair.patch'
        for path in [source, patch, Path(__file__)]:
            evidence['inputs'][str(path.relative_to(REPO))] = sha(path.read_bytes())
        candidate = work / 'candidate'
        candidate.mkdir()
        shutil.copy2(source, candidate / 'server.mjs')
        check('既有修复补丁重建', command(['git', 'apply', str(patch)], candidate).returncode == 0)
        fixed = (candidate / 'server.mjs').read_text()
        fixed = fixed.replace("const port = Number(process.env.EVAL_PORT);",
                              "const version = JSON.parse(await fs.readFile(new URL('./version.json', import.meta.url), 'utf8'));\nconst port = Number(process.env.EVAL_PORT);")
        old_health = "{ kind: 'engineering-fixture' }"
        check('健康身份修改位置唯一', fixed.count(old_health) == 1)
        fixed = fixed.replace(old_health, "{ kind: 'operations-fixture', ...version }")
        write = 'await writeItems([...items, item]);'
        check('受控故障修改位置唯一', fixed.count(write) == 1)
        bad = fixed.replace(write, '// 故障注入：响应成功但未持久化')
        directories = {}
        for label, content in [('good', fixed), ('bad', bad)]:
            manifest = {'release_id': 'ops-%s-1' % label, 'source_sha256': sha(content.encode())}
            files = {'server.mjs': content.encode(),
                     'version.json': (json.dumps(manifest, sort_keys=True) + '\n').encode(),
                     'README.md': ('# 隔离源码包\n需要本机 Node；无第三方依赖。\n'
                                   '在解包根目录配置 EVAL_PORT 和独立 EVAL_DATA_FILE 后执行 node server.mjs。\n'
                                   'GET /health 核对版本；POST /test/login role=editor 后保存/读回。\n'
                                   '向自管进程发送 SIGTERM 并等待结束；数据留在指定文件，不能用于生产。\n').encode()}
            archive = work / ('%s.tar.gz' % label)
            with archive.open('wb') as raw:
                with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as zipped:
                    with tarfile.open(fileobj=zipped, mode='w') as tar:
                        for name, data in sorted(files.items()):
                            info = tarfile.TarInfo(name)
                            info.size, info.mode, info.mtime = len(data), 0o644, 0
                            tar.addfile(info, io.BytesIO(data))
            directory = work / ('unpacked-' + label)
            directory.mkdir()
            # 只解包本函数生成并核验名称的文件，不接收外部归档。
            with tarfile.open(archive) as tar:
                check('包文件范围 ' + label, sorted(tar.getnames()) == sorted(files))
                for member in tar.getmembers():
                    (directory / member.name).write_bytes(tar.extractfile(member).read())
            check('实际解包内容 ' + label,
                  all((directory / name).read_bytes() == data for name, data in files.items()))
            evidence['artifacts'][label] = {**manifest, 'sha256': sha(archive.read_bytes()),
                                           'path': str(archive), 'unpacked': str(directory),
                                           'files': {name: sha(data) for name, data in files.items()}}
            directories[label] = directory
        data_file = work / 'data/items.json'
        env = {key: value for key, value in os.environ.items()
               if key not in ['EVAL_PORT', 'EVAL_DATA_FILE']}
        missing = command(['node', 'server.mjs'], directories['good'], env)
        check('缺少配置可定位启动失败', missing.returncode != 0 and '需要 EVAL_PORT' in missing.stderr)
        good = start(directories['good'], data_file)
        cookie, snapshot = save(good, '回退前保留条目', True)
        viewer = login(good, 'viewer')
        status, _, _ = request(good[2]['port'], '/api/items', {'title': '越权'}, viewer)
        check('拒绝越权且无副作用', status == 403 and items(good, cookie) == snapshot)
        status, _, _ = request(good[2]['port'], '/api/items', {'title': '  '}, cookie)
        check('拒绝空标题且无副作用', status == 422 and items(good, cookie) == snapshot)
        stop(good)
        restarted = start(directories['good'], data_file)
        check('跨进程数据保留', items(restarted, login(restarted, 'editor')) == snapshot)
        stop(restarted)
        faulty = start(directories['bad'], data_file)
        _, failed_snapshot = save(faulty, '响应成功但缺失条目', False)
        check('健康正常但业务失败可识别', failed_snapshot == snapshot)
        stop(faulty)
        recovered = start(directories['good'], data_file)
        check('应用回退保留原数据', items(recovered, login(recovered, 'editor')) == snapshot)
        _, snapshot = save(recovered, '回退后写入恢复', True)
        stop(recovered)
        backup = work / 'backup/items.json'
        backup.parent.mkdir()
        shutil.copy2(data_file, backup)
        evidence['backup'] = {'path': str(backup), 'sha256': sha(backup.read_bytes()),
                              'consistent': '已停止全部样本写入进程后复制', 'items': snapshot}
        data_file.write_text('[]\n')
        lost = start(directories['good'], data_file)
        check('隔离数据丢失可观察', items(lost, login(lost, 'editor')) == [])
        stop(lost)
        restored_file = work / 'restored/items.json'
        restored_file.parent.mkdir()
        shutil.copy2(backup, restored_file)
        restored = start(directories['good'], restored_file)
        check('实际恢复完整快照', items(restored, login(restored, 'editor')) == snapshot)
        _, final_items = save(restored, '恢复后可继续使用', True)
        evidence['restored'] = {'path': str(restored_file), 'items': final_items,
                                'data_loss_boundary': '恢复停止写入备份点全部条目；没有覆盖后续写入/数据库/生产环境'}
        stop(restored)
        evidence['outcome'] = 'passed'
    except Exception as error:
        evidence['outcome'] = 'failed'
        evidence['error'] = repr(error)
    finally:
        for entry in running:
            if entry[0].poll() is None:
                stop(entry)
        (output / 'checks.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')
        passed = sum(item['passed'] for item in evidence['checks'])
        report = ('# 运维隔离执行结果\n\n实际方式：主 Agent 自执行工具案例，未委派。\n\n'
                  '结果：%s；检查 %s/%s 通过。原始命令、请求、包/源码摘要及停止结果见 [checks.json](checks.json)。\n\n'
                  '范围：新解包目录、本机 Node、串行 HTTP/JSON 文件、受控故障、应用回退与停止写入后的文件备份恢复。\n'
                  '未覆盖：独立角色行为、原生派发、新机器、框架构建、真实项目、并发/数据库、云发布、生产灾备与下一任务复用。\n'
                  % (evidence['outcome'], passed, len(evidence['checks'])))
        (output / 'report.md').write_text(report)
        print(json.dumps({'outcome': evidence['outcome'], 'checks': len(evidence['checks']),
                          'passed': passed, 'output': str(output)}, ensure_ascii=False))
    if evidence['outcome'] != 'passed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
