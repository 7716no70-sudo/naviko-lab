from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
RC_DIR = WORKSPACE_DIR / "original_ai_os_rc_finalization"

PACKAGE_PATH = RC_DIR / "original_ai_os_rc_finalization_package.json"
DIAGNOSTICS_PATH = RC_DIR / "original_ai_os_rc_finalization_diagnostics.json"
OUTPUT_PATH = RC_DIR / "original_ai_os_rc_finalization_completion_report.json"

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
        and package.get("ReleaseCandidateReady") is True
        and safety.get("WorkspaceOnly") is True
        and safety.get("OriginalWrite") is False
        and safety.get("OriginalWriteBlocked") is True
        and safety.get("HumanApprovalRequired") is True
        and safety.get("PermissionPolicyRequired") is True
    )

    result = {
        "status": "completed",
        "phase": "Phase22-4 Original Naviko AI OS RC Finalization Completion Report",
        "PackageFound": package_found,
        "DiagnosticsFound": diagnostics_found,
        "DiagnosticsConfirmed": diagnostics.get("SafeToContinue") is True,
        "RCFinalizationCompleted": completed,
        "ReleaseCandidateReady": completed,
        "Project": package.get("Project"),
        "RCFinalizationStatus": package.get("RCFinalizationStatus"),
        "ReleaseCandidateMode": package.get("ReleaseCandidateMode"),
        "FinalizedPhaseRange": package.get("FinalizedPhaseRange"),
        "SourceCount": package.get("SourceCount"),
        "MissingSourceCount": package.get("MissingSourceCount"),
        "FinalPackageReady": package.get("FinalPackageReady"),
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
        "NextPhase": "Phase23 Original Naviko AI OS Final Release Report",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Original Naviko AI OS RC Finalization Completion Report ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"PackageFound: {result['PackageFound']}")
    print(f"DiagnosticsFound: {result['DiagnosticsFound']}")
    print(f"DiagnosticsConfirmed: {result['DiagnosticsConfirmed']}")
    print(f"RCFinalizationCompleted: {result['RCFinalizationCompleted']}")
    print(f"ReleaseCandidateReady: {result['ReleaseCandidateReady']}")
    print(f"Project: {result['Project']}")
    print(f"RCFinalizationStatus: {result['RCFinalizationStatus']}")
    print(f"ReleaseCandidateMode: {result['ReleaseCandidateMode']}")
    print(f"FinalizedPhaseRange: {result['FinalizedPhaseRange']}")
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
    print(f"NextPhase: {result['NextPhase']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()