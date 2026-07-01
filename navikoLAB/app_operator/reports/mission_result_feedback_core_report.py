from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.task_planner import TaskPlanner
from navikoLAB.core.mission_capability_bridge import MissionCapabilityBridge
from navikoLAB.connectors.connector_dispatcher import ConnectorDispatcher
from navikoLAB.planner_feedback.mission_result_feedback_core import (
    build_mission_result_feedback,
)


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
WORKSPACE = ROOT / "navikoLAB" / "workspace"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    mission = {
        "mission_id": "phase14_mission_result_feedback_core",
        "purpose": "Phase14 Mission Result Feedback Core diagnostics",
    }

    planner = TaskPlanner(WORKSPACE)
    plan = planner.create_plan(mission["purpose"])

    bridge = MissionCapabilityBridge(WORKSPACE)
    bridge_result = bridge.attach_capability_result(mission)

    capability_result = bridge_result.get("capability_result", {})
    agent_result = bridge_result.get("agent_result", {})
    agents = agent_result.get("agents", []) if isinstance(agent_result, dict) else []

    agent_id = "unknown_feedback_test_agent"
    if agents:
        agent_id = agents[0].get("agent_id", agent_id)

    context = {
        "feedback_priority": capability_result.get("feedback_priority"),
        "experience_based_score": capability_result.get("experience_based_score"),
        "feedback_based_selection": capability_result.get("feedback_based_selection"),
        "task_type": "general",
        "mission_id": mission["mission_id"],
    }

    dispatcher = ConnectorDispatcher(WORKSPACE)
    dispatch_result = dispatcher.run(
        agent_id=agent_id,
        goal=mission["purpose"],
        context=context,
    )

    feedback = build_mission_result_feedback(
        mission=mission,
        plan=plan,
        dispatch_result=dispatch_result,
    )

    report = {
        "status": "completed",
        "phase": "Phase14-1 Mission Result Feedback Core Report",
        "mission_result_feedback_ready": feedback.get("learning_loop_ready"),
        "success_signal": feedback.get("success_signal"),
        "failure_signal": feedback.get("failure_signal"),
        "reflection_target": feedback.get("reflection_target"),
        "experience_target": feedback.get("experience_target"),
        "experience_based_score": feedback.get("experience_based_score"),
        "feedback_priority": feedback.get("feedback_priority"),
        "connector_feedback_connected": feedback.get("connector_feedback_connected"),
        "risk_count": feedback.get("risk_count"),
        "safe_to_continue": feedback.get("safe_to_continue"),
        "workspace_only": feedback.get("workspace_only"),
        "original_write": feedback.get("original_write"),
        "file_delete": feedback.get("file_delete"),
        "external_operation": feedback.get("external_operation"),
        "real_gui_operation": feedback.get("real_gui_operation"),
        "next_phase": "Phase14-2 Mission Result Reflection Adapter",
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"mission_result_feedback_core_report_{timestamp}.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Mission Result Feedback Core Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("MissionResultFeedbackReady:", report["mission_result_feedback_ready"])
    print("SuccessSignal:", report["success_signal"])
    print("FailureSignal:", report["failure_signal"])
    print("ReflectionTarget:", report["reflection_target"])
    print("ExperienceTarget:", report["experience_target"])
    print("ExperienceBasedScore:", report["experience_based_score"])
    print("FeedbackPriority:", report["feedback_priority"])
    print("ConnectorFeedbackConnected:", report["connector_feedback_connected"])
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