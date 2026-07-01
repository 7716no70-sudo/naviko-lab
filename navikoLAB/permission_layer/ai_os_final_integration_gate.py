from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase90-1 AI OS Final Integration Gate"

REQUIRED_COMPLETION_REPORTS = {
    "permission_layer": BASE_DIR / "permission_layer_completion_report.json",
    "permission_layer_integration": BASE_DIR / "permission_layer_integration_completion_report.json",
    "human_approval": BASE_DIR / "human_approval_workflow_completion_report.json",
    "policy_engine": BASE_DIR / "policy_engine_completion_report.json",
    "capability_permission": BASE_DIR / "capability_permission_completion_report.json",
    "external_ai_permission": BASE_DIR / "external_ai_permission_completion_report.json",
    "browser_permission": BASE_DIR / "browser_permission_completion_report.json",
    "gui_permission": BASE_DIR / "gui_permission_completion_report.json",
}

def load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def build_gate_report():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    loaded_reports = {}
    report_status = {}

    for name, path in REQUIRED_COMPLETION_REPORTS.items():
        data = load_json(path)
        loaded_reports[name] = data
        report_status[name] = {
            "path": str(path),
            "found": data is not None,
            "completed": data is not None and data.get("status") == "completed",
            "safe_to_continue": data is not None and data.get("SafeToContinue") is True,
            "risk_count": data.get("RiskCount") if data else None,
        }

    all_reports_found = all(item["found"] for item in report_status.values())
    all_reports_completed = all(item["completed"] for item in report_status.values())
    all_safe_to_continue = all(item["safe_to_continue"] for item in report_status.values())
    all_risk_zero = all(item["risk_count"] == 0 for item in report_status.values())

    dangerous_flags_all_false = True

    for data in loaded_reports.values():
        if not data:
            dangerous_flags_all_false = False
            break

        if data.get("OriginalWrite", False) is not False:
            dangerous_flags_all_false = False

        if data.get("ExternalOperation", False) is not False:
            dangerous_flags_all_false = False

        if data.get("BrowserOperation", False) is not False:
            dangerous_flags_all_false = False

        if data.get("RealGUIOperation", False) is not False:
            dangerous_flags_all_false = False

        if data.get("FileDelete", False) is not False:
            dangerous_flags_all_false = False

        if data.get("HumanApproved", False) is not False:
            dangerous_flags_all_false = False

    integration_gate_open = (
        all_reports_found
        and all_reports_completed
        and all_safe_to_continue
        and all_risk_zero
        and dangerous_flags_all_false
    )

    report = {
        "status": "completed" if integration_gate_open else "failed",
        "phase": PHASE,
        "RequiredCompletionReportCount": len(REQUIRED_COMPLETION_REPORTS),
        "AllReportsFound": all_reports_found,
        "AllReportsCompleted": all_reports_completed,
        "AllSafeToContinue": all_safe_to_continue,
        "AllRiskZero": all_risk_zero,
        "DangerousFlagsAllFalse": dangerous_flags_all_false,
        "AIOSFinalIntegrationGateOpen": integration_gate_open,
        "IntegratedSafetyLayers": [
            "Permission Layer",
            "Permission Layer Integration",
            "Human Approval Workflow",
            "Policy Engine",
            "Capability Permission System",
            "External AI Permission Router",
            "Browser Permission Router",
            "GUI Permission Router",
        ],
        "ReportStatus": report_status,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "HumanApproved": False,
        "Mode": "dry_run",
        "RiskCount": 0 if integration_gate_open else 1,
        "SafeToContinue": integration_gate_open,
        "NextPhase": "Phase90-2 AI OS Final Integration Diagnostics",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"ai_os_final_integration_gate_{timestamp}.json"
    latest_path = BASE_DIR / "ai_os_final_integration_gate.json"

    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    latest_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return report, report_path

def main():
    report, report_path = build_gate_report()

    print("=== AI OS Final Integration Gate ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"RequiredCompletionReportCount: {report['RequiredCompletionReportCount']}")
    print(f"AllReportsFound: {report['AllReportsFound']}")
    print(f"AllReportsCompleted: {report['AllReportsCompleted']}")
    print(f"AllSafeToContinue: {report['AllSafeToContinue']}")
    print(f"AllRiskZero: {report['AllRiskZero']}")
    print(f"DangerousFlagsAllFalse: {report['DangerousFlagsAllFalse']}")
    print(f"AIOSFinalIntegrationGateOpen: {report['AIOSFinalIntegrationGateOpen']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(f"Mode: {report['Mode']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"NextPhase: {report['NextPhase']}")
    print(f"保存先: {report_path}")

if __name__ == "__main__":
    main()