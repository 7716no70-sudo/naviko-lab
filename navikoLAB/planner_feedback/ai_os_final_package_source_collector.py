from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
OUTPUT_DIR = WORKSPACE_DIR / "ai_os_final_package"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_SOURCES = [
    "mission_success_history.json",
    "mission_success_statistics.json",
    "mission_success_trend.json",
    "mission_long_term_learning_profile.json",
    "mission_self_optimization_hint.json",
    "mission_self_optimization_integration_source.json",
    "planner_mission_optimization_hint.json",
    "capability_mission_optimization_hint.json",
    "connector_mission_optimization_hint.json",
    "mission_policy_source.json",
    "mission_stability_policy.json",
    "mission_policy_hint.json",
    "ai_os_stability_source.json",
    "ai_os_stability_profile.json",
]

def load_json_safe(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"load_error": str(e)}

def main():
    collected = {}
    missing = []

    for name in REQUIRED_SOURCES:
        path = WORKSPACE_DIR / name
        data = load_json_safe(path)
        if data is None:
            missing.append(name)
        else:
            collected[name] = data

    result = {
        "status": "completed",
        "phase": "Phase21-1 AI OS Final Package Source Collector",
        "SourceCount": len(collected),
        "MissingSourceCount": len(missing),
        "MissingSources": missing,
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "FileDelete": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "HumanApprovalRequired": True,
        "PermissionPolicyRequired": True,
        "RiskCount": 0,
        "SafeToContinue": len(missing) == 0,
        "CollectedSources": collected,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    output_path = OUTPUT_DIR / "ai_os_final_package_source.json"
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== AI OS Final Package Source Collector ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"SourceCount: {result['SourceCount']}")
    print(f"MissingSourceCount: {result['MissingSourceCount']}")
    print(f"WorkspaceOnly: {result['WorkspaceOnly']}")
    print(f"OriginalWrite: {result['OriginalWrite']}")
    print(f"RiskCount: {result['RiskCount']}")
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"保存先: {output_path}")

if __name__ == "__main__":
    main()