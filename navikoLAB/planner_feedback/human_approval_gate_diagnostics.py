from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
GATE_DIR = WORKSPACE_DIR / "human_approval_gate"

PACKAGE_PATH = GATE_DIR / "human_approval_gate_package.json"
OUTPUT_PATH = GATE_DIR / "human_approval_gate_diagnostics.json"

REQUIRED_KEYS = [
    "status",
    "phase",
    "Project",
    "GateStatus",
    "GateMode",
    "SourceFound",
    "SourceCount",
    "MissingSourceCount",
    "AdoptionReadyForHumanApproval",
    "HumanApprovalRequired",
    "HumanApproved",
    "PermissionPolicyRequired",
    "PermissionPolicyApproved",
    "OriginalAdoptionAllowed",
    "OriginalWrite",
    "OriginalWriteBlocked",
    "WorkspaceOnly",
    "ApprovalGateConditions",
    "SafetyPolicy",
    "RiskCount",
    "SafeToContinue",
    "CollectedSources",
]

REQUIRED_SAFETY = {
    "WorkspaceOnly": True,
    "OriginalWrite": False,
    "OriginalWriteBlocked": True,
    "OriginalAdoptionAllowed": False,
    "PlannerWriteAllowed": False,
    "CapabilityRouterWriteAllowed": False,
    "ConnectorDispatcherWriteAllowed": False,
    "AutoPatch": False,
    "FileDelete": False,
    "ExternalOperation": False,
    "RealGUIOperation": False,
    "HumanApprovalRequired": True,
    "HumanApproved": False,
    "PermissionPolicyRequired": True,
    "PermissionPolicyApproved": False,
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
        and package.get("GateStatus") == "built"
        and package.get("GateMode") == "human_approval_and_permission_policy_required"
        and package.get("SourceFound") is True
        and package.get("SourceCount") == 1
        and package.get("MissingSourceCount") == 0
        and package.get("AdoptionReadyForHumanApproval") is True
        and package.get("HumanApprovalRequired") is True
        and package.get("HumanApproved") is False
        and package.get("PermissionPolicyRequired") is True
        and package.get("PermissionPolicyApproved") is False
        and package.get("OriginalAdoptionAllowed") is False
        and package.get("OriginalWrite") is False
        and package.get("OriginalWriteBlocked") is True
        and package.get("WorkspaceOnly") is True
        and package.get("RiskCount") == 0
        and package.get("SafeToContinue") is True
    )

    result = {
        "status": "completed",
        "phase": "Phase26-3 Human Approval Gate Diagnostics",
        "PackageFound": package_found,
        "RequiredKeysOK": len(missing_keys) == 0,
        "MissingKeys": missing_keys,
        "SafetyPolicyOK": len(safety_mismatches) == 0,
        "SafetyMismatches": safety_mismatches,
        "GateStatusOK": package.get("GateStatus") == "built",
        "GateModeOK": package.get("GateMode") == "human_approval_and_permission_policy_required",
        "SourceFound": package.get("SourceFound") is True,
        "SourceCountOK": package.get("SourceCount") == 1,
        "MissingSourceCountOK": package.get("MissingSourceCount") == 0,
        "AdoptionReadyForHumanApproval": package.get("AdoptionReadyForHumanApproval"),
        "HumanApprovalRequired": package.get("HumanApprovalRequired"),
        "HumanApproved": package.get("HumanApproved"),
        "PermissionPolicyRequired": package.get("PermissionPolicyRequired"),
        "PermissionPolicyApproved": package.get("PermissionPolicyApproved"),
        "OriginalAdoptionAllowed": package.get("OriginalAdoptionAllowed"),
        "WorkspaceOnly": package.get("WorkspaceOnly"),
        "OriginalWrite": package.get("OriginalWrite"),
        "OriginalWriteBlocked": package.get("OriginalWriteBlocked"),
        "RiskCount": 0 if diagnostics_ok else 1,
        "SafeToContinue": diagnostics_ok,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Human Approval Gate Diagnostics ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"PackageFound: {result['PackageFound']}")
    print(f"RequiredKeysOK: {result['RequiredKeysOK']}")
    print(f"SafetyPolicyOK: {result['SafetyPolicyOK']}")
    print(f"GateStatusOK: {result['GateStatusOK']}")
    print(f"GateModeOK: {result['GateModeOK']}")
    print(f"SourceFound: {result['SourceFound']}")
    print(f"SourceCountOK: {result['SourceCountOK']}")
    print(f"MissingSourceCountOK: {result['MissingSourceCountOK']}")
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
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()