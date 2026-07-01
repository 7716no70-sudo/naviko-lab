from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase86-3 Capability Permission Completion Report"

SYSTEM_PATH = BASE_DIR / "capability_permission_system.json"
DIAGNOSTICS_PATH = BASE_DIR / "capability_permission_diagnostics.json"

def load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def build_report():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    system = load_json(SYSTEM_PATH)
    diagnostics = load_json(DIAGNOSTICS_PATH)

    system_found = system is not None
    diagnostics_found = diagnostics is not None

    system_completed = system_found and system.get("status") == "completed"
    diagnostics_completed = diagnostics_found and diagnostics.get("status") == "completed"

    capability_system_created = (
        system_found
        and system.get("CapabilityPermissionSystemCreated") is True
    )

    diagnostics_passed = (
        diagnostics_found
        and diagnostics.get("CapabilityPermissionDiagnosticsPassed") is True
    )

    allowed_policy_ok = (
        diagnostics_found
        and diagnostics.get("AllowedCapabilityPolicyOK") is True
    )

    approval_policy_ok = (
        diagnostics_found
        and diagnostics.get("ApprovalCapabilityPolicyOK") is True
    )

    denied_policy_ok = (
        diagnostics_found
        and diagnostics.get("DeniedCapabilityPolicyOK") is True
    )

    default_policy_ok = (
        diagnostics_found
        and diagnostics.get("DefaultCapabilityPolicyOK") is True
    )

    system_summary_ok = (
        diagnostics_found
        and diagnostics.get("CapabilitySystemSummaryOK") is True
    )

    completed = (
        system_completed
        and diagnostics_completed
        and capability_system_created
        and diagnostics_passed
        and allowed_policy_ok
        and approval_policy_ok
        and denied_policy_ok
        and default_policy_ok
        and system_summary_ok
    )

    report = {
        "status": "completed" if completed else "failed",
        "phase": PHASE,
        "CapabilitySystemFound": system_found,
        "DiagnosticsFound": diagnostics_found,
        "CapabilitySystemCompleted": system_completed,
        "DiagnosticsCompleted": diagnostics_completed,
        "CapabilityPermissionSystemCreated": capability_system_created,
        "CapabilityPermissionDiagnosticsPassed": diagnostics_passed,
        "AllowedCapabilityPolicyOK": allowed_policy_ok,
        "ApprovalCapabilityPolicyOK": approval_policy_ok,
        "DeniedCapabilityPolicyOK": denied_policy_ok,
        "DefaultCapabilityPolicyOK": default_policy_ok,
        "CapabilitySystemSummaryOK": system_summary_ok,
        "CapabilityPermissionCompletionConfirmed": completed,
        "AllowedCapabilities": [
            "health",
            "stability",
            "backup",
            "recovery",
            "goal",
            "event",
            "daemon",
            "audit",
        ],
        "ApprovalRequiredCapabilities": [
            "text_ai",
            "image_ai",
            "video_ai",
            "voice_ai",
            "browser",
            "gui",
            "app_operator",
            "external_ai",
        ],
        "DeniedCapabilities": [
            "unknown_capability",
        ],
        "HumanApproved": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": "Phase87 External AI Permission Router",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"capability_permission_completion_report_{timestamp}.json"
    latest_json_path = BASE_DIR / "capability_permission_completion_report.json"
    txt_path = BASE_DIR / "capability_permission_completion_report.txt"

    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    latest_json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    lines = [
        "=== Capability Permission Completion Report ===",
        f"status: {report['status']}",
        f"phase: {report['phase']}",
        f"CapabilitySystemFound: {report['CapabilitySystemFound']}",
        f"DiagnosticsFound: {report['DiagnosticsFound']}",
        f"CapabilitySystemCompleted: {report['CapabilitySystemCompleted']}",
        f"DiagnosticsCompleted: {report['DiagnosticsCompleted']}",
        f"CapabilityPermissionSystemCreated: {report['CapabilityPermissionSystemCreated']}",
        f"CapabilityPermissionDiagnosticsPassed: {report['CapabilityPermissionDiagnosticsPassed']}",
        f"AllowedCapabilityPolicyOK: {report['AllowedCapabilityPolicyOK']}",
        f"ApprovalCapabilityPolicyOK: {report['ApprovalCapabilityPolicyOK']}",
        f"DeniedCapabilityPolicyOK: {report['DeniedCapabilityPolicyOK']}",
        f"DefaultCapabilityPolicyOK: {report['DefaultCapabilityPolicyOK']}",
        f"CapabilitySystemSummaryOK: {report['CapabilitySystemSummaryOK']}",
        f"CapabilityPermissionCompletionConfirmed: {report['CapabilityPermissionCompletionConfirmed']}",
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