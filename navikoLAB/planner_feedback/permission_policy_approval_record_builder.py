from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
POLICY_DIR = WORKSPACE_DIR / "permission_policy_approval_record"

SOURCE_PATH = POLICY_DIR / "permission_policy_approval_record_source.json"
OUTPUT_PATH = POLICY_DIR / "permission_policy_approval_record.json"

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(SOURCE_PATH)

    record = {
        "status": "completed",
        "phase": "Phase28-2 Permission Policy Approval Record Builder",
        "Project": "Original Naviko AI OS v2.0 Final Release",
        "PermissionPolicyRecordStatus": "built",
        "PermissionPolicyMode": "permission_policy_approval_required",
        "SourceFound": SOURCE_PATH.exists(),
        "SourceCount": source.get("SourceCount", 0),
        "MissingSourceCount": source.get("MissingSourceCount", 0),
        "ReadyForPermissionPolicyApproval": source.get("ReadyForPermissionPolicyApproval") is True,
        "HumanApprovalRequired": True,
        "HumanApproved": False,
        "PermissionPolicyRequired": True,
        "PermissionPolicyApproved": False,
        "PermissionPolicyRecordCreated": True,
        "OriginalAdoptionAllowed": False,
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "PermissionPolicyNote": "Permission policy approval is required before Original adoption. This record does not grant approval.",
        "SafetyPolicy": {
            "WorkspaceOnly": True,
            "OriginalWrite": False,
            "OriginalWriteBlocked": True,
            "OriginalAdoptionAllowed": False,
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
            and source.get("HumanApproved") is False
            and source.get("PermissionPolicyApproved") is False
            and source.get("OriginalWrite") is False
            and source.get("OriginalWriteBlocked") is True
        ),
        "CollectedSources": source.get("CollectedSources", {}),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Permission Policy Approval Record Builder ===")
    print(f"status: {record['status']}")
    print(f"phase: {record['phase']}")
    print(f"PermissionPolicyRecordStatus: {record['PermissionPolicyRecordStatus']}")
    print(f"PermissionPolicyMode: {record['PermissionPolicyMode']}")
    print(f"SourceFound: {record['SourceFound']}")
    print(f"SourceCount: {record['SourceCount']}")
    print(f"MissingSourceCount: {record['MissingSourceCount']}")
    print(f"ReadyForPermissionPolicyApproval: {record['ReadyForPermissionPolicyApproval']}")
    print(f"HumanApprovalRequired: {record['HumanApprovalRequired']}")
    print(f"HumanApproved: {record['HumanApproved']}")
    print(f"PermissionPolicyRequired: {record['PermissionPolicyRequired']}")
    print(f"PermissionPolicyApproved: {record['PermissionPolicyApproved']}")
    print(f"PermissionPolicyRecordCreated: {record['PermissionPolicyRecordCreated']}")
    print(f"OriginalAdoptionAllowed: {record['OriginalAdoptionAllowed']}")
    print(f"WorkspaceOnly: {record['WorkspaceOnly']}")
    print(f"OriginalWrite: {record['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {record['OriginalWriteBlocked']}")
    print(f"RiskCount: {record['RiskCount']}")
    print(f"SafeToContinue: {record['SafeToContinue']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()