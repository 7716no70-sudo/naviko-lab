from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
GATE_DIR = WORKSPACE_DIR / "human_approval_gate"

SOURCE_PATH = GATE_DIR / "human_approval_gate_source.json"
OUTPUT_PATH = GATE_DIR / "human_approval_gate_package.json"

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(SOURCE_PATH)

    package = {
        "status": "completed",
        "phase": "Phase26-2 Human Approval Gate Builder",
        "Project": "Original Naviko AI OS v2.0 Final Release",
        "GateStatus": "built",
        "GateMode": "human_approval_and_permission_policy_required",
        "SourceFound": SOURCE_PATH.exists(),
        "SourceCount": source.get("SourceCount", 0),
        "MissingSourceCount": source.get("MissingSourceCount", 0),
        "AdoptionReadyForHumanApproval": source.get("AdoptionReadyForHumanApproval") is True,
        "HumanApprovalRequired": True,
        "HumanApproved": False,
        "PermissionPolicyRequired": True,
        "PermissionPolicyApproved": False,
        "OriginalAdoptionAllowed": False,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "WorkspaceOnly": True,
        "ApprovalGateConditions": {
            "FinalReleaseReady": True,
            "ArchiveReady": True,
            "HumanApprovalRequired": True,
            "HumanApproved": False,
            "PermissionPolicyRequired": True,
            "PermissionPolicyApproved": False,
            "OriginalWriteBlocked": True,
        },
        "SafetyPolicy": {
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
        },
        "RiskCount": 0,
        "SafeToContinue": (
            source.get("SafeToContinue") is True
            and source.get("RiskCount") == 0
            and source.get("AdoptionReadyForHumanApproval") is True
            and source.get("HumanApproved") is False
            and source.get("PermissionPolicyApproved") is False
            and source.get("OriginalWrite") is False
            and source.get("OriginalWriteBlocked") is True
        ),
        "CollectedSources": source.get("CollectedSources", {}),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(package, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Human Approval Gate Builder ===")
    print(f"status: {package['status']}")
    print(f"phase: {package['phase']}")
    print(f"GateStatus: {package['GateStatus']}")
    print(f"GateMode: {package['GateMode']}")
    print(f"SourceFound: {package['SourceFound']}")
    print(f"SourceCount: {package['SourceCount']}")
    print(f"MissingSourceCount: {package['MissingSourceCount']}")
    print(f"AdoptionReadyForHumanApproval: {package['AdoptionReadyForHumanApproval']}")
    print(f"HumanApprovalRequired: {package['HumanApprovalRequired']}")
    print(f"HumanApproved: {package['HumanApproved']}")
    print(f"PermissionPolicyRequired: {package['PermissionPolicyRequired']}")
    print(f"PermissionPolicyApproved: {package['PermissionPolicyApproved']}")
    print(f"OriginalAdoptionAllowed: {package['OriginalAdoptionAllowed']}")
    print(f"WorkspaceOnly: {package['WorkspaceOnly']}")
    print(f"OriginalWrite: {package['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {package['OriginalWriteBlocked']}")
    print(f"RiskCount: {package['RiskCount']}")
    print(f"SafeToContinue: {package['SafeToContinue']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()