from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_LOOP_DIR = ROOT / "workspace" / "feedback_loop"

CAPABILITY_PROFILE_PATH = FEEDBACK_LOOP_DIR / "capability_optimization_profile.json"
CONNECTOR_PROFILE_PATH = FEEDBACK_LOOP_DIR / "connector_optimization_profile.json"
MERGED_PROFILE_PATH = FEEDBACK_LOOP_DIR / "capability_connector_optimization_profile.json"


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def merge_capability_connector_optimization_profile():
    capability_profile = _load_json(CAPABILITY_PROFILE_PATH)
    connector_profile = _load_json(CONNECTOR_PROFILE_PATH)

    capability_found = isinstance(capability_profile, dict)
    connector_found = isinstance(connector_profile, dict)

    merged_ready = capability_found and connector_found

    merged = {
        "status": "completed" if merged_ready else "incomplete",
        "phase": "Phase16-4 Capability Connector Optimization Merge Adapter",
        "capability_profile_found": capability_found,
        "connector_profile_found": connector_found,
        "mission_success_rate": (
            capability_profile.get("mission_success_rate", 0.0)
            if capability_found
            else 0.0
        ),
        "planner_mode": (
            capability_profile.get("planner_mode", "unknown")
            if capability_found
            else "unknown"
        ),
        "capability_mode": (
            capability_profile.get("capability_mode", "unknown")
            if capability_found
            else "unknown"
        ),
        "connector_mode": (
            connector_profile.get("connector_mode", "unknown")
            if connector_found
            else "unknown"
        ),
        "capability_recommendations": (
            capability_profile.get("recommendations", [])
            if capability_found
            else []
        ),
        "connector_recommendations": (
            connector_profile.get("recommendations", [])
            if connector_found
            else []
        ),
        "capability_connector_optimization_ready": merged_ready,
        "capability_router_write_allowed": False,
        "capability_router_patch_allowed": False,
        "connector_dispatcher_write_allowed": False,
        "connector_dispatcher_patch_allowed": False,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "external_operation": False,
        "real_gui_operation": False,
        "risk_count": 0,
        "safe_to_continue": merged_ready,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "paths": {
            "capability_profile": str(CAPABILITY_PROFILE_PATH),
            "connector_profile": str(CONNECTOR_PROFILE_PATH),
            "merged_profile": str(MERGED_PROFILE_PATH),
        },
    }

    FEEDBACK_LOOP_DIR.mkdir(parents=True, exist_ok=True)
    MERGED_PROFILE_PATH.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return merged


if __name__ == "__main__":
    result = merge_capability_connector_optimization_profile()

    print("=== Capability Connector Optimization Merge Adapter ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['phase']}")
    print(f"CapabilityProfileFound: {result['capability_profile_found']}")
    print(f"ConnectorProfileFound: {result['connector_profile_found']}")
    print(f"MissionSuccessRate: {result['mission_success_rate']}")
    print(f"PlannerMode: {result['planner_mode']}")
    print(f"CapabilityMode: {result['capability_mode']}")
    print(f"ConnectorMode: {result['connector_mode']}")
    print(f"CapabilityRecommendationCount: {len(result['capability_recommendations'])}")
    print(f"ConnectorRecommendationCount: {len(result['connector_recommendations'])}")
    print(f"CapabilityConnectorOptimizationReady: {result['capability_connector_optimization_ready']}")
    print(f"CapabilityRouterWriteAllowed: {result['capability_router_write_allowed']}")
    print(f"CapabilityRouterPatchAllowed: {result['capability_router_patch_allowed']}")
    print(f"ConnectorDispatcherWriteAllowed: {result['connector_dispatcher_write_allowed']}")
    print(f"ConnectorDispatcherPatchAllowed: {result['connector_dispatcher_patch_allowed']}")
    print(f"WorkspaceOnly: {result['workspace_only']}")
    print(f"OriginalWrite: {result['original_write']}")
    print(f"FileDelete: {result['file_delete']}")
    print(f"ExternalOperation: {result['external_operation']}")
    print(f"RealGUIOperation: {result['real_gui_operation']}")
    print(f"RiskCount: {result['risk_count']}")
    print(f"SafeToContinue: {result['safe_to_continue']}")
    print(f"保存先: {MERGED_PROFILE_PATH}")