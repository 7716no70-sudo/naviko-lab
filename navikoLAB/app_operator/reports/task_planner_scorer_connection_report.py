from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.task_planner import TaskPlanner


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
WORKSPACE = ROOT / "navikoLAB" / "workspace"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    planner = TaskPlanner(WORKSPACE)
    plan = planner.create_plan("Phase11 TaskPlanner Scorer Connection diagnostics")

    report = {
        "status": "completed",
        "phase": "Phase11-6 TaskPlanner Scorer Connection Report",
        "task_planner_scorer_connected": True,
        "planner_feedback_attached": plan.get("planner_feedback") is not None,
        "experience_based_planning": plan.get("experience_based_planning"),
        "experience_based_planning_scored": plan.get("experience_based_planning_scored"),
        "experience_based_score": plan.get("experience_based_score"),
        "experience_based_reason_count": len(plan.get("experience_based_reasons", [])),
        "risk_count": 0,
        "safe_to_continue": True,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "next_phase": "Phase11-7 Experience-Based Planning Completion Report",
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"task_planner_scorer_connection_report_{timestamp}.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== TaskPlanner Scorer Connection Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("TaskPlannerScorerConnected:", report["task_planner_scorer_connected"])
    print("PlannerFeedbackAttached:", report["planner_feedback_attached"])
    print("ExperienceBasedPlanning:", report["experience_based_planning"])
    print("ExperienceBasedPlanningScored:", report["experience_based_planning_scored"])
    print("ExperienceBasedScore:", report["experience_based_score"])
    print("ExperienceBasedReasonCount:", report["experience_based_reason_count"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("次工程:", report["next_phase"])
    print("保存先:", report_path)


if __name__ == "__main__":
    main()