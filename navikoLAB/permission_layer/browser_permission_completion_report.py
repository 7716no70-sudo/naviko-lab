from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase88-3 Browser Permission Completion Report"

ROUTER_PATH = BASE_DIR / "browser_permission_router.json"
DIAGNOSTICS_PATH = BASE_DIR / "browser_permission_diagnostics.json"

def load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def build_report():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    router = load_json(ROUTER_PATH)
    diagnostics = load_json(DIAGNOSTICS_PATH)

    router_found = router is not None
    diagnostics_found = diagnostics is not None

    router_completed = router_found and router.get("status") == "completed"
    diagnostics_completed = diagnostics_found and diagnostics.get("status") == "completed"

    router_created = (
        router_found
        and router.get("BrowserPermissionRouterCreated") is True
    )

    diagnostics_passed = (
        diagnostics_found
        and diagnostics.get("BrowserPermissionDiagnosticsPassed") is True
    )

    allowed_policy_ok = (
        diagnostics_found
        and diagnostics.get("AllowedBrowserPolicyOK") is True
    )

    approval_policy_ok = (
        diagnostics_found
        and diagnostics.get("ApprovalBrowserPolicyOK") is True
    )

    denied_policy_ok = (
        diagnostics_found
        and diagnostics.get("DeniedBrowserPolicyOK") is True
    )

    router_summary_ok = (
        diagnostics_found
        and diagnostics.get("BrowserRouterSummaryOK") is True
    )

    browser_operation_blocked = (
        diagnostics_found
        and diagnostics.get("BrowserOperation") is False
        and diagnostics.get("BrowserOpened") is False
        and diagnostics.get("ExternalCommunicationExecuted") is False
    )

    completed = (
        router_completed
        and diagnostics_completed
        and router_created
        and diagnostics_passed
        and allowed_policy_ok
        and approval_policy_ok
        and denied_policy_ok
        and router_summary_ok
        and browser_operation_blocked
    )

    report = {
        "status": "completed" if completed else "failed",
        "phase": PHASE,
        "BrowserRouterFound": router_found,
        "DiagnosticsFound": diagnostics_found,
        "BrowserRouterCompleted": router_completed,
        "DiagnosticsCompleted": diagnostics_completed,
        "BrowserPermissionRouterCreated": router_created,
        "BrowserPermissionDiagnosticsPassed": diagnostics_passed,
        "AllowedBrowserPolicyOK": allowed_policy_ok,
        "ApprovalBrowserPolicyOK": approval_policy_ok,
        "DeniedBrowserPolicyOK": denied_policy_ok,
        "BrowserRouterSummaryOK": router_summary_ok,
        "BrowserOperation": False,
        "BrowserOpened": False,
        "ExternalCommunicationExecuted": False,
        "BrowserPermissionCompletionConfirmed": completed,
        "AllowedBrowserActions": [
            "browser_check",
            "browser_plan",
        ],
        "ApprovalRequiredBrowserActions": [
            "browser_open",
            "browser_click",
            "browser_input",
            "browser_submit",
            "browser_download",
        ],
        "DeniedBrowserActions": [
            "unknown_browser_action",
        ],
        "HumanApproved": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": "Phase89 GUI Permission",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"browser_permission_completion_report_{timestamp}.json"
    latest_json_path = BASE_DIR / "browser_permission_completion_report.json"
    txt_path = BASE_DIR / "browser_permission_completion_report.txt"

    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    latest_json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    lines = [
        "=== Browser Permission Completion Report ===",
        f"status: {report['status']}",
        f"phase: {report['phase']}",
        f"BrowserRouterFound: {report['BrowserRouterFound']}",
        f"DiagnosticsFound: {report['DiagnosticsFound']}",
        f"BrowserRouterCompleted: {report['BrowserRouterCompleted']}",
        f"DiagnosticsCompleted: {report['DiagnosticsCompleted']}",
        f"BrowserPermissionRouterCreated: {report['BrowserPermissionRouterCreated']}",
        f"BrowserPermissionDiagnosticsPassed: {report['BrowserPermissionDiagnosticsPassed']}",
        f"AllowedBrowserPolicyOK: {report['AllowedBrowserPolicyOK']}",
        f"ApprovalBrowserPolicyOK: {report['ApprovalBrowserPolicyOK']}",
        f"DeniedBrowserPolicyOK: {report['DeniedBrowserPolicyOK']}",
        f"BrowserRouterSummaryOK: {report['BrowserRouterSummaryOK']}",
        f"BrowserOperation: {report['BrowserOperation']}",
        f"BrowserOpened: {report['BrowserOpened']}",
        f"ExternalCommunicationExecuted: {report['ExternalCommunicationExecuted']}",
        f"BrowserPermissionCompletionConfirmed: {report['BrowserPermissionCompletionConfirmed']}",
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