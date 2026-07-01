from __future__ import annotations

from typing import Any, Dict, List


def score_plan_with_experience(plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Planner Feedback を使って plan に経験ベースの評価を付与する。
    既存planは破壊せず copy して返す。
    """

    scored_plan = dict(plan)

    feedback = scored_plan.get("planner_feedback", {})
    recommendations: List[str] = feedback.get("recommendations", []) or feedback.get(
        "planner_recommendations",
        [],
    )
    hints = feedback.get("planner_hints", {})

    score = 0
    reasons: List[str] = []

    if hints.get("use_knowledge_records"):
        score += 25
        reasons.append("knowledge records available")

    if hints.get("use_reflection_records"):
        score += 25
        reasons.append("reflection records available")

    if hints.get("use_experience_records"):
        score += 25
        reasons.append("experience records available")

    if hints.get("prefer_success_patterns"):
        score += 25
        reasons.append("success patterns available")

    if hints.get("avoid_failure_patterns"):
        score -= 15
        reasons.append("failure patterns require avoidance")

    scored_plan["experience_based_score"] = max(0, min(score, 100))
    scored_plan["experience_based_reasons"] = reasons
    scored_plan["experience_based_recommendation_count"] = len(recommendations)
    scored_plan["experience_based_planning_scored"] = True

    return scored_plan