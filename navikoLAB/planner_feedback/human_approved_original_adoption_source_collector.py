from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"

FINAL_RELEASE_DIR = WORKSPACE_DIR / "original_ai_os_final_release"
ARCHIVE_DIR = WORKSPACE_DIR / "optional_release_archive"
ADOPTION_DIR = WORKSPACE_DIR / "human_approved_original_adoption"
ADOPTION_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_FILES = [
    FINAL_RELEASE_DIR / "original_ai_os_final_release_completion_report.json",
    ARCHIVE_DIR / "optional_release_archive_completion_report.json",
]

OUTPUT_PATH = ADOPTION_DIR / "human_approved_original_adoption_source.json"

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

    final_release = collected.get(
        "original_ai_os_final_release_completion_report.json", {}
    )
    archive = collected.get(
        "optional_release_archive_completion_report.json", {}
    )

    result = {
        "status": "completed",
        "phase": "Phase25-1 Human Approved Original Adoption Source Collector",
        "SourceCount": len(collected),
        "MissingSourceCount": len(missing),
        "MissingSources": missing,
        "FinalReleaseReady": final_release.get("FinalReleaseReady") is True,
        "ArchiveReady": archive.get("ArchiveReady") is True,
        "AdoptionMode": "pre_adoption_read_only_preparation",
        "HumanApprovalRequired": True,
        "HumanApproved": False,
        "PermissionPolicyRequired": True,
        "PermissionPolicyApproved": False,
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "AutoPatch": False,
        "FileDelete": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "RiskCount": 0 if len(missing) == 0 else 1,
        "SafeToContinue": (
            len(missing) == 0
            and final_release.get("FinalReleaseReady") is True
            and final_release.get("RiskCount") == 0
            and archive.get("ArchiveReady") is True
            and archive.get("RiskCount") == 0
        ),
        "CollectedSources": collected,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Human Approved Original Adoption Source Collector ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"SourceCount: {result['SourceCount']}")
    print(f"MissingSourceCount: {result['MissingSourceCount']}")
    print(f"FinalReleaseReady: {result['FinalReleaseReady']}")
    print(f"ArchiveReady: {result['ArchiveReady']}")
    print(f"AdoptionMode: {result['AdoptionMode']}")
    print(f"HumanApprovalRequired: {result['HumanApprovalRequired']}")
    print(f"HumanApproved: {result['HumanApproved']}")
    print(f"PermissionPolicyRequired: {result['PermissionPolicyRequired']}")
    print(f"PermissionPolicyApproved: {result['PermissionPolicyApproved']}")
    print(f"WorkspaceOnly: {result['WorkspaceOnly']}")
    print(f"OriginalWrite: {result['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {result['OriginalWriteBlocked']}")
    print(f"RiskCount: {result['RiskCount']}")
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()