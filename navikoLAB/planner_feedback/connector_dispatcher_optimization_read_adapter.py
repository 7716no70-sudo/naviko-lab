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


def load_connector_dispatcher_optimization_context():
    profile = _load_json(PROFILE_PATH)

    if not isinstance(profile, dict):
        return {
            "status": "missing",
            "optimization_context_found": False,
            "mission_success_rate": 0.0,
            "planner_mode": "unknown",
            "connector_mode": "unknown",
            "connector_recommendations": [],
            "connector_dispatcher_hint": "Connector最適化情報はまだ利用できません。",
            "connector_dispatcher_write_allowed": False,
            "connector_dispatcher_patch_allowed": False,
            "workspace_only": True,
            "original_write": False,
            "external_operation": False,
            "safe_to_continue": False,
        }

    mission_success_rate = profile.get("mission_success_rate", 0.0)
    planner_mode = profile.get("planner_mode", "unknown")
    connector_mode = profile.get("connector_mode", "unknown")
    recommendations = profile.get("connector_recommendations", [])

    hint = (
        f"ConnectorMode={connector_mode}, "
        f"PlannerMode={planner_mode}, "
        f"MissionSuccessRate={mission_success_rate}, "
        f"ConnectorRecommendationCount={len(recommendations)}"
    )

    return {
        "status": "completed",
        "optimization_context_found": True,
        "mission_success_rate": mission_success_rate,
        "planner_mode": planner_mode,
        "connector_mode": connector_mode,
        "connector_recommendations": recommendations,
        "connector_dispatcher_hint": hint,
        "connector_dispatcher_write_allowed": False,
        "connector_dispatcher_patch_allowed": False,
        "workspace_only": True,
        "original_write": False,
        "external_operation": False,
        "safe_to_continue": True,
    }


if __name__ == "__main__":
    result = load_connector_dispatcher_optimization_context()

    print("=== Connector Dispatcher Optimization Read Adapter ===")
    print(f"状態: {result['status']}")
    print("工程: Phase16-6 Connector Dispatcher Optimization Read Adapter")
    print(f"OptimizationContextFound: {result['optimization_context_found']}")
    print(f"MissionSuccessRate: {result['mission_success_rate']}")
    print(f"PlannerMode: {result['planner_mode']}")
    print(f"ConnectorMode: {result['connector_mode']}")
    print(f"ConnectorRecommendationCount: {len(result['connector_recommendations'])}")
    print(f"ConnectorDispatcherHint: {result['connector_dispatcher_hint']}")
    print(f"ConnectorDispatcherWriteAllowed: {result['connector_dispatcher_write_allowed']}")
    print(f"ConnectorDispatcherPatchAllowed: {result['connector_dispatcher_patch_allowed']}")
    print(f"WorkspaceOnly: {result['workspace_only']}")
    print(f"OriginalWrite: {result['original_write']}")
    print(f"ExternalOperation: {result['external_operation']}")
    print(f"SafeToContinue: {result['safe_to_continue']}")