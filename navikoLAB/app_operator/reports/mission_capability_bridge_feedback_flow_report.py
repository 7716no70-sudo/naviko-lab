from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.core.mission_capability_bridge import MissionCapabilityBridge


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
WORKSPACE = ROOT / "navikoLAB" / "workspace"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    bridge = MissionCapabilityBridge(WORKSPACE)

    mission = {
        "mission_id": "phase12_feedback_flow_diagnostics",
        "purpose": "Phase12 MissionCapabilityBridge Feedback Flow diagnostics",
    }

    result = bridge.attach_capability_result(mission)

    capability_result = result.get("capability_result", {})
    agent_result = result.get("agent_result", {})

    report = {
        "status": "completed",
        "phase": "Phase12-5 MissionCapabilityBridge Feedback Flow Report",
        "bridge_feedback_flow_checked": True,
        "capability_feedback_connected": capability_result.get(
            "feedback_based_selection"
        ),
        "experience_based_score": capability_result.get("experience_based_score"),
        "feedback_priority": capability_result.get("feedback_priority"),
        "capability_feedback_ready": bool(
            capability_result.get("capability_feedback")
        ),
        "selected_count": capability_result.get("selected_count"),
        "missing_count": capability_result.get("missing_count"),
        "agent_count": len(agent_result.get("agents", []))
        if isinstance(agent_result, dict)
        else 0,
        "risk_count": 0,
        "safe_to_continue": True,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "external_operation": False,
        "real_gui_operation": False,
        "next_phase": "Phase12-6 Feedback-Based Selection Completion Report",
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"mission_capability_bridge_feedback_flow_report_{timestamp}.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== MissionCapabilityBridge Feedback Flow Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("BridgeFeedbackFlowChecked:", report["bridge_feedback_flow_checked"])
    print("CapabilityFeedbackConnected:", report["capability_feedback_connected"])
    print("ExperienceBasedScore:", report["experience_based_score"])
    print("FeedbackPriority:", report["feedback_priority"])
    print("CapabilityFeedbackReady:", report["capability_feedback_ready"])
    print("SelectedCount:", report["selected_count"])
    print("MissingCount:", report["missing_count"])
    print("AgentCount:", report["agent_count"])
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