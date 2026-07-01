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
from navikoLAB.planner_feedback.mission_result_experience_adapter import (
    adapt_mission_feedback_to_experience,
)
from navikoLAB.planner_feedback.feedback_loop_workspace_save_adapter import (
    save_feedback_loop_records,
)


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
WORKSPACE = ROOT / "navikoLAB" / "workspace"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    mission = {
        "mission_id": "phase14_feedback_loop_workspace_save",
        "purpose": "Phase14 Feedback Loop Workspace Save Adapter diagnostics",
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

    reflection_candidate = adapt_mission_feedback_to_reflection(mission_feedback)
    experience_candidate = adapt_mission_feedback_to_experience(mission_feedback)

    save_result = save_feedback_loop_records(
        root_dir=WORKSPACE,
        reflection_candidate=reflection_candidate,
        experience_candidate=experience_candidate,
    )

    report = {
        "status": "completed",
        "phase": "Phase14-4 Feedback Loop Workspace Save Adapter Report",
        "feedback_loop_saved": save_result.get("feedback_loop_saved"),
        "reflection_saved": save_result.get("reflection_saved"),
        "experience_saved": save_result.get("experience_saved"),
        "reflection_path": save_result.get("reflection_path"),
        "experience_path": save_result.get("experience_path"),
        "workspace_only": save_result.get("workspace_only"),
        "original_write": save_result.get("original_write"),
        "file_delete": save_result.get("file_delete"),
        "external_operation": save_result.get("external_operation"),
        "real_gui_operation": save_result.get("real_gui_operation"),
        "risk_count": save_result.get("risk_count"),
        "safe_to_continue": save_result.get("safe_to_continue"),
        "next_phase": "Phase14-5 Feedback Loop Index Update",
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"feedback_loop_workspace_save_adapter_report_{timestamp}.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Feedback Loop Workspace Save Adapter Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("FeedbackLoopSaved:", report["feedback_loop_saved"])
    print("ReflectionSaved:", report["reflection_saved"])
    print("ExperienceSaved:", report["experience_saved"])
    print("ReflectionPath:", report["reflection_path"])
    print("ExperiencePath:", report["experience_path"])
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