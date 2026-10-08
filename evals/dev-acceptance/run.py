#!/usr/bin/env python3
"""隔离运行固定 HTTP/UI 判据，校验缺陷检出和修复复验；不是模型行为评测。"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile


def command(args, cwd, env=None, timeout=180):
    result = subprocess.run(args, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    return {"argv": args, "exit_code": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr}


def collect_cases(suite, output):
    for spec in suite.get("specs", []):
        case_id = spec["title"].split()[0]
        tests = spec["tests"]
        if len(tests) != 1 or len(tests[0]["results"]) != 1:
            raise ValueError("本案例要求一个项目且不重试：" + case_id)
        output[case_id] = tests[0]["results"][0]["status"]
    for child in suite.get("suites", []):
        collect_cases(child, output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared-project", type=Path,
                        help="本次隔离工作副本，已安装依赖；省略则复制样本并 npm ci")
    parser.add_argument("--install-browser", action="store_true")
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    repo = base.parent.parent
    fixture = base / "fixtures/http-ui"
    if args.prepared_project:
        project = args.prepared_project.resolve()
        if not project.is_relative_to(repo / ".dev-flow"):
            raise ValueError("预准备副本必须位于本仓库忽略的 .dev-flow 范围")
        run = project.parent
    else:
        (repo / ".dev-flow").mkdir(exist_ok=True)
        run = Path(tempfile.mkdtemp(prefix="acceptance-eval-", dir=repo / ".dev-flow"))
        project = run / "project"
        shutil.copytree(fixture, project)
    setup = []
    if not args.prepared_project:
        setup.append(command(["npm", "ci", "--ignore-scripts", "--no-audit", "--no-fund"], project))
    if args.install_browser:
        setup.append(command(["npx", "--no-install", "playwright", "install", "chromium", "--only-shell"], project, timeout=300))
    if any(item["exit_code"] != 0 for item in setup):
        raise RuntimeError(json.dumps(setup, ensure_ascii=False))
    expected_fixed = {case: "passed" for case in (
        "TC-API-01", "TC-API-02", "TC-API-03", "TC-E2E-01", "TC-UI-01", "TC-UI-02")}
    expected_broken = dict(expected_fixed)
    for case in ("TC-API-01", "TC-API-02", "TC-E2E-01", "TC-UI-01"):
        expected_broken[case] = "failed"
    phases = []
    for variant, expected in (("broken", expected_broken), ("fixed", expected_fixed)):
        phase = run / variant
        phase.mkdir(exist_ok=True)
        with socket.socket() as reservation:
            reservation.bind(("127.0.0.1", 0))
            port = reservation.getsockname()[1]
        data = phase / "items.json"
        data.write_text("[]\n")
        report_file = phase / "playwright-report.json"
        env = dict(os.environ, EVAL_VARIANT=variant, EVAL_PORT=str(port),
                   EVAL_DATA_FILE=str(data), EVAL_RESULT_FILE=str(report_file))
        execution = command(["npm", "run", "test", "--", "--output", str(phase / "artifacts")], project, env)
        if not report_file.is_file():
            raise RuntimeError(json.dumps(execution, ensure_ascii=False))
        report = json.loads(report_file.read_text())
        actual = {}
        for suite in report.get("suites", []):
            collect_cases(suite, actual)
        with socket.socket() as probe:
            probe.settimeout(1)
            closed = probe.connect_ex(("127.0.0.1", port)) != 0
        valid = (actual == expected and not report.get("errors") and closed
                 and execution["exit_code"] == (1 if variant == "broken" else 0))
        phases.append({"variant": variant, "port": port, "cases": actual,
                       "expected_cases": expected, "oracle_matched": valid,
                       "process_port_closed": closed, "command": execution,
                       "report": str(report_file), "data_file": str(data)})
    node = command(["node", "--version"], project)
    playwright = command(["npx", "--no-install", "playwright", "--version"], project)
    hashes = {str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(fixture.rglob("*")) if p.is_file()}
    browser = command(["node", "--input-type=module", "-e",
                       "import { chromium } from 'playwright'; const b = await chromium.launch({executablePath: process.env.EVAL_BROWSER_EXECUTABLE}); console.log(b.version()); await b.close();"], project)
    record = {"executed_at": datetime.now(timezone.utc).isoformat(), "operator": "主 Agent / 固定工具案例",
              "scope": "本地真实 HTTP + JSON 文件 + Chromium；UI 故障一例为明确 route mock",
              "run": str(run), "setup": setup, "node": node["stdout"].strip(),
              "playwright": playwright["stdout"].strip(), "browser_version": browser["stdout"].strip(),
              "browser_executable": os.environ.get("EVAL_BROWSER_EXECUTABLE", "Playwright 默认 Chromium"),
              "fixture_sha256": hashes,
              "phases": phases, "all_oracles_matched": all(p["oracle_matched"] for p in phases)}
    (run / "checks.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"run": str(run), "all_oracles_matched": record["all_oracles_matched"],
                      "phases": [{k: p[k] for k in ("variant", "cases", "oracle_matched", "process_port_closed")}
                                 for p in phases]}, ensure_ascii=False, indent=2))
    if not record["all_oracles_matched"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
