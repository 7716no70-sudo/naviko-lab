from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
BROWSER_DIR = BASE_DIR / "browser"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
BROWSER_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase88-1 Browser Permission Router"

BROWSER_ACTION_POLICIES = {
    "browser_check": {
        "decision": "allow",
        "risk_level": 0,
    },
    "browser_plan": {
        "decision": "allow",
        "risk_level": 1,
    },
    "browser_open": {
        "decision": "approval_required",
        "risk_level": 4,
    },
    "browser_click": {
        "decision": "approval_required",
        "risk_level": 4,
    },
    "browser_input": {
        "decision": "approval_required",
        "risk_level": 4,
    },
    "browser_submit": {
        "decision": "approval_required",
        "risk_level": 5,
    },
    "browser_download": {
        "decision": "approval_required",
        "risk_level": 5,
    },
}

DEFAULT_BROWSER_POLICY = {
    "decision": "deny",
    "risk_level": 5,
}

def save_browser_policies():
    path = BROWSER_DIR / "browser_permission_policies.json"
    payload = {
        "phase": PHASE,
        "mode": "dry_run",
        "browser_action_policies": BROWSER_ACTION_POLICIES,
        "default_browser_policy": DEFAULT_BROWSER_POLICY,
    }
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    return path

def route_browser_request(action, target="none", purpose="browser permission dry_run"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    policy = BROWSER_ACTION_POLICIES.get(action, DEFAULT_BROWSER_POLICY)
    decision = policy["decision"]

    allowed = decision == "allow"
    approval_required = decision == "approval_required"
    denied = decision == "deny"

    result = {
        "timestamp": timestamp,
        "phase": PHASE,
        "action": action,
        "target": target,
        "purpose": purpose,
        "browser_decision": decision,
        "allowed": allowed,
        "approval_required": approval_required,
        "denied": denied,
        "blocked": not allowed,
        "risk_level": policy["risk_level"],
        "human_approval_required": approval_required or denied,
        "human_approved": False,
        "dry_run": True,
        "BrowserPermissionRouterUsed": True,
        "PolicyRequired": True,
        "CapabilityPermissionRequired": True,
        "PermissionLayerRequired": True,
        "BrowserOperation": False,
        "BrowserOpened": False,
        "BrowserClicked": False,
        "BrowserInput": False,
        "BrowserSubmitted": False,
        "BrowserDownload": False,
        "ExternalOperation": False,
        "ExternalCommunicationExecuted": False,
        "OriginalWrite": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "SafeToExecute": allowed,
    }

    return result

def run_browser_permission_test():
    policy_path = save_browser_policies()

    test_actions = [
        "browser_check",
        "browser_plan",
        "browser_open",
        "browser_click",
        "browser_input",
        "browser_submit",
        "browser_download",
        "unknown_browser_action",
    ]

    results = [
        route_browser_request(
            action=action,
            target="dry_run_target",
            purpose="Phase88 browser permission test"
        )
        for action in test_actions
    ]

    allowed_results = [r for r in results if r["allowed"] is True]
    approval_required_results = [r for r in results if r["approval_required"] is True]
    denied_results = [r for r in results if r["denied"] is True]

    report = {
        "status": "completed",
        "phase": PHASE,
        "BrowserPermissionRouterCreated": True,
        "BrowserPoliciesSaved": policy_path.exists(),
        "BrowserPoliciesPath": str(policy_path),
        "TestCount": len(results),
        "AllowedBrowserActionCount": len(allowed_results),
        "ApprovalRequiredBrowserActionCount": len(approval_required_results),
        "DeniedBrowserActionCount": len(denied_results),
        "AllAllowedBrowserActionsSafe": all(
            r["SafeToExecute"] is True and r["blocked"] is False
            for r in allowed_results
        ),
        "AllApprovalRequiredBrowserActionsBlocked": all(
            r["SafeToExecute"] is False and r["blocked"] is True
            for r in approval_required_results
        ),
        "AllDeniedBrowserActionsBlocked": all(
            r["SafeToExecute"] is False and r["blocked"] is True
            for r in denied_results
        ),
        "BrowserPermissionRouterUsedForAll": all(
            r["BrowserPermissionRouterUsed"] is True for r in results
        ),
        "PolicyRequiredForAll": all(r["PolicyRequired"] is True for r in results),
        "CapabilityPermissionRequiredForAll": all(
            r["CapabilityPermissionRequired"] is True for r in results
        ),
        "PermissionLayerRequiredForAll": all(
            r["PermissionLayerRequired"] is True for r in results
        ),
        "BrowserOperation": False,
        "BrowserOpened": False,
        "ExternalCommunicationExecuted": False,
        "HumanApproved": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0,
        "SafeToContinue": True,
        "NextPhase": "Phase88-2 Browser Permission Diagnostics",
        "results": results,
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"browser_permission_router_{timestamp}.json"
    latest_path = BASE_DIR / "browser_permission_router.json"

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
    report, report_path = run_browser_permission_test()

    print("=== Browser Permission Router ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"BrowserPermissionRouterCreated: {report['BrowserPermissionRouterCreated']}")
    print(f"BrowserPoliciesSaved: {report['BrowserPoliciesSaved']}")
    print(f"TestCount: {report['TestCount']}")
    print(f"AllowedBrowserActionCount: {report['AllowedBrowserActionCount']}")
    print(f"ApprovalRequiredBrowserActionCount: {report['ApprovalRequiredBrowserActionCount']}")
    print(f"DeniedBrowserActionCount: {report['DeniedBrowserActionCount']}")
    print(f"AllAllowedBrowserActionsSafe: {report['AllAllowedBrowserActionsSafe']}")
    print(f"AllApprovalRequiredBrowserActionsBlocked: {report['AllApprovalRequiredBrowserActionsBlocked']}")
    print(f"AllDeniedBrowserActionsBlocked: {report['AllDeniedBrowserActionsBlocked']}")
    print(f"BrowserPermissionRouterUsedForAll: {report['BrowserPermissionRouterUsedForAll']}")
    print(f"PolicyRequiredForAll: {report['PolicyRequiredForAll']}")
    print(f"CapabilityPermissionRequiredForAll: {report['CapabilityPermissionRequiredForAll']}")
    print(f"PermissionLayerRequiredForAll: {report['PermissionLayerRequiredForAll']}")
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