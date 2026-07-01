from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
CAPABILITY_DIR = BASE_DIR / "capabilities"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase86-2 Capability Permission Diagnostics"

SYSTEM_PATH = BASE_DIR / "capability_permission_system.json"
POLICY_PATH = CAPABILITY_DIR / "capability_permission_policies.json"

REQUIRED_ALLOWED = [
    "health",
    "stability",
    "backup",
    "recovery",
    "goal",
    "event",
    "daemon",
    "audit",
]

REQUIRED_APPROVAL = [
    "text_ai",
    "image_ai",
    "video_ai",
    "voice_ai",
    "browser",
    "gui",
    "app_operator",
    "external_ai",
]

REQUIRED_DENIED = [
    "unknown_capability",
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

    system = load_json(SYSTEM_PATH)
    policies = load_json(POLICY_PATH)

    system_found = system is not None
    policies_found = policies is not None

    results = system.get("results", []) if system_found else []
    capability_policies = policies.get("capability_policies", {}) if policies_found else {}
    default_policy = policies.get("default_capability_policy", {}) if policies_found else {}

    result_by_capability = {
        r.get("capability"): r for r in results
    }

    missing_allowed = [c for c in REQUIRED_ALLOWED if c not in result_by_capability]
    missing_approval = [c for c in REQUIRED_APPROVAL if c not in result_by_capability]
    missing_denied = [c for c in REQUIRED_DENIED if c not in result_by_capability]

    allowed_ok = (
        len(missing_allowed) == 0
        and all(
            result_by_capability[c].get("allowed") is True
            and result_by_capability[c].get("SafeToExecute") is True
            and result_by_capability[c].get("blocked") is False
            for c in REQUIRED_ALLOWED
        )
    )

    approval_ok = (
        len(missing_approval) == 0
        and all(
            result_by_capability[c].get("approval_required") is True
            and result_by_capability[c].get("human_approval_required") is True
            and result_by_capability[c].get("human_approved") is False
            and result_by_capability[c].get("SafeToExecute") is False
            and result_by_capability[c].get("blocked") is True
            for c in REQUIRED_APPROVAL
        )
    )

    denied_ok = (
        len(missing_denied) == 0
        and all(
            result_by_capability[c].get("denied") is True
            and result_by_capability[c].get("SafeToExecute") is False
            and result_by_capability[c].get("blocked") is True
            for c in REQUIRED_DENIED
        )
    )

    policies_include_allowed = all(c in capability_policies for c in REQUIRED_ALLOWED)
    policies_include_approval = all(c in capability_policies for c in REQUIRED_APPROVAL)

    default_policy_ok = (
        default_policy.get("decision") == "deny"
        and default_policy.get("risk_level") == 5
        and default_policy.get("human_approval_required") is True
    )

    system_summary_ok = (
        system_found
        and system.get("CapabilityPermissionSystemCreated") is True
        and system.get("CapabilityPoliciesSaved") is True
        and system.get("AllAllowedCapabilitiesSafe") is True
        and system.get("AllApprovalRequiredCapabilitiesBlocked") is True
        and system.get("AllDeniedCapabilitiesBlocked") is True
        and system.get("CapabilityPermissionSystemUsedForAll") is True
        and system.get("HumanApproved") is False
        and system.get("OriginalWrite") is False
        and system.get("ExternalOperation") is False
        and system.get("BrowserOperation") is False
        and system.get("RealGUIOperation") is False
        and system.get("FileDelete") is False
    )

    diagnostics_passed = (
        system_found
        and policies_found
        and allowed_ok
        and approval_ok
        and denied_ok
        and policies_include_allowed
        and policies_include_approval
        and default_policy_ok
        and system_summary_ok
    )

    report = {
        "status": "completed" if diagnostics_passed else "failed",
        "phase": PHASE,
        "CapabilitySystemFound": system_found,
        "CapabilityPoliciesFound": policies_found,
        "RequiredAllowedCapabilityCount": len(REQUIRED_ALLOWED),
        "RequiredApprovalCapabilityCount": len(REQUIRED_APPROVAL),
        "RequiredDeniedCapabilityCount": len(REQUIRED_DENIED),
        "MissingAllowedCapabilityCount": len(missing_allowed),
        "MissingApprovalCapabilityCount": len(missing_approval),
        "MissingDeniedCapabilityCount": len(missing_denied),
        "MissingAllowedCapabilities": missing_allowed,
        "MissingApprovalCapabilities": missing_approval,
        "MissingDeniedCapabilities": missing_denied,
        "AllowedCapabilityPolicyOK": allowed_ok,
        "ApprovalCapabilityPolicyOK": approval_ok,
        "DeniedCapabilityPolicyOK": denied_ok,
        "PoliciesIncludeAllowedCapabilities": policies_include_allowed,
        "PoliciesIncludeApprovalCapabilities": policies_include_approval,
        "DefaultCapabilityPolicyOK": default_policy_ok,
        "CapabilitySystemSummaryOK": system_summary_ok,
        "CapabilityPermissionDiagnosticsPassed": diagnostics_passed,
        "HumanApproved": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0 if diagnostics_passed else 1,
        "SafeToContinue": diagnostics_passed,
        "NextPhase": "Phase86-3 Capability Permission Completion Report",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"capability_permission_diagnostics_{timestamp}.json"
    latest_path = BASE_DIR / "capability_permission_diagnostics.json"

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

    print("=== Capability Permission Diagnostics ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"CapabilitySystemFound: {report['CapabilitySystemFound']}")
    print(f"CapabilityPoliciesFound: {report['CapabilityPoliciesFound']}")
    print(f"RequiredAllowedCapabilityCount: {report['RequiredAllowedCapabilityCount']}")
    print(f"RequiredApprovalCapabilityCount: {report['RequiredApprovalCapabilityCount']}")
    print(f"RequiredDeniedCapabilityCount: {report['RequiredDeniedCapabilityCount']}")
    print(f"MissingAllowedCapabilityCount: {report['MissingAllowedCapabilityCount']}")
    print(f"MissingApprovalCapabilityCount: {report['MissingApprovalCapabilityCount']}")
    print(f"MissingDeniedCapabilityCount: {report['MissingDeniedCapabilityCount']}")
    print(f"AllowedCapabilityPolicyOK: {report['AllowedCapabilityPolicyOK']}")
    print(f"ApprovalCapabilityPolicyOK: {report['ApprovalCapabilityPolicyOK']}")
    print(f"DeniedCapabilityPolicyOK: {report['DeniedCapabilityPolicyOK']}")
    print(f"PoliciesIncludeAllowedCapabilities: {report['PoliciesIncludeAllowedCapabilities']}")
    print(f"PoliciesIncludeApprovalCapabilities: {report['PoliciesIncludeApprovalCapabilities']}")
    print(f"DefaultCapabilityPolicyOK: {report['DefaultCapabilityPolicyOK']}")
    print(f"CapabilitySystemSummaryOK: {report['CapabilitySystemSummaryOK']}")
    print(f"CapabilityPermissionDiagnosticsPassed: {report['CapabilityPermissionDiagnosticsPassed']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(f"Mode: {report['Mode']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"NextPhase: {report['NextPhase']}")
    print(f"保存先: {report_path}")

if __name__ == "__main__":
    main()