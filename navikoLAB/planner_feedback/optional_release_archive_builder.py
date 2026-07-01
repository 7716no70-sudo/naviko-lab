from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
ARCHIVE_DIR = WORKSPACE_DIR / "optional_release_archive"

SOURCE_PATH = ARCHIVE_DIR / "optional_release_archive_source.json"
OUTPUT_PATH = ARCHIVE_DIR / "optional_release_archive_package.json"

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(SOURCE_PATH)

    package = {
        "status": "completed",
        "phase": "Phase24-2 Optional Release Archive Builder",
        "Project": "Original Naviko AI OS v2.0 Final Release",
        "ArchiveStatus": "built",
        "ArchiveMode": "workspace_only_safe_archive",
        "SourceFound": SOURCE_PATH.exists(),
        "SourceCount": source.get("SourceCount", 0),
        "MissingSourceCount": source.get("MissingSourceCount", 0),
        "FinalReleaseCompleted": source.get("FinalReleaseCompleted") is True,
        "FinalReleaseReady": source.get("FinalReleaseReady") is True,
        "ProjectStatus": source.get("ProjectStatus"),
        "ArchiveReady": True,
        "ArchivedPhaseRange": "Phase1 to Phase24",
        "SafetyPolicy": {
            "WorkspaceOnly": True,
            "OriginalWrite": False,
            "OriginalWriteBlocked": True,
            "PlannerWriteAllowed": False,
            "CapabilityRouterWriteAllowed": False,
            "ConnectorDispatcherWriteAllowed": False,
            "AutoPatch": False,
            "FileDelete": False,
            "ExternalOperation": False,
            "RealGUIOperation": False,
            "HumanApprovalRequired": True,
            "PermissionPolicyRequired": True,
            "ReadOnlyReference": True,
        },
        "ArchiveContents": [
            "Final Release Source",
            "Final Release Package",
            "Final Release Diagnostics",
            "Final Release Completion Report",
        ],
        "RiskCount": 0,
        "SafeToContinue": (
            source.get("SafeToContinue") is True
            and source.get("RiskCount") == 0
            and source.get("OriginalWrite") is False
            and source.get("OriginalWriteBlocked") is True
            and source.get("FinalReleaseCompleted") is True
            and source.get("FinalReleaseReady") is True
        ),
        "CollectedSources": source.get("CollectedSources", {}),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(package, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Optional Release Archive Builder ===")
    print(f"status: {package['status']}")
    print(f"phase: {package['phase']}")
    print(f"ArchiveStatus: {package['ArchiveStatus']}")
    print(f"ArchiveMode: {package['ArchiveMode']}")
    print(f"SourceFound: {package['SourceFound']}")
    print(f"SourceCount: {package['SourceCount']}")
    print(f"MissingSourceCount: {package['MissingSourceCount']}")
    print(f"FinalReleaseCompleted: {package['FinalReleaseCompleted']}")
    print(f"FinalReleaseReady: {package['FinalReleaseReady']}")
    print(f"ProjectStatus: {package['ProjectStatus']}")
    print(f"ArchiveReady: {package['ArchiveReady']}")
    print(f"WorkspaceOnly: {package['SafetyPolicy']['WorkspaceOnly']}")
    print(f"OriginalWrite: {package['SafetyPolicy']['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {package['SafetyPolicy']['OriginalWriteBlocked']}")
    print(f"RiskCount: {package['RiskCount']}")
    print(f"SafeToContinue: {package['SafeToContinue']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()