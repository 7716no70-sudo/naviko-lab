from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase41-3 Original Adoption Queue Completion Report"
ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"


def load_latest_diagnostics():
    files = sorted(
        REPORT_DIR.glob("original_adoption_queue_diagnostics_*.json"),
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
        and diagnostics.get("OriginalAdoptionQueueReady") is True
        and diagnostics.get("RequiredQueueStepsComplete") is True
        and diagnostics.get("RequiredQueueStatusesComplete") is True
        and diagnostics.get("RequiredQueueSchemaComplete") is True
        and diagnostics.get("AutoExecutableRiskLevels") == [0, 1]
        and diagnostics.get("ApprovalRequiredRiskLevels") == [2, 3]
        and diagnostics.get("BlockedRiskLevels") == [4]
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
        "OriginalAdoptionQueueCompleted": completed,
        "OriginalAdoptionQueueReady": completed,
        "QueueMode": "safe_workspace_only_original_adoption_queue",
        "QueueStatus": "ready_for_approval_management",
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "OriginalAdoptionAllowed": False,
        "HumanApprovalRequiredForOriginalAdoption": True,
        "HumanApproved": False,
        "PermissionPolicyRequired": True,
        "PermissionPolicyApproved": False,
        "AutomaticValidationRequired": True,
        "AutoExecutableRiskLevels": [0, 1],
        "ApprovalRequiredRiskLevels": [2, 3],
        "BlockedRiskLevels": [4],
        "WorkspaceOnly": True,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": "Phase42 Creator Approval UI"
        if completed
        else "Review Phase41-2 Diagnostics",
        "source_diagnostics_path": str(diagnostics_path) if diagnostics_path else None,
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"original_adoption_queue_completion_report_{ts}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Original Adoption Queue Completion Report ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"保存先: {report_path}")


if __name__ == "__main__":
    main()