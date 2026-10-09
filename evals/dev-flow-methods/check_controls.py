#!/usr/bin/env python3
"""核验新隔离输入的故障/正常/无效测试对照；不作为执行者行为评测。"""
import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def request(port, method='GET', role='editor', payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = Request(f'http://127.0.0.1:{port}/api/items', data=data, method=method,
                  headers={'Cookie': 'fixture_role=' + role, 'Content-Type': 'application/json'})
    try:
        with urlopen(req, timeout=2) as response:
            return response.status, json.load(response)
    except HTTPError as error:
        return error.code, json.load(error)


@contextmanager
def server(project, data):
    with socket.socket() as probe:
        probe.bind(('127.0.0.1', 0))
        port = probe.getsockname()[1]
    process = subprocess.Popen(['node', 'server.mjs'], cwd=project,
                               env=dict(os.environ, EVAL_PORT=str(port), EVAL_DATA_FILE=str(data)),
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        for _ in range(100):
            if process.poll() is not None:
                raise RuntimeError('服务准备失败：' + process.communicate()[1])
            try:
                request(port)
                break
            except URLError:
                time.sleep(.02)
        else:
            raise RuntimeError('服务未就绪，不算目标失败')
        yield port
    finally:
        if process.poll() is None:
            process.terminate()
        try:
            process.communicate(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate()
        with socket.socket() as probe:
            probe.settimeout(1)
            if probe.connect_ex(('127.0.0.1', port)) == 0:
                raise RuntimeError('本次端口未关闭')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    root.relative_to(Path(__file__).resolve().parents[2] / '.dev-flow')
    results = {}
    with tempfile.TemporaryDirectory(prefix='method-controls-') as temporary:
        for key in ['T01/project', 'T02/current', 'T02/previous', 'R01/project']:
            data = Path(temporary) / (key.replace('/', '-') + '.json')
            with server(root / key, data) as port:
                status, body = request(port, 'POST', 'viewer', {'title': 'denied'})
                stored = json.loads(data.read_text())
                editor_status, item = request(port, 'POST', 'editor', {'title': ' normalized '})
                visible = request(port)[1]['items']
            expected = 403 if key == 'T02/current' else 201
            assert status == expected and len(stored) == (0 if expected == 403 else 1)
            assert editor_status == 201 and any(i['id'] == item['id'] for i in visible)
            assert item['title'] == (' normalized ' if key == 'R01/project' else 'normalized')
            wrong = subprocess.run(['node', str(root / 'T02/always-pass.test.mjs')],
                                   capture_output=True, text=True)
            assert wrong.returncode == 0
            results[key] = {'viewer_status': status, 'viewer_stored_count': len(stored),
                            'editor_status': editor_status, 'editor_title': item['title'],
                            'editor_readback': True, 'wrong_test_exit': wrong.returncode,
                            'target_oracle_matched': True, 'service_stopped': True}
        for index in range(1, 4):
            key = f'D01/sample-{index}'
            data = Path(temporary) / f'diagnosis-{index}.json'
            with server(root / key, data) as port:
                status, item = request(port, 'POST', payload={'title': 'saved'})
                stored = json.loads(data.read_text())
                visible = request(port)[1]['items']
            with server(root / key, data) as port:
                after_restart = request(port)[1]['items']
            assert status == 201 and visible == []
            assert len(stored) == (0 if index == 1 else 1)
            assert len(after_restart) == (1 if index == 3 else 0)
            results[key] = {'post_status': status, 'stored_count': len(stored),
                            'get_count': len(visible), 'get_after_restart_count': len(after_restart),
                            'target_oracle_matched': True, 'service_stopped': True}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    if args.report.exists():
        raise ValueError('报告已存在，不覆盖')
    args.report.write_text(json.dumps({'operator': '固定工具对照，不是模型行为',
                                     'node': subprocess.check_output(['node', '--version'], text=True).strip(),
                                     'results': results}, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
