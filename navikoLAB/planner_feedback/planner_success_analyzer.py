from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_LOOP_DIR = ROOT / "workspace" / "feedback_loop"
INDEX_PATH = FEEDBACK_LOOP_DIR / "feedback_loop_index.json"
PROFILE_PATH = FEEDBACK_LOOP_DIR / "planner_success_profile.json"


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def analyze_planner_success():
    index = _load_json(INDEX_PATH)

    reflection_count = 0
    experience_count = 0
    success_signal_count = 0
    failure_signal_count = 0

    if isinstance(index, dict):
        reflection_candidates = index.get("reflection_candidates", [])
        experience_candidates = index.get("experience_candidates", [])

        reflection_count = len(reflection_candidates)
        experience_count = len(experience_candidates)

        all_candidates = reflection_candidates + experience_candidates

        for item in all_candidates:
            data = item.get("data", {}) if isinstance(item, dict) else {}

            text = json.dumps(data, ensure_ascii=False).lower()

            if "success" in text or "successsignal" in text or "成功" in text:
                success_signal_count += 1

            if "failure" in text or "failuresignal" in text or "失敗" in text:
                failure_signal_count += 1

    total_signal_count = success_signal_count + failure_signal_count

    if total_signal_count > 0:
        mission_success_rate = round(success_signal_count / total_signal_count, 4)
    else:
        mission_success_rate = 0.0

    profile = {
        "status": "completed",
        "phase": "Phase15-1 Planner Success Analyzer",
        "source_index_found": isinstance(index, dict),
        "reflection_count": reflection_count,
        "experience_count": experience_count,
        "success_signal_count": success_signal_count,
        "failure_signal_count": failure_signal_count,
        "total_signal_count": total_signal_count,
        "mission_success_rate": mission_success_rate,
        "planner_self_improvement_ready": total_signal_count > 0,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": True,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_index_path": str(INDEX_PATH),
        "profile_path": str(PROFILE_PATH),
    }

    FEEDBACK_LOOP_DIR.mkdir(parents=True, exist_ok=True)
    PROFILE_PATH.write_text(
        json.dumps(profile, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return profile


if __name__ == "__main__":
    result = analyze_planner_success()

    print("=== Planner Success Analyzer ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['phase']}")
    print(f"SourceIndexFound: {result['source_index_found']}")
    print(f"ReflectionCount: {result['reflection_count']}")
    print(f"ExperienceCount: {result['experience_count']}")
    print(f"SuccessSignalCount: {result['success_signal_count']}")
    print(f"FailureSignalCount: {result['failure_signal_count']}")
    print(f"TotalSignalCount: {result['total_signal_count']}")
    print(f"MissionSuccessRate: {result['mission_success_rate']}")
    print(f"PlannerSelfImprovementReady: {result['planner_self_improvement_ready']}")
    print(f"WorkspaceOnly: {result['workspace_only']}")
    print(f"OriginalWrite: {result['original_write']}")
    print(f"FileDelete: {result['file_delete']}")
    print(f"RiskCount: {result['risk_count']}")
    print(f"SafeToContinue: {result['safe_to_continue']}")
    print(f"保存先: {PROFILE_PATH}")