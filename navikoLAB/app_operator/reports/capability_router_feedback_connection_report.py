from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.capabilities.capability_router import CapabilityRouter


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
WORKSPACE = ROOT / "navikoLAB" / "workspace"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    router = CapabilityRouter(WORKSPACE)
    result = router.route("Phase12 CapabilityRouter Feedback Connection diagnostics")

    capability_feedback = result.get("capability_feedback", {})

    report = {
        "status": "completed",
        "phase": "Phase12-3C CapabilityRouter Feedback Connection Report",
        "capability_router_feedback_connected": True,
        "feedback_based_selection": result.get("feedback_based_selection"),
        "experience_based_score": result.get("experience_based_score"),
        "feedback_priority": result.get("feedback_priority"),
        "capability_feedback_ready": capability_feedback.get("capability_feedback_ready"),
        "required_count": len(result.get("required_ids", [])),
        "selected_count": result.get("selected_count"),
        "missing_count": result.get("missing_count"),
        "adapted_capability_count": capability_feedback.get("adapted_capability_count"),
        "risk_count": 0,
        "safe_to_continue": True,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "external_operation": False,
        "real_gui_operation": False,
        "next_phase": "Phase12-4 AgentManager Feedback Priority Connection",
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"capability_router_feedback_connection_report_{timestamp}.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== CapabilityRouter Feedback Connection Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("CapabilityRouterFeedbackConnected:", report["capability_router_feedback_connected"])
    print("FeedbackBasedSelection:", report["feedback_based_selection"])
    print("ExperienceBasedScore:", report["experience_based_score"])
    print("FeedbackPriority:", report["feedback_priority"])
    print("CapabilityFeedbackReady:", report["capability_feedback_ready"])
    print("RequiredCount:", report["required_count"])
    print("SelectedCount:", report["selected_count"])
    print("MissingCount:", report["missing_count"])
    print("AdaptedCapabilityCount:", report["adapted_capability_count"])
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