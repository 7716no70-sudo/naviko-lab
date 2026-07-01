from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
POLICY_DIR = BASE_DIR / "policies"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase85-2 Policy Engine Diagnostics"

POLICY_ENGINE_PATH = BASE_DIR / "policy_engine.json"
POLICY_RULES_PATH = POLICY_DIR / "policy_rules.json"

REQUIRED_ALLOWED = [
    "dry_run_cycle",
    "health_check",
    "stability_check",
    "backup_check",
    "recovery_check",
    "goal_check",
    "event_check",
    "daemon_check",
    "audit_check",
]

REQUIRED_APPROVAL = [
    "external_operation",
    "original_write",
    "file_delete",
    "real_gui_operation",
    "browser_operation",
    "auto_execute",
    "capability_execute",
    "external_ai_execute",
]

REQUIRED_DENIED = [
    "unknown_operation",
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

    engine = load_json(POLICY_ENGINE_PATH)
    rules = load_json(POLICY_RULES_PATH)

    engine_found = engine is not None
    rules_found = rules is not None

    results = engine.get("results", []) if engine_found else []
    policy_rules = rules.get("policy_rules", {}) if rules_found else {}
    default_policy = rules.get("default_policy", {}) if rules_found else {}

    result_by_operation = {
        r.get("operation"): r for r in results
    }

    missing_allowed = [
        op for op in REQUIRED_ALLOWED
        if op not in result_by_operation
    ]

    missing_approval = [
        op for op in REQUIRED_APPROVAL
        if op not in result_by_operation
    ]

    missing_denied = [
        op for op in REQUIRED_DENIED
        if op not in result_by_operation
    ]

    allowed_ok = (
        len(missing_allowed) == 0
        and all(
            result_by_operation[op].get("allowed") is True
            and result_by_operation[op].get("SafeToExecute") is True
            and result_by_operation[op].get("blocked") is False
            for op in REQUIRED_ALLOWED
        )
    )

    approval_ok = (
        len(missing_approval) == 0
        and all(
            result_by_operation[op].get("approval_required") is True
            and result_by_operation[op].get("blocked") is True
            and result_by_operation[op].get("SafeToExecute") is False
            and result_by_operation[op].get("human_approval_required") is True
            for op in REQUIRED_APPROVAL
        )
    )

    denied_ok = (
        len(missing_denied) == 0
        and all(
            result_by_operation[op].get("denied") is True
            and result_by_operation[op].get("blocked") is True
            and result_by_operation[op].get("SafeToExecute") is False
            for op in REQUIRED_DENIED
        )
    )

    rules_include_allowed = all(op in policy_rules for op in REQUIRED_ALLOWED)
    rules_include_approval = all(op in policy_rules for op in REQUIRED_APPROVAL)

    default_policy_ok = (
        default_policy.get("decision") == "deny"
        and default_policy.get("risk_level") == 5
        and default_policy.get("human_approval_required") is True
    )

    engine_summary_ok = (
        engine_found
        and engine.get("PolicyEngineCreated") is True
        and engine.get("PolicyRulesSaved") is True
        and engine.get("AllAllowedSafeToExecute") is True
        and engine.get("AllApprovalRequiredBlocked") is True
        and engine.get("AllDeniedBlocked") is True
        and engine.get("PolicyEngineUsedForAll") is True
        and engine.get("HumanApproved") is False
        and engine.get("OriginalWrite") is False
        and engine.get("ExternalOperation") is False
        and engine.get("BrowserOperation") is False
        and engine.get("RealGUIOperation") is False
        and engine.get("FileDelete") is False
    )

    diagnostics_passed = (
        engine_found
        and rules_found
        and allowed_ok
        and approval_ok
        and denied_ok
        and rules_include_allowed
        and rules_include_approval
        and default_policy_ok
        and engine_summary_ok
    )

    report = {
        "status": "completed" if diagnostics_passed else "failed",
        "phase": PHASE,
        "PolicyEngineFound": engine_found,
        "PolicyRulesFound": rules_found,
        "RequiredAllowedCount": len(REQUIRED_ALLOWED),
        "RequiredApprovalCount": len(REQUIRED_APPROVAL),
        "RequiredDeniedCount": len(REQUIRED_DENIED),
        "MissingAllowedCount": len(missing_allowed),
        "MissingApprovalCount": len(missing_approval),
        "MissingDeniedCount": len(missing_denied),
        "MissingAllowed": missing_allowed,
        "MissingApproval": missing_approval,
        "MissingDenied": missing_denied,
        "AllowedPolicyOK": allowed_ok,
        "ApprovalPolicyOK": approval_ok,
        "DeniedPolicyOK": denied_ok,
        "RulesIncludeAllowed": rules_include_allowed,
        "RulesIncludeApproval": rules_include_approval,
        "DefaultPolicyOK": default_policy_ok,
        "EngineSummaryOK": engine_summary_ok,
        "PolicyEngineDiagnosticsPassed": diagnostics_passed,
        "HumanApproved": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0 if diagnostics_passed else 1,
        "SafeToContinue": diagnostics_passed,
        "NextPhase": "Phase85-3 Policy Engine Completion Report",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"policy_engine_diagnostics_{timestamp}.json"
    latest_path = BASE_DIR / "policy_engine_diagnostics.json"

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

    print("=== Policy Engine Diagnostics ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"PolicyEngineFound: {report['PolicyEngineFound']}")
    print(f"PolicyRulesFound: {report['PolicyRulesFound']}")
    print(f"RequiredAllowedCount: {report['RequiredAllowedCount']}")
    print(f"RequiredApprovalCount: {report['RequiredApprovalCount']}")
    print(f"RequiredDeniedCount: {report['RequiredDeniedCount']}")
    print(f"MissingAllowedCount: {report['MissingAllowedCount']}")
    print(f"MissingApprovalCount: {report['MissingApprovalCount']}")
    print(f"MissingDeniedCount: {report['MissingDeniedCount']}")
    print(f"AllowedPolicyOK: {report['AllowedPolicyOK']}")
    print(f"ApprovalPolicyOK: {report['ApprovalPolicyOK']}")
    print(f"DeniedPolicyOK: {report['DeniedPolicyOK']}")
    print(f"RulesIncludeAllowed: {report['RulesIncludeAllowed']}")
    print(f"RulesIncludeApproval: {report['RulesIncludeApproval']}")
    print(f"DefaultPolicyOK: {report['DefaultPolicyOK']}")
    print(f"EngineSummaryOK: {report['EngineSummaryOK']}")
    print(f"PolicyEngineDiagnosticsPassed: {report['PolicyEngineDiagnosticsPassed']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(f"Mode: {report['Mode']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"NextPhase: {report['NextPhase']}")
    print(f"保存先: {report_path}")

if __name__ == "__main__":
    main()