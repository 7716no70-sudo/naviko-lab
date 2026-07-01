from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
GATE_DIR = WORKSPACE_DIR / "human_approval_gate"

PACKAGE_PATH = GATE_DIR / "human_approval_gate_package.json"
DIAGNOSTICS_PATH = GATE_DIR / "human_approval_gate_diagnostics.json"
OUTPUT_PATH = GATE_DIR / "human_approval_gate_completion_report.json"

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
        and package.get("AdoptionReadyForHumanApproval") is True
        and package.get("HumanApprovalRequired") is True
        and package.get("HumanApproved") is False
        and package.get("PermissionPolicyRequired") is True
        and package.get("PermissionPolicyApproved") is False
        and package.get("OriginalAdoptionAllowed") is False
        and safety.get("WorkspaceOnly") is True
        and safety.get("OriginalWrite") is False
        and safety.get("OriginalWriteBlocked") is True
    )

    result = {
        "status": "completed",
        "phase": "Phase26-4 Human Approval Gate Completion Report",
        "PackageFound": package_found,
        "DiagnosticsFound": diagnostics_found,
        "DiagnosticsConfirmed": diagnostics.get("SafeToContinue") is True,
        "HumanApprovalGateCompleted": completed,
        "ReadyForExplicitHumanApproval": completed,
        "Project": package.get("Project"),
        "GateStatus": package.get("GateStatus"),
        "GateMode": package.get("GateMode"),
        "AdoptionReadyForHumanApproval": package.get("AdoptionReadyForHumanApproval"),
        "HumanApprovalRequired": package.get("HumanApprovalRequired"),
        "HumanApproved": package.get("HumanApproved"),
        "PermissionPolicyRequired": package.get("PermissionPolicyRequired"),
        "PermissionPolicyApproved": package.get("PermissionPolicyApproved"),
        "OriginalAdoptionAllowed": package.get("OriginalAdoptionAllowed"),
        "WorkspaceOnly": safety.get("WorkspaceOnly"),
        "OriginalWrite": safety.get("OriginalWrite"),
        "OriginalWriteBlocked": safety.get("OriginalWriteBlocked"),
        "AutoPatch": safety.get("AutoPatch"),
        "FileDelete": safety.get("FileDelete"),
        "ExternalOperation": safety.get("ExternalOperation"),
        "RealGUIOperation": safety.get("RealGUIOperation"),
        "ReadOnlyReference": safety.get("ReadOnlyReference"),
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": "Phase27 Explicit Human Approval Record",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Human Approval Gate Completion Report ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"PackageFound: {result['PackageFound']}")
    print(f"DiagnosticsFound: {result['DiagnosticsFound']}")
    print(f"DiagnosticsConfirmed: {result['DiagnosticsConfirmed']}")
    print(f"HumanApprovalGateCompleted: {result['HumanApprovalGateCompleted']}")
    print(f"ReadyForExplicitHumanApproval: {result['ReadyForExplicitHumanApproval']}")
    print(f"Project: {result['Project']}")
    print(f"GateStatus: {result['GateStatus']}")
    print(f"GateMode: {result['GateMode']}")
    print(f"AdoptionReadyForHumanApproval: {result['AdoptionReadyForHumanApproval']}")
    print(f"HumanApprovalRequired: {result['HumanApprovalRequired']}")
    print(f"HumanApproved: {result['HumanApproved']}")
    print(f"PermissionPolicyRequired: {result['PermissionPolicyRequired']}")
    print(f"PermissionPolicyApproved: {result['PermissionPolicyApproved']}")
    print(f"OriginalAdoptionAllowed: {result['OriginalAdoptionAllowed']}")
    print(f"WorkspaceOnly: {result['WorkspaceOnly']}")
    print(f"OriginalWrite: {result['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {result['OriginalWriteBlocked']}")
    print(f"RiskCount: {result['RiskCount']}")
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"NextPhase: {result['NextPhase']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()