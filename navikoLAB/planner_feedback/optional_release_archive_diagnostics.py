from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
ARCHIVE_DIR = WORKSPACE_DIR / "optional_release_archive"

PACKAGE_PATH = ARCHIVE_DIR / "optional_release_archive_package.json"
OUTPUT_PATH = ARCHIVE_DIR / "optional_release_archive_diagnostics.json"

REQUIRED_KEYS = [
    "status",
    "phase",
    "Project",
    "ArchiveStatus",
    "ArchiveMode",
    "SourceFound",
    "SourceCount",
    "MissingSourceCount",
    "FinalReleaseCompleted",
    "FinalReleaseReady",
    "ProjectStatus",
    "ArchiveReady",
    "ArchivedPhaseRange",
    "SafetyPolicy",
    "ArchiveContents",
    "RiskCount",
    "SafeToContinue",
    "CollectedSources",
]

REQUIRED_SAFETY = {
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
}

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    package_found = PACKAGE_PATH.exists()
    package = load_json(PACKAGE_PATH) if package_found else {}

    missing_keys = [key for key in REQUIRED_KEYS if key not in package]

    safety = package.get("SafetyPolicy", {})
    safety_mismatches = {
        key: {"expected": expected, "actual": safety.get(key)}
        for key, expected in REQUIRED_SAFETY.items()
        if safety.get(key) != expected
    }

    diagnostics_ok = (
        package_found
        and not missing_keys
        and not safety_mismatches
        and package.get("ArchiveStatus") == "built"
        and package.get("ArchiveMode") == "workspace_only_safe_archive"
        and package.get("SourceFound") is True
        and package.get("SourceCount") == 4
        and package.get("MissingSourceCount") == 0
        and package.get("FinalReleaseCompleted") is True
        and package.get("FinalReleaseReady") is True
        and package.get("ArchiveReady") is True
        and package.get("RiskCount") == 0
        and package.get("SafeToContinue") is True
    )

    result = {
        "status": "completed",
        "phase": "Phase24-3 Optional Release Archive Diagnostics",
        "PackageFound": package_found,
        "RequiredKeysOK": len(missing_keys) == 0,
        "MissingKeys": missing_keys,
        "SafetyPolicyOK": len(safety_mismatches) == 0,
        "SafetyMismatches": safety_mismatches,
        "ArchiveStatusOK": package.get("ArchiveStatus") == "built",
        "ArchiveModeOK": package.get("ArchiveMode") == "workspace_only_safe_archive",
        "SourceFound": package.get("SourceFound") is True,
        "SourceCountOK": package.get("SourceCount") == 4,
        "MissingSourceCountOK": package.get("MissingSourceCount") == 0,
        "FinalReleaseCompleted": package.get("FinalReleaseCompleted") is True,
        "FinalReleaseReady": package.get("FinalReleaseReady") is True,
        "ArchiveReady": package.get("ArchiveReady") is True,
        "WorkspaceOnly": safety.get("WorkspaceOnly"),
        "OriginalWrite": safety.get("OriginalWrite"),
        "OriginalWriteBlocked": safety.get("OriginalWriteBlocked"),
        "HumanApprovalRequired": safety.get("HumanApprovalRequired"),
        "PermissionPolicyRequired": safety.get("PermissionPolicyRequired"),
        "RiskCount": 0 if diagnostics_ok else 1,
        "SafeToContinue": diagnostics_ok,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Optional Release Archive Diagnostics ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"PackageFound: {result['PackageFound']}")
    print(f"RequiredKeysOK: {result['RequiredKeysOK']}")
    print(f"SafetyPolicyOK: {result['SafetyPolicyOK']}")
    print(f"ArchiveStatusOK: {result['ArchiveStatusOK']}")
    print(f"ArchiveModeOK: {result['ArchiveModeOK']}")
    print(f"SourceFound: {result['SourceFound']}")
    print(f"SourceCountOK: {result['SourceCountOK']}")
    print(f"MissingSourceCountOK: {result['MissingSourceCountOK']}")
    print(f"FinalReleaseCompleted: {result['FinalReleaseCompleted']}")
    print(f"FinalReleaseReady: {result['FinalReleaseReady']}")
    print(f"ArchiveReady: {result['ArchiveReady']}")
    print(f"WorkspaceOnly: {result['WorkspaceOnly']}")
    print(f"OriginalWrite: {result['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {result['OriginalWriteBlocked']}")
    print(f"RiskCount: {result['RiskCount']}")
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()