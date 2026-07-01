from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
GUI_DIR = BASE_DIR / "gui"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase89-2 GUI Permission Diagnostics"

ROUTER_PATH = BASE_DIR / "gui_permission_router.json"
POLICY_PATH = GUI_DIR / "gui_permission_policies.json"

REQUIRED_ALLOWED = [
    "gui_check",
    "gui_plan",
]

REQUIRED_APPROVAL = [
    "gui_click",
    "gui_input",
    "gui_drag",
    "gui_hotkey",
    "gui_app_control",
]

REQUIRED_DENIED = [
    "unknown_gui_action",
]

def load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def build_diagnostics():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    router = load_json(ROUTER_PATH)
    policies = load_json(POLICY_PATH)

    router_found = router is not None
    policies_found = policies is not None

    results = router.get("results", []) if router_found else []
    action_policies = policies.get("gui_action_policies", {}) if policies_found else {}
    default_policy = policies.get("default_gui_policy", {}) if policies_found else {}

    result_by_action = {
        r.get("action"): r for r in results
    }

    missing_allowed = [a for a in REQUIRED_ALLOWED if a not in result_by_action]
    missing_approval = [a for a in REQUIRED_APPROVAL if a not in result_by_action]
    missing_denied = [a for a in REQUIRED_DENIED if a not in result_by_action]

    allowed_ok = (
        len(missing_allowed) == 0
        and all(
            result_by_action[a].get("allowed") is True
            and result_by_action[a].get("SafeToExecute") is True
            and result_by_action[a].get("blocked") is False
            for a in REQUIRED_ALLOWED
        )
    )

    approval_ok = (
        len(missing_approval) == 0
        and all(
            result_by_action[a].get("approval_required") is True
            and result_by_action[a].get("human_approval_required") is True
            and result_by_action[a].get("human_approved") is False
            and result_by_action[a].get("SafeToExecute") is False
            and result_by_action[a].get("blocked") is True
            for a in REQUIRED_APPROVAL
        )
    )

    denied_ok = (
        len(missing_denied) == 0
        and all(
            result_by_action[a].get("denied") is True
            and result_by_action[a].get("SafeToExecute") is False
            and result_by_action[a].get("blocked") is True
            for a in REQUIRED_DENIED
        )
    )

    policies_include_allowed = all(a in action_policies for a in REQUIRED_ALLOWED)
    policies_include_approval = all(a in action_policies for a in REQUIRED_APPROVAL)

    default_policy_ok = (
        default_policy.get("decision") == "deny"
        and default_policy.get("risk_level") == 5
    )

    router_summary_ok = (
        router_found
        and router.get("GUIPermissionRouterCreated") is True
        and router.get("GUIPoliciesSaved") is True
        and router.get("AllAllowedGUIActionsSafe") is True
        and router.get("AllApprovalRequiredGUIActionsBlocked") is True
        and router.get("AllDeniedGUIActionsBlocked") is True
        and router.get("GUIPermissionRouterUsedForAll") is True
        and router.get("PolicyRequiredForAll") is True
        and router.get("CapabilityPermissionRequiredForAll") is True
        and router.get("PermissionLayerRequiredForAll") is True
        and router.get("RealGUIOperation") is False
        and router.get("GUIClicked") is False
        and router.get("GUIInput") is False
        and router.get("GUIDrag") is False
        and router.get("GUIHotkey") is False
        and router.get("GUIAppControl") is False
        and router.get("ExternalCommunicationExecuted") is False
        and router.get("HumanApproved") is False
        and router.get("OriginalWrite") is False
        and router.get("ExternalOperation") is False
        and router.get("BrowserOperation") is False
        and router.get("FileDelete") is False
    )

    diagnostics_passed = (
        router_found
        and policies_found
        and allowed_ok
        and approval_ok
        and denied_ok
        and policies_include_allowed
        and policies_include_approval
        and default_policy_ok
        and router_summary_ok
    )

    report = {
        "status": "completed" if diagnostics_passed else "failed",
        "phase": PHASE,
        "GUIRouterFound": router_found,
        "GUIPoliciesFound": policies_found,
        "RequiredAllowedGUIActionCount": len(REQUIRED_ALLOWED),
        "RequiredApprovalGUIActionCount": len(REQUIRED_APPROVAL),
        "RequiredDeniedGUIActionCount": len(REQUIRED_DENIED),
        "MissingAllowedGUIActionCount": len(missing_allowed),
        "MissingApprovalGUIActionCount": len(missing_approval),
        "MissingDeniedGUIActionCount": len(missing_denied),
        "MissingAllowedGUIActions": missing_allowed,
        "MissingApprovalGUIActions": missing_approval,
        "MissingDeniedGUIActions": missing_denied,
        "AllowedGUIPolicyOK": allowed_ok,
        "ApprovalGUIPolicyOK": approval_ok,
        "DeniedGUIPolicyOK": denied_ok,
        "PoliciesIncludeAllowedGUIActions": policies_include_allowed,
        "PoliciesIncludeApprovalGUIActions": policies_include_approval,
        "DefaultGUIPolicyOK": default_policy_ok,
        "GUIRouterSummaryOK": router_summary_ok,
        "GUIPermissionDiagnosticsPassed": diagnostics_passed,
        "RealGUIOperation": False,
        "GUIClicked": False,
        "GUIInput": False,
        "GUIDrag": False,
        "GUIHotkey": False,
        "GUIAppControl": False,
        "ExternalCommunicationExecuted": False,
        "HumanApproved": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0 if diagnostics_passed else 1,
        "SafeToContinue": diagnostics_passed,
        "NextPhase": "Phase89-3 GUI Permission Completion Report",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"gui_permission_diagnostics_{timestamp}.json"
    latest_path = BASE_DIR / "gui_permission_diagnostics.json"

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

    print("=== GUI Permission Diagnostics ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"GUIRouterFound: {report['GUIRouterFound']}")
    print(f"GUIPoliciesFound: {report['GUIPoliciesFound']}")
    print(f"RequiredAllowedGUIActionCount: {report['RequiredAllowedGUIActionCount']}")
    print(f"RequiredApprovalGUIActionCount: {report['RequiredApprovalGUIActionCount']}")
    print(f"RequiredDeniedGUIActionCount: {report['RequiredDeniedGUIActionCount']}")
    print(f"MissingAllowedGUIActionCount: {report['MissingAllowedGUIActionCount']}")
    print(f"MissingApprovalGUIActionCount: {report['MissingApprovalGUIActionCount']}")
    print(f"MissingDeniedGUIActionCount: {report['MissingDeniedGUIActionCount']}")
    print(f"AllowedGUIPolicyOK: {report['AllowedGUIPolicyOK']}")
    print(f"ApprovalGUIPolicyOK: {report['ApprovalGUIPolicyOK']}")
    print(f"DeniedGUIPolicyOK: {report['DeniedGUIPolicyOK']}")
    print(f"PoliciesIncludeAllowedGUIActions: {report['PoliciesIncludeAllowedGUIActions']}")
    print(f"PoliciesIncludeApprovalGUIActions: {report['PoliciesIncludeApprovalGUIActions']}")
    print(f"DefaultGUIPolicyOK: {report['DefaultGUIPolicyOK']}")
    print(f"GUIRouterSummaryOK: {report['GUIRouterSummaryOK']}")
    print(f"GUIPermissionDiagnosticsPassed: {report['GUIPermissionDiagnosticsPassed']}")
    print(f"RealGUIOperation: {report['RealGUIOperation']}")
    print(f"GUIClicked: {report['GUIClicked']}")
    print(f"GUIInput: {report['GUIInput']}")
    print(f"GUIDrag: {report['GUIDrag']}")
    print(f"GUIHotkey: {report['GUIHotkey']}")
    print(f"GUIAppControl: {report['GUIAppControl']}")
    print(f"ExternalCommunicationExecuted: {report['ExternalCommunicationExecuted']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(f"Mode: {report['Mode']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"NextPhase: {report['NextPhase']}")
    print(f"保存先: {report_path}")

if __name__ == "__main__":
    main()