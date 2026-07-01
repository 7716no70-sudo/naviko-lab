from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase84-3 Human Approval Workflow Completion Report"

WORKFLOW_PATH = BASE_DIR / "human_approval_workflow.json"
DIAGNOSTICS_PATH = BASE_DIR / "human_approval_workflow_diagnostics.json"

def load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def build_report():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    workflow = load_json(WORKFLOW_PATH)
    diagnostics = load_json(DIAGNOSTICS_PATH)

    workflow_found = workflow is not None
    diagnostics_found = diagnostics is not None

    workflow_completed = workflow_found and workflow.get("status") == "completed"
    diagnostics_completed = diagnostics_found and diagnostics.get("status") == "completed"

    workflow_created = (
        workflow_found
        and workflow.get("HumanApprovalWorkflowCreated") is True
    )

    diagnostics_passed = (
        diagnostics_found
        and diagnostics.get("HumanApprovalDiagnosticsPassed") is True
    )

    all_approval_required_blocked = (
        workflow_found
        and workflow.get("AllApprovalRequiredBlocked") is True
    )

    all_approval_requests_pending = (
        workflow_found
        and workflow.get("AllApprovalRequestsPending") is True
    )

    all_requests_not_approved = (
        diagnostics_found
        and diagnostics.get("AllRequestsNotApproved") is True
    )

    all_requests_not_safe_to_execute = (
        diagnostics_found
        and diagnostics.get("AllRequestsNotSafeToExecute") is True
    )

    workflow_flags_ok = (
        diagnostics_found
        and diagnostics.get("WorkflowFlagsOK") is True
    )

    completed = (
        workflow_completed
        and diagnostics_completed
        and workflow_created
        and diagnostics_passed
        and all_approval_required_blocked
        and all_approval_requests_pending
        and all_requests_not_approved
        and all_requests_not_safe_to_execute
        and workflow_flags_ok
    )

    report = {
        "status": "completed" if completed else "failed",
        "phase": PHASE,
        "WorkflowFound": workflow_found,
        "DiagnosticsFound": diagnostics_found,
        "WorkflowCompleted": workflow_completed,
        "DiagnosticsCompleted": diagnostics_completed,
        "HumanApprovalWorkflowCreated": workflow_created,
        "HumanApprovalDiagnosticsPassed": diagnostics_passed,
        "AllApprovalRequiredBlocked": all_approval_required_blocked,
        "AllApprovalRequestsPending": all_approval_requests_pending,
        "AllRequestsNotApproved": all_requests_not_approved,
        "AllRequestsNotSafeToExecute": all_requests_not_safe_to_execute,
        "WorkflowFlagsOK": workflow_flags_ok,
        "HumanApprovalWorkflowCompleted": completed,
        "HumanApproved": False,
        "ApprovalRequiredOperations": [
            "external_operation",
            "original_write",
            "file_delete",
            "real_gui_operation",
            "browser_operation",
            "auto_execute",
            "capability_execute",
            "external_ai_execute",
        ],
        "AutoAllowedDryRunOperations": [
            "dry_run_cycle",
            "health_check",
            "stability_check",
            "backup_check",
            "recovery_check",
            "goal_check",
            "event_check",
            "daemon_check",
            "audit_check",
        ],
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": "Phase85 Policy Engine",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"human_approval_workflow_completion_report_{timestamp}.json"
    latest_json_path = BASE_DIR / "human_approval_workflow_completion_report.json"
    txt_path = BASE_DIR / "human_approval_workflow_completion_report.txt"

    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    latest_json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    lines = [
        "=== Human Approval Workflow Completion Report ===",
        f"status: {report['status']}",
        f"phase: {report['phase']}",
        f"WorkflowFound: {report['WorkflowFound']}",
        f"DiagnosticsFound: {report['DiagnosticsFound']}",
        f"WorkflowCompleted: {report['WorkflowCompleted']}",
        f"DiagnosticsCompleted: {report['DiagnosticsCompleted']}",
        f"HumanApprovalWorkflowCreated: {report['HumanApprovalWorkflowCreated']}",
        f"HumanApprovalDiagnosticsPassed: {report['HumanApprovalDiagnosticsPassed']}",
        f"AllApprovalRequiredBlocked: {report['AllApprovalRequiredBlocked']}",
        f"AllApprovalRequestsPending: {report['AllApprovalRequestsPending']}",
        f"AllRequestsNotApproved: {report['AllRequestsNotApproved']}",
        f"AllRequestsNotSafeToExecute: {report['AllRequestsNotSafeToExecute']}",
        f"WorkflowFlagsOK: {report['WorkflowFlagsOK']}",
        f"HumanApprovalWorkflowCompleted: {report['HumanApprovalWorkflowCompleted']}",
        f"HumanApproved: {report['HumanApproved']}",
        f"Mode: {report['Mode']}",
        f"RiskCount: {report['RiskCount']}",
        f"SafeToContinue: {report['SafeToContinue']}",
        f"NextPhase: {report['NextPhase']}",
        f"保存先: {report_path}",
    ]

    txt_path.write_text("\n".join(lines), encoding="utf-8")

    return lines

def main():
    for line in build_report():
        print(line)

if __name__ == "__main__":
    main()