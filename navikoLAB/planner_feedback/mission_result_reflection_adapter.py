from __future__ import annotations

from typing import Any, Dict


def adapt_mission_feedback_to_reflection(
    mission_feedback: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Mission Result Feedback を Reflection 用レコード候補へ変換する。
    書き込みは行わず、構造化データのみ返す。
    """

    success_signal = bool(mission_feedback.get("success_signal"))
    failure_signal = bool(mission_feedback.get("failure_signal"))

    reflection_summary = "Mission completed with neutral result."

    if success_signal:
        reflection_summary = "Mission result indicates a success pattern."
    elif failure_signal:
        reflection_summary = "Mission result indicates a failure pattern."

    return {
        "phase": "Phase14-2 Mission Result Reflection Adapter",
        "reflection_adapter_ready": True,
        "mission_id": mission_feedback.get("mission_id"),
        "purpose": mission_feedback.get("purpose"),
        "reflection_summary": reflection_summary,
        "success_signal": success_signal,
        "failure_signal": failure_signal,
        "experience_based_score": mission_feedback.get("experience_based_score"),
        "feedback_priority": mission_feedback.get("feedback_priority"),
        "feedback_based_selection": mission_feedback.get("feedback_based_selection"),
        "connector_feedback_connected": mission_feedback.get(
            "connector_feedback_connected"
        ),
        "reflection_learning_target": True,
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