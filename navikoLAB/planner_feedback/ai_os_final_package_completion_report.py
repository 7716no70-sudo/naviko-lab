from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
PACKAGE_DIR = WORKSPACE_DIR / "ai_os_final_package"

PACKAGE_PATH = PACKAGE_DIR / "ai_os_final_package.json"
DIAGNOSTICS_PATH = PACKAGE_DIR / "ai_os_final_package_diagnostics.json"
OUTPUT_PATH = PACKAGE_DIR / "ai_os_final_package_completion_report.json"

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
        and safety.get("WorkspaceOnly") is True
        and safety.get("OriginalWrite") is False
        and safety.get("HumanApprovalRequired") is True
        and safety.get("PermissionPolicyRequired") is True
    )

    result = {
        "status": "completed",
        "phase": "Phase21-4 AI OS Final Package Completion Report",
        "PackageFound": package_found,
        "DiagnosticsFound": diagnostics_found,
        "DiagnosticsConfirmed": diagnostics.get("SafeToContinue") is True,
        "FinalPackageCompleted": completed,
        "FinalPackageReady": completed,
        "Project": package.get("Project"),
        "PackageStatus": package.get("PackageStatus"),
        "SourceCount": package.get("SourceCount"),
        "MissingSourceCount": package.get("MissingSourceCount"),
        "AIOSStabilityReady": package.get("AIOSStabilityReady"),
        "WorkspaceOnly": safety.get("WorkspaceOnly") is True,
        "OriginalWrite": safety.get("OriginalWrite") is True,
        "OriginalWriteBlocked": safety.get("OriginalWrite") is False,
        "PlannerWriteAllowed": safety.get("PlannerWriteAllowed") is True,
        "CapabilityRouterWriteAllowed": safety.get("CapabilityRouterWriteAllowed") is True,
        "ConnectorDispatcherWriteAllowed": safety.get("ConnectorDispatcherWriteAllowed") is True,
        "FileDelete": safety.get("FileDelete") is True,
        "ExternalOperation": safety.get("ExternalOperation") is True,
        "RealGUIOperation": safety.get("RealGUIOperation") is True,
        "HumanApprovalRequired": safety.get("HumanApprovalRequired") is True,
        "PermissionPolicyRequired": safety.get("PermissionPolicyRequired") is True,
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": "Phase22 Original Naviko AI OS Release Candidate Finalization",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== AI OS Final Package Completion Report ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"PackageFound: {result['PackageFound']}")
    print(f"DiagnosticsFound: {result['DiagnosticsFound']}")
    print(f"DiagnosticsConfirmed: {result['DiagnosticsConfirmed']}")
    print(f"FinalPackageCompleted: {result['FinalPackageCompleted']}")
    print(f"FinalPackageReady: {result['FinalPackageReady']}")
    print(f"Project: {result['Project']}")
    print(f"PackageStatus: {result['PackageStatus']}")
    print(f"SourceCount: {result['SourceCount']}")
    print(f"MissingSourceCount: {result['MissingSourceCount']}")
    print(f"AIOSStabilityReady: {result['AIOSStabilityReady']}")
    print(f"WorkspaceOnly: {safety.get('WorkspaceOnly')}")
    print(f"OriginalWrite: {safety.get('OriginalWrite')}")
    print(f"OriginalWriteBlocked: {result['OriginalWriteBlocked']}")
    print(f"HumanApprovalRequired: {result['HumanApprovalRequired']}")
    print(f"PermissionPolicyRequired: {result['PermissionPolicyRequired']}")
    print(f"RiskCount: {result['RiskCount']}")
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"NextPhase: {result['NextPhase']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()