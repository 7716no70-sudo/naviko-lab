from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase42-2 Creator Approval UI Diagnostics"
ROOT = Path(__file__).resolve().parents[2]

WORKSPACE = ROOT / "navikoLAB" / "workspace"
APPROVAL_UI_DIR = WORKSPACE / "creator_approval_ui"
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"


def load_latest_json(directory: Path, pattern: str):
    files = sorted(directory.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        return None, None

    path = files[0]
    try:
        return path, json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return path, None


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    ui_path, ui = load_latest_json(APPROVAL_UI_DIR, "creator_approval_ui_*.json")

    ui_found = ui is not None
    actions = ui.get("ApprovalActions", []) if ui else []
    flow_steps = ui.get("ApprovalFlowSteps", []) if ui else []
    schema = ui.get("ApprovalRecordSchema", {}) if ui else {}

    required_actions = [
        "approve",
        "reject",
        "hold",
        "request_more_validation",
        "request_permission_policy_review",
    ]

    required_flow_steps = [
        "LoadOriginalAdoptionQueue",
        "DisplayCandidateSummary",
        "DisplayRiskClassification",
        "DisplayValidationResult",
        "CreatorSelectAction",
        "SaveApprovalRecord",
        "KeepOriginalWriteBlocked",
        "PassToOriginalSafeAdoptionOnlyAfterApproval",
    ]

    required_schema_keys = [
        "approval_id",
        "candidate_id",
        "creator_action",
        "creator_comment",
        "human_approved",
        "permission_policy_approved",
        "original_write_allowed",
        "created_at",
    ]

    missing_actions = [action for action in required_actions if action not in actions]
    missing_flow_steps = [step for step in required_flow_steps if step not in flow_steps]
    missing_schema_keys = [key for key in required_schema_keys if key not in schema]

    checks = {
        "CreatorApprovalUIFound": ui_found,
        "CreatorApprovalUICreated": bool(ui and ui.get("CreatorApprovalUICreated") is True),
        "CreatorApprovalUIReady": bool(ui and ui.get("CreatorApprovalUIReady") is True),
        "RequiredApprovalActionsComplete": ui_found and not missing_actions,
        "MissingApprovalActionCount": len(missing_actions),
        "MissingApprovalActions": missing_actions,
        "RequiredApprovalFlowStepsComplete": ui_found and not missing_flow_steps,
        "MissingApprovalFlowStepCount": len(missing_flow_steps),
        "MissingApprovalFlowSteps": missing_flow_steps,
        "RequiredApprovalRecordSchemaComplete": ui_found and not missing_schema_keys,
        "MissingApprovalRecordSchemaKeyCount": len(missing_schema_keys),
        "MissingApprovalRecordSchemaKeys": missing_schema_keys,
        "WorkspaceOnly": bool(ui and ui.get("WorkspaceOnly") is True),
        "OriginalWrite": bool(ui and ui.get("OriginalWrite") is True),
        "OriginalWriteBlocked": bool(ui and ui.get("OriginalWriteBlocked") is True),
        "OriginalAdoptionAllowed": bool(ui and ui.get("OriginalAdoptionAllowed") is True),
        "ExternalOperation": bool(ui and ui.get("ExternalOperation") is True),
        "RealGUIOperation": bool(ui and ui.get("RealGUIOperation") is True),
        "FileDelete": bool(ui and ui.get("FileDelete") is True),
        "HumanApprovalRequiredForOriginalAdoption": bool(
            ui and ui.get("HumanApprovalRequiredForOriginalAdoption") is True
        ),
        "HumanApproved": bool(ui and ui.get("HumanApproved") is True),
        "PermissionPolicyRequired": bool(ui and ui.get("PermissionPolicyRequired") is True),
        "PermissionPolicyApproved": bool(ui and ui.get("PermissionPolicyApproved") is True),
        "AutomaticValidationRequired": bool(ui and ui.get("AutomaticValidationRequired") is True),
        "RiskCount": int(ui.get("RiskCount", 999)) if ui else 999,
    }

    safe_to_continue = (
        checks["CreatorApprovalUIFound"]
        and checks["CreatorApprovalUICreated"]
        and checks["CreatorApprovalUIReady"]
        and checks["RequiredApprovalActionsComplete"]
        and checks["RequiredApprovalFlowStepsComplete"]
        and checks["RequiredApprovalRecordSchemaComplete"]
        and checks["WorkspaceOnly"]
        and not checks["OriginalWrite"]
        and checks["OriginalWriteBlocked"]
        and not checks["OriginalAdoptionAllowed"]
        and not checks["ExternalOperation"]
        and not checks["RealGUIOperation"]
        and not checks["FileDelete"]
        and checks["HumanApprovalRequiredForOriginalAdoption"]
        and not checks["HumanApproved"]
        and checks["PermissionPolicyRequired"]
        and not checks["PermissionPolicyApproved"]
        and checks["AutomaticValidationRequired"]
        and checks["RiskCount"] == 0
    )

    report = {
        "status": "completed" if safe_to_continue else "blocked",
        "phase": PHASE,
        "source_ui_path": str(ui_path) if ui_path else None,
        **checks,
        "SafeToContinue": safe_to_continue,
        "NextPhase": "Phase42-3 Creator Approval UI Completion Report"
        if safe_to_continue
        else "Review Phase42-1 Creator Approval UI Builder",
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"creator_approval_ui_diagnostics_{ts}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Creator Approval UI Diagnostics ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"保存先: {report_path}")


if __name__ == "__main__":
    main()