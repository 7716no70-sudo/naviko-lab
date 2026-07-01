from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_LOOP_DIR = ROOT / "workspace" / "feedback_loop"

SUCCESS_PROFILE_PATH = FEEDBACK_LOOP_DIR / "planner_success_profile.json"
RECOMMENDATION_PATH = FEEDBACK_LOOP_DIR / "planner_improvement_recommendation.json"
SELF_IMPROVEMENT_PROFILE_PATH = FEEDBACK_LOOP_DIR / "planner_self_improvement_profile.json"


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def create_planner_self_improvement_profile():
    success_profile = _load_json(SUCCESS_PROFILE_PATH)
    recommendation = _load_json(RECOMMENDATION_PATH)

    success_found = isinstance(success_profile, dict)
    recommendation_found = isinstance(recommendation, dict)

    mission_success_rate = 0.0
    planner_mode = "unknown"
    recommendations = []

    if success_found:
        mission_success_rate = success_profile.get("mission_success_rate", 0.0)

    if recommendation_found:
        planner_mode = recommendation.get("planner_mode", "unknown")
        recommendations = recommendation.get("recommendations", [])

    profile_ready = success_found and recommendation_found

    profile = {
        "status": "completed" if profile_ready else "incomplete",
        "phase": "Phase15-3 Planner Self Improvement Profile Adapter",
        "success_profile_found": success_found,
        "recommendation_found": recommendation_found,
        "mission_success_rate": mission_success_rate,
        "planner_mode": planner_mode,
        "recommendations": recommendations,
        "planner_self_improvement_profile_ready": profile_ready,
        "planner_write_allowed": False,
        "planner_patch_allowed": False,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": profile_ready,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "success_profile_path": str(SUCCESS_PROFILE_PATH),
        "recommendation_path": str(RECOMMENDATION_PATH),
        "self_improvement_profile_path": str(SELF_IMPROVEMENT_PROFILE_PATH),
    }

    FEEDBACK_LOOP_DIR.mkdir(parents=True, exist_ok=True)
    SELF_IMPROVEMENT_PROFILE_PATH.write_text(
        json.dumps(profile, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return profile


if __name__ == "__main__":
    result = create_planner_self_improvement_profile()

    print("=== Planner Self Improvement Profile Adapter ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['phase']}")
    print(f"SuccessProfileFound: {result['success_profile_found']}")
    print(f"RecommendationFound: {result['recommendation_found']}")
    print(f"MissionSuccessRate: {result['mission_success_rate']}")
    print(f"PlannerMode: {result['planner_mode']}")
    print(f"RecommendationCount: {len(result['recommendations'])}")
    print(f"PlannerSelfImprovementProfileReady: {result['planner_self_improvement_profile_ready']}")
    print(f"PlannerWriteAllowed: {result['planner_write_allowed']}")
    print(f"PlannerPatchAllowed: {result['planner_patch_allowed']}")
    print(f"WorkspaceOnly: {result['workspace_only']}")
    print(f"OriginalWrite: {result['original_write']}")
    print(f"FileDelete: {result['file_delete']}")
    print(f"RiskCount: {result['risk_count']}")
    print(f"SafeToContinue: {result['safe_to_continue']}")
    print(f"保存先: {SELF_IMPROVEMENT_PROFILE_PATH}")