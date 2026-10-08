#!/usr/bin/env python3
"""执行隔离修复案例的一个阶段；不实施修复，不派发模型。"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import socket
import sys


sys.dont_write_bytecode = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--phase", choices=("before", "after"))
    parser.add_argument("--prepare", action="store_true", help="在尚不存在的路径复制固定输入")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    project = args.project.resolve()
    project.relative_to(repo / ".dev-flow")
    run = project.parent
    record_file = run / "checks.json"
    if args.prepare:
        if args.phase or project.exists() or record_file.exists():
            parser.error("准备使用新路径，且不同时执行测试阶段")
        donor = repo / "evals/dev-acceptance/fixtures/http-ui"
        before = repo / "evals/dev-engineering/fixtures/http-ui/server.before.mjs"
        shutil.copytree(donor, project)
        shutil.copy2(before, project / "server.mjs")
        record = {
            "run": str(run), "project": str(project),
            "operator": "固定隔离修复案例执行，不代表模型派发",
            "input_sha256": {
                str(p.relative_to(donor)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(donor.rglob("*")) if p.is_file()
            },
            "server_before_sha256": hashlib.sha256(before.read_bytes()).hexdigest(),
            "phases": [],
        }
        record_file.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({"prepared_project": str(project)}, ensure_ascii=False))
        return
    if not args.phase:
        parser.error("执行测试需提供 --phase before|after")
    record = json.loads(record_file.read_text())
    assert Path(record["project"]) == project
    phase = run / args.phase
    phase.mkdir()
    helper_path = repo / "evals/dev-acceptance/run.py"
    spec = importlib.util.spec_from_file_location("acceptance_runner", helper_path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    stable = {
        key: hashlib.sha256((project / key).read_bytes()).hexdigest()
        for key in record["input_sha256"] if key != "server.mjs"
    }
    assert all(value == record["input_sha256"][key] for key, value in stable.items())
    source_hash = hashlib.sha256((project / "server.mjs").read_bytes()).hexdigest()
    if args.phase == "before":
        assert source_hash == record["server_before_sha256"]
    else:
        assert source_hash != record["server_before_sha256"]
    data = phase / "items.json"
    data.write_text("[]\n")
    report_file = phase / "playwright-report.json"
    with socket.socket() as reservation:
        reservation.bind(("127.0.0.1", 0))
        port = reservation.getsockname()[1]
    env = dict(os.environ, EVAL_PORT=str(port), EVAL_DATA_FILE=str(data),
               EVAL_RESULT_FILE=str(report_file))
    execution = helper.command(["npm", "run", "test", "--", "--output",
                                str(phase / "artifacts")], project, env)
    report = json.loads(report_file.read_text())
    cases = {}
    for suite in report.get("suites", []):
        helper.collect_cases(suite, cases)
    expected = {key: "passed" for key in (
        "TC-API-01", "TC-API-02", "TC-API-03", "TC-E2E-01", "TC-UI-01", "TC-UI-02")}
    if args.phase == "before":
        for key in ("TC-API-01", "TC-API-02", "TC-E2E-01", "TC-UI-01"):
            expected[key] = "failed"
    with socket.socket() as probe:
        probe.settimeout(1)
        closed = probe.connect_ex(("127.0.0.1", port)) != 0
    valid = (cases == expected and closed and not report.get("errors")
             and execution["exit_code"] == (1 if args.phase == "before" else 0))
    record["phases"].append({
        "phase": args.phase, "executed_at": datetime.now(timezone.utc).isoformat(),
        "source_sha256": source_hash, "stable_input_sha256": stable,
        "helper_sha256": hashlib.sha256(helper_path.read_bytes()).hexdigest(),
        "port": port, "process_port_closed": closed, "cases": cases,
        "expected_cases": expected, "oracle_matched": valid,
        "command": execution, "report": str(report_file), "stats": report["stats"],
        "node": helper.command(["node", "--version"], project)["stdout"].strip(),
        "playwright": helper.command(["npx", "--no-install", "playwright", "--version"],
                                     project)["stdout"].strip(),
        "browser_executable": os.environ.get("EVAL_BROWSER_EXECUTABLE", "Playwright 默认 Chromium"),
    })
    record_file.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"phase": args.phase, "cases": cases,
                      "process_port_closed": closed, "oracle_matched": valid}, ensure_ascii=False))
    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
