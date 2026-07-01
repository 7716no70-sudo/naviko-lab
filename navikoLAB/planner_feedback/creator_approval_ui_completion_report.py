from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase42-3 Creator Approval UI Completion Report"
ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"


def load_latest_diagnostics():
    files = sorted(
        REPORT_DIR.glob("creator_approval_ui_diagnostics_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not files:
        return None, None

    path = files[0]
    try:
        return path, json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return path, None


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    diagnostics_path, diagnostics = load_latest_diagnostics()
    diagnostics_found = diagnostics is not None

    diagnostics_confirmed = bool(
        diagnostics
        and diagnostics.get("status") == "completed"
        and diagnostics.get("CreatorApprovalUIReady") is True
        and diagnostics.get("RequiredApprovalActionsComplete") is True
        and diagnostics.get("RequiredApprovalFlowStepsComplete") is True
        and diagnostics.get("RequiredApprovalRecordSchemaComplete") is True
        and diagnostics.get("WorkspaceOnly") is True
        and diagnostics.get("OriginalWrite") is False
        and diagnostics.get("OriginalWriteBlocked") is True
        and diagnostics.get("OriginalAdoptionAllowed") is False
        and diagnostics.get("ExternalOperation") is False
        and diagnostics.get("RealGUIOperation") is False
        and diagnostics.get("FileDelete") is False
        and diagnostics.get("HumanApprovalRequiredForOriginalAdoption") is True
        and diagnostics.get("HumanApproved") is False
        and diagnostics.get("PermissionPolicyRequired") is True
        and diagnostics.get("PermissionPolicyApproved") is False
        and diagnostics.get("AutomaticValidationRequired") is True
        and diagnostics.get("RiskCount") == 0
        and diagnostics.get("SafeToContinue") is True
    )

    completed = diagnostics_found and diagnostics_confirmed

    report = {
        "status": "completed" if completed else "blocked",
        "phase": PHASE,
        "DiagnosticsFound": diagnostics_found,
        "DiagnosticsConfirmed": diagnostics_confirmed,
        "CreatorApprovalUICompleted": completed,
        "CreatorApprovalUIReady": completed,
        "ApprovalUIMode": "safe_workspace_only_creator_approval_ui",
        "ApprovalUIStatus": "ready_for_creator_review_records",
        "ApprovalActions": [
            "approve",
            "reject",
            "hold",
            "request_more_validation",
            "request_permission_policy_review",
        ],
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "OriginalAdoptionAllowed": False,
        "HumanApprovalRequiredForOriginalAdoption": True,
        "HumanApproved": False,
        "PermissionPolicyRequired": True,
        "PermissionPolicyApproved": False,
        "AutomaticValidationRequired": True,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": "Phase43 Original Safe Adoption"
        if completed
        else "Review Phase42-2 Diagnostics",
        "source_diagnostics_path": str(diagnostics_path) if diagnostics_path else None,
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"creator_approval_ui_completion_report_{ts}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Creator Approval UI Completion Report ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"保存先: {report_path}")


if __name__ == "__main__":
    main()