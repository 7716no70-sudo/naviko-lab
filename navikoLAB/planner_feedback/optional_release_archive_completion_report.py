from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
ARCHIVE_DIR = WORKSPACE_DIR / "optional_release_archive"

PACKAGE_PATH = ARCHIVE_DIR / "optional_release_archive_package.json"
DIAGNOSTICS_PATH = ARCHIVE_DIR / "optional_release_archive_diagnostics.json"
OUTPUT_PATH = ARCHIVE_DIR / "optional_release_archive_completion_report.json"

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    package_found = PACKAGE_PATH.exists()
    diagnostics_found = DIAGNOSTICS_PATH.exists()

    package = load_json(PACKAGE_PATH) if package_found else {}
    diagnostics = load_json(DIAGNOSTICS_PATH) if diagnostics_found else {}

    safety = package.get("SafetyPolicy", {})

    completed = (
        package_found
        and diagnostics_found
        and diagnostics.get("SafeToContinue") is True
        and diagnostics.get("RiskCount") == 0
        and package.get("ArchiveReady") is True
        and safety.get("WorkspaceOnly") is True
        and safety.get("OriginalWrite") is False
        and safety.get("OriginalWriteBlocked") is True
    )

    result = {
        "status": "completed",
        "phase": "Phase24-4 Optional Release Archive Completion Report",
        "PackageFound": package_found,
        "DiagnosticsFound": diagnostics_found,
        "DiagnosticsConfirmed": diagnostics.get("SafeToContinue") is True,
        "ArchiveCompleted": completed,
        "ArchiveReady": completed,
        "Project": package.get("Project"),
        "ArchiveStatus": package.get("ArchiveStatus"),
        "ArchiveMode": package.get("ArchiveMode"),
        "ArchivedPhaseRange": package.get("ArchivedPhaseRange"),
        "SourceCount": package.get("SourceCount"),
        "MissingSourceCount": package.get("MissingSourceCount"),
        "FinalReleaseCompleted": package.get("FinalReleaseCompleted"),
        "FinalReleaseReady": package.get("FinalReleaseReady"),
        "ProjectStatus": package.get("ProjectStatus"),
        "WorkspaceOnly": safety.get("WorkspaceOnly"),
        "OriginalWrite": safety.get("OriginalWrite"),
        "OriginalWriteBlocked": safety.get("OriginalWriteBlocked"),
        "PlannerWriteAllowed": safety.get("PlannerWriteAllowed"),
        "CapabilityRouterWriteAllowed": safety.get("CapabilityRouterWriteAllowed"),
        "ConnectorDispatcherWriteAllowed": safety.get("ConnectorDispatcherWriteAllowed"),
        "AutoPatch": safety.get("AutoPatch"),
        "FileDelete": safety.get("FileDelete"),
        "ExternalOperation": safety.get("ExternalOperation"),
        "RealGUIOperation": safety.get("RealGUIOperation"),
        "HumanApprovalRequired": safety.get("HumanApprovalRequired"),
        "PermissionPolicyRequired": safety.get("PermissionPolicyRequired"),
        "ReadOnlyReference": safety.get("ReadOnlyReference"),
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": "Post-v2.0 Human Approved Original Adoption",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Optional Release Archive Completion Report ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"PackageFound: {result['PackageFound']}")
    print(f"DiagnosticsFound: {result['DiagnosticsFound']}")
    print(f"DiagnosticsConfirmed: {result['DiagnosticsConfirmed']}")
    print(f"ArchiveCompleted: {result['ArchiveCompleted']}")
    print(f"ArchiveReady: {result['ArchiveReady']}")
    print(f"Project: {result['Project']}")
    print(f"ArchiveStatus: {result['ArchiveStatus']}")
    print(f"ArchiveMode: {result['ArchiveMode']}")
    print(f"ArchivedPhaseRange: {result['ArchivedPhaseRange']}")
    print(f"FinalReleaseCompleted: {result['FinalReleaseCompleted']}")
    print(f"FinalReleaseReady: {result['FinalReleaseReady']}")
    print(f"ProjectStatus: {result['ProjectStatus']}")
    print(f"WorkspaceOnly: {result['WorkspaceOnly']}")
    print(f"OriginalWrite: {result['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {result['OriginalWriteBlocked']}")
    print(f"HumanApprovalRequired: {result['HumanApprovalRequired']}")
    print(f"PermissionPolicyRequired: {result['PermissionPolicyRequired']}")
    print(f"RiskCount: {result['RiskCount']}")
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"NextPhase: {result['NextPhase']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()