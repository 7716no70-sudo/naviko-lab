from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
POLICY_DIR = BASE_DIR / "policies"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
POLICY_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase85-1 Policy Engine"

POLICY_RULES = {
    "dry_run_cycle": {
        "decision": "allow",
        "risk_level": 0,
        "human_approval_required": False,
    },
    "health_check": {
        "decision": "allow",
        "risk_level": 0,
        "human_approval_required": False,
    },
    "stability_check": {
        "decision": "allow",
        "risk_level": 0,
        "human_approval_required": False,
    },
    "backup_check": {
        "decision": "allow",
        "risk_level": 1,
        "human_approval_required": False,
    },
    "recovery_check": {
        "decision": "allow",
        "risk_level": 1,
        "human_approval_required": False,
    },
    "goal_check": {
        "decision": "allow",
        "risk_level": 0,
        "human_approval_required": False,
    },
    "event_check": {
        "decision": "allow",
        "risk_level": 0,
        "human_approval_required": False,
    },
    "daemon_check": {
        "decision": "allow",
        "risk_level": 1,
        "human_approval_required": False,
    },
    "audit_check": {
        "decision": "allow",
        "risk_level": 0,
        "human_approval_required": False,
    },

    "external_operation": {
        "decision": "approval_required",
        "risk_level": 4,
        "human_approval_required": True,
    },
    "original_write": {
        "decision": "approval_required",
        "risk_level": 4,
        "human_approval_required": True,
    },
    "file_delete": {
        "decision": "approval_required",
        "risk_level": 4,
        "human_approval_required": True,
    },
    "real_gui_operation": {
        "decision": "approval_required",
        "risk_level": 4,
        "human_approval_required": True,
    },
    "browser_operation": {
        "decision": "approval_required",
        "risk_level": 4,
        "human_approval_required": True,
    },
    "auto_execute": {
        "decision": "approval_required",
        "risk_level": 4,
        "human_approval_required": True,
    },
    "capability_execute": {
        "decision": "approval_required",
        "risk_level": 3,
        "human_approval_required": True,
    },
    "external_ai_execute": {
        "decision": "approval_required",
        "risk_level": 3,
        "human_approval_required": True,
    },
}

DEFAULT_POLICY = {
    "decision": "deny",
    "risk_level": 5,
    "human_approval_required": True,
}

def save_policy_rules():
    path = POLICY_DIR / "policy_rules.json"
    payload = {
        "phase": PHASE,
        "mode": "dry_run",
        "policy_rules": POLICY_RULES,
        "default_policy": DEFAULT_POLICY,
    }
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    return path

def evaluate_policy(operation, module_name="unknown", context=None):
    context = context or {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    rule = POLICY_RULES.get(operation, DEFAULT_POLICY)
    decision = rule["decision"]

    allowed = decision == "allow"
    approval_required = decision == "approval_required"
    denied = decision == "deny"

    result = {
        "timestamp": timestamp,
        "phase": PHASE,
        "operation": operation,
        "module": module_name,
        "context": context,
        "policy_decision": decision,
        "allowed": allowed,
        "approval_required": approval_required,
        "denied": denied,
        "blocked": not allowed,
        "risk_level": rule["risk_level"],
        "human_approval_required": rule["human_approval_required"],
        "human_approved": False,
        "dry_run": True,
        "PolicyEngineUsed": True,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "SafeToExecute": allowed,
    }

    return result

def run_policy_engine_test():
    policy_path = save_policy_rules()

    test_operations = [
        ("dry_run_cycle", "cycle"),
        ("health_check", "health"),
        ("stability_check", "stability"),
        ("backup_check", "backup"),
        ("recovery_check", "recovery"),
        ("goal_check", "goal"),
        ("event_check", "event"),
        ("daemon_check", "daemon"),
        ("audit_check", "audit"),
        ("external_operation", "connector"),
        ("original_write", "original"),
        ("file_delete", "storage"),
        ("real_gui_operation", "gui"),
        ("browser_operation", "browser"),
        ("auto_execute", "daemon"),
        ("capability_execute", "capability"),
        ("external_ai_execute", "external_ai"),
        ("unknown_operation", "unknown"),
    ]

    results = [
        evaluate_policy(operation, module_name)
        for operation, module_name in test_operations
    ]

    allowed_results = [r for r in results if r["allowed"] is True]
    approval_required_results = [r for r in results if r["approval_required"] is True]
    denied_results = [r for r in results if r["denied"] is True]

    report = {
        "status": "completed",
        "phase": PHASE,
        "PolicyEngineCreated": True,
        "PolicyRulesSaved": policy_path.exists(),
        "PolicyRulesPath": str(policy_path),
        "TestCount": len(results),
        "AllowedCount": len(allowed_results),
        "ApprovalRequiredCount": len(approval_required_results),
        "DeniedCount": len(denied_results),
        "AllAllowedSafeToExecute": all(
            r["SafeToExecute"] is True and r["blocked"] is False
            for r in allowed_results
        ),
        "AllApprovalRequiredBlocked": all(
            r["blocked"] is True and r["SafeToExecute"] is False
            for r in approval_required_results
        ),
        "AllDeniedBlocked": all(
            r["blocked"] is True and r["SafeToExecute"] is False
            for r in denied_results
        ),
        "PolicyEngineUsedForAll": all(
            r["PolicyEngineUsed"] is True for r in results
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
        "NextPhase": "Phase85-2 Policy Engine Diagnostics",
        "results": results,
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"policy_engine_{timestamp}.json"
    latest_path = BASE_DIR / "policy_engine.json"

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
    report, report_path = run_policy_engine_test()

    print("=== Policy Engine ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"PolicyEngineCreated: {report['PolicyEngineCreated']}")
    print(f"PolicyRulesSaved: {report['PolicyRulesSaved']}")
    print(f"TestCount: {report['TestCount']}")
    print(f"AllowedCount: {report['AllowedCount']}")
    print(f"ApprovalRequiredCount: {report['ApprovalRequiredCount']}")
    print(f"DeniedCount: {report['DeniedCount']}")
    print(f"AllAllowedSafeToExecute: {report['AllAllowedSafeToExecute']}")
    print(f"AllApprovalRequiredBlocked: {report['AllApprovalRequiredBlocked']}")
    print(f"AllDeniedBlocked: {report['AllDeniedBlocked']}")
    print(f"PolicyEngineUsedForAll: {report['PolicyEngineUsedForAll']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(f"Mode: {report['Mode']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"NextPhase: {report['NextPhase']}")
    print(f"保存先: {report_path}")

if __name__ == "__main__":
    main()