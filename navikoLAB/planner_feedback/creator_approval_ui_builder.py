from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase42-1 Creator Approval UI Builder"
ROOT = Path(__file__).resolve().parents[2]

WORKSPACE = ROOT / "navikoLAB" / "workspace"
APPROVAL_UI_DIR = WORKSPACE / "creator_approval_ui"
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"


def load_latest_phase41_completion():
    files = sorted(
        REPORT_DIR.glob("original_adoption_queue_completion_report_*.json"),
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
    APPROVAL_UI_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    phase41_path, phase41 = load_latest_phase41_completion()

    phase41_ready = bool(
        phase41
        and phase41.get("status") == "completed"
        and phase41.get("OriginalAdoptionQueueReady") is True
        and phase41.get("WorkspaceOnly") is True
        and phase41.get("OriginalWrite") is False
        and phase41.get("OriginalWriteBlocked") is True
        and phase41.get("OriginalAdoptionAllowed") is False
        and phase41.get("HumanApproved") is False
        and phase41.get("PermissionPolicyApproved") is False
        and phase41.get("RiskCount") == 0
        and phase41.get("SafeToContinue") is True
    )

    approval_ui = {
        "phase": PHASE,
        "CreatorApprovalUICreated": phase41_ready,
        "CreatorApprovalUIReady": phase41_ready,
        "ApprovalUIMode": "safe_workspace_only_creator_approval_ui",
        "ApprovalUIPurpose": "Allow creator review records without writing to Original.",
        "ApprovalActions": [
            "approve",
            "reject",
            "hold",
            "request_more_validation",
            "request_permission_policy_review",
        ],
        "ApprovalRecordSchema": {
            "approval_id": "string",
            "candidate_id": "string",
            "creator_action": "approve_or_reject_or_hold",
            "creator_comment": "string",
            "human_approved": False,
            "permission_policy_approved": False,
            "original_write_allowed": False,
            "created_at": "iso_datetime",
        },
        "ApprovalFlowSteps": [
            "LoadOriginalAdoptionQueue",
            "DisplayCandidateSummary",
            "DisplayRiskClassification",
            "DisplayValidationResult",
            "CreatorSelectAction",
            "SaveApprovalRecord",
            "KeepOriginalWriteBlocked",
            "PassToOriginalSafeAdoptionOnlyAfterApproval",
        ],
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "OriginalAdoptionAllowed": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "HumanApprovalRequiredForOriginalAdoption": True,
        "HumanApproved": False,
        "PermissionPolicyRequired": True,
        "PermissionPolicyApproved": False,
        "AutomaticValidationRequired": True,
        "RiskCount": 0 if phase41_ready else 1,
        "SafeToContinue": phase41_ready,
        "SourcePhase41CompletionPath": str(phase41_path) if phase41_path else None,
        "NextPhase": "Phase42-2 Creator Approval UI Diagnostics"
        if phase41_ready
        else "Review Phase41 Completion Report",
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    ui_path = APPROVAL_UI_DIR / f"creator_approval_ui_{ts}.json"
    ui_path.write_text(json.dumps(approval_ui, ensure_ascii=False, indent=2), encoding="utf-8")

    report_path = REPORT_DIR / f"creator_approval_ui_builder_report_{ts}.json"
    report_path.write_text(json.dumps(approval_ui, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Creator Approval UI Builder ===")
    print(f"status: {'completed' if phase41_ready else 'blocked'}")
    for key, value in approval_ui.items():
        print(f"{key}: {value}")
    print(f"保存先: {ui_path}")
    print(f"レポート保存先: {report_path}")


if __name__ == "__main__":
    main()