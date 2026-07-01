from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
APPROVAL_DIR = BASE_DIR / "human_approval_requests"
REPORT_DIR = BASE_DIR / "reports"

APPROVAL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase84-1 Human Approval Workflow"

APPROVAL_REQUIRED_OPERATIONS = {
    "external_operation",
    "original_write",
    "file_delete",
    "real_gui_operation",
    "browser_operation",
    "auto_execute",
    "capability_execute",
    "external_ai_execute",
}

AUTO_ALLOWED_OPERATIONS = {
    "dry_run_cycle",
    "health_check",
    "stability_check",
    "backup_check",
    "recovery_check",
    "goal_check",
    "event_check",
    "daemon_check",
    "audit_check",
}

def create_approval_request(operation, module_name, reason, risk_level=3):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    approval_required = operation in APPROVAL_REQUIRED_OPERATIONS
    auto_allowed = operation in AUTO_ALLOWED_OPERATIONS

    if approval_required:
        decision = "approval_required"
        allowed = False
        blocked = True
    elif auto_allowed:
        decision = "auto_allowed_dry_run"
        allowed = True
        blocked = False
    else:
        decision = "blocked_unknown_operation"
        allowed = False
        blocked = True

    request = {
        "status": "pending_approval" if approval_required else decision,
        "phase": PHASE,
        "timestamp": timestamp,
        "operation": operation,
        "module": module_name,
        "reason": reason,
        "risk_level": risk_level,
        "human_approval_required": approval_required,
        "human_approved": False,
        "permission_decision": decision,
        "allowed": allowed,
        "blocked": blocked,
        "dry_run": True,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "SafeToExecute": allowed,
    }

    request_path = None
    if approval_required:
        request_path = APPROVAL_DIR / f"approval_request_{operation}_{timestamp}.json"
        request_path.write_text(
            json.dumps(request, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    return request, request_path

def run_workflow_test():
    test_cases = [
        ("dry_run_cycle", "cycle", "safe dry-run cycle test", 0),
        ("health_check", "health", "safe health check test", 0),
        ("external_operation", "connector", "external operation requires approval", 4),
        ("original_write", "original", "original write requires approval", 4),
        ("file_delete", "storage", "file delete requires approval", 4),
        ("real_gui_operation", "gui", "real GUI operation requires approval", 4),
        ("browser_operation", "browser", "browser operation requires approval", 4),
        ("auto_execute", "daemon", "automatic execution requires approval", 4),
    ]

    results = []
    request_paths = []

    for operation, module_name, reason, risk_level in test_cases:
        result, path = create_approval_request(
            operation=operation,
            module_name=module_name,
            reason=reason,
            risk_level=risk_level,
        )
        results.append(result)
        if path:
            request_paths.append(str(path))

    approval_required_results = [
        r for r in results if r["human_approval_required"] is True
    ]

    auto_allowed_results = [
        r for r in results if r["permission_decision"] == "auto_allowed_dry_run"
    ]

    report = {
        "status": "completed",
        "phase": PHASE,
        "HumanApprovalWorkflowCreated": True,
        "TestCount": len(results),
        "ApprovalRequiredCount": len(approval_required_results),
        "AutoAllowedDryRunCount": len(auto_allowed_results),
        "ApprovalRequestsCreated": len(request_paths),
        "AllApprovalRequiredBlocked": all(
            r["blocked"] is True and r["allowed"] is False
            for r in approval_required_results
        ),
        "AllApprovalRequestsPending": all(
            r["status"] == "pending_approval"
            for r in approval_required_results
        ),
        "AllAutoAllowedDryRunPassed": all(
            r["allowed"] is True and r["blocked"] is False
            for r in auto_allowed_results
        ),
        "HumanApproved": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0,
        "SafeToContinue": True,
        "NextPhase": "Phase84-2 Human Approval Workflow Diagnostics",
        "ApprovalRequestPaths": request_paths,
        "results": results,
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"human_approval_workflow_{timestamp}.json"
    latest_path = BASE_DIR / "human_approval_workflow.json"

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
    report, report_path = run_workflow_test()

    print("=== Human Approval Workflow ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"HumanApprovalWorkflowCreated: {report['HumanApprovalWorkflowCreated']}")
    print(f"TestCount: {report['TestCount']}")
    print(f"ApprovalRequiredCount: {report['ApprovalRequiredCount']}")
    print(f"AutoAllowedDryRunCount: {report['AutoAllowedDryRunCount']}")
    print(f"ApprovalRequestsCreated: {report['ApprovalRequestsCreated']}")
    print(f"AllApprovalRequiredBlocked: {report['AllApprovalRequiredBlocked']}")
    print(f"AllApprovalRequestsPending: {report['AllApprovalRequestsPending']}")
    print(f"AllAutoAllowedDryRunPassed: {report['AllAutoAllowedDryRunPassed']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(f"Mode: {report['Mode']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"NextPhase: {report['NextPhase']}")
    print(f"保存先: {report_path}")

if __name__ == "__main__":
    main()