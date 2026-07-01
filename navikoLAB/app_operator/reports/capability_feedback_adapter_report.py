from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.task_planner import TaskPlanner
from navikoLAB.planner_feedback.capability_feedback_adapter import (
    adapt_capability_selection_with_feedback,
)


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
WORKSPACE = ROOT / "navikoLAB" / "workspace"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    mission = "Phase12 CapabilityRouter Feedback Adapter diagnostics"

    planner = TaskPlanner(WORKSPACE)
    plan = planner.create_plan(mission)

    capabilities = plan.get("capabilities", [])
    if not capabilities:
        capabilities = ["text_ai", "app", "browser"]

    adapted = adapt_capability_selection_with_feedback(plan, capabilities)

    report = {
        "status": "completed",
        "phase": "Phase12-2 CapabilityRouter Feedback Adapter Report",
        "capability_feedback_ready": adapted.get("capability_feedback_ready"),
        "input_capability_count": adapted.get("input_capability_count"),
        "adapted_capability_count": adapted.get("adapted_capability_count"),
        "experience_based_score": adapted.get("experience_based_score"),
        "feedback_priority": adapted.get("feedback_priority"),
        "capability_router_hint_ready": bool(adapted.get("capability_router_hint")),
        "read_only": adapted.get("read_only"),
        "workspace_only": adapted.get("workspace_only"),
        "original_write": adapted.get("original_write"),
        "file_delete": adapted.get("file_delete"),
        "external_operation": adapted.get("external_operation"),
        "real_gui_operation": adapted.get("real_gui_operation"),
        "risk_count": adapted.get("risk_count"),
        "safe_to_continue": adapted.get("safe_to_continue"),
        "next_phase": "Phase12-3 CapabilityRouter Minimal Patch Connection",
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"capability_feedback_adapter_report_{timestamp}.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Capability Feedback Adapter Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("CapabilityFeedbackReady:", report["capability_feedback_ready"])
    print("InputCapabilityCount:", report["input_capability_count"])
    print("AdaptedCapabilityCount:", report["adapted_capability_count"])
    print("ExperienceBasedScore:", report["experience_based_score"])
    print("FeedbackPriority:", report["feedback_priority"])
    print("CapabilityRouterHintReady:", report["capability_router_hint_ready"])
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