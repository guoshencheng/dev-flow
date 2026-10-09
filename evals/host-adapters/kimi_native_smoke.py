#!/usr/bin/env python3
"""使用隔离 Kimi 与本地确定性模型验证原生发现/派发/Read/交接，不调用真实模型。"""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import threading
import time
import urllib.request

ROLES = ('product', 'visual', 'architecture', 'engineering', 'acceptance', 'operations')


def free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def run(package):
    package = package.resolve()
    evidence = {'mock_model': True, 'real_business_validation': False, 'roles': {}}
    with tempfile.TemporaryDirectory(prefix='dev-flow-kimi-native-') as temporary:
        base = Path(temporary); home = base / 'home'; home.mkdir(mode=0o700)
        project = base / 'business'; project.mkdir()
        subprocess.run(['git', 'init', '-q', str(project)], check=True)
        managed = home / 'plugins/managed/dev-flow'
        failures = []

        class Model(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                messages = body.get('messages', [])
                system = '\n'.join(str(m.get('content', '')) for m in messages if m.get('role') == 'system')
                role = next((r for r in ROLES if f'你承担 Dev Flow 的 dev-{r} 专业职责' in system), None)
                tools = [m for m in messages if m.get('role') == 'tool']
                available = [t.get('function', {}).get('name') for t in body.get('tools', [])]
                call = None
                content = 'Dev Flow adapter smoke'
                if role:
                    record = evidence['roles'].setdefault(role, {'base_prompt_expanded': '${base_prompt}' not in system,
                        'agent_tool_absent': 'Agent' not in available and 'AgentSwarm' not in available, 'reads': [], 'handoff': False})
                    if len(tools) < 2:
                        path = managed / ('skills/dev-'+role+'/SKILL.md' if not tools else 'skills/dev-flow/references/constitution.md')
                        call = ('Read', {'path': str(path)})
                        record['reads'].append(str(path.relative_to(managed)))
                    else:
                        expected = ('name: dev-'+role, '# 多角色研发体系总纲')
                        for marker, result in zip(expected, tools[-2:]):
                            if marker not in str(result.get('content', '')):
                                failures.append('Read did not return '+marker)
                        content = f'ADAPTER_HANDOFF_{role}: 已读取共用 Skill 与总纲；范围为宿主适配冒烟，未执行真实业务验收。'
                        record['handoff'] = True
                elif any('ADAPTER_PARENT_SMOKE' in str(m.get('content','')) for m in messages):
                    if len(tools) < len(ROLES):
                        role = ROLES[len(tools)]
                        prompt = (f'职责：dev-{role}。宿主适配冒烟；项目根路径：{project}。'
                            f'Skill：{managed}/skills/dev-{role}/SKILL.md。候选为当前隔离安装包；'
                            '授权仅为只读 Skill 与总纲，不修改文件、不派发其他 Agent。'
                            '最终给出完整交接，注明未执行真实业务验收。')
                        call = ('Agent', {'subagent_type': 'dev-'+role, 'description': '验证职责入口与交接',
                            'prompt': prompt, 'run_in_background': False})
                    else:
                        for role, result in zip(ROLES, tools[-6:]):
                            if 'ADAPTER_HANDOFF_'+role not in str(result.get('content', '')):
                                failures.append('Parent did not receive '+role)
                        content = 'ADAPTER_PARENT_COMPLETE'
                if call:
                    name, args = call
                    delta = {'role': 'assistant', 'tool_calls': [{'index': 0, 'id': 'call_'+str(time.time_ns()),
                        'type': 'function', 'function': {'name': name, 'arguments': json.dumps(args,ensure_ascii=False)}}]}
                    finish = 'tool_calls'
                else:
                    delta = {'role': 'assistant', 'content': content}; finish = 'stop'
                self.send_response(200)
                self.send_header('Content-Type', 'text/event-stream')
                self.end_headers()
                for d, reason in ((delta, None), ({}, finish)):
                    event = {'id': 'adapter-smoke', 'object': 'chat.completion.chunk', 'created': int(time.time()),
                        'model': 'gpt-4o', 'choices': [{'index': 0, 'delta': d, 'finish_reason': reason}]}
                    self.wfile.write(('data: '+json.dumps(event,ensure_ascii=False)+'\n\n').encode())
                self.wfile.write(b'data: [DONE]\n\n'); self.wfile.flush()

        model = ThreadingHTTPServer(('127.0.0.1', 0), Model)
        threading.Thread(target=model.serve_forever, daemon=True).start()
        # 假凭据仅发送给回环地址；不读取或复制用户真实 config/credentials。
        (home/'config.toml').write_text(f'''default_model = "adapter-fixture"
[providers.adapter-fixture]
type = "openai"
base_url = "http://127.0.0.1:{model.server_port}/v1"
api_key = "adapter-local-test-only"
[models.adapter-fixture]
provider = "adapter-fixture"
model = "gpt-4o"
max_context_size = 128000
''')
        env = dict(os.environ, KIMI_CODE_HOME=str(home))
        port = free_port()
        log = (base/'server.log').open('w')
        server = subprocess.Popen(['kimi','web','--no-open','--port',str(port),'--debug-endpoints'],
            cwd=project,env=env,stdout=log,stderr=log)
        try:
            for _ in range(100):
                if server.poll() is not None:
                    raise RuntimeError('Kimi server exited')
                try:
                    urllib.request.urlopen(f'http://127.0.0.1:{port}/api/v1/healthz',timeout=.2); break
                except (OSError, urllib.error.URLError): time.sleep(.1)
            else: raise RuntimeError('Kimi server readiness timeout')
            token = (home/'server.token').read_text().strip()
            def api(path, data=None):
                headers={'Authorization': 'Bearer '+token}
                if data is not None: headers['Content-Type']='application/json'
                request=urllib.request.Request(f'http://127.0.0.1:{port}'+path,
                    data=None if data is None else json.dumps(data).encode(),headers=headers)
                result=json.load(urllib.request.urlopen(request,timeout=15))
                if result['code'] != 0: raise RuntimeError(result['msg'])
                return result['data']
            installed=api('/api/v1/plugins',{'source':str(package)})
            assert installed['skillCount']==7 and not installed['hasErrors']
            assert installed['manifestKind']=='kimi-plugin-root'
            session=api('/api/v1/sessions',{'metadata':{'cwd':str(project)}})
            catalog=api('/api/v1/debug/session/'+session['id']+'/sessionAgentProfileCatalog/list')
            profiles=[p for p in catalog if p['name'].startswith('dev-')]
            assert {p['name'] for p in profiles}=={'dev-'+r for r in ROLES}
            assert all(p['subagents']==[] for p in profiles)
            evidence.update({'kimi_version':subprocess.check_output(['kimi','--version'],text=True).strip(),
                'native_install':True,'skills_discovered':7,'agents_discovered':len(profiles),'diagnostics':installed['diagnostics']})
            process=subprocess.run(['kimi','-p','ADAPTER_PARENT_SMOKE：按本次测试协议逐个验证六个职责子 Agent 的加载与交接。'],
                cwd=project,env=env,text=True,capture_output=True,timeout=90)
            if process.returncode or 'ADAPTER_PARENT_COMPLETE' not in process.stdout:
                raise RuntimeError('Native dispatch failed: '+process.stderr[-2000:]+' '+process.stdout[-2000:])
            assert not failures, failures
            assert set(evidence['roles'])==set(ROLES)
            assert all(r['base_prompt_expanded'] and r['agent_tool_absent'] and r['handoff'] and len(r['reads'])==2
                for r in evidence['roles'].values()), evidence
            evidence['native_dispatch_read_handoff']=True
            return evidence
        finally:
            server.terminate()
            try: server.wait(timeout=10)
            except subprocess.TimeoutExpired: server.kill();server.wait()
            model.shutdown();model.server_close();log.close()


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package',type=Path)
    args=parser.parse_args()
    print(json.dumps(run(args.package),ensure_ascii=False,indent=2))
