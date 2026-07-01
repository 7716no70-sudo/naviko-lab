from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
CAPABILITY_DIR = BASE_DIR / "capabilities"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
CAPABILITY_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase86-1 Capability Permission System"

CAPABILITY_POLICIES = {
    "health": {
        "decision": "allow",
        "risk_level": 0,
        "human_approval_required": False,
    },
    "stability": {
        "decision": "allow",
        "risk_level": 0,
        "human_approval_required": False,
    },
    "backup": {
        "decision": "allow",
        "risk_level": 1,
        "human_approval_required": False,
    },
    "recovery": {
        "decision": "allow",
        "risk_level": 1,
        "human_approval_required": False,
    },
    "goal": {
        "decision": "allow",
        "risk_level": 0,
        "human_approval_required": False,
    },
    "event": {
        "decision": "allow",
        "risk_level": 0,
        "human_approval_required": False,
    },
    "daemon": {
        "decision": "allow",
        "risk_level": 1,
        "human_approval_required": False,
    },
    "audit": {
        "decision": "allow",
        "risk_level": 0,
        "human_approval_required": False,
    },

    "text_ai": {
        "decision": "approval_required",
        "risk_level": 2,
        "human_approval_required": True,
    },
    "image_ai": {
        "decision": "approval_required",
        "risk_level": 3,
        "human_approval_required": True,
    },
    "video_ai": {
        "decision": "approval_required",
        "risk_level": 3,
        "human_approval_required": True,
    },
    "voice_ai": {
        "decision": "approval_required",
        "risk_level": 3,
        "human_approval_required": True,
    },
    "browser": {
        "decision": "approval_required",
        "risk_level": 4,
        "human_approval_required": True,
    },
    "gui": {
        "decision": "approval_required",
        "risk_level": 4,
        "human_approval_required": True,
    },
    "app_operator": {
        "decision": "approval_required",
        "risk_level": 4,
        "human_approval_required": True,
    },
    "external_ai": {
        "decision": "approval_required",
        "risk_level": 3,
        "human_approval_required": True,
    },
}

DEFAULT_CAPABILITY_POLICY = {
    "decision": "deny",
    "risk_level": 5,
    "human_approval_required": True,
}

def save_capability_policies():
    path = CAPABILITY_DIR / "capability_permission_policies.json"
    payload = {
        "phase": PHASE,
        "mode": "dry_run",
        "capability_policies": CAPABILITY_POLICIES,
        "default_capability_policy": DEFAULT_CAPABILITY_POLICY,
    }

    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    return path

def evaluate_capability_permission(capability_name, requested_action="check", context=None):
    context = context or {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    policy = CAPABILITY_POLICIES.get(capability_name, DEFAULT_CAPABILITY_POLICY)
    decision = policy["decision"]

    allowed = decision == "allow"
    approval_required = decision == "approval_required"
    denied = decision == "deny"

    result = {
        "timestamp": timestamp,
        "phase": PHASE,
        "capability": capability_name,
        "requested_action": requested_action,
        "context": context,
        "capability_decision": decision,
        "allowed": allowed,
        "approval_required": approval_required,
        "denied": denied,
        "blocked": not allowed,
        "risk_level": policy["risk_level"],
        "human_approval_required": policy["human_approval_required"],
        "human_approved": False,
        "dry_run": True,
        "CapabilityPermissionSystemUsed": True,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "SafeToExecute": allowed,
    }

    return result

def run_capability_permission_test():
    policy_path = save_capability_policies()

    test_capabilities = [
        "health",
        "stability",
        "backup",
        "recovery",
        "goal",
        "event",
        "daemon",
        "audit",
        "text_ai",
        "image_ai",
        "video_ai",
        "voice_ai",
        "browser",
        "gui",
        "app_operator",
        "external_ai",
        "unknown_capability",
    ]

    results = [
        evaluate_capability_permission(
            capability_name=capability,
            requested_action="check"
        )
        for capability in test_capabilities
    ]

    allowed_results = [r for r in results if r["allowed"] is True]
    approval_required_results = [r for r in results if r["approval_required"] is True]
    denied_results = [r for r in results if r["denied"] is True]

    report = {
        "status": "completed",
        "phase": PHASE,
        "CapabilityPermissionSystemCreated": True,
        "CapabilityPoliciesSaved": policy_path.exists(),
        "CapabilityPoliciesPath": str(policy_path),
        "TestCount": len(results),
        "AllowedCapabilityCount": len(allowed_results),
        "ApprovalRequiredCapabilityCount": len(approval_required_results),
        "DeniedCapabilityCount": len(denied_results),
        "AllAllowedCapabilitiesSafe": all(
            r["SafeToExecute"] is True and r["blocked"] is False
            for r in allowed_results
        ),
        "AllApprovalRequiredCapabilitiesBlocked": all(
            r["SafeToExecute"] is False and r["blocked"] is True
            for r in approval_required_results
        ),
        "AllDeniedCapabilitiesBlocked": all(
            r["SafeToExecute"] is False and r["blocked"] is True
            for r in denied_results
        ),
        "CapabilityPermissionSystemUsedForAll": all(
            r["CapabilityPermissionSystemUsed"] is True
            for r in results
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
        "NextPhase": "Phase86-2 Capability Permission Diagnostics",
        "results": results,
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"capability_permission_system_{timestamp}.json"
    latest_path = BASE_DIR / "capability_permission_system.json"

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
    report, report_path = run_capability_permission_test()

    print("=== Capability Permission System ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"CapabilityPermissionSystemCreated: {report['CapabilityPermissionSystemCreated']}")
    print(f"CapabilityPoliciesSaved: {report['CapabilityPoliciesSaved']}")
    print(f"TestCount: {report['TestCount']}")
    print(f"AllowedCapabilityCount: {report['AllowedCapabilityCount']}")
    print(f"ApprovalRequiredCapabilityCount: {report['ApprovalRequiredCapabilityCount']}")
    print(f"DeniedCapabilityCount: {report['DeniedCapabilityCount']}")
    print(f"AllAllowedCapabilitiesSafe: {report['AllAllowedCapabilitiesSafe']}")
    print(f"AllApprovalRequiredCapabilitiesBlocked: {report['AllApprovalRequiredCapabilitiesBlocked']}")
    print(f"AllDeniedCapabilitiesBlocked: {report['AllDeniedCapabilitiesBlocked']}")
    print(f"CapabilityPermissionSystemUsedForAll: {report['CapabilityPermissionSystemUsedForAll']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(f"Mode: {report['Mode']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"NextPhase: {report['NextPhase']}")
    print(f"保存先: {report_path}")

if __name__ == "__main__":
    main()