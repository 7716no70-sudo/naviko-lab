from __future__ import annotations

from typing import Any, Dict


def adapt_mission_feedback_to_experience(
    mission_feedback: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Mission Result Feedback を Experience 用レコード候補へ変換する。
    書き込みは行わず、構造化データのみ返す。
    """

    return {
        "phase": "Phase14-3 Mission Result Experience Adapter",
        "experience_adapter_ready": True,
        "mission_id": mission_feedback.get("mission_id"),
        "purpose": mission_feedback.get("purpose"),
        "dispatch_status": mission_feedback.get("dispatch_status"),
        "success_signal": bool(mission_feedback.get("success_signal")),
        "failure_signal": bool(mission_feedback.get("failure_signal")),
        "experience_based_score": mission_feedback.get("experience_based_score"),
        "feedback_priority": mission_feedback.get("feedback_priority"),
        "feedback_based_selection": mission_feedback.get("feedback_based_selection"),
        "connector_feedback_connected": mission_feedback.get(
            "connector_feedback_connected"
        ),
        "agent_id": mission_feedback.get("agent_id"),
        "dispatcher": mission_feedback.get("dispatcher"),
        "experience_learning_target": True,
        "planner_feedback_candidate": True,
        "read_only": True,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "external_operation": False,
        "real_gui_operation": False,
        "risk_count": 0,
        "safe_to_continue": True,
    }