from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase85-3 Policy Engine Completion Report"

ENGINE_PATH = BASE_DIR / "policy_engine.json"
DIAGNOSTICS_PATH = BASE_DIR / "policy_engine_diagnostics.json"

def load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def build_report():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    engine = load_json(ENGINE_PATH)
    diagnostics = load_json(DIAGNOSTICS_PATH)

    engine_found = engine is not None
    diagnostics_found = diagnostics is not None

    engine_completed = engine_found and engine.get("status") == "completed"
    diagnostics_completed = diagnostics_found and diagnostics.get("status") == "completed"

    policy_engine_created = (
        engine_found
        and engine.get("PolicyEngineCreated") is True
    )

    diagnostics_passed = (
        diagnostics_found
        and diagnostics.get("PolicyEngineDiagnosticsPassed") is True
    )

    allowed_policy_ok = (
        diagnostics_found
        and diagnostics.get("AllowedPolicyOK") is True
    )

    approval_policy_ok = (
        diagnostics_found
        and diagnostics.get("ApprovalPolicyOK") is True
    )

    denied_policy_ok = (
        diagnostics_found
        and diagnostics.get("DeniedPolicyOK") is True
    )

    default_policy_ok = (
        diagnostics_found
        and diagnostics.get("DefaultPolicyOK") is True
    )

    engine_summary_ok = (
        diagnostics_found
        and diagnostics.get("EngineSummaryOK") is True
    )

    completed = (
        engine_completed
        and diagnostics_completed
        and policy_engine_created
        and diagnostics_passed
        and allowed_policy_ok
        and approval_policy_ok
        and denied_policy_ok
        and default_policy_ok
        and engine_summary_ok
    )

    report = {
        "status": "completed" if completed else "failed",
        "phase": PHASE,
        "PolicyEngineFound": engine_found,
        "DiagnosticsFound": diagnostics_found,
        "PolicyEngineCompleted": engine_completed,
        "DiagnosticsCompleted": diagnostics_completed,
        "PolicyEngineCreated": policy_engine_created,
        "PolicyEngineDiagnosticsPassed": diagnostics_passed,
        "AllowedPolicyOK": allowed_policy_ok,
        "ApprovalPolicyOK": approval_policy_ok,
        "DeniedPolicyOK": denied_policy_ok,
        "DefaultPolicyOK": default_policy_ok,
        "EngineSummaryOK": engine_summary_ok,
        "PolicyEngineCompletionConfirmed": completed,
        "PolicyModes": {
            "allow": "safe dry_run operations only",
            "approval_required": "dangerous or capability operations require human approval",
            "deny": "unknown operations are denied by default",
        },
        "HumanApproved": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": "Phase86 Capability Permission System",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"policy_engine_completion_report_{timestamp}.json"
    latest_json_path = BASE_DIR / "policy_engine_completion_report.json"
    txt_path = BASE_DIR / "policy_engine_completion_report.txt"

    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    latest_json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    lines = [
        "=== Policy Engine Completion Report ===",
        f"status: {report['status']}",
        f"phase: {report['phase']}",
        f"PolicyEngineFound: {report['PolicyEngineFound']}",
        f"DiagnosticsFound: {report['DiagnosticsFound']}",
        f"PolicyEngineCompleted: {report['PolicyEngineCompleted']}",
        f"DiagnosticsCompleted: {report['DiagnosticsCompleted']}",
        f"PolicyEngineCreated: {report['PolicyEngineCreated']}",
        f"PolicyEngineDiagnosticsPassed: {report['PolicyEngineDiagnosticsPassed']}",
        f"AllowedPolicyOK: {report['AllowedPolicyOK']}",
        f"ApprovalPolicyOK: {report['ApprovalPolicyOK']}",
        f"DeniedPolicyOK: {report['DeniedPolicyOK']}",
        f"DefaultPolicyOK: {report['DefaultPolicyOK']}",
        f"EngineSummaryOK: {report['EngineSummaryOK']}",
        f"PolicyEngineCompletionConfirmed: {report['PolicyEngineCompletionConfirmed']}",
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