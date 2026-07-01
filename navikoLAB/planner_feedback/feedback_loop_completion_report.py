from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "workspace" / "feedback_loop"
INDEX_PATH = WORKSPACE / "feedback_loop_index.json"
REPORT_DIR = ROOT / "app_operator" / "reports"


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def create_feedback_loop_completion_report():
    index = _load_json(INDEX_PATH)

    reflection_count = 0
    experience_count = 0
    safe_to_continue = False

    if isinstance(index, dict):
        counts = index.get("counts", {})
        reflection_count = counts.get("reflection", 0)
        experience_count = counts.get("experience", 0)
        safe_to_continue = bool(index.get("safe_to_continue", False))

    completed = (
        isinstance(index, dict)
        and reflection_count >= 1
        and experience_count >= 1
        and safe_to_continue is True
    )

    report = {
        "status": "completed" if completed else "incomplete",
        "phase": "Phase14-6 Feedback Loop Completion Report",
        "phase14_completed": completed,
        "feedback_loop_index_found": isinstance(index, dict),
        "reflection_count": reflection_count,
        "experience_count": experience_count,
        "feedback_learning_loop_ready": completed,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": completed,
        "next_phase": "Phase15 Planner Self Improvement" if completed else "Phase14 review required",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "index_path": str(INDEX_PATH),
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    report_path = REPORT_DIR / "feedback_loop_completion_report.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return report, report_path


if __name__ == "__main__":
    report, report_path = create_feedback_loop_completion_report()

    print("=== Feedback Loop Completion Report ===")
    print(f"状態: {report['status']}")
    print(f"工程: {report['phase']}")
    print(f"Phase14Completed: {report['phase14_completed']}")
    print(f"FeedbackLoopIndexFound: {report['feedback_loop_index_found']}")
    print(f"ReflectionCount: {report['reflection_count']}")
    print(f"ExperienceCount: {report['experience_count']}")
    print(f"FeedbackLearningLoopReady: {report['feedback_learning_loop_ready']}")
    print(f"WorkspaceOnly: {report['workspace_only']}")
    print(f"OriginalWrite: {report['original_write']}")
    print(f"FileDelete: {report['file_delete']}")
    print(f"RiskCount: {report['risk_count']}")
    print(f"SafeToContinue: {report['safe_to_continue']}")
    print(f"次工程: {report['next_phase']}")
    print(f"保存先: {report_path}")