from __future__ import annotations

from typing import Any, Dict

from navikoLAB.planner_feedback.planner_feedback_adapter import build_task_planner_feedback


def attach_feedback_to_plan(mission: str, plan: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """
    既存TaskPlannerのplanに PlannerFeedback を安全に付与する。
    既存planは破壊せず copy して返す。
    """

    base_plan: Dict[str, Any] = dict(plan or {})
    feedback = build_task_planner_feedback(mission=mission)

    base_plan["planner_feedback_attached"] = True
    base_plan["planner_feedback"] = {
        "feedback_available": feedback.get("feedback_available"),
        "success_count": feedback.get("success_count"),
        "failure_count": feedback.get("failure_count"),
        "planner_recommendations": feedback.get("planner_recommendations", []),
        "planner_hints": feedback.get("planner_hints", {}),
    }

    base_plan["safety"] = {
        "read_only": True,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": True,
    }

    return base_plan


def build_feedback_enhanced_plan(mission: str) -> Dict[str, Any]:
    """
    Phase11用の簡易Plan生成。
    後続Phaseで既存TaskPlanner本体へ接続する。
    """

    initial_plan = {
        "mission": mission,
        "phase": "Phase11-3 TaskPlanner Feedback Integration",
        "planning_mode": "experience_based_planning",
        "steps": [
            "Read mission",
            "Load planner feedback",
            "Use knowledge records",
            "Use reflection records",
            "Use experience records",
            "Improve planning hints",
            "Return enhanced plan",
        ],
    }

    return attach_feedback_to_plan(mission=mission, plan=initial_plan)