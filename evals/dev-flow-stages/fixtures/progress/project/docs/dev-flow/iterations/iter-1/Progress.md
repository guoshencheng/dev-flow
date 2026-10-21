# 全局进度（合成评测）

设计/计划及实施已完成；正式用例Review与验收当前待进行，交付、架构收尾未开始。唯一总体权威为本页。当前目标：核实候选后验收前置，下一步用例独立Review。

```dev-flow-state
{
  "schema_version": 1,
  "candidate": "C1",
  "scopes": [
    {
      "id": "rename",
      "route": "quick",
      "implementation": true,
      "reason": "按钮文案修改，已有行为和验收含义不变；局部渲染检查兼验源码交付",
      "before_implementation": [
        "plan-review",
        "implementation-authorize"
      ],
      "before_finish": [
        "result-check"
      ]
    },
    {
      "id": "mobile",
      "route": "standard",
      "implementation": true,
      "reason": "新增手机体验；实施前确认业务完成标准，完整候选后维护正式 TC",
      "before_implementation": [
        "design-preview",
        "design-confirm",
        "solution-review",
        "mobile-plan",
        "mobile-start"
      ],
      "before_finish": [
        "implementation-review",
        "cases-review",
        "reopen",
        "share",
        "delivery-check"
      ]
    }
  ],
  "artifacts": [
    {
      "id": "spec",
      "path": "index.md",
      "version": "v1"
    }
  ],
  "gates": [
    {
      "id": "plan-review",
      "kind": "review",
      "stage": "plan",
      "status": "passed",
      "inputs": {
        "spec": "v1"
      },
      "required_coverage": [
        "rename"
      ],
      "coverage": [
        "rename"
      ],
      "after": [],
      "record": "index.md",
      "completed_at": "2026-10-12T10:00:00+08:00",
      "actor": "主 Agent",
      "mode": "self",
      "checks": [
        "对照有效预期核对计划和回归范围"
      ],
      "findings": [],
      "review_scopes": [
        "rename"
      ]
    },
    {
      "id": "result-check",
      "kind": "check",
      "stage": "acceptance",
      "status": "passed",
      "inputs": {
        "spec": "v1"
      },
      "required_coverage": [
        "rename"
      ],
      "coverage": [
        "rename"
      ],
      "after": [],
      "record": "index.md",
      "completed_at": "2026-10-12T10:00:00+08:00",
      "candidate": "C1",
      "expects": [
        {
          "kind": "unit",
          "observations": [
            "rename"
          ]
        }
      ],
      "evidence": [
        {
          "kind": "unit",
          "observations": [
            "rename"
          ],
          "candidate": "C1",
          "inputs": {
            "spec": "v1"
          },
          "path": "evidence.txt"
        }
      ]
    },
    {
      "id": "implementation-authorize",
      "kind": "confirmation",
      "stage": "implementation-authorization",
      "status": "passed",
      "inputs": {
        "spec": "v1"
      },
      "required_coverage": [
        "rename"
      ],
      "coverage": [
        "rename"
      ],
      "after": [
        "plan-review"
      ],
      "record": "index.md",
      "completed_at": "2026-10-12T10:00:00+08:00",
      "source": "本会话用户消息",
      "quote": "同意按此范围开始修改并验证交付",
      "authorizes": [
        "rename"
      ]
    },
    {
      "id": "design-preview",
      "kind": "check",
      "stage": "design",
      "status": "passed",
      "inputs": {
        "spec": "v1"
      },
      "required_coverage": [
        "UI-phone"
      ],
      "coverage": [
        "UI-phone"
      ],
      "after": [],
      "record": "index.md",
      "completed_at": "2026-10-12T10:00:00+08:00",
      "expects": [
        {
          "kind": "prototype",
          "observations": [
            "UI-phone"
          ]
        }
      ],
      "evidence": [
        {
          "kind": "prototype",
          "observations": [
            "UI-phone"
          ],
          "inputs": {
            "spec": "v1"
          },
          "path": "evidence.txt"
        }
      ]
    },
    {
      "id": "design-confirm",
      "kind": "confirmation",
      "stage": "design",
      "status": "passed",
      "inputs": {
        "spec": "v1"
      },
      "required_coverage": [
        "RULE-mobile",
        "UI-phone",
        "AC-mobile"
      ],
      "coverage": [
        "RULE-mobile",
        "UI-phone",
        "AC-mobile"
      ],
      "after": [
        "design-preview"
      ],
      "record": "index.md",
      "completed_at": "2026-10-12T10:00:00+08:00",
      "source": "本会话用户消息",
      "quote": "同意此版本的场景和结果"
    },
    {
      "id": "solution-review",
      "kind": "review",
      "stage": "solution",
      "status": "passed",
      "inputs": {
        "spec": "v1"
      },
      "required_coverage": [
        "RULE-mobile",
        "UI-phone",
        "OUT-mobile"
      ],
      "coverage": [
        "RULE-mobile",
        "UI-phone",
        "OUT-mobile"
      ],
      "after": [
        "design-confirm"
      ],
      "record": "index.md",
      "completed_at": "2026-10-12T10:00:00+08:00",
      "actor": "独立架构执行者",
      "mode": "independent",
      "checks": [
        "产品：原规格与结果双向覆盖",
        "UI：手机入口与恢复状态",
        "架构：沿用桌面契约"
      ],
      "findings": [],
      "review_scopes": [
        "mobile"
      ]
    },
    {
      "id": "mobile-plan",
      "kind": "review",
      "stage": "plan",
      "status": "passed",
      "inputs": {
        "spec": "v1"
      },
      "required_coverage": [
        "AC-mobile",
        "OUT-mobile"
      ],
      "coverage": [
        "AC-mobile",
        "OUT-mobile"
      ],
      "after": [
        "solution-review"
      ],
      "record": "index.md",
      "completed_at": "2026-10-12T10:00:00+08:00",
      "actor": "独立架构执行者",
      "mode": "independent",
      "checks": [
        "对照有效预期核对计划和回归范围"
      ],
      "findings": [],
      "review_scopes": [
        "mobile"
      ]
    },
    {
      "id": "mobile-start",
      "kind": "confirmation",
      "stage": "implementation-authorization",
      "status": "passed",
      "inputs": {
        "spec": "v1"
      },
      "required_coverage": [
        "mobile"
      ],
      "coverage": [
        "mobile"
      ],
      "after": [
        "mobile-plan"
      ],
      "record": "index.md",
      "completed_at": "2026-10-12T10:00:00+08:00",
      "source": "本会话用户消息",
      "quote": "同意按已确认标准开始手机实现",
      "authorizes": [
        "mobile"
      ]
    },
    {
      "id": "implementation-review",
      "kind": "review",
      "stage": "implementation",
      "status": "pending",
      "inputs": {
        "spec": "v1"
      },
      "required_coverage": [
        "OUT-mobile"
      ],
      "coverage": [
        "OUT-mobile"
      ],
      "after": [
        "mobile-start"
      ],
      "record": "index.md",
      "actor": "独立架构执行者",
      "mode": "independent",
      "checks": [
        "对照有效预期核对计划和回归范围"
      ],
      "findings": [],
      "candidate": "C1",
      "review_scopes": [
        "mobile"
      ]
    },
    {
      "id": "cases-review",
      "kind": "review",
      "stage": "cases",
      "status": "pending",
      "inputs": {
        "spec": "v1"
      },
      "required_coverage": [
        "AC-mobile",
        "TC-mobile"
      ],
      "coverage": [
        "AC-mobile",
        "TC-mobile"
      ],
      "after": [
        "implementation-review"
      ],
      "record": "index.md",
      "actor": "独立验收执行者",
      "mode": "independent",
      "checks": [
        "对照实施前确认的完成标准",
        "覆盖及交付证据可执行性"
      ],
      "findings": [],
      "candidate": "C1",
      "review_scopes": [
        "mobile"
      ]
    },
    {
      "id": "reopen",
      "kind": "check",
      "stage": "acceptance",
      "status": "passed",
      "inputs": {
        "spec": "v1"
      },
      "required_coverage": [
        "TC-mobile"
      ],
      "coverage": [
        "TC-mobile"
      ],
      "after": [
        "cases-review"
      ],
      "record": "index.md",
      "completed_at": "2026-10-12T10:00:00+08:00",
      "candidate": "C1",
      "expects": [
        {
          "kind": "native-ui",
          "observations": [
            "app-reopen"
          ]
        }
      ],
      "evidence": [
        {
          "kind": "native-ui",
          "observations": [
            "app-reopen"
          ],
          "candidate": "C1",
          "inputs": {
            "spec": "v1"
          },
          "path": "evidence.txt"
        }
      ]
    },
    {
      "id": "share",
      "kind": "check",
      "stage": "acceptance",
      "status": "passed",
      "inputs": {
        "spec": "v1"
      },
      "required_coverage": [
        "TC-mobile"
      ],
      "coverage": [
        "TC-mobile"
      ],
      "after": [
        "cases-review"
      ],
      "record": "index.md",
      "completed_at": "2026-10-12T10:00:00+08:00",
      "candidate": "C1",
      "expects": [
        {
          "kind": "native-ui",
          "observations": [
            "system-share"
          ]
        }
      ],
      "evidence": [
        {
          "kind": "native-ui",
          "observations": [
            "system-share"
          ],
          "candidate": "C1",
          "inputs": {
            "spec": "v1"
          },
          "path": "evidence.txt"
        }
      ]
    },
    {
      "id": "delivery-check",
      "kind": "check",
      "stage": "delivery",
      "status": "passed",
      "inputs": {
        "spec": "v1"
      },
      "required_coverage": [
        "TC-mobile"
      ],
      "coverage": [
        "TC-mobile"
      ],
      "after": [
        "cases-review"
      ],
      "record": "index.md",
      "completed_at": "2026-10-12T10:00:00+08:00",
      "candidate": "C1",
      "expects": [
        {
          "kind": "artifact",
          "observations": [
            "launch-and-core-task"
          ]
        }
      ],
      "evidence": [
        {
          "kind": "artifact",
          "observations": [
            "launch-and-core-task"
          ],
          "candidate": "C1",
          "inputs": {
            "spec": "v1"
          },
          "path": "evidence.txt"
        }
      ]
    }
  ],
  "cases": [
    {
      "id": "TC-rename",
      "scope": "rename",
      "required_checks": [
        "result-check"
      ]
    },
    {
      "id": "TC-mobile",
      "scope": "mobile",
      "required_checks": [
        "reopen",
        "share",
        "delivery-check"
      ]
    }
  ]
}
```
