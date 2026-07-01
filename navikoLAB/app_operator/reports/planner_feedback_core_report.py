from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.planner_feedback.planner_feedback_core import build_planner_feedback_context


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    context = build_planner_feedback_context(
        mission="Phase11 Planner Feedback Core diagnostics"
    )

    report = {
        "status": "completed",
        "phase": "Phase11-1 Planner Feedback Core Report",
        "planner_feedback_ready": True,
        "read_only": context.get("read_only"),
        "workspace_only": context.get("workspace_only"),
        "original_write": context.get("original_write"),
        "file_delete": context.get("file_delete"),
        "risk_count": context.get("risk_count"),
        "safe_to_continue": context.get("safe_to_continue"),
        "knowledge_index_loaded": context.get("knowledge_index_loaded"),
        "reflection_experience_index_loaded": context.get("reflection_experience_index_loaded"),
        "recent_knowledge_count": context.get("recent_knowledge_count"),
        "recent_reflection_count": context.get("recent_reflection_count"),
        "recent_experience_count": context.get("recent_experience_count"),
        "success_count": context.get("success_count"),
        "failure_count": context.get("failure_count"),
        "planner_hints": context.get("planner_hints"),
        "next_phase": "Phase11-2 Planner Feedback Adapter / TaskPlanner Integration",
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"planner_feedback_core_report_{timestamp}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Planner Feedback Core Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("PlannerFeedbackReady:", report["planner_feedback_ready"])
    print("KnowledgeIndexLoaded:", report["knowledge_index_loaded"])
    print("ReflectionExperienceIndexLoaded:", report["reflection_experience_index_loaded"])
    print("RecentKnowledgeCount:", report["recent_knowledge_count"])
    print("RecentReflectionCount:", report["recent_reflection_count"])
    print("RecentExperienceCount:", report["recent_experience_count"])
    print("SuccessCount:", report["success_count"])
    print("FailureCount:", report["failure_count"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("次工程:", report["next_phase"])
    print("保存先:", report_path)


if __name__ == "__main__":
    main()