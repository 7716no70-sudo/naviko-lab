from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
APPROVAL_DIR = WORKSPACE_DIR / "explicit_human_approval_record"

RECORD_PATH = APPROVAL_DIR / "explicit_human_approval_record.json"
DIAGNOSTICS_PATH = APPROVAL_DIR / "explicit_human_approval_record_diagnostics.json"
OUTPUT_PATH = APPROVAL_DIR / "explicit_human_approval_record_completion_report.json"

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    record_found = RECORD_PATH.exists()
    diagnostics_found = DIAGNOSTICS_PATH.exists()

    record = load_json(RECORD_PATH) if record_found else {}
    diagnostics = load_json(DIAGNOSTICS_PATH) if diagnostics_found else {}

    safety = record.get("SafetyPolicy", {})

    completed = (
        record_found
        and diagnostics_found
        and diagnostics.get("SafeToContinue") is True
        and diagnostics.get("RiskCount") == 0
        and record.get("ReadyForExplicitHumanApproval") is True
        and record.get("HumanApprovalRequired") is True
        and record.get("HumanApproved") is False
        and record.get("HumanApprovalRecordCreated") is True
        and record.get("PermissionPolicyRequired") is True
        and record.get("PermissionPolicyApproved") is False
        and record.get("OriginalAdoptionAllowed") is False
        and safety.get("WorkspaceOnly") is True
        and safety.get("OriginalWrite") is False
        and safety.get("OriginalWriteBlocked") is True
    )

    result = {
        "status": "completed",
        "phase": "Phase27-4 Explicit Human Approval Record Completion Report",
        "RecordFound": record_found,
        "DiagnosticsFound": diagnostics_found,
        "DiagnosticsConfirmed": diagnostics.get("SafeToContinue") is True,
        "ExplicitHumanApprovalRecordCompleted": completed,
        "ReadyForPermissionPolicyApproval": completed,
        "Project": record.get("Project"),
        "ApprovalRecordStatus": record.get("ApprovalRecordStatus"),
        "ApprovalMode": record.get("ApprovalMode"),
        "ReadyForExplicitHumanApproval": record.get("ReadyForExplicitHumanApproval"),
        "HumanApprovalRequired": record.get("HumanApprovalRequired"),
        "HumanApproved": record.get("HumanApproved"),
        "HumanApprovalRecordCreated": record.get("HumanApprovalRecordCreated"),
        "PermissionPolicyRequired": record.get("PermissionPolicyRequired"),
        "PermissionPolicyApproved": record.get("PermissionPolicyApproved"),
        "OriginalAdoptionAllowed": record.get("OriginalAdoptionAllowed"),
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
        "NextPhase": "Phase28 Permission Policy Approval Record",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Explicit Human Approval Record Completion Report ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"RecordFound: {result['RecordFound']}")
    print(f"DiagnosticsFound: {result['DiagnosticsFound']}")
    print(f"DiagnosticsConfirmed: {result['DiagnosticsConfirmed']}")
    print(f"ExplicitHumanApprovalRecordCompleted: {result['ExplicitHumanApprovalRecordCompleted']}")
    print(f"ReadyForPermissionPolicyApproval: {result['ReadyForPermissionPolicyApproval']}")
    print(f"Project: {result['Project']}")
    print(f"ApprovalRecordStatus: {result['ApprovalRecordStatus']}")
    print(f"ApprovalMode: {result['ApprovalMode']}")
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