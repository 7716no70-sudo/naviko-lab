from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


PHASE = "Phase28-4 Permission Policy Approval Record Completion Report"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def workspace_dir() -> Path:
    return (
        project_root()
        / "navikoLAB"
        / "workspace"
        / "permission_policy_approval_record"
    )


def latest(pattern: str) -> Path | None:
    files = sorted(
        workspace_dir().glob(pattern),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return files[0] if files else None


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main():

    workspace_dir().mkdir(parents=True, exist_ok=True)

    source = latest("permission_policy_approval_record_source*.json")
    record = latest("permission_policy_approval_record_*.json")
    diagnostics = latest("permission_policy_approval_record_diagnostics_*.json")

    source_found = source is not None
    record_found = record is not None
    diagnostics_found = diagnostics is not None

    diagnostics_passed = False

    if diagnostics_found:
        diagnostics_json = load_json(diagnostics)
        diagnostics_passed = diagnostics_json.get(
            "DiagnosticsPassed", False
        )

    completed = (
        source_found
        and record_found
        and diagnostics_found
        and diagnostics_passed
    )

    report = {
        "status": "completed" if completed else "blocked",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),

        "SourceCollectorFound": source_found,
        "ApprovalRecordFound": record_found,
        "DiagnosticsFound": diagnostics_found,
        "DiagnosticsPassed": diagnostics_passed,

        "PermissionPolicyApprovalRecordCompleted": completed,
        "ReadyForFinalAuthorization": completed,

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

        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,

        "NextPhase": (
            "Phase29 Original Adoption Final Authorization"
            if completed
            else "Fix Permission Policy Approval Record"
        ),
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    save_path = (
        workspace_dir()
        / f"permission_policy_approval_record_completion_report_{timestamp}.json"
    )

    save_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Permission Policy Approval Record Completion Report ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"SourceCollectorFound: {report['SourceCollectorFound']}")
    print(f"ApprovalRecordFound: {report['ApprovalRecordFound']}")
    print(f"DiagnosticsFound: {report['DiagnosticsFound']}")
    print(f"DiagnosticsPassed: {report['DiagnosticsPassed']}")
    print(
        "PermissionPolicyApprovalRecordCompleted:",
        report["PermissionPolicyApprovalRecordCompleted"],
    )
    print(
        "ReadyForFinalAuthorization:",
        report["ReadyForFinalAuthorization"],
    )
    print(f"WorkspaceOnly: {report['WorkspaceOnly']}")
    print(f"OriginalWrite: {report['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {report['OriginalWriteBlocked']}")
    print(f"HumanApprovalRequired: {report['HumanApprovalRequired']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(f"PermissionPolicyRequired: {report['PermissionPolicyRequired']}")
    print(f"PermissionPolicyApproved: {report['PermissionPolicyApproved']}")
    print(f"OriginalAdoptionAllowed: {report['OriginalAdoptionAllowed']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"保存先: {save_path}")


if __name__ == "__main__":
    main()