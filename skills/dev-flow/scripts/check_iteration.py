#!/usr/bin/env python3
"""只读核验迭代索引中的 dev-flow-state；不证明记录真实性或拦截操作。"""

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys


ROUTES = {"undecided", "quick", "standard", "system", "incident", "exploration"}
KINDS = {"confirmation", "review", "check"}
STATUSES = {"pending", "passed", "failed", "blocked", "not_applicable"}
EVIDENCE_KINDS = {"prototype", "native-ui", "web-ui", "api", "service", "unit", "artifact", "other"}


class StateError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise StateError(message)


def string(value, label):
    require(isinstance(value, str) and bool(value.strip()), label + " 必须是非空字符串")


def strings(value, label, nonempty=False):
    require(isinstance(value, list), label + " 必须是列表")
    for item in value:
        string(item, label)
    require(len(value) == len(set(value)), label + " 有重复项")
    if nonempty:
        require(bool(value), label + " 不能为空")


def objects(value, label):
    require(isinstance(value, list), label + " 必须是列表")
    result = {}
    for item in value:
        require(isinstance(item, dict), label + " 的成员必须是对象")
        string(item.get("id"), label + ".id")
        require(item["id"] not in result, label + " 有重复 id：" + item["id"])
        result[item["id"]] = item
    return result


def timestamp(value):
    string(value, "completed_at")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise StateError("completed_at 需要 ISO 8601 时间") from exc
    require(result.utcoffset() is not None, "completed_at 需要时区")
    return result


def read_state(path):
    content = Path(path).read_text(encoding="utf-8")
    if Path(path).suffix == ".json":
        return json.loads(content)
    blocks = re.findall(r"^```dev-flow-state\s*\n(.*?)^```\s*$", content, re.M | re.S)
    require(len(blocks) == 1, "迭代索引必须恰有一个 dev-flow-state 代码块")
    return json.loads(blocks[0])


def validate(state):
    require(isinstance(state, dict), "状态必须是对象")
    require(type(state.get("schema_version")) is int and state["schema_version"] == 1,
            "只支持 schema_version: 1")
    string(state.get("candidate"), "candidate")
    scopes = objects(state.get("scopes"), "scopes")
    require(bool(scopes), "至少登记一个工作范围")
    artifacts = objects(state.get("artifacts"), "artifacts")
    gates = objects(state.get("gates"), "gates")
    cases = objects(state.get("cases"), "cases")
    for artifact in artifacts.values():
        string(artifact.get("version"), "artifact.version")
        string(artifact.get("path"), "artifact.path")
    for scope in scopes.values():
        require(isinstance(scope.get("route"), str) and scope["route"] in ROUTES, "未知 route：" + scope["id"])
        require(type(scope.get("implementation")) is bool, "scope.implementation 必须是布尔值")
        require(isinstance(scope.get("reason"), str), "scope.reason 必须是字符串")
        for field in ("before_implementation", "before_finish"):
            strings(scope.get(field), field)
            require(set(scope[field]) <= gates.keys(), field + " 引用了不存在的 gate")
        require(bool(scope["before_finish"]), "before_finish 至少明确一个完成检查")
    for gate in gates.values():
        require(isinstance(gate.get("kind"), str) and gate["kind"] in KINDS, "未知 gate.kind：" + gate["id"])
        require(isinstance(gate.get("status"), str) and gate["status"] in STATUSES, "未知 gate.status：" + gate["id"])
        string(gate.get("stage"), "gate.stage")
        require(isinstance(gate.get("inputs"), dict), "gate.inputs 必须是版本映射")
        require(set(gate["inputs"]) <= artifacts.keys(), "gate.inputs 引用了不存在的 artifact")
        for version in gate["inputs"].values():
            string(version, "gate.inputs.version")
        for field in ("required_coverage", "coverage", "after"):
            strings(gate.get(field), "gate." + field)
        require(set(gate["after"]) <= gates.keys(), "gate.after 引用了不存在的 gate")
        if gate.get("expects") is not None:
            require(isinstance(gate["expects"], list), "expects 必须是列表")
            for expected in gate["expects"]:
                require(isinstance(expected, dict), "expects 成员必须是对象")
                require(isinstance(expected.get("kind"), str) and expected["kind"] in EVIDENCE_KINDS, "未知证据 kind")
                strings(expected.get("observations"), "expects.observations", nonempty=True)
        if gate.get("evidence") is not None:
            require(isinstance(gate["evidence"], list), "evidence 必须是列表")
            for evidence in gate["evidence"]:
                require(isinstance(evidence, dict), "evidence 成员必须是对象")
                require(isinstance(evidence.get("kind"), str) and evidence["kind"] in EVIDENCE_KINDS, "未知证据 kind")
                string(evidence.get("path"), "evidence.path")
                strings(evidence.get("observations"), "evidence.observations", nonempty=True)
                require(isinstance(evidence.get("inputs"), dict), "evidence.inputs 必须是版本映射")
    for case in cases.values():
        require(isinstance(case.get("scope"), str) and case["scope"] in scopes, "case.scope 不存在")
        strings(case.get("required_checks"), "case.required_checks", nonempty=True)
        require(set(case["required_checks"]) <= gates.keys(), "case 引用了不存在的检查")
        require(all(gates[g]["kind"] == "check" for g in case["required_checks"]),
                "用户用例必须关联 check，不能用确认或 Review 代替实际验证")

    # 所有依赖均检查，包括目前未被选中的范围，防止循环递归或残留坏引用。
    seen, active = set(), set()

    def visit(gate_id):
        require(gate_id not in active, "gate.after 存在循环依赖：" + gate_id)
        if gate_id in seen:
            return
        active.add(gate_id)
        for dependency in gates[gate_id]["after"]:
            visit(dependency)
        active.remove(gate_id)
        seen.add(gate_id)

    for gate_id in gates:
        visit(gate_id)
    return scopes, artifacts, gates, cases


def inspect(state, root, selected=None):
    scopes, artifacts, gates, cases = validate(state)
    root = Path(root).resolve()
    selected = list(scopes) if selected is None else selected
    require(bool(selected) and set(selected) <= scopes.keys(), "所选 scope 不存在")
    def closure(ids):
        result = set(ids)
        for gate_id in ids:
            result.update(closure(gates[gate_id]["after"]))
        return result

    # 完成汇总依赖的实际检查也须绑定候选，不能藏在 summary 的 after 中复用旧结果。
    # 实施前设计/方案/用例 Review 则只绑定有效输入。
    direct_final = {g for s in scopes.values() for g in s["before_finish"]}
    direct_final.update(g for c in cases.values() for g in c["required_checks"])
    pre_gates = closure([g for s in scopes.values() for g in s["before_implementation"]])
    candidate_gates = (closure(list(direct_final)) - pre_gates) | direct_final
    cache = {}

    def exists(relative):
        if not isinstance(relative, str) or not relative.strip():
            return False
        file = (root / relative).resolve()
        return not Path(relative).is_absolute() and file.is_relative_to(root) and file.is_file()

    def problems(gate_id):
        if gate_id in cache:
            return cache[gate_id]
        gate = gates[gate_id]
        issues = []
        status = gate["status"]
        if status == "not_applicable":
            if not isinstance(gate.get("reason"), str) or not gate["reason"].strip():
                issues.append("不适用缺少裁剪依据")
            if not exists(gate.get("record")):
                issues.append("不适用缺少实际依据记录")
        elif status != "passed":
            issues.append("状态为 " + status)
        else:
            if not exists(gate.get("record")):
                issues.append("缺少实际记录文件")
            if not gate["inputs"]:
                issues.append("缺少被核验的输入版本")
            if not gate["required_coverage"]:
                issues.append("缺少预定核验范围")
            missing = sorted(set(gate["required_coverage"]) - set(gate["coverage"]))
            if missing:
                issues.append("覆盖不足：" + ", ".join(missing))
            for artifact_id, version in gate["inputs"].items():
                artifact = artifacts[artifact_id]
                if artifact["version"] != version:
                    issues.append("输入版本失效：" + artifact_id)
                if not exists(artifact["path"]):
                    issues.append("输入文件不存在：" + artifact_id)
            try:
                completed = timestamp(gate.get("completed_at"))
            except StateError as exc:
                issues.append(str(exc))
                completed = None
            for dependency in gate["after"]:
                if problems(dependency):
                    issues.append("前置未成立：" + dependency)
                elif gates[dependency]["status"] == "passed" and completed:
                    try:
                        if completed < timestamp(gates[dependency].get("completed_at")):
                            issues.append("执行早于前置完成：" + dependency)
                    except StateError:
                        issues.append("前置时间无效：" + dependency)
            if gate["kind"] == "confirmation":
                for field in ("source", "quote"):
                    if not isinstance(gate.get(field), str) or not gate[field].strip():
                        issues.append("确认缺少 " + field)
            elif gate["kind"] == "review":
                if not isinstance(gate.get("actor"), str) or not gate["actor"].strip():
                    issues.append("Review 缺少执行者")
                if not isinstance(gate.get("mode"), str) or gate["mode"] not in {"self", "independent", "delegated"}:
                    issues.append("Review 缺少实际执行方式")
                try:
                    strings(gate.get("checks"), "review.checks", nonempty=True)
                except StateError as exc:
                    issues.append(str(exc))
                findings = gate.get("findings")
                if not isinstance(findings, list):
                    issues.append("Review 缺少明确发现（零发现写 []）")
                else:
                    for finding in findings:
                        if (not isinstance(finding, dict) or not isinstance(finding.get("severity"), str)
                                or not isinstance(finding.get("status"), str) or finding["severity"] not in
                                {"blocking", "nonblocking"} or finding["status"] not in
                                {"open", "closed"} or not isinstance(finding.get("text"), str)
                                or not finding["text"].strip()):
                            issues.append("Review 发现格式无效")
                        elif finding["severity"] == "blocking" and finding["status"] != "closed":
                            issues.append("Review 尚有阻断发现")
            if gate_id in candidate_gates and gate["kind"] in {"review", "check"}:
                expected_candidate = state["candidate"]
                if gate.get("candidate") != expected_candidate:
                    reuse = gate.get("reuse", {})
                    if (not isinstance(reuse, dict) or not gate.get("candidate") or
                            reuse.get("from_candidate") != gate.get("candidate") or
                            reuse.get("to_candidate") != expected_candidate or
                            not isinstance(reuse.get("reason"), str) or not reuse["reason"].strip()
                            or not exists(reuse.get("record"))):
                        issues.append("未绑定当前候选或缺少结果复用依据")
            if gate["kind"] == "check":
                expects, evidence = gate.get("expects", []), gate.get("evidence", [])
                if not expects:
                    issues.append("检查缺少预定证据类型与观察项")
                valid = []
                for item in evidence:
                    if not exists(item["path"]):
                        issues.append("证据文件不存在：" + item["path"])
                    elif item["inputs"] != gate["inputs"]:
                        issues.append("证据输入版本不符：" + item["path"])
                    elif (gate_id in candidate_gates or gate.get("candidate")) and (
                            item.get("candidate") != gate.get("candidate")):
                        issues.append("证据候选不符：" + item["path"])
                    else:
                        valid.append(item)
                for expected in expects:
                    observed = {observation for item in valid if item["kind"] == expected["kind"]
                                for observation in item["observations"]}
                    missing = sorted(set(expected["observations"]) - observed)
                    if missing:
                        issues.append("缺少 " + expected["kind"] + " 证据：" + ", ".join(missing))
        cache[gate_id] = issues
        return issues

    results, case_results = {}, {}
    for scope_id in selected:
        scope = scopes[scope_id]
        pre_ids = scope["before_implementation"]
        finish_ids = list(dict.fromkeys(pre_ids + scope["before_finish"] +
                                       [g for c in cases.values() if c["scope"] == scope_id
                                        for g in c["required_checks"]]))
        route_issues = []
        if scope["route"] == "undecided" or not scope["reason"].strip():
            route_issues.append({"gate": "route", "reason": "先确定任务路径、范围与裁剪依据"})
        pre = route_issues + [{"gate": g, "reason": issue} for g in pre_ids for issue in problems(g)]
        finish = route_issues + [{"gate": g, "reason": issue} for g in finish_ids for issue in problems(g)]
        for case_id, case in cases.items():
            if case["scope"] != scope_id:
                continue
            incomplete = [g for g in case["required_checks"]
                          if gates[g]["status"] != "passed" or problems(g)]
            for g in incomplete:
                if gates[g]["status"] == "not_applicable":
                    finish.append({"gate": g, "reason": case_id + " 的必需检查不能标不适用"})
            case_results[case_id] = {
                "status": "failed" if any(gates[g]["status"] == "failed" for g in incomplete)
                else "incomplete" if incomplete else "passed", "incomplete_checks": incomplete}
        can_start = scope["implementation"] and not pre
        can_finish = not finish
        blockers = pre if scope["implementation"] and pre else finish
        results[scope_id] = {
            "can_start_implementation": can_start, "can_finish": can_finish,
            "blocking_items": finish,
            "current_stage": "ready_to_finish" if can_finish else
            gates[blockers[0]["gate"]]["stage"] if blockers[0]["gate"] in gates else "routing",
            "next_action": "核验目标成果并更新项目入口后结束" if can_finish else
            ("继续已授权实现/复验，补齐 " if can_start else "完成 ") +
            blockers[0]["gate"] + "：" + blockers[0]["reason"]}
    return {
        "schema_version": 1, "recorded_state_only": True, "candidate": state["candidate"],
        "selected_scopes": selected,
        "can_start_implementation": bool([s for s in selected if scopes[s]["implementation"]])
        and all(results[s]["can_start_implementation"] for s in selected if scopes[s]["implementation"]),
        "can_finish": all(r["can_finish"] for r in results.values()),
        "blocking_items": [{"scope": s, **item} for s, r in results.items() for item in r["blocking_items"]],
        "next_action": next((r["next_action"] for r in results.values() if not r["can_finish"]),
                            "核验目标成果并更新项目入口后结束"),
        "scopes": results, "cases": case_results}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("index", type=Path, help="迭代索引 Markdown；测试夹具也可为 JSON")
    parser.add_argument("--root", type=Path, required=True, help="业务项目根目录；路径均相对此处")
    parser.add_argument("--scope", action="append", help="只核验所选范围，可重复；默认核验全部")
    parser.add_argument("--phase", choices=("implementation", "finish"), default="finish")
    args = parser.parse_args(argv)
    try:
        result = inspect(read_state(args.index), args.root, args.scope)
    except (StateError, OSError, ValueError) as exc:
        print(json.dumps({"can_start_implementation": False, "can_finish": False,
                          "error": str(exc), "next_action": "修正状态格式或引用后重新核验"}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_start_implementation" if args.phase == "implementation" else "can_finish"] else 1


if __name__ == "__main__":
    sys.exit(main())
