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
from navikoLAB.planner_feedback.mission_result_reflection_adapter import (
    adapt_mission_feedback_to_reflection,
)


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
WORKSPACE = ROOT / "navikoLAB" / "workspace"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    mission = {
        "mission_id": "phase14_mission_result_reflection_adapter",
        "purpose": "Phase14 Mission Result Reflection Adapter diagnostics",
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

    mission_feedback = build_mission_result_feedback(
        mission=mission,
        plan=plan,
        dispatch_result=dispatch_result,
    )

    reflection_candidate = adapt_mission_feedback_to_reflection(
        mission_feedback
    )

    report = {
        "status": "completed",
        "phase": "Phase14-2 Mission Result Reflection Adapter Report",
        "reflection_adapter_ready": reflection_candidate.get(
            "reflection_adapter_ready"
        ),
        "reflection_learning_target": reflection_candidate.get(
            "reflection_learning_target"
        ),
        "planner_feedback_candidate": reflection_candidate.get(
            "planner_feedback_candidate"
        ),
        "success_signal": reflection_candidate.get("success_signal"),
        "failure_signal": reflection_candidate.get("failure_signal"),
        "experience_based_score": reflection_candidate.get("experience_based_score"),
        "feedback_priority": reflection_candidate.get("feedback_priority"),
        "connector_feedback_connected": reflection_candidate.get(
            "connector_feedback_connected"
        ),
        "risk_count": reflection_candidate.get("risk_count"),
        "safe_to_continue": reflection_candidate.get("safe_to_continue"),
        "workspace_only": reflection_candidate.get("workspace_only"),
        "original_write": reflection_candidate.get("original_write"),
        "file_delete": reflection_candidate.get("file_delete"),
        "external_operation": reflection_candidate.get("external_operation"),
        "real_gui_operation": reflection_candidate.get("real_gui_operation"),
        "next_phase": "Phase14-3 Mission Result Experience Adapter",
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"mission_result_reflection_adapter_report_{timestamp}.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Mission Result Reflection Adapter Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("ReflectionAdapterReady:", report["reflection_adapter_ready"])
    print("ReflectionLearningTarget:", report["reflection_learning_target"])
    print("PlannerFeedbackCandidate:", report["planner_feedback_candidate"])
    print("SuccessSignal:", report["success_signal"])
    print("FailureSignal:", report["failure_signal"])
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