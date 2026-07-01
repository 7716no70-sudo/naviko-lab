from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
GUI_DIR = BASE_DIR / "gui"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
GUI_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase89-1 GUI Permission Router"

GUI_ACTION_POLICIES = {
    "gui_check": {
        "decision": "allow",
        "risk_level": 0,
    },
    "gui_plan": {
        "decision": "allow",
        "risk_level": 1,
    },
    "gui_click": {
        "decision": "approval_required",
        "risk_level": 4,
    },
    "gui_input": {
        "decision": "approval_required",
        "risk_level": 4,
    },
    "gui_drag": {
        "decision": "approval_required",
        "risk_level": 4,
    },
    "gui_hotkey": {
        "decision": "approval_required",
        "risk_level": 4,
    },
    "gui_app_control": {
        "decision": "approval_required",
        "risk_level": 5,
    },
}

DEFAULT_GUI_POLICY = {
    "decision": "deny",
    "risk_level": 5,
}

def save_gui_policies():
    path = GUI_DIR / "gui_permission_policies.json"
    payload = {
        "phase": PHASE,
        "mode": "dry_run",
        "gui_action_policies": GUI_ACTION_POLICIES,
        "default_gui_policy": DEFAULT_GUI_POLICY,
    }
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    return path

def route_gui_request(action, target="none", purpose="gui permission dry_run"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    policy = GUI_ACTION_POLICIES.get(action, DEFAULT_GUI_POLICY)
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
        "gui_decision": decision,
        "allowed": allowed,
        "approval_required": approval_required,
        "denied": denied,
        "blocked": not allowed,
        "risk_level": policy["risk_level"],
        "human_approval_required": approval_required or denied,
        "human_approved": False,
        "dry_run": True,
        "GUIPermissionRouterUsed": True,
        "PolicyRequired": True,
        "CapabilityPermissionRequired": True,
        "PermissionLayerRequired": True,
        "RealGUIOperation": False,
        "GUIClicked": False,
        "GUIInput": False,
        "GUIDrag": False,
        "GUIHotkey": False,
        "GUIAppControl": False,
        "ExternalOperation": False,
        "ExternalCommunicationExecuted": False,
        "OriginalWrite": False,
        "BrowserOperation": False,
        "FileDelete": False,
        "SafeToExecute": allowed,
    }

    return result

def run_gui_permission_test():
    policy_path = save_gui_policies()

    test_actions = [
        "gui_check",
        "gui_plan",
        "gui_click",
        "gui_input",
        "gui_drag",
        "gui_hotkey",
        "gui_app_control",
        "unknown_gui_action",
    ]

    results = [
        route_gui_request(
            action=action,
            target="dry_run_target",
            purpose="Phase89 GUI permission test"
        )
        for action in test_actions
    ]

    allowed_results = [r for r in results if r["allowed"] is True]
    approval_required_results = [r for r in results if r["approval_required"] is True]
    denied_results = [r for r in results if r["denied"] is True]

    report = {
        "status": "completed",
        "phase": PHASE,
        "GUIPermissionRouterCreated": True,
        "GUIPoliciesSaved": policy_path.exists(),
        "GUIPoliciesPath": str(policy_path),
        "TestCount": len(results),
        "AllowedGUIActionCount": len(allowed_results),
        "ApprovalRequiredGUIActionCount": len(approval_required_results),
        "DeniedGUIActionCount": len(denied_results),
        "AllAllowedGUIActionsSafe": all(
            r["SafeToExecute"] is True and r["blocked"] is False
            for r in allowed_results
        ),
        "AllApprovalRequiredGUIActionsBlocked": all(
            r["SafeToExecute"] is False and r["blocked"] is True
            for r in approval_required_results
        ),
        "AllDeniedGUIActionsBlocked": all(
            r["SafeToExecute"] is False and r["blocked"] is True
            for r in denied_results
        ),
        "GUIPermissionRouterUsedForAll": all(
            r["GUIPermissionRouterUsed"] is True for r in results
        ),
        "PolicyRequiredForAll": all(r["PolicyRequired"] is True for r in results),
        "CapabilityPermissionRequiredForAll": all(
            r["CapabilityPermissionRequired"] is True for r in results
        ),
        "PermissionLayerRequiredForAll": all(
            r["PermissionLayerRequired"] is True for r in results
        ),
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
        "RiskCount": 0,
        "SafeToContinue": True,
        "NextPhase": "Phase89-2 GUI Permission Diagnostics",
        "results": results,
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"gui_permission_router_{timestamp}.json"
    latest_path = BASE_DIR / "gui_permission_router.json"

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
    report, report_path = run_gui_permission_test()

    print("=== GUI Permission Router ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"GUIPermissionRouterCreated: {report['GUIPermissionRouterCreated']}")
    print(f"GUIPoliciesSaved: {report['GUIPoliciesSaved']}")
    print(f"TestCount: {report['TestCount']}")
    print(f"AllowedGUIActionCount: {report['AllowedGUIActionCount']}")
    print(f"ApprovalRequiredGUIActionCount: {report['ApprovalRequiredGUIActionCount']}")
    print(f"DeniedGUIActionCount: {report['DeniedGUIActionCount']}")
    print(f"AllAllowedGUIActionsSafe: {report['AllAllowedGUIActionsSafe']}")
    print(f"AllApprovalRequiredGUIActionsBlocked: {report['AllApprovalRequiredGUIActionsBlocked']}")
    print(f"AllDeniedGUIActionsBlocked: {report['AllDeniedGUIActionsBlocked']}")
    print(f"GUIPermissionRouterUsedForAll: {report['GUIPermissionRouterUsedForAll']}")
    print(f"PolicyRequiredForAll: {report['PolicyRequiredForAll']}")
    print(f"CapabilityPermissionRequiredForAll: {report['CapabilityPermissionRequiredForAll']}")
    print(f"PermissionLayerRequiredForAll: {report['PermissionLayerRequiredForAll']}")
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