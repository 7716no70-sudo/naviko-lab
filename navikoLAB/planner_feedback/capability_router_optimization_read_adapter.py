from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = (
    ROOT
    / "workspace"
    / "feedback_loop"
    / "capability_connector_optimization_profile.json"
)


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def load_capability_router_optimization_context():
    profile = _load_json(PROFILE_PATH)

    if not isinstance(profile, dict):
        return {
            "status": "missing",
            "optimization_context_found": False,
            "mission_success_rate": 0.0,
            "planner_mode": "unknown",
            "capability_mode": "unknown",
            "capability_recommendations": [],
            "capability_router_hint": "Capability最適化情報はまだ利用できません。",
            "capability_router_write_allowed": False,
            "capability_router_patch_allowed": False,
            "workspace_only": True,
            "original_write": False,
            "safe_to_continue": False,
        }

    mission_success_rate = profile.get("mission_success_rate", 0.0)
    planner_mode = profile.get("planner_mode", "unknown")
    capability_mode = profile.get("capability_mode", "unknown")
    recommendations = profile.get("capability_recommendations", [])

    hint = (
        f"CapabilityMode={capability_mode}, "
        f"PlannerMode={planner_mode}, "
        f"MissionSuccessRate={mission_success_rate}, "
        f"CapabilityRecommendationCount={len(recommendations)}"
    )

    return {
        "status": "completed",
        "optimization_context_found": True,
        "mission_success_rate": mission_success_rate,
        "planner_mode": planner_mode,
        "capability_mode": capability_mode,
        "capability_recommendations": recommendations,
        "capability_router_hint": hint,
        "capability_router_write_allowed": False,
        "capability_router_patch_allowed": False,
        "workspace_only": True,
        "original_write": False,
        "safe_to_continue": True,
    }


if __name__ == "__main__":
    result = load_capability_router_optimization_context()

    print("=== Capability Router Optimization Read Adapter ===")
    print(f"状態: {result['status']}")
    print("工程: Phase16-5 Capability Router Optimization Read Adapter")
    print(f"OptimizationContextFound: {result['optimization_context_found']}")
    print(f"MissionSuccessRate: {result['mission_success_rate']}")
    print(f"PlannerMode: {result['planner_mode']}")
    print(f"CapabilityMode: {result['capability_mode']}")
    print(f"CapabilityRecommendationCount: {len(result['capability_recommendations'])}")
    print(f"CapabilityRouterHint: {result['capability_router_hint']}")
    print(f"CapabilityRouterWriteAllowed: {result['capability_router_write_allowed']}")
    print(f"CapabilityRouterPatchAllowed: {result['capability_router_patch_allowed']}")
    print(f"WorkspaceOnly: {result['workspace_only']}")
    print(f"OriginalWrite: {result['original_write']}")
    print(f"SafeToContinue: {result['safe_to_continue']}")