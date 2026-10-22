"""阶段核验契约测试；合成记录不代表新上下文 Agent 行为或业务验收通过。"""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/dev-flow/scripts/check_iteration.py"
spec = importlib.util.spec_from_file_location("iteration_checks", SCRIPT)
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)


def gate(gate_id, kind, coverage, **extra):
    result = {"id": gate_id, "kind": kind, "stage": "plan", "status": "passed",
              "inputs": {"spec": "v1"}, "required_coverage": coverage, "coverage": coverage.copy(),
              "after": [], "record": "index.md", "completed_at": "2026-10-12T10:00:00+08:00"}
    if kind == "review":
        result.update(actor="主 Agent", mode="self", checks=["对照有效预期核对计划和回归范围"], findings=[])
    elif kind == "confirmation":
        result.update(source="本会话用户消息", quote="同意此版本的场景和结果")
    else:
        result.update(stage="acceptance", candidate="C1",
                      expects=[{"kind": "unit", "observations": coverage.copy()}],
                      evidence=[{"kind": "unit", "observations": coverage.copy(), "candidate": "C1",
                                 "inputs": {"spec": "v1"}, "path": "evidence.txt"}])
    result.update(extra)
    return result


def quick_state():
    return {"schema_version": 1, "candidate": "C1",
            "scopes": [{"id": "rename", "route": "quick", "implementation": True,
                        "reason": "按钮文案修改，已有行为和验收含义不变；局部渲染检查兼验源码交付",
                        "before_implementation": ["plan-review", "implementation-authorize"],
                        "before_finish": ["result-check"]}],
            "artifacts": [{"id": "spec", "path": "index.md", "version": "v1"}],
            "gates": [gate("plan-review", "review", ["rename"], review_scopes=["rename"]),
                      gate("result-check", "check", ["rename"]),
                      gate("implementation-authorize", "confirmation", ["rename"],
                           stage="implementation-authorization", after=["plan-review"],
                           authorizes=["rename"], quote="同意按此范围开始修改并验证交付")],
            "cases": [{"id": "TC-rename", "scope": "rename", "required_checks": ["result-check"]}]}


def mixed_state():
    result = quick_state()
    result["scopes"].append({"id": "mobile", "route": "standard", "implementation": True,
                            "reason": "新增手机体验；实施前确认业务完成标准，完整候选后维护正式 TC",
                            "before_implementation": ["design-preview", "design-confirm", "solution-review",
                                                      "mobile-plan", "mobile-start"],
                            "before_finish": ["implementation-review", "cases-review", "reopen", "share",
                                              "delivery-check"]})
    preview = gate("design-preview", "check", ["UI-phone"])
    preview.pop("candidate")
    preview.update(stage="design", expects=[{"kind": "prototype", "observations": ["UI-phone"]}])
    preview["evidence"] = [{"kind": "prototype", "observations": ["UI-phone"],
                            "inputs": {"spec": "v1"}, "path": "evidence.txt"}]
    result["gates"].extend([
        preview,
        gate("design-confirm", "confirmation", ["RULE-mobile", "UI-phone", "AC-mobile"],
             stage="design", after=["design-preview"]),
        gate("solution-review", "review", ["RULE-mobile", "UI-phone", "OUT-mobile"],
             stage="solution", after=["design-confirm"], review_scopes=["mobile"],
             actor="独立架构执行者", mode="independent",
             checks=["产品：原规格与结果双向覆盖", "UI：手机入口与恢复状态", "架构：沿用桌面契约"]),
        gate("mobile-plan", "review", ["AC-mobile", "OUT-mobile"], after=["solution-review"],
             actor="独立架构执行者", mode="independent", review_scopes=["mobile"]),
        gate("mobile-start", "confirmation", ["mobile"], stage="implementation-authorization",
             after=["mobile-plan"], authorizes=["mobile"], quote="同意按已确认标准开始手机实现"),
        gate("implementation-review", "review", ["OUT-mobile"], stage="implementation",
             candidate="C1", after=["mobile-start"], actor="独立架构执行者", mode="independent",
             review_scopes=["mobile"]),
        gate("cases-review", "review", ["AC-mobile", "TC-mobile"], stage="cases", candidate="C1",
             after=["implementation-review"], actor="独立验收执行者", mode="independent",
             review_scopes=["mobile"],
             checks=["对照实施前确认的完成标准", "覆盖及交付证据可执行性"]),
        gate("reopen", "check", ["TC-mobile"], after=["cases-review"],
             expects=[{"kind": "native-ui", "observations": ["app-reopen"]}],
             evidence=[{"kind": "native-ui", "observations": ["app-reopen"], "candidate": "C1",
                        "inputs": {"spec": "v1"}, "path": "evidence.txt"}]),
        gate("share", "check", ["TC-mobile"], after=["cases-review"],
             expects=[{"kind": "native-ui", "observations": ["system-share"]}],
             evidence=[{"kind": "native-ui", "observations": ["system-share"], "candidate": "C1",
                        "inputs": {"spec": "v1"}, "path": "evidence.txt"}]),
        gate("delivery-check", "check", ["TC-mobile"], stage="delivery", after=["cases-review"],
             expects=[{"kind": "artifact", "observations": ["launch-and-core-task"]}],
             evidence=[{"kind": "artifact", "observations": ["launch-and-core-task"],
                        "candidate": "C1", "inputs": {"spec": "v1"}, "path": "evidence.txt"}])])
    result["cases"].append({"id": "TC-mobile", "scope": "mobile",
                            "required_checks": ["reopen", "share", "delivery-check"]})
    return result


class IterationChecksTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "index.md").write_text("测试夹具：合并规格、确认与 Review 记录。", encoding="utf-8")
        (self.root / "evidence.txt").write_text("合成证据文件，仅用于一致性测试。", encoding="utf-8")

    def inspect(self, state, selected=None):
        return checks.inspect(state, self.root, selected)

    def find(self, state, gate_id):
        return next(g for g in state["gates"] if g["id"] == gate_id)

    def reasons(self, result):
        return "\n".join(i["reason"] for i in result["blocking_items"])

    def test_implementation_routes_require_explicit_user_authorization(self):
        for route in ("quick", "standard", "system", "incident", "exploration"):
            with self.subTest(route=route):
                state = quick_state()
                state["scopes"][0]["route"] = route
                for item in state["gates"]:
                    item.pop("authorizes", None)
                result = self.inspect(state)
                self.assertFalse(result["can_start_implementation"])
                self.assertFalse(result["can_finish"])
                self.assertIn("实施授权", self.reasons(result))

    def test_design_confirmation_alone_does_not_authorize_implementation(self):
        state = quick_state()
        for item in state["gates"]:
            item.pop("authorizes", None)
        state["gates"].append(gate("design-only", "confirmation", ["rename"],
                                  quote="同意文案展示"))
        state["scopes"][0]["before_implementation"].append("design-only")
        self.assertFalse(self.inspect(state)["can_start_implementation"])

    def test_unlinked_authorization_does_not_allow_implementation(self):
        state = quick_state()
        state["scopes"][0]["before_implementation"] = ["plan-review"]
        state["gates"].append(gate("unlinked", "confirmation", ["rename"], authorizes=["rename"],
                                  quote="同意按此范围开始实现"))
        self.assertFalse(self.inspect(state)["can_start_implementation"])

    def test_authorization_cannot_be_marked_not_applicable(self):
        state = quick_state()
        state["gates"].append(gate("skip-authorization", "confirmation", ["rename"],
                                  authorizes=["rename"], status="not_applicable",
                                  reason="局部可逆修改", quote=""))
        state["scopes"][0]["before_implementation"] = ["plan-review", "skip-authorization"]
        self.assertFalse(self.inspect(state)["can_start_implementation"])

    def test_authorization_is_bound_to_each_scope(self):
        state = mixed_state()
        for item in state["gates"]:
            item.pop("authorizes", None)
        state["gates"].append(gate("rename-start", "confirmation", ["rename"],
                                  authorizes=["rename"], quote="只同意开始更名"))
        state["scopes"][0]["before_implementation"].append("rename-start")
        state["scopes"][1]["before_implementation"].append("rename-start")
        result = self.inspect(state)
        self.assertTrue(result["scopes"]["rename"]["can_start_implementation"])
        self.assertFalse(result["scopes"]["mobile"]["can_start_implementation"])
        self.assertTrue(self.inspect(state, ["rename"])["can_finish"])

    def test_only_user_confirmation_can_declare_known_authorized_scopes(self):
        for item in (gate("invalid", "review", ["rename"], authorizes=["rename"]),
                     gate("invalid", "confirmation", ["rename"], authorizes=["missing"]),
                     gate("invalid", "confirmation", ["rename"], authorizes="rename")):
            with self.subTest(item=item):
                state = quick_state()
                state["gates"].append(item)
                with self.assertRaises(checks.StateError):
                    self.inspect(state)

    def test_small_fix_self_review_combined_document_no_extra_approvals(self):
        result = self.inspect(quick_state())
        self.assertTrue(result["can_start_implementation"])
        self.assertTrue(result["can_finish"])
        self.assertEqual(result["cases"]["TC-rename"]["status"], "passed")

    def test_full_scope_and_combined_confirmation_are_allowed(self):
        result = self.inspect(mixed_state())
        self.assertTrue(result["can_finish"])
        self.assertEqual(len(result["scopes"]), 2)

    def test_standard_design_and_plan_self_review_block_implementation(self):
        for gate_id in ("solution-review", "mobile-plan"):
            with self.subTest(gate_id=gate_id):
                state = mixed_state()
                self.find(state, gate_id)["mode"] = "self"
                result = self.inspect(state)
                self.assertFalse(result["scopes"]["mobile"]["can_start_implementation"])
                self.assertIn("独立执行者", self.reasons(result))
                self.assertTrue(result["scopes"]["rename"]["can_finish"])

    def test_all_standard_professional_self_reviews_cannot_pass(self):
        state = mixed_state()
        for gate_id in ("solution-review", "mobile-plan", "cases-review", "implementation-review"):
            self.find(state, gate_id)["mode"] = "self"
        result = self.inspect(state)
        self.assertFalse(result["scopes"]["mobile"]["can_start_implementation"])
        self.assertFalse(result["scopes"]["mobile"]["can_finish"])
        self.assertTrue(result["scopes"]["rename"]["can_finish"])

    def test_standard_review_cannot_hide_in_authorization_dependency(self):
        state = mixed_state()
        mobile = state["scopes"][1]
        mobile["before_implementation"] = ["design-preview", "design-confirm", "mobile-start"]
        for gate_id in ("solution-review", "mobile-plan"):
            self.find(state, gate_id)["mode"] = "self"
        result = self.inspect(state)
        self.assertFalse(result["scopes"]["mobile"]["can_start_implementation"])
        self.assertFalse(result["scopes"]["mobile"]["can_finish"])
        self.assertIn("独立执行者", self.reasons(result))
        self.assertTrue(result["scopes"]["rename"]["can_finish"])

    def test_indirect_standard_review_cannot_claim_other_scope(self):
        state = mixed_state()
        state["scopes"][1]["before_implementation"] = ["design-preview", "design-confirm", "mobile-start"]
        self.find(state, "mobile-plan")["review_scopes"] = ["rename"]
        result = self.inspect(state)
        self.assertFalse(result["scopes"]["mobile"]["can_start_implementation"])
        self.assertIn("归属与标准/系统范围", self.reasons(result))

    def test_shared_authorization_requires_indirect_review_attribution(self):
        state = mixed_state()
        state["gates"].append(gate("combined-start", "confirmation", ["rename", "AC-mobile"],
                                   authorizes=["rename", "mobile"], after=["plan-review", "mobile-plan"],
                                   quote="同意更名与手机范围开始"))
        state["scopes"][1]["before_implementation"] = ["design-preview", "design-confirm", "combined-start"]
        self.find(state, "mobile-plan").pop("review_scopes")
        result = self.inspect(state)
        self.assertFalse(result["scopes"]["mobile"]["can_start_implementation"])
        self.assertIn("缺少 review_scopes", self.reasons(result))

    def test_standard_case_and_implementation_self_review_block_finish_only(self):
        for gate_id in ("cases-review", "implementation-review"):
            with self.subTest(gate_id=gate_id):
                state = mixed_state()
                self.find(state, gate_id)["mode"] = "self"
                result = self.inspect(state)
                self.assertTrue(result["scopes"]["mobile"]["can_start_implementation"])
                self.assertFalse(result["scopes"]["mobile"]["can_finish"])
                self.assertIn("独立执行者", self.reasons(result))

    def test_standard_direct_review_cannot_opt_out_of_independence(self):
        state = mixed_state()
        self.find(state, "mobile-plan").update(mode="self", requires_independent=False)
        self.assertFalse(self.inspect(state)["scopes"]["mobile"]["can_start_implementation"])

    def test_declared_independent_review_rejects_self_outside_standard(self):
        state = quick_state()
        self.find(state, "plan-review")["requires_independent"] = True
        self.assertFalse(self.inspect(state)["can_start_implementation"])
        self.find(state, "plan-review")["requires_independent"] = False
        self.assertTrue(self.inspect(state)["can_finish"])

    def test_standard_implementation_does_not_depend_on_formal_cases(self):
        state = mixed_state()
        self.find(state, "cases-review")["status"] = "pending"
        self.assertTrue(self.inspect(state)["can_start_implementation"])
        self.assertFalse(self.inspect(state)["can_finish"])

    def test_standard_scope_can_start_before_cases_but_cannot_finish_empty_cases(self):
        state = mixed_state()
        state["cases"] = [case for case in state["cases"] if case["scope"] != "mobile"]
        for gate_id in ("cases-review", "reopen", "share", "delivery-check"):
            self.find(state, gate_id)["status"] = "pending"
        result = self.inspect(state)
        self.assertTrue(result["can_start_implementation"])
        self.assertFalse(result["can_finish"])
        self.assertIn("空 cases", self.reasons(result))
        for gate_id in ("cases-review", "reopen", "share", "delivery-check"):
            self.find(state, gate_id)["status"] = "passed"
        state["cases"].append({"id": "TC-mobile", "scope": "mobile",
                               "required_checks": ["reopen", "share", "delivery-check"]})
        self.assertTrue(self.inspect(state)["can_finish"])

    def test_formal_case_review_and_delivery_are_finish_conditions(self):
        for gate_id in ("cases-review", "delivery-check"):
            with self.subTest(gate_id=gate_id):
                state = mixed_state()
                self.find(state, gate_id)["status"] = "pending"
                result = self.inspect(state)
                self.assertTrue(result["can_start_implementation"])
                self.assertFalse(result["can_finish"])

    def test_formal_case_review_is_bound_to_current_candidate(self):
        state = mixed_state()
        state["candidate"] = "C2"
        result = self.inspect(state)
        self.assertTrue(result["can_start_implementation"])
        self.assertFalse(result["can_finish"])
        self.assertIn("未绑定当前候选", self.reasons(result))

    def test_existing_confirmation_can_be_reused_without_new_user_reply(self):
        state = mixed_state()
        self.find(state, "design-preview")["completed_at"] = "2026-10-01T08:00:00+08:00"
        self.find(state, "design-confirm").update(completed_at="2026-10-01T09:00:00+08:00",
                                                 source="有效历史规格 v1 的用户确认")
        self.assertTrue(self.inspect(state)["can_start_implementation"])

    def test_authorization_can_be_reused_and_transitively_required(self):
        state = quick_state()
        authorization = self.find(state, "implementation-authorize")
        authorization.update(after=[], completed_at="2026-10-01T09:00:00+08:00",
                             source="已展示同一范围的历史实施同意")
        self.find(state, "plan-review")["after"] = ["implementation-authorize"]
        state["scopes"][0]["before_implementation"] = ["plan-review"]
        self.assertTrue(self.inspect(state)["can_start_implementation"])
        authorization["status"] = "pending"
        self.assertFalse(self.inspect(state)["can_start_implementation"])

    def test_authorization_input_change_requires_affected_confirmation(self):
        state = quick_state()
        state["artifacts"].append({"id": "scope-summary", "path": "index.md", "version": "v2"})
        self.find(state, "implementation-authorize")["inputs"] = {"scope-summary": "v1"}
        result = self.inspect(state)
        self.assertFalse(result["can_start_implementation"])
        self.assertIn("scope-summary", self.reasons(result))

    def test_one_reply_can_authorize_multiple_explicit_scopes(self):
        state = mixed_state()
        for item in state["gates"]:
            item.pop("authorizes", None)
        state["gates"].append(gate("combined-start", "confirmation", ["rename", "AC-mobile"],
                                  authorizes=["rename", "mobile"], after=["plan-review", "mobile-plan"],
                                  quote="同意更名和手机范围及预期，计划复核后开始"))
        for scope in state["scopes"]:
            scope["before_implementation"].append("combined-start")
        self.assertTrue(self.inspect(state)["can_start_implementation"])

    def test_narrow_layout_reply_does_not_confirm_rules_and_completion_standard(self):
        state = mixed_state()
        design = self.find(state, "design-confirm")
        design.update(coverage=["UI-phone"], quote="iPad 沿用 Mac；iPhone 按此布局")
        result = self.inspect(state)
        self.assertFalse(result["can_start_implementation"])
        self.assertIn("RULE-mobile", self.reasons(result))
        self.assertFalse(result["scopes"]["mobile"]["can_finish"])
        self.assertTrue(result["scopes"]["rename"]["can_start_implementation"])
        self.assertTrue(result["scopes"]["rename"]["can_finish"])
        self.assertTrue(self.inspect(state, ["rename"])["can_finish"])

    def test_prototype_produced_after_confirmation_invalidates_order(self):
        state = mixed_state()
        self.find(state, "design-preview")["completed_at"] = "2026-10-12T11:00:00+08:00"
        result = self.inspect(state)
        self.assertFalse(result["can_start_implementation"])
        self.assertIn("执行早于前置完成", self.reasons(result))

    def test_plan_review_before_design_confirmation_is_not_effective(self):
        state = mixed_state()
        self.find(state, "mobile-plan")["completed_at"] = "2026-10-12T09:00:00+08:00"
        self.assertFalse(self.inspect(state)["can_start_implementation"])

    def test_input_version_change_invalidates_previous_confirmation_and_reviews(self):
        state = mixed_state()
        state["artifacts"][0]["version"] = "v2"
        result = self.inspect(state)
        self.assertFalse(result["can_start_implementation"])
        self.assertFalse(result["can_finish"])
        self.assertIn("输入版本失效", self.reasons(result))

    def test_empty_review_and_open_blocking_findings_are_rejected(self):
        for mutate in (lambda g: g.pop("checks"),
                       lambda g: g.pop("findings"),
                       lambda g: g.update(findings=[{"severity": "blocking", "status": "open", "text": "漏掉拒绝场景"}])):
            with self.subTest(mutate=mutate):
                state = quick_state()
                mutate(state["gates"][0])
                self.assertFalse(self.inspect(state)["can_start_implementation"])

    def test_quote_and_confirmation_source_are_required(self):
        state = mixed_state()
        self.find(state, "design-confirm").pop("quote")
        self.assertIn("确认缺少 quote", self.reasons(self.inspect(state)))

    def test_service_save_load_is_not_app_reopen(self):
        state = mixed_state()
        self.find(state, "reopen")["evidence"][0].update(kind="service", observations=["save-load"])
        result = self.inspect(state)
        self.assertFalse(result["can_finish"])
        self.assertEqual(result["cases"]["TC-mobile"]["status"], "incomplete")
        self.assertIn("app-reopen", self.reasons(result))

    def test_export_coordinator_is_not_system_share(self):
        state = mixed_state()
        self.find(state, "share")["evidence"][0].update(kind="service", observations=["export-file"])
        self.assertFalse(self.inspect(state)["can_finish"])

    def test_html_preview_is_not_native_rendering(self):
        state = mixed_state()
        self.find(state, "reopen")["evidence"][0]["kind"] = "prototype"
        self.assertFalse(self.inspect(state)["can_finish"])

    def test_blocked_not_run_failed_and_na_required_checks_never_pass_case(self):
        for status in ("blocked", "pending", "failed", "not_applicable"):
            with self.subTest(status=status):
                state = mixed_state()
                self.find(state, "share").update(status=status, reason="缺少系统环境", record="index.md")
                result = self.inspect(state)
                self.assertFalse(result["can_finish"])
                self.assertNotEqual(result["cases"]["TC-mobile"]["status"], "passed")

    def test_old_candidate_and_mismatched_evidence_are_rejected(self):
        for mutate in (lambda s: s.update(candidate="C2"),
                       lambda s: s["gates"][1]["evidence"][0].update(candidate="C0"),
                       lambda s: s["gates"][1]["evidence"][0].update(inputs={"spec": "v0"})):
            with self.subTest(mutate=mutate):
                state = quick_state()
                mutate(state)
                self.assertFalse(self.inspect(state)["can_finish"])

    def test_finish_summary_cannot_hide_old_candidate_check_in_dependencies(self):
        state = quick_state()
        state["cases"] = []
        summary = gate("summary", "review", ["TC-rename"], stage="delivery", candidate="C1",
                       after=["result-check"])
        state["gates"].append(summary)
        state["scopes"][0]["before_finish"] = ["summary"]
        state["gates"][1]["candidate"] = "C0"
        state["gates"][1]["evidence"][0]["candidate"] = "C0"
        self.assertFalse(self.inspect(state)["can_finish"])

    def test_unaffected_candidate_result_can_be_reused_with_current_basis(self):
        state = quick_state()
        state["candidate"] = "C2"
        state["gates"][1]["reuse"] = {"from_candidate": "C1", "to_candidate": "C2",
                                      "reason": "仅无关模块变化；该检查输入、实现和环境未变", "record": "index.md"}
        self.assertTrue(self.inspect(state)["can_finish"])

    def test_na_stage_requires_reason_and_source_record(self):
        state = quick_state()
        state["gates"].append(gate("ui-design", "confirmation", ["UI"], status="not_applicable",
                                  reason="后端局部修复，无 UI 变化"))
        state["scopes"][0]["before_implementation"].append("ui-design")
        self.assertTrue(self.inspect(state)["can_start_implementation"])
        self.find(state, "ui-design").pop("reason")
        self.assertFalse(self.inspect(state)["can_start_implementation"])

    def test_missing_file_or_outside_project_is_not_evidence(self):
        for path in ("missing.txt", "../evidence.txt", str(self.root / "evidence.txt")):
            with self.subTest(path=path):
                state = quick_state()
                state["gates"][1]["evidence"][0]["path"] = path
                self.assertFalse(self.inspect(state)["can_finish"])

    def test_format_errors_fail_closed(self):
        for mutate in (lambda s: s.update(schema_version=2),
                       lambda s: s["gates"][0].update(kind=[]),
                       lambda s: s["gates"].append(copy.deepcopy(s["gates"][0])),
                       lambda s: s["scopes"][0]["before_finish"].append("missing"),
                       lambda s: s["gates"][0].update(after=["result-check"])
                       or s["gates"][1].update(after=["plan-review"]),
                       lambda s: s["cases"][0].update(required_checks=["plan-review"])):
            with self.subTest(mutate=mutate):
                state = quick_state()
                mutate(state)
                with self.assertRaises(checks.StateError):
                    self.inspect(state)

    def test_no_implementation_task_has_no_implementation_permission(self):
        state = quick_state()
        state["scopes"][0]["implementation"] = False
        state["scopes"][0]["before_implementation"] = ["plan-review"]
        self.find(state, "implementation-authorize")["status"] = "pending"
        result = self.inspect(state)
        self.assertFalse(result["can_start_implementation"])
        self.assertTrue(result["can_finish"])

    def test_markdown_reader_and_cli_exit_status_are_readonly(self):
        path = self.root / "index.md"
        content = "# 合并记录\n\n```dev-flow-state\n" + json.dumps(quick_state(), ensure_ascii=False) + "\n```\n"
        path.write_text(content, encoding="utf-8")
        result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--root", str(self.root)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["recorded_state_only"])
        self.assertEqual(path.read_text(encoding="utf-8"), content)
        state = quick_state()
        state["gates"][1]["status"] = "blocked"
        path.write_text("```dev-flow-state\n" + json.dumps(state) + "\n```\n", encoding="utf-8")
        result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--root", str(self.root)], capture_output=True)
        self.assertEqual(result.returncode, 1)
        path.write_text(content + content, encoding="utf-8")
        result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--root", str(self.root)], capture_output=True)
        self.assertEqual(result.returncode, 2)

    def test_progress_file_can_be_the_only_state_authority(self):
        path = self.root / "Progress.md"
        path.write_text("# 进度权威\n\n```dev-flow-state\n" +
                        json.dumps(mixed_state(), ensure_ascii=False) + "\n```\n", encoding="utf-8")
        (self.root / "index.md").write_text("[总体进度](Progress.md)\n", encoding="utf-8")
        result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--root", str(self.root)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["can_finish"])

    def test_repository_example_is_executable_and_template_stays_pending(self):
        example = ROOT / "skills/dev-flow/assets/examples/iteration-state.md"
        self.assertTrue(checks.inspect(checks.read_state(example), example.parent)["can_finish"])
        template = ROOT / "skills/dev-flow/assets/templates/progress.md"
        result = checks.inspect(checks.read_state(template), self.root)
        self.assertFalse(result["can_start_implementation"])
        self.assertFalse(result["can_finish"])
        index = ROOT / "skills/document-management/assets/templates/iteration-index.md"
        with self.assertRaises(checks.StateError):
            checks.read_state(index)


if __name__ == "__main__":
    unittest.main()
