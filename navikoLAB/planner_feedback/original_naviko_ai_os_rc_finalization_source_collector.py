from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
PACKAGE_DIR = WORKSPACE_DIR / "ai_os_final_package"
OUTPUT_DIR = WORKSPACE_DIR / "original_ai_os_rc_finalization"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_FILES = [
    PACKAGE_DIR / "ai_os_final_package_source.json",
    PACKAGE_DIR / "ai_os_final_package.json",
    PACKAGE_DIR / "ai_os_final_package_diagnostics.json",
    PACKAGE_DIR / "ai_os_final_package_completion_report.json",
]

OUTPUT_PATH = OUTPUT_DIR / "original_ai_os_rc_finalization_source.json"

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

    for path in REQUIRED_FILES:
        data = load_json_safe(path)
        key = path.name
        if data is None:
            missing.append(str(path))
        else:
            collected[key] = data

    completion = collected.get("ai_os_final_package_completion_report.json", {})

    result = {
        "status": "completed",
        "phase": "Phase22-1 Original Naviko AI OS Release Candidate Finalization Source Collector",
        "SourceCount": len(collected),
        "MissingSourceCount": len(missing),
        "MissingSources": missing,
        "FinalPackageReady": completion.get("FinalPackageReady") is True,
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "HumanApprovalRequired": True,
        "PermissionPolicyRequired": True,
        "FileDelete": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "RiskCount": 0 if len(missing) == 0 else 1,
        "SafeToContinue": (
            len(missing) == 0
            and completion.get("FinalPackageReady") is True
            and completion.get("RiskCount") == 0
            and completion.get("SafeToContinue") is True
        ),
        "CollectedSources": collected,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Original Naviko AI OS RC Finalization Source Collector ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"SourceCount: {result['SourceCount']}")
    print(f"MissingSourceCount: {result['MissingSourceCount']}")
    print(f"FinalPackageReady: {result['FinalPackageReady']}")
    print(f"WorkspaceOnly: {result['WorkspaceOnly']}")
    print(f"OriginalWrite: {result['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {result['OriginalWriteBlocked']}")
    print(f"HumanApprovalRequired: {result['HumanApprovalRequired']}")
    print(f"PermissionPolicyRequired: {result['PermissionPolicyRequired']}")
    print(f"RiskCount: {result['RiskCount']}")
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()