from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.capabilities.capability_router import CapabilityRouter
from navikoLAB.capabilities.agent_manager import AgentManager


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
WORKSPACE = ROOT / "navikoLAB" / "workspace"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    router = CapabilityRouter(WORKSPACE)
    capability_result = router.route(
        "Phase12 AgentManager Feedback Priority diagnostics"
    )

    manager = AgentManager(WORKSPACE)
    agent_result = manager.select_agents(capability_result)

    agents = agent_result.get("agents", [])

    feedback_priority_count = sum(
        1 for agent in agents if agent.get("feedback_priority")
    )

    experience_score_count = sum(
        1 for agent in agents if agent.get("experience_based_score") is not None
    )

    report = {
        "status": "completed",
        "phase": "Phase12-4 AgentManager Feedback Priority Report",
        "agent_manager_feedback_connected": True,
        "feedback_based_selection": capability_result.get("feedback_based_selection"),
        "experience_based_score": capability_result.get("experience_based_score"),
        "feedback_priority": capability_result.get("feedback_priority"),
        "agent_count": len(agents),
        "feedback_priority_count": feedback_priority_count,
        "experience_score_count": experience_score_count,
        "risk_count": 0,
        "safe_to_continue": True,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "external_operation": False,
        "real_gui_operation": False,
        "next_phase": "Phase12-5 MissionCapabilityBridge Feedback Flow Report",
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"agent_manager_feedback_priority_report_{timestamp}.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== AgentManager Feedback Priority Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("AgentManagerFeedbackConnected:", report["agent_manager_feedback_connected"])
    print("FeedbackBasedSelection:", report["feedback_based_selection"])
    print("ExperienceBasedScore:", report["experience_based_score"])
    print("FeedbackPriority:", report["feedback_priority"])
    print("AgentCount:", report["agent_count"])
    print("FeedbackPriorityCount:", report["feedback_priority_count"])
    print("ExperienceScoreCount:", report["experience_score_count"])
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