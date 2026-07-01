from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
APPROVAL_DIR = BASE_DIR / "human_approval_requests"
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase84-2 Human Approval Workflow Diagnostics"

WORKFLOW_PATH = BASE_DIR / "human_approval_workflow.json"

REQUIRED_APPROVAL_OPERATIONS = [
    "external_operation",
    "original_write",
    "file_delete",
    "real_gui_operation",
    "browser_operation",
    "auto_execute",
]

def load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def load_approval_requests():
    if not APPROVAL_DIR.exists():
        return []

    requests = []
    for path in sorted(APPROVAL_DIR.glob("approval_request_*.json")):
        data = load_json(path)
        if data:
            data["_path"] = str(path)
            requests.append(data)
    return requests

def build_diagnostics():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    workflow = load_json(WORKFLOW_PATH)
    approval_requests = load_approval_requests()

    workflow_found = workflow is not None
    workflow_completed = workflow_found and workflow.get("status") == "completed"

    request_ops = sorted(set(
        r.get("operation")
        for r in approval_requests
        if r.get("operation") in REQUIRED_APPROVAL_OPERATIONS
    ))

    missing_ops = sorted(set(REQUIRED_APPROVAL_OPERATIONS) - set(request_ops))

    required_requests = [
        r for r in approval_requests
        if r.get("operation") in REQUIRED_APPROVAL_OPERATIONS
    ]

    all_required_requests_found = len(missing_ops) == 0

    all_requests_pending = (
        bool(required_requests)
        and all(r.get("status") == "pending_approval" for r in required_requests)
    )

    all_requests_not_approved = (
        bool(required_requests)
        and all(r.get("human_approved") is False for r in required_requests)
    )

    all_requests_blocked = (
        bool(required_requests)
        and all(r.get("blocked") is True and r.get("allowed") is False for r in required_requests)
    )

    all_requests_not_safe_to_execute = (
        bool(required_requests)
        and all(r.get("SafeToExecute") is False for r in required_requests)
    )

    workflow_flags_ok = (
        workflow_found
        and workflow.get("AllApprovalRequiredBlocked") is True
        and workflow.get("AllApprovalRequestsPending") is True
        and workflow.get("HumanApproved") is False
        and workflow.get("OriginalWrite") is False
        and workflow.get("ExternalOperation") is False
        and workflow.get("BrowserOperation") is False
        and workflow.get("RealGUIOperation") is False
        and workflow.get("FileDelete") is False
    )

    diagnostics_passed = (
        workflow_found
        and workflow_completed
        and all_required_requests_found
        and all_requests_pending
        and all_requests_not_approved
        and all_requests_blocked
        and all_requests_not_safe_to_execute
        and workflow_flags_ok
    )

    report = {
        "status": "completed" if diagnostics_passed else "failed",
        "phase": PHASE,
        "WorkflowFound": workflow_found,
        "WorkflowCompleted": workflow_completed,
        "ApprovalRequestDirFound": APPROVAL_DIR.exists(),
        "RequiredApprovalOperationCount": len(REQUIRED_APPROVAL_OPERATIONS),
        "ApprovalRequestCount": len(required_requests),
        "MissingApprovalOperationCount": len(missing_ops),
        "MissingApprovalOperations": missing_ops,
        "AllRequiredRequestsFound": all_required_requests_found,
        "AllRequestsPending": all_requests_pending,
        "AllRequestsNotApproved": all_requests_not_approved,
        "AllRequestsBlocked": all_requests_blocked,
        "AllRequestsNotSafeToExecute": all_requests_not_safe_to_execute,
        "WorkflowFlagsOK": workflow_flags_ok,
        "HumanApprovalDiagnosticsPassed": diagnostics_passed,
        "HumanApproved": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0 if diagnostics_passed else 1,
        "SafeToContinue": diagnostics_passed,
        "NextPhase": "Phase84-3 Human Approval Workflow Completion Report",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"human_approval_workflow_diagnostics_{timestamp}.json"
    latest_path = BASE_DIR / "human_approval_workflow_diagnostics.json"

    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    latest_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    return report, report_path

def main():
    report, report_path = build_diagnostics()

    print("=== Human Approval Workflow Diagnostics ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"WorkflowFound: {report['WorkflowFound']}")
    print(f"WorkflowCompleted: {report['WorkflowCompleted']}")
    print(f"ApprovalRequestDirFound: {report['ApprovalRequestDirFound']}")
    print(f"RequiredApprovalOperationCount: {report['RequiredApprovalOperationCount']}")
    print(f"ApprovalRequestCount: {report['ApprovalRequestCount']}")
    print(f"MissingApprovalOperationCount: {report['MissingApprovalOperationCount']}")
    print(f"AllRequiredRequestsFound: {report['AllRequiredRequestsFound']}")
    print(f"AllRequestsPending: {report['AllRequestsPending']}")
    print(f"AllRequestsNotApproved: {report['AllRequestsNotApproved']}")
    print(f"AllRequestsBlocked: {report['AllRequestsBlocked']}")
    print(f"AllRequestsNotSafeToExecute: {report['AllRequestsNotSafeToExecute']}")
    print(f"WorkflowFlagsOK: {report['WorkflowFlagsOK']}")
    print(f"HumanApprovalDiagnosticsPassed: {report['HumanApprovalDiagnosticsPassed']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(f"Mode: {report['Mode']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"NextPhase: {report['NextPhase']}")
    print(f"保存先: {report_path}")

if __name__ == "__main__":
    main()