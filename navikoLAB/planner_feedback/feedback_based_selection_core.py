from __future__ import annotations

from typing import Any, Dict, List


def build_feedback_selection_hints(plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Experience-Based Planning の結果から、
    CapabilityRouter / ConnectorDispatcher が参照できる選択ヒントを生成する。
    読み取り専用・Workspace限定・Original書込み禁止。
    """

    feedback = plan.get("planner_feedback", {})
    hints = feedback.get("planner_hints", {})
    recommendations: List[str] = (
        feedback.get("recommendations", [])
        or feedback.get("planner_recommendations", [])
        or []
    )

    score = int(plan.get("experience_based_score", 0) or 0)

    preferred_selection_rules: List[str] = []
    avoidance_rules: List[str] = []

    if hints.get("use_knowledge_records"):
        preferred_selection_rules.append("prefer_capabilities_supported_by_knowledge")

    if hints.get("use_reflection_records"):
        preferred_selection_rules.append("prefer_capabilities_supported_by_reflection")

    if hints.get("use_experience_records"):
        preferred_selection_rules.append("prefer_capabilities_supported_by_experience")

    if hints.get("prefer_success_patterns"):
        preferred_selection_rules.append("prefer_successful_capability_connector_patterns")

    if hints.get("avoid_failure_patterns"):
        avoidance_rules.append("avoid_failed_capability_connector_patterns")

    selection_hints = {
        "phase": "Phase12-1 Feedback-Based Selection Core",
        "feedback_selection_ready": True,
        "experience_based_score": score,
        "high_confidence_selection": score >= 80,
        "medium_confidence_selection": 50 <= score < 80,
        "low_confidence_selection": score < 50,
        "recommendation_count": len(recommendations),
        "preferred_selection_rules": preferred_selection_rules,
        "avoidance_rules": avoidance_rules,
        "capability_router_hint": {
            "use_feedback": True,
            "prefer_success_patterns": hints.get("prefer_success_patterns", False),
            "use_experience_records": hints.get("use_experience_records", False),
        },
        "connector_dispatcher_hint": {
            "use_feedback": True,
            "avoid_failure_patterns": hints.get("avoid_failure_patterns", False),
            "prefer_success_patterns": hints.get("prefer_success_patterns", False),
        },
        "read_only": True,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "external_operation": False,
        "real_gui_operation": False,
        "risk_count": 0,
        "safe_to_continue": True,
    }

    return selection_hints