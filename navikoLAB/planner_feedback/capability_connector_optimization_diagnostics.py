from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_LOOP_DIR = ROOT / "workspace" / "feedback_loop"
REPORT_DIR = ROOT / "app_operator" / "reports"

SOURCE_PATH = FEEDBACK_LOOP_DIR / "capability_connector_optimization_source.json"
CAPABILITY_PROFILE_PATH = FEEDBACK_LOOP_DIR / "capability_optimization_profile.json"
CONNECTOR_PROFILE_PATH = FEEDBACK_LOOP_DIR / "connector_optimization_profile.json"
MERGED_PROFILE_PATH = FEEDBACK_LOOP_DIR / "capability_connector_optimization_profile.json"

DIAGNOSTICS_PATH = REPORT_DIR / "capability_connector_optimization_diagnostics.json"


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def run_capability_connector_optimization_diagnostics():
    source = _load_json(SOURCE_PATH)
    capability_profile = _load_json(CAPABILITY_PROFILE_PATH)
    connector_profile = _load_json(CONNECTOR_PROFILE_PATH)
    merged_profile = _load_json(MERGED_PROFILE_PATH)

    source_found = isinstance(source, dict)
    capability_found = isinstance(capability_profile, dict)
    connector_found = isinstance(connector_profile, dict)
    merged_found = isinstance(merged_profile, dict)

    risk_count = 0

    for data in [source, capability_profile, connector_profile, merged_profile]:
        if not isinstance(data, dict):
            continue

        if data.get("original_write") is not False:
            risk_count += 1
        if data.get("file_delete") is not False:
            risk_count += 1
        if data.get("external_operation") is not False:
            risk_count += 1
        if data.get("real_gui_operation") is not False:
            risk_count += 1

    if isinstance(merged_profile, dict):
        if merged_profile.get("capability_router_write_allowed") is not False:
            risk_count += 1
        if merged_profile.get("capability_router_patch_allowed") is not False:
            risk_count += 1
        if merged_profile.get("connector_dispatcher_write_allowed") is not False:
            risk_count += 1
        if merged_profile.get("connector_dispatcher_patch_allowed") is not False:
            risk_count += 1

    required_ok = all([
        source_found,
        capability_found,
        connector_found,
        merged_found,
    ])

    completed = required_ok and risk_count == 0

    diagnostics = {
        "status": "completed" if completed else "incomplete",
        "phase": "Phase16-7 Capability Connector Optimization Diagnostics",
        "source_found": source_found,
        "capability_profile_found": capability_found,
        "connector_profile_found": connector_found,
        "merged_profile_found": merged_found,
        "required_ok": required_ok,
        "capability_connector_optimization_ready": completed,
        "capability_router_write_allowed": False,
        "capability_router_patch_allowed": False,
        "connector_dispatcher_write_allowed": False,
        "connector_dispatcher_patch_allowed": False,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "external_operation": False,
        "real_gui_operation": False,
        "risk_count": risk_count,
        "safe_to_continue": completed,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "paths": {
            "source": str(SOURCE_PATH),
            "capability_profile": str(CAPABILITY_PROFILE_PATH),
            "connector_profile": str(CONNECTOR_PROFILE_PATH),
            "merged_profile": str(MERGED_PROFILE_PATH),
            "diagnostics": str(DIAGNOSTICS_PATH),
        },
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    DIAGNOSTICS_PATH.write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return diagnostics


if __name__ == "__main__":
    result = run_capability_connector_optimization_diagnostics()

    print("=== Capability Connector Optimization Diagnostics ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['phase']}")
    print(f"SourceFound: {result['source_found']}")
    print(f"CapabilityProfileFound: {result['capability_profile_found']}")
    print(f"ConnectorProfileFound: {result['connector_profile_found']}")
    print(f"MergedProfileFound: {result['merged_profile_found']}")
    print(f"RequiredOK: {result['required_ok']}")
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
    print(f"保存先: {DIAGNOSTICS_PATH}")