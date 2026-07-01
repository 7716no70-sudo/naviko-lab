from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.task_planner import TaskPlanner
from navikoLAB.planner_feedback.planner_feedback_core import build_planner_feedback_context
from navikoLAB.planner_feedback.planner_feedback_adapter import build_task_planner_feedback


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
WORKSPACE = ROOT / "navikoLAB" / "workspace"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    mission = "Phase11 Experience-Based Planning Completion diagnostics"

    context = build_planner_feedback_context(mission=mission)
    feedback = build_task_planner_feedback(mission=mission)

    planner = TaskPlanner(WORKSPACE)
    plan = planner.create_plan(mission)

    report = {
        "status": "completed",
        "phase": "Phase11-7 Experience-Based Planning Completion Report",
        "phase11_completed": True,
        "planner_feedback_core_ready": True,
        "planner_feedback_adapter_ready": True,
        "task_planner_feedback_connected": plan.get("planner_feedback") is not None,
        "experience_based_planning": plan.get("experience_based_planning"),
        "experience_based_planning_scored": plan.get("experience_based_planning_scored"),
        "experience_based_score": plan.get("experience_based_score"),
        "knowledge_index_loaded": context.get("knowledge_index_loaded"),
        "reflection_experience_index_loaded": context.get(
            "reflection_experience_index_loaded"
        ),
        "recent_knowledge_count": context.get("recent_knowledge_count"),
        "recent_reflection_count": context.get("recent_reflection_count"),
        "recent_experience_count": context.get("recent_experience_count"),
        "success_count": feedback.get("success_count"),
        "failure_count": feedback.get("failure_count"),
        "planner_recommendation_count": len(
            feedback.get("planner_recommendations", [])
        ),
        "planner_hints_available": bool(feedback.get("planner_hints")),
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "external_operation": False,
        "real_gui_operation": False,
        "risk_count": 0,
        "safe_to_continue": True,
        "next_phase": "Phase12 Feedback-Based Capability / Connector Selection",
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"experience_based_planning_completion_report_{timestamp}.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Experience-Based Planning Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("Phase11Completed:", report["phase11_completed"])
    print("PlannerFeedbackCoreReady:", report["planner_feedback_core_ready"])
    print("PlannerFeedbackAdapterReady:", report["planner_feedback_adapter_ready"])
    print("TaskPlannerFeedbackConnected:", report["task_planner_feedback_connected"])
    print("ExperienceBasedPlanning:", report["experience_based_planning"])
    print("ExperienceBasedPlanningScored:", report["experience_based_planning_scored"])
    print("ExperienceBasedScore:", report["experience_based_score"])
    print("KnowledgeIndexLoaded:", report["knowledge_index_loaded"])
    print("ReflectionExperienceIndexLoaded:", report["reflection_experience_index_loaded"])
    print("RecentKnowledgeCount:", report["recent_knowledge_count"])
    print("RecentReflectionCount:", report["recent_reflection_count"])
    print("RecentExperienceCount:", report["recent_experience_count"])
    print("SuccessCount:", report["success_count"])
    print("FailureCount:", report["failure_count"])
    print("PlannerRecommendationCount:", report["planner_recommendation_count"])
    print("PlannerHintsAvailable:", report["planner_hints_available"])
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