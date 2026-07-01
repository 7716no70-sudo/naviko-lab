from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"

FINAL_RELEASE_DIR = WORKSPACE_DIR / "original_ai_os_final_release"
ARCHIVE_DIR = WORKSPACE_DIR / "optional_release_archive"
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_FILES = [
    FINAL_RELEASE_DIR / "original_ai_os_final_release_source.json",
    FINAL_RELEASE_DIR / "original_ai_os_final_release_package.json",
    FINAL_RELEASE_DIR / "original_ai_os_final_release_diagnostics.json",
    FINAL_RELEASE_DIR / "original_ai_os_final_release_completion_report.json",
]

OUTPUT_PATH = ARCHIVE_DIR / "optional_release_archive_source.json"

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
        if data is None:
            missing.append(str(path))
        else:
            collected[path.name] = data

    completion = collected.get(
        "original_ai_os_final_release_completion_report.json", {}
    )

    result = {
        "status": "completed",
        "phase": "Phase24-1 Optional Release Archive Source Collector",
        "SourceCount": len(collected),
        "MissingSourceCount": len(missing),
        "MissingSources": missing,
        "FinalReleaseCompleted": completion.get("FinalReleaseCompleted") is True,
        "FinalReleaseReady": completion.get("FinalReleaseReady") is True,
        "ProjectStatus": completion.get("ProjectStatus"),
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
            and completion.get("FinalReleaseCompleted") is True
            and completion.get("FinalReleaseReady") is True
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

    print("=== Optional Release Archive Source Collector ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"SourceCount: {result['SourceCount']}")
    print(f"MissingSourceCount: {result['MissingSourceCount']}")
    print(f"FinalReleaseCompleted: {result['FinalReleaseCompleted']}")
    print(f"FinalReleaseReady: {result['FinalReleaseReady']}")
    print(f"ProjectStatus: {result['ProjectStatus']}")
    print(f"WorkspaceOnly: {result['WorkspaceOnly']}")
    print(f"OriginalWrite: {result['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {result['OriginalWriteBlocked']}")
    print(f"RiskCount: {result['RiskCount']}")
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()