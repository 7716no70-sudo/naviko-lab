from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


PHASE = "Phase29-1 Original Adoption Final Authorization Builder"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def permission_policy_workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "permission_policy_approval_record"


def authorization_workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "original_adoption_final_authorization"


def latest_completion_report() -> Path | None:
    base = permission_policy_workspace_dir()
    if not base.exists():
        return None

    candidates = sorted(
        base.glob("permission_policy_approval_record_completion_report_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_authorization(source_path: Path | None) -> dict:
    completion_report_found = source_path is not None
    completion_report_valid = False

    if source_path is not None:
        source = load_json(source_path)
        completion_report_valid = (
            source.get("PermissionPolicyApprovalRecordCompleted") is True
            and source.get("ReadyForFinalAuthorization") is True
            and source.get("RiskCount") == 0
            and source.get("SafeToContinue") is True
        )

    safe_to_continue = completion_report_found and completion_report_valid

    return {
        "status": "completed" if safe_to_continue else "blocked",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "CompletionReportFound": completion_report_found,
        "CompletionReportValid": completion_report_valid,
        "SourcePath": str(source_path) if source_path else None,
        "FinalAuthorizationRecordCreated": safe_to_continue,
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "HumanApprovalRequired": True,
        "HumanApproved": False,
        "PermissionPolicyRequired": True,
        "PermissionPolicyApproved": False,
        "OriginalAdoptionAllowed": False,
        "PlannerWriteAllowed": False,
        "CapabilityRouterWriteAllowed": False,
        "ConnectorDispatcherWriteAllowed": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "RiskCount": 0 if safe_to_continue else 1,
        "SafeToContinue": safe_to_continue,
        "NextPhase": (
            "Phase29-2 Original Adoption Final Authorization Diagnostics"
            if safe_to_continue
            else "Fix Permission Policy Approval Record Completion Report"
        ),
    }


def save_authorization(record: dict) -> Path:
    out_dir = authorization_workspace_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"original_adoption_final_authorization_{timestamp}.json"
    out_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    source_path = latest_completion_report()
    record = build_authorization(source_path)
    out_path = save_authorization(record)

    print("=== Original Adoption Final Authorization Builder ===")
    print(f"status: {record['status']}")
    print(f"phase: {record['phase']}")
    print(f"CompletionReportFound: {record['CompletionReportFound']}")
    print(f"CompletionReportValid: {record['CompletionReportValid']}")
    print(f"FinalAuthorizationRecordCreated: {record['FinalAuthorizationRecordCreated']}")
    print(f"WorkspaceOnly: {record['WorkspaceOnly']}")
    print(f"OriginalWrite: {record['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {record['OriginalWriteBlocked']}")
    print(f"HumanApprovalRequired: {record['HumanApprovalRequired']}")
    print(f"HumanApproved: {record['HumanApproved']}")
    print(f"PermissionPolicyRequired: {record['PermissionPolicyRequired']}")
    print(f"PermissionPolicyApproved: {record['PermissionPolicyApproved']}")
    print(f"OriginalAdoptionAllowed: {record['OriginalAdoptionAllowed']}")
    print(f"RiskCount: {record['RiskCount']}")
    print(f"SafeToContinue: {record['SafeToContinue']}")
    print(f"保存先: {out_path}")


if __name__ == "__main__":
    main()