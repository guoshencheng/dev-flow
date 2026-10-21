# 局部任务的状态格式示例

**合成示例，不是业务项目完成证据。** 在真实项目采用时恢复实际规格、授权、候选、Review 和检查；状态保存在选定的唯一 Progress/迭代索引权威，另一入口只作链接。示例的 path 相对本 examples 目录，实际项目均相对项目根目录。

本例将规格、简短计划/自查和结果合并在同一文件；不新增 UI、架构、人工计划审批或部署。它仅演示字段、读取与汇总，不演示完整新功能的必需前置。

示例规格/计划 v1：整理一份已有记录的文案，不改变行为；针对检查和源码交付合并核验。示例 Review：执行者为主 Agent，方式为自查；核对原预期、变更范围和定向验证，没有发现。示例实施摘要：快速路径只整理已有记录文案，定向检查后交付源码；示例用户答复为“同意按这个范围开始修改并验证交付”。这是假设的合成授权，不可登记为真实同意。示例结果：仅有合成的 example-check 观察，不能推导实际用户行为验证。

```dev-flow-state
{
  "schema_version": 1,
  "candidate": "EXAMPLE-C1",
  "scopes": [{
    "id": "local", "route": "quick", "implementation": true,
    "reason": "示例：既有预期内局部修改，合并简短计划和针对验证；不涉及新体验或部署",
    "before_implementation": ["plan-review", "implementation-authorize"], "before_finish": ["result-check"]
  }],
  "artifacts": [{"id": "local-spec", "path": "iteration-state.md", "version": "v1"}],
  "gates": [
    {
      "id": "plan-review", "kind": "review", "stage": "plan", "status": "passed",
      "inputs": {"local-spec": "v1"}, "required_coverage": ["RULE-local"], "coverage": ["RULE-local"],
      "after": [], "record": "iteration-state.md", "completed_at": "2026-10-12T10:00:00+08:00",
      "actor": "主 Agent（示例）", "mode": "self",
      "checks": ["原预期和局部影响核对", "针对验证及交付范围核对"], "findings": []
    },
    {
      "id": "implementation-authorize", "kind": "confirmation", "stage": "implementation-authorization",
      "status": "passed", "authorizes": ["local"],
      "inputs": {"local-spec": "v1"}, "required_coverage": ["RULE-local"], "coverage": ["RULE-local"],
      "after": ["plan-review"], "record": "iteration-state.md", "completed_at": "2026-10-12T10:30:00+08:00",
      "source": "合成示例用户消息", "quote": "同意按这个范围开始修改并验证交付"
    },
    {
      "id": "result-check", "kind": "check", "stage": "acceptance", "status": "passed",
      "inputs": {"local-spec": "v1"}, "required_coverage": ["TC-local"], "coverage": ["TC-local"],
      "after": ["implementation-authorize"], "record": "iteration-state.md", "completed_at": "2026-10-12T11:00:00+08:00",
      "candidate": "EXAMPLE-C1",
      "expects": [{"kind": "other", "observations": ["example-check"]}],
      "evidence": [{"kind": "other", "observations": ["example-check"], "path": "iteration-state.md",
                    "inputs": {"local-spec": "v1"}, "candidate": "EXAMPLE-C1"}]
    }
  ],
  "cases": [{"id": "TC-local", "scope": "local", "required_checks": ["result-check"]}]
}
```

当前源目录中可用 `python3 skills/dev-flow/scripts/check_iteration.py skills/dev-flow/assets/examples/iteration-state.md --root skills/dev-flow/assets/examples` 演示解析。返回记录成立只代表示例一致，绝不代表专业行为通过。
