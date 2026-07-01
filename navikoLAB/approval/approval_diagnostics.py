from pathlib import Path

from navikoLAB.approval.human_approval_workflow import HumanApprovalWorkflow
from navikoLAB.approval.approval_request_manager import ApprovalRequestManager
from navikoLAB.approval.approval_safety_checker import ApprovalSafetyChecker


def run_approval_diagnostics():
    workflow = HumanApprovalWorkflow()

    request, request_path = workflow.create_request({
        "source": "BridgeDiagnostics",
        "target": "Original Naviko",
        "purpose": "approval diagnostics",
    })

    manager = ApprovalRequestManager()
    approved, approved_path = manager.approve_latest()

    checker = ApprovalSafetyChecker()
    safety = checker.check_request(Path(approved_path))

    precheck, precheck_path = workflow.run_pre_apply_checks()

    checks = {
        "RequestCreated": request_path.exists(),
        "HumanApproval": approved is not None and approved.get("approved") is True,
        "SafetyChecker": safety["status"] == "passed",
        "BackupCreated": precheck["backup_created"] is True,
        "SyntaxCheck": precheck["syntax_ok"] is True,
        "StartupCheck": precheck["startup_ok"] is True,
        "DirectWriteFalse": precheck["direct_write"] is False,
        "AutoApplyFalse": precheck["auto_apply"] is False,
        "RollbackRequired": precheck["rollback_required"] is True,
    }

    passed = sum(1 for v in checks.values() if v)
    failed = len(checks) - passed

    return {
        "status": "passed" if failed == 0 else "failed",
        "check_count": len(checks),
        "passed": passed,
        "failed": failed,
        "checks": checks,
        "request_path": str(request_path),
        "precheck_path": str(precheck_path),
    }


if __name__ == "__main__":
    result = run_approval_diagnostics()

    print("=== Approval Diagnostics ===")
    print("状態:", result["status"])
    print("確認項目:", result["check_count"])
    print("通過:", result["passed"])
    print("失敗:", result["failed"])

    for name, ok in result["checks"].items():
        print(f"- {name}: {'OK' if ok else 'NG'}")