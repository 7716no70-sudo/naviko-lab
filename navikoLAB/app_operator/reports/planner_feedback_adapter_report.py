from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.planner_feedback.planner_feedback_adapter import build_task_planner_feedback


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    feedback = build_task_planner_feedback(
        mission="Phase11 Planner Feedback Adapter diagnostics"
    )

    report = {
        "status": "completed",
        "phase": "Phase11-2 Planner Feedback Adapter Report",
        "adapter_ready": True,
        "feedback_available": feedback.get("feedback_available"),
        "read_only": feedback.get("read_only"),
        "workspace_only": feedback.get("workspace_only"),
        "original_write": feedback.get("original_write"),
        "file_delete": feedback.get("file_delete"),
        "risk_count": feedback.get("risk_count"),
        "safe_to_continue": feedback.get("safe_to_continue"),
        "success_count": feedback.get("success_count"),
        "failure_count": feedback.get("failure_count"),
        "recent_knowledge_count": feedback.get("recent_knowledge_count"),
        "recent_reflection_count": feedback.get("recent_reflection_count"),
        "recent_experience_count": feedback.get("recent_experience_count"),
        "planner_recommendation_count": len(feedback.get("planner_recommendations", [])),
        "planner_recommendations": feedback.get("planner_recommendations", []),
        "next_phase": "Phase11-3 TaskPlanner Feedback Integration",
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"planner_feedback_adapter_report_{timestamp}.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Planner Feedback Adapter Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("AdapterReady:", report["adapter_ready"])
    print("FeedbackAvailable:", report["feedback_available"])
    print("SuccessCount:", report["success_count"])
    print("FailureCount:", report["failure_count"])
    print("RecentKnowledgeCount:", report["recent_knowledge_count"])
    print("RecentReflectionCount:", report["recent_reflection_count"])
    print("RecentExperienceCount:", report["recent_experience_count"])
    print("PlannerRecommendationCount:", report["planner_recommendation_count"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("次工程:", report["next_phase"])
    print("保存先:", report_path)


if __name__ == "__main__":
    main()