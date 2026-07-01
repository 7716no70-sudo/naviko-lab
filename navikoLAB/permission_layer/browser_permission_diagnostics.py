from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
BROWSER_DIR = BASE_DIR / "browser"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase88-2 Browser Permission Diagnostics"

ROUTER_PATH = BASE_DIR / "browser_permission_router.json"
POLICY_PATH = BROWSER_DIR / "browser_permission_policies.json"

REQUIRED_ALLOWED = [
    "browser_check",
    "browser_plan",
]

REQUIRED_APPROVAL = [
    "browser_open",
    "browser_click",
    "browser_input",
    "browser_submit",
    "browser_download",
]

REQUIRED_DENIED = [
    "unknown_browser_action",
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
    action_policies = policies.get("browser_action_policies", {}) if policies_found else {}
    default_policy = policies.get("default_browser_policy", {}) if policies_found else {}

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
        and router.get("BrowserPermissionRouterCreated") is True
        and router.get("BrowserPoliciesSaved") is True
        and router.get("AllAllowedBrowserActionsSafe") is True
        and router.get("AllApprovalRequiredBrowserActionsBlocked") is True
        and router.get("AllDeniedBrowserActionsBlocked") is True
        and router.get("BrowserPermissionRouterUsedForAll") is True
        and router.get("PolicyRequiredForAll") is True
        and router.get("CapabilityPermissionRequiredForAll") is True
        and router.get("PermissionLayerRequiredForAll") is True
        and router.get("BrowserOperation") is False
        and router.get("BrowserOpened") is False
        and router.get("ExternalCommunicationExecuted") is False
        and router.get("HumanApproved") is False
        and router.get("OriginalWrite") is False
        and router.get("ExternalOperation") is False
        and router.get("RealGUIOperation") is False
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
        "BrowserRouterFound": router_found,
        "BrowserPoliciesFound": policies_found,
        "RequiredAllowedBrowserActionCount": len(REQUIRED_ALLOWED),
        "RequiredApprovalBrowserActionCount": len(REQUIRED_APPROVAL),
        "RequiredDeniedBrowserActionCount": len(REQUIRED_DENIED),
        "MissingAllowedBrowserActionCount": len(missing_allowed),
        "MissingApprovalBrowserActionCount": len(missing_approval),
        "MissingDeniedBrowserActionCount": len(missing_denied),
        "MissingAllowedBrowserActions": missing_allowed,
        "MissingApprovalBrowserActions": missing_approval,
        "MissingDeniedBrowserActions": missing_denied,
        "AllowedBrowserPolicyOK": allowed_ok,
        "ApprovalBrowserPolicyOK": approval_ok,
        "DeniedBrowserPolicyOK": denied_ok,
        "PoliciesIncludeAllowedBrowserActions": policies_include_allowed,
        "PoliciesIncludeApprovalBrowserActions": policies_include_approval,
        "DefaultBrowserPolicyOK": default_policy_ok,
        "BrowserRouterSummaryOK": router_summary_ok,
        "BrowserPermissionDiagnosticsPassed": diagnostics_passed,
        "BrowserOperation": False,
        "BrowserOpened": False,
        "ExternalCommunicationExecuted": False,
        "HumanApproved": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0 if diagnostics_passed else 1,
        "SafeToContinue": diagnostics_passed,
        "NextPhase": "Phase88-3 Browser Permission Completion Report",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"browser_permission_diagnostics_{timestamp}.json"
    latest_path = BASE_DIR / "browser_permission_diagnostics.json"

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

    print("=== Browser Permission Diagnostics ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"BrowserRouterFound: {report['BrowserRouterFound']}")
    print(f"BrowserPoliciesFound: {report['BrowserPoliciesFound']}")
    print(f"RequiredAllowedBrowserActionCount: {report['RequiredAllowedBrowserActionCount']}")
    print(f"RequiredApprovalBrowserActionCount: {report['RequiredApprovalBrowserActionCount']}")
    print(f"RequiredDeniedBrowserActionCount: {report['RequiredDeniedBrowserActionCount']}")
    print(f"MissingAllowedBrowserActionCount: {report['MissingAllowedBrowserActionCount']}")
    print(f"MissingApprovalBrowserActionCount: {report['MissingApprovalBrowserActionCount']}")
    print(f"MissingDeniedBrowserActionCount: {report['MissingDeniedBrowserActionCount']}")
    print(f"AllowedBrowserPolicyOK: {report['AllowedBrowserPolicyOK']}")
    print(f"ApprovalBrowserPolicyOK: {report['ApprovalBrowserPolicyOK']}")
    print(f"DeniedBrowserPolicyOK: {report['DeniedBrowserPolicyOK']}")
    print(f"PoliciesIncludeAllowedBrowserActions: {report['PoliciesIncludeAllowedBrowserActions']}")
    print(f"PoliciesIncludeApprovalBrowserActions: {report['PoliciesIncludeApprovalBrowserActions']}")
    print(f"DefaultBrowserPolicyOK: {report['DefaultBrowserPolicyOK']}")
    print(f"BrowserRouterSummaryOK: {report['BrowserRouterSummaryOK']}")
    print(f"BrowserPermissionDiagnosticsPassed: {report['BrowserPermissionDiagnosticsPassed']}")
    print(f"BrowserOperation: {report['BrowserOperation']}")
    print(f"BrowserOpened: {report['BrowserOpened']}")
    print(f"ExternalCommunicationExecuted: {report['ExternalCommunicationExecuted']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(f"Mode: {report['Mode']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"NextPhase: {report['NextPhase']}")
    print(f"保存先: {report_path}")

if __name__ == "__main__":
    main()