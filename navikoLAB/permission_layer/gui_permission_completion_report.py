from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase89-3 GUI Permission Completion Report"

ROUTER_PATH = BASE_DIR / "gui_permission_router.json"
DIAGNOSTICS_PATH = BASE_DIR / "gui_permission_diagnostics.json"

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
        and router.get("GUIPermissionRouterCreated") is True
    )

    diagnostics_passed = (
        diagnostics_found
        and diagnostics.get("GUIPermissionDiagnosticsPassed") is True
    )

    allowed_policy_ok = (
        diagnostics_found
        and diagnostics.get("AllowedGUIPolicyOK") is True
    )

    approval_policy_ok = (
        diagnostics_found
        and diagnostics.get("ApprovalGUIPolicyOK") is True
    )

    denied_policy_ok = (
        diagnostics_found
        and diagnostics.get("DeniedGUIPolicyOK") is True
    )

    router_summary_ok = (
        diagnostics_found
        and diagnostics.get("GUIRouterSummaryOK") is True
    )

    gui_operation_blocked = (
        diagnostics_found
        and diagnostics.get("RealGUIOperation") is False
        and diagnostics.get("GUIClicked") is False
        and diagnostics.get("GUIInput") is False
        and diagnostics.get("GUIDrag") is False
        and diagnostics.get("GUIHotkey") is False
        and diagnostics.get("GUIAppControl") is False
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
        and gui_operation_blocked
    )

    report = {
        "status": "completed" if completed else "failed",
        "phase": PHASE,
        "GUIRouterFound": router_found,
        "DiagnosticsFound": diagnostics_found,
        "GUIRouterCompleted": router_completed,
        "DiagnosticsCompleted": diagnostics_completed,
        "GUIPermissionRouterCreated": router_created,
        "GUIPermissionDiagnosticsPassed": diagnostics_passed,
        "AllowedGUIPolicyOK": allowed_policy_ok,
        "ApprovalGUIPolicyOK": approval_policy_ok,
        "DeniedGUIPolicyOK": denied_policy_ok,
        "GUIRouterSummaryOK": router_summary_ok,
        "RealGUIOperation": False,
        "GUIClicked": False,
        "GUIInput": False,
        "GUIDrag": False,
        "GUIHotkey": False,
        "GUIAppControl": False,
        "GUIPermissionCompletionConfirmed": completed,
        "AllowedGUIActions": [
            "gui_check",
            "gui_plan",
        ],
        "ApprovalRequiredGUIActions": [
            "gui_click",
            "gui_input",
            "gui_drag",
            "gui_hotkey",
            "gui_app_control",
        ],
        "DeniedGUIActions": [
            "unknown_gui_action",
        ],
        "HumanApproved": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": "Phase90 AI OS Final Integration",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"gui_permission_completion_report_{timestamp}.json"
    latest_json_path = BASE_DIR / "gui_permission_completion_report.json"
    txt_path = BASE_DIR / "gui_permission_completion_report.txt"

    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    latest_json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    lines = [
        "=== GUI Permission Completion Report ===",
        f"status: {report['status']}",
        f"phase: {report['phase']}",
        f"GUIRouterFound: {report['GUIRouterFound']}",
        f"DiagnosticsFound: {report['DiagnosticsFound']}",
        f"GUIRouterCompleted: {report['GUIRouterCompleted']}",
        f"DiagnosticsCompleted: {report['DiagnosticsCompleted']}",
        f"GUIPermissionRouterCreated: {report['GUIPermissionRouterCreated']}",
        f"GUIPermissionDiagnosticsPassed: {report['GUIPermissionDiagnosticsPassed']}",
        f"AllowedGUIPolicyOK: {report['AllowedGUIPolicyOK']}",
        f"ApprovalGUIPolicyOK: {report['ApprovalGUIPolicyOK']}",
        f"DeniedGUIPolicyOK: {report['DeniedGUIPolicyOK']}",
        f"GUIRouterSummaryOK: {report['GUIRouterSummaryOK']}",
        f"RealGUIOperation: {report['RealGUIOperation']}",
        f"GUIClicked: {report['GUIClicked']}",
        f"GUIInput: {report['GUIInput']}",
        f"GUIDrag: {report['GUIDrag']}",
        f"GUIHotkey: {report['GUIHotkey']}",
        f"GUIAppControl: {report['GUIAppControl']}",
        f"GUIPermissionCompletionConfirmed: {report['GUIPermissionCompletionConfirmed']}",
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