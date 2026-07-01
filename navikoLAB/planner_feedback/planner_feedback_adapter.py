from __future__ import annotations

from typing import Any, Dict, List

from navikoLAB.planner_feedback.planner_feedback_core import build_planner_feedback_context


def build_task_planner_feedback(mission: str = "") -> Dict[str, Any]:
    """
    PlannerFeedbackCore の情報を TaskPlanner が使いやすい形へ変換する。
    読み取り専用・Workspace限定・Original書込み禁止。
    """

    context = build_planner_feedback_context(mission=mission)

    planner_hints = context.get("planner_hints", {})

    recommendations: List[str] = []

    if planner_hints.get("use_knowledge_records"):
        recommendations.append("Use recent knowledge records for mission planning.")

    if planner_hints.get("use_reflection_records"):
        recommendations.append("Use recent reflection records to improve planning quality.")

    if planner_hints.get("use_experience_records"):
        recommendations.append("Use recent experience records to avoid repeating mistakes.")

    if planner_hints.get("prefer_success_patterns"):
        recommendations.append("Prefer patterns that previously produced success signals.")

    if planner_hints.get("avoid_failure_patterns"):
        recommendations.append("Avoid patterns related to previous failure signals.")

    adapted_feedback = {
        "phase": "Phase11-2 Planner Feedback Adapter",
        "mission": mission,
        "read_only": True,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": True,
        "feedback_available": True,
        "success_count": context.get("success_count", 0),
        "failure_count": context.get("failure_count", 0),
        "recent_knowledge_count": context.get("recent_knowledge_count", 0),
        "recent_reflection_count": context.get("recent_reflection_count", 0),
        "recent_experience_count": context.get("recent_experience_count", 0),
        "planner_recommendations": recommendations,
        "planner_hints": planner_hints,
    }

    return adapted_feedback