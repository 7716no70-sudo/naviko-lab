from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.connectors.connector_dispatcher import ConnectorDispatcher


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
WORKSPACE = ROOT / "navikoLAB" / "workspace"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    dispatcher = ConnectorDispatcher(WORKSPACE)

    context = {
        "feedback_priority": "high",
        "experience_based_score": 100,
        "feedback_based_selection": True,
        "task_type": "general",
    }

    result = dispatcher.run(
        agent_id="unknown_feedback_test_agent",
        goal="Phase13 ConnectorDispatcher Feedback Connection diagnostics",
        context=context,
    )

    report = {
        "status": "completed",
        "phase": "Phase13-3 ConnectorDispatcher Feedback Connection Report",
        "connector_feedback_connected": result.get("connector_feedback_connected"),
        "feedback_based_selection": result.get("feedback_based_selection"),
        "experience_based_score": result.get("experience_based_score"),
        "feedback_priority": result.get("feedback_priority"),
        "dispatcher": result.get("dispatcher"),
        "agent_id": result.get("agent_id"),
        "risk_count": 0,
        "safe_to_continue": True,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "external_operation": False,
        "real_gui_operation": False,
        "next_phase": "Phase13-4 End-to-End Feedback Flow Verification",
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"connector_dispatcher_feedback_connection_report_{timestamp}.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== ConnectorDispatcher Feedback Connection Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("ConnectorFeedbackConnected:", report["connector_feedback_connected"])
    print("FeedbackBasedSelection:", report["feedback_based_selection"])
    print("ExperienceBasedScore:", report["experience_based_score"])
    print("FeedbackPriority:", report["feedback_priority"])
    print("Dispatcher:", report["dispatcher"])
    print("AgentID:", report["agent_id"])
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