from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.task_planner import TaskPlanner
from navikoLAB.planner_feedback.feedback_based_selection_core import (
    build_feedback_selection_hints,
)


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
WORKSPACE = ROOT / "navikoLAB" / "workspace"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    planner = TaskPlanner(WORKSPACE)
    plan = planner.create_plan("Phase12 Feedback-Based Selection Core diagnostics")

    selection_hints = build_feedback_selection_hints(plan)

    report = {
        "status": "completed",
        "phase": "Phase12-1 Feedback-Based Selection Core Report",
        "feedback_selection_ready": selection_hints.get("feedback_selection_ready"),
        "experience_based_score": selection_hints.get("experience_based_score"),
        "high_confidence_selection": selection_hints.get("high_confidence_selection"),
        "preferred_rule_count": len(selection_hints.get("preferred_selection_rules", [])),
        "avoidance_rule_count": len(selection_hints.get("avoidance_rules", [])),
        "capability_router_hint_ready": bool(
            selection_hints.get("capability_router_hint")
        ),
        "connector_dispatcher_hint_ready": bool(
            selection_hints.get("connector_dispatcher_hint")
        ),
        "read_only": selection_hints.get("read_only"),
        "workspace_only": selection_hints.get("workspace_only"),
        "original_write": selection_hints.get("original_write"),
        "file_delete": selection_hints.get("file_delete"),
        "external_operation": selection_hints.get("external_operation"),
        "real_gui_operation": selection_hints.get("real_gui_operation"),
        "risk_count": selection_hints.get("risk_count"),
        "safe_to_continue": selection_hints.get("safe_to_continue"),
        "next_phase": "Phase12-2 CapabilityRouter Feedback Adapter",
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"feedback_based_selection_core_report_{timestamp}.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Feedback-Based Selection Core Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("FeedbackSelectionReady:", report["feedback_selection_ready"])
    print("ExperienceBasedScore:", report["experience_based_score"])
    print("HighConfidenceSelection:", report["high_confidence_selection"])
    print("PreferredRuleCount:", report["preferred_rule_count"])
    print("AvoidanceRuleCount:", report["avoidance_rule_count"])
    print("CapabilityRouterHintReady:", report["capability_router_hint_ready"])
    print("ConnectorDispatcherHintReady:", report["connector_dispatcher_hint_ready"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("ExternalOperation:", report["external_operation"])
    print("RealGUIOperation:", report["real_gui_operation"])
    print("次工程:", report["next_phase"])
    print("保存先:", report_path)


if __name__ == "__main__":
    main()