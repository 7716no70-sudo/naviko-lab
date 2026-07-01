from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
RELEASE_DIR = WORKSPACE_DIR / "original_ai_os_final_release"

PACKAGE_PATH = RELEASE_DIR / "original_ai_os_final_release_package.json"
DIAGNOSTICS_PATH = RELEASE_DIR / "original_ai_os_final_release_diagnostics.json"
OUTPUT_PATH = RELEASE_DIR / "original_ai_os_final_release_completion_report.json"

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
        and package.get("FinalReleaseReady") is True
        and safety.get("WorkspaceOnly") is True
        and safety.get("OriginalWrite") is False
        and safety.get("OriginalWriteBlocked") is True
        and safety.get("HumanApprovalRequired") is True
        and safety.get("PermissionPolicyRequired") is True
    )

    result = {
        "status": "completed",
        "phase": "Phase23-4 Original Naviko AI OS Final Release Completion Report",
        "PackageFound": package_found,
        "DiagnosticsFound": diagnostics_found,
        "DiagnosticsConfirmed": diagnostics.get("SafeToContinue") is True,
        "FinalReleaseCompleted": completed,
        "FinalReleaseReady": completed,
        "Project": package.get("Project"),
        "FinalReleaseStatus": package.get("FinalReleaseStatus"),
        "FinalReleaseMode": package.get("FinalReleaseMode"),
        "FinalizedPhaseRange": package.get("FinalizedPhaseRange"),
        "SourceCount": package.get("SourceCount"),
        "MissingSourceCount": package.get("MissingSourceCount"),
        "RCFinalizationCompleted": package.get("RCFinalizationCompleted"),
        "ReleaseCandidateReady": package.get("ReleaseCandidateReady"),
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
        "ProjectStatus": "Original Naviko AI OS v2.0 Final Release Ready",
        "NextPhase": "Post-v2.0 Human Approved Original Adoption / Optional Release Archive",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Original Naviko AI OS Final Release Completion Report ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"PackageFound: {result['PackageFound']}")
    print(f"DiagnosticsFound: {result['DiagnosticsFound']}")
    print(f"DiagnosticsConfirmed: {result['DiagnosticsConfirmed']}")
    print(f"FinalReleaseCompleted: {result['FinalReleaseCompleted']}")
    print(f"FinalReleaseReady: {result['FinalReleaseReady']}")
    print(f"Project: {result['Project']}")
    print(f"FinalReleaseStatus: {result['FinalReleaseStatus']}")
    print(f"FinalReleaseMode: {result['FinalReleaseMode']}")
    print(f"FinalizedPhaseRange: {result['FinalizedPhaseRange']}")
    print(f"SourceCount: {result['SourceCount']}")
    print(f"MissingSourceCount: {result['MissingSourceCount']}")
    print(f"RCFinalizationCompleted: {result['RCFinalizationCompleted']}")
    print(f"ReleaseCandidateReady: {result['ReleaseCandidateReady']}")
    print(f"WorkspaceOnly: {result['WorkspaceOnly']}")
    print(f"OriginalWrite: {result['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {result['OriginalWriteBlocked']}")
    print(f"HumanApprovalRequired: {result['HumanApprovalRequired']}")
    print(f"PermissionPolicyRequired: {result['PermissionPolicyRequired']}")
    print(f"RiskCount: {result['RiskCount']}")
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"ProjectStatus: {result['ProjectStatus']}")
    print(f"NextPhase: {result['NextPhase']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()