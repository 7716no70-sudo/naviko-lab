from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.planner_feedback.task_planner_feedback_integration import (
    build_feedback_enhanced_plan,
)


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    plan = build_feedback_enhanced_plan(
        mission="Phase11 TaskPlanner Feedback Integration diagnostics"
    )

    feedback = plan.get("planner_feedback", {})
    safety = plan.get("safety", {})

    report = {
        "status": "completed",
        "phase": "Phase11-3 TaskPlanner Feedback Integration Report",
        "task_planner_feedback_integrated": True,
        "planner_feedback_attached": plan.get("planner_feedback_attached"),
        "feedback_available": feedback.get("feedback_available"),
        "success_count": feedback.get("success_count"),
        "failure_count": feedback.get("failure_count"),
        "planner_recommendation_count": len(feedback.get("planner_recommendations", [])),
        "planner_hints_available": bool(feedback.get("planner_hints")),
        "step_count": len(plan.get("steps", [])),
        "read_only": safety.get("read_only"),
        "workspace_only": safety.get("workspace_only"),
        "original_write": safety.get("original_write"),
        "file_delete": safety.get("file_delete"),
        "risk_count": safety.get("risk_count"),
        "safe_to_continue": safety.get("safe_to_continue"),
        "next_phase": "Phase11-4 Existing TaskPlanner Minimal Patch Connection",
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"task_planner_feedback_integration_report_{timestamp}.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== TaskPlanner Feedback Integration Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("TaskPlannerFeedbackIntegrated:", report["task_planner_feedback_integrated"])
    print("PlannerFeedbackAttached:", report["planner_feedback_attached"])
    print("FeedbackAvailable:", report["feedback_available"])
    print("SuccessCount:", report["success_count"])
    print("FailureCount:", report["failure_count"])
    print("PlannerRecommendationCount:", report["planner_recommendation_count"])
    print("PlannerHintsAvailable:", report["planner_hints_available"])
    print("StepCount:", report["step_count"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("次工程:", report["next_phase"])
    print("保存先:", report_path)


if __name__ == "__main__":
    main()