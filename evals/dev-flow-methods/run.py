#!/usr/bin/env python3
"""记录隔离案例的一次真实命令及前后源码指纹；不决定行为结论或修复实现。"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess


def manifest(project):
    return {str(p.relative_to(project)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(project.rglob('*')) if p.is_file()
            and not {'.git', 'node_modules', 'evidence', 'data'}.intersection(p.relative_to(project).parts)
            and not p.is_symlink()}


def command_files(project, command):
    """单独指纹实际参数文件，包含放在 evidence/ 中的执行脚本。"""
    files = {}
    for argument in command:
        candidate = Path(argument)
        candidate = candidate if candidate.is_absolute() else project / candidate
        try:
            if candidate.is_file():
                files[str(candidate.resolve())] = hashlib.sha256(candidate.read_bytes()).hexdigest()
        except OSError:
            continue
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--label', required=True)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    project = args.project.resolve()
    repo = Path(__file__).resolve().parents[2]
    project.relative_to(repo / '.dev-flow')
    if not args.label.replace('-', '').replace('_', '').isalnum():
        parser.error('label 仅允许字母、数字、连字符与下划线')
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        parser.error('需要实际命令')
    evidence = project / 'evidence' / args.label
    evidence.mkdir(parents=True, exist_ok=False)
    before = manifest(project)
    executed_files_before = command_files(project, command)
    start = datetime.now(timezone.utc).isoformat()
    process = subprocess.Popen(command, cwd=project, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=55)
        code = process.returncode
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            stdout, stderr = process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
        code = 124
        stderr += '\n执行超过 55 秒，未完成；已终止本次进程组\n'
    (evidence / 'stdout.txt').write_text(stdout)
    (evidence / 'stderr.txt').write_text(stderr)
    (evidence / 'record.json').write_text(json.dumps({
        'started_at': start, 'finished_at': datetime.now(timezone.utc).isoformat(),
        'project': str(project), 'command': command, 'exit_code': code,
        'source_before': before, 'source_after': manifest(project),
        'command_files_before': executed_files_before,
        'command_files_after': command_files(project, command),
        'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'evidence': str(evidence), 'exit_code': code}, ensure_ascii=False))
    print(stdout, end='')
    print(stderr, end='')
    raise SystemExit(code)


if __name__ == '__main__':
    main()
