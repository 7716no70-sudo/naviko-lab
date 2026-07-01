from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
APPROVAL_DIR = WORKSPACE_DIR / "explicit_human_approval_record"

RECORD_PATH = APPROVAL_DIR / "explicit_human_approval_record.json"
OUTPUT_PATH = APPROVAL_DIR / "explicit_human_approval_record_diagnostics.json"

REQUIRED_KEYS = [
    "status",
    "phase",
    "Project",
    "ApprovalRecordStatus",
    "ApprovalMode",
    "SourceFound",
    "SourceCount",
    "MissingSourceCount",
    "ReadyForExplicitHumanApproval",
    "HumanApprovalRequired",
    "HumanApproved",
    "HumanApprovalRecordCreated",
    "PermissionPolicyRequired",
    "PermissionPolicyApproved",
    "OriginalAdoptionAllowed",
    "WorkspaceOnly",
    "OriginalWrite",
    "OriginalWriteBlocked",
    "ApprovalNote",
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
    record_found = RECORD_PATH.exists()
    record = load_json(RECORD_PATH) if record_found else {}

    missing_keys = [key for key in REQUIRED_KEYS if key not in record]

    safety = record.get("SafetyPolicy", {})
    safety_mismatches = {
        key: {"expected": expected, "actual": safety.get(key)}
        for key, expected in REQUIRED_SAFETY.items()
        if safety.get(key) != expected
    }

    diagnostics_ok = (
        record_found
        and not missing_keys
        and not safety_mismatches
        and record.get("ApprovalRecordStatus") == "built"
        and record.get("ApprovalMode") == "explicit_human_approval_record_required"
        and record.get("SourceFound") is True
        and record.get("SourceCount") == 1
        and record.get("MissingSourceCount") == 0
        and record.get("ReadyForExplicitHumanApproval") is True
        and record.get("HumanApprovalRequired") is True
        and record.get("HumanApproved") is False
        and record.get("HumanApprovalRecordCreated") is True
        and record.get("PermissionPolicyRequired") is True
        and record.get("PermissionPolicyApproved") is False
        and record.get("OriginalAdoptionAllowed") is False
        and record.get("WorkspaceOnly") is True
        and record.get("OriginalWrite") is False
        and record.get("OriginalWriteBlocked") is True
        and record.get("RiskCount") == 0
        and record.get("SafeToContinue") is True
    )

    result = {
        "status": "completed",
        "phase": "Phase27-3 Explicit Human Approval Record Diagnostics",
        "RecordFound": record_found,
        "RequiredKeysOK": len(missing_keys) == 0,
        "MissingKeys": missing_keys,
        "SafetyPolicyOK": len(safety_mismatches) == 0,
        "SafetyMismatches": safety_mismatches,
        "ApprovalRecordStatusOK": record.get("ApprovalRecordStatus") == "built",
        "ApprovalModeOK": record.get("ApprovalMode") == "explicit_human_approval_record_required",
        "SourceFound": record.get("SourceFound") is True,
        "SourceCountOK": record.get("SourceCount") == 1,
        "MissingSourceCountOK": record.get("MissingSourceCount") == 0,
        "ReadyForExplicitHumanApproval": record.get("ReadyForExplicitHumanApproval"),
        "HumanApprovalRequired": record.get("HumanApprovalRequired"),
        "HumanApproved": record.get("HumanApproved"),
        "HumanApprovalRecordCreated": record.get("HumanApprovalRecordCreated"),
        "PermissionPolicyRequired": record.get("PermissionPolicyRequired"),
        "PermissionPolicyApproved": record.get("PermissionPolicyApproved"),
        "OriginalAdoptionAllowed": record.get("OriginalAdoptionAllowed"),
        "WorkspaceOnly": record.get("WorkspaceOnly"),
        "OriginalWrite": record.get("OriginalWrite"),
        "OriginalWriteBlocked": record.get("OriginalWriteBlocked"),
        "RiskCount": 0 if diagnostics_ok else 1,
        "SafeToContinue": diagnostics_ok,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Explicit Human Approval Record Diagnostics ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"RecordFound: {result['RecordFound']}")
    print(f"RequiredKeysOK: {result['RequiredKeysOK']}")
    print(f"SafetyPolicyOK: {result['SafetyPolicyOK']}")
    print(f"ApprovalRecordStatusOK: {result['ApprovalRecordStatusOK']}")
    print(f"ApprovalModeOK: {result['ApprovalModeOK']}")
    print(f"SourceFound: {result['SourceFound']}")
    print(f"SourceCountOK: {result['SourceCountOK']}")
    print(f"MissingSourceCountOK: {result['MissingSourceCountOK']}")
    print(f"ReadyForExplicitHumanApproval: {result['ReadyForExplicitHumanApproval']}")
    print(f"HumanApprovalRequired: {result['HumanApprovalRequired']}")
    print(f"HumanApproved: {result['HumanApproved']}")
    print(f"HumanApprovalRecordCreated: {result['HumanApprovalRecordCreated']}")
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