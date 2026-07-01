from __future__ import annotations

from typing import Any, Dict


def build_mission_result_feedback(
    mission: Dict[str, Any],
    plan: Dict[str, Any],
    dispatch_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Mission実行結果を Reflection / Experience に戻すための
    安全なFeedback Recordを生成する。
    書き込みは行わず、構造化データのみ返す。
    """

    status = dispatch_result.get("status", "unknown")

    success_signal = status in {
        "completed",
        "success",
        "dry_run",
        "safe_skipped",
        "mock_completed",
    }

    failure_signal = status in {
        "failed",
        "error",
        "blocked",
    }

    feedback = {
        "phase": "Phase14-1 Mission Result Feedback Core",
        "mission_id": mission.get("mission_id"),
        "purpose": mission.get("purpose"),
        "dispatch_status": status,
        "success_signal": success_signal,
        "failure_signal": failure_signal,
        "planner_feedback_attached": plan.get("planner_feedback") is not None,
        "experience_based_score": plan.get("experience_based_score"),
        "feedback_priority": dispatch_result.get("feedback_priority"),
        "feedback_based_selection": dispatch_result.get("feedback_based_selection"),
        "connector_feedback_connected": dispatch_result.get(
            "connector_feedback_connected"
        ),
        "agent_id": dispatch_result.get("agent_id"),
        "dispatcher": dispatch_result.get("dispatcher"),
        "learning_loop_ready": True,
        "reflection_target": True,
        "experience_target": True,
        "read_only": True,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "external_operation": False,
        "real_gui_operation": False,
        "risk_count": 0,
        "safe_to_continue": True,
    }

    return feedback