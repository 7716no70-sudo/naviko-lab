from __future__ import annotations

from typing import Any, Dict, List

from navikoLAB.planner_feedback.feedback_based_selection_core import (
    build_feedback_selection_hints,
)


def adapt_capability_selection_with_feedback(
    plan: Dict[str, Any],
    capabilities: List[str],
) -> Dict[str, Any]:
    """
    CapabilityRouter が使える形へ Feedback Selection Hint を変換する。
    既存Capabilityは削除せず、優先度情報のみ付与する。
    """

    selection_hints = build_feedback_selection_hints(plan)

    score = int(selection_hints.get("experience_based_score", 0) or 0)
    preferred_rules = selection_hints.get("preferred_selection_rules", [])

    priority = "low"
    if score >= 80:
        priority = "high"
    elif score >= 50:
        priority = "medium"

    adapted_capabilities = []

    for capability in capabilities:
        adapted_capabilities.append({
            "capability": capability,
            "feedback_priority": priority,
            "experience_based_score": score,
            "preferred_rules": preferred_rules,
            "selected_by_feedback": score >= 50,
        })

    return {
        "phase": "Phase12-2 CapabilityRouter Feedback Adapter",
        "capability_feedback_ready": True,
        "input_capability_count": len(capabilities),
        "adapted_capability_count": len(adapted_capabilities),
        "experience_based_score": score,
        "feedback_priority": priority,
        "adapted_capabilities": adapted_capabilities,
        "capability_router_hint": selection_hints.get("capability_router_hint", {}),
        "read_only": True,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "external_operation": False,
        "real_gui_operation": False,
        "risk_count": 0,
        "safe_to_continue": True,
    }