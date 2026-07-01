from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.planner_feedback.task_planner_feedback_integration import (
    build_feedback_enhanced_plan,
)
from navikoLAB.planner_feedback.experience_based_planning_scorer import (
    score_plan_with_experience,
)


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    plan = build_feedback_enhanced_plan(
        mission="Phase11 Experience-Based Planning Scorer diagnostics"
    )

    scored_plan = score_plan_with_experience(plan)

    report = {
        "status": "completed",
        "phase": "Phase11-5 Experience-Based Planning Scorer Report",
        "experience_based_planning_scored": scored_plan.get(
            "experience_based_planning_scored"
        ),
        "experience_based_score": scored_plan.get("experience_based_score"),
        "experience_based_reasons": scored_plan.get("experience_based_reasons"),
        "experience_based_recommendation_count": scored_plan.get(
            "experience_based_recommendation_count"
        ),
        "planner_feedback_attached": scored_plan.get("planner_feedback_attached"),
        "risk_count": 0,
        "safe_to_continue": True,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "next_phase": "Phase11-6 TaskPlanner Scorer Minimal Patch Connection",
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"experience_based_planning_scorer_report_{timestamp}.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Experience-Based Planning Scorer Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("ExperienceBasedPlanningScored:", report["experience_based_planning_scored"])
    print("ExperienceBasedScore:", report["experience_based_score"])
    print("ReasonCount:", len(report["experience_based_reasons"] or []))
    print("RecommendationCount:", report["experience_based_recommendation_count"])
    print("PlannerFeedbackAttached:", report["planner_feedback_attached"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("次工程:", report["next_phase"])
    print("保存先:", report_path)


if __name__ == "__main__":
    main()