from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SELF_IMPROVEMENT_PROFILE_PATH = (
    ROOT
    / "workspace"
    / "feedback_loop"
    / "planner_self_improvement_profile.json"
)


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def load_taskplanner_self_improvement_context():
    profile = _load_json(SELF_IMPROVEMENT_PROFILE_PATH)

    if not isinstance(profile, dict):
        return {
            "status": "missing",
            "self_improvement_context_found": False,
            "mission_success_rate": 0.0,
            "planner_mode": "unknown",
            "recommendations": [],
            "taskplanner_hint": "Planner自己改善情報はまだ利用できません。",
            "planner_write_allowed": False,
            "planner_patch_allowed": False,
            "workspace_only": True,
            "original_write": False,
            "safe_to_continue": False,
        }

    mission_success_rate = profile.get("mission_success_rate", 0.0)
    planner_mode = profile.get("planner_mode", "unknown")
    recommendations = profile.get("recommendations", [])

    taskplanner_hint = (
        f"PlannerMode={planner_mode}, "
        f"MissionSuccessRate={mission_success_rate}, "
        f"RecommendationCount={len(recommendations)}"
    )

    return {
        "status": "completed",
        "self_improvement_context_found": True,
        "mission_success_rate": mission_success_rate,
        "planner_mode": planner_mode,
        "recommendations": recommendations,
        "taskplanner_hint": taskplanner_hint,
        "planner_write_allowed": False,
        "planner_patch_allowed": False,
        "workspace_only": True,
        "original_write": False,
        "safe_to_continue": True,
    }


if __name__ == "__main__":
    result = load_taskplanner_self_improvement_context()

    print("=== TaskPlanner Self Improvement Read Adapter ===")
    print(f"状態: {result['status']}")
    print("工程: Phase15-4 TaskPlanner Self Improvement Read Adapter")
    print(f"SelfImprovementContextFound: {result['self_improvement_context_found']}")
    print(f"MissionSuccessRate: {result['mission_success_rate']}")
    print(f"PlannerMode: {result['planner_mode']}")
    print(f"RecommendationCount: {len(result['recommendations'])}")
    print(f"TaskPlannerHint: {result['taskplanner_hint']}")
    print(f"PlannerWriteAllowed: {result['planner_write_allowed']}")
    print(f"PlannerPatchAllowed: {result['planner_patch_allowed']}")
    print(f"WorkspaceOnly: {result['workspace_only']}")
    print(f"OriginalWrite: {result['original_write']}")
    print(f"SafeToContinue: {result['safe_to_continue']}")