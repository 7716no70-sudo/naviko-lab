from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase90-3 AI OS Final Integration Completion Report"

GATE_PATH = BASE_DIR / "ai_os_final_integration_gate.json"
DIAGNOSTICS_PATH = BASE_DIR / "ai_os_final_integration_diagnostics.json"

def load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def build_report():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    gate = load_json(GATE_PATH)
    diagnostics = load_json(DIAGNOSTICS_PATH)

    gate_found = gate is not None
    diagnostics_found = diagnostics is not None

    gate_completed = gate_found and gate.get("status") == "completed"
    diagnostics_completed = diagnostics_found and diagnostics.get("status") == "completed"

    gate_open = gate_found and gate.get("AIOSFinalIntegrationGateOpen") is True
    diagnostics_passed = diagnostics_found and diagnostics.get("AIOSFinalIntegrationDiagnosticsPassed") is True

    all_layers_completed = diagnostics_found and diagnostics.get("AllLayersCompleted") is True
    all_layers_safe = diagnostics_found and diagnostics.get("AllLayersSafe") is True
    all_layers_risk_zero = diagnostics_found and diagnostics.get("AllLayersRiskZero") is True

    completed = (
        gate_completed
        and diagnostics_completed
        and gate_open
        and diagnostics_passed
        and all_layers_completed
        and all_layers_safe
        and all_layers_risk_zero
    )

    report = {
        "status": "completed" if completed else "failed",
        "phase": PHASE,
        "GateFound": gate_found,
        "DiagnosticsFound": diagnostics_found,
        "GateCompleted": gate_completed,
        "DiagnosticsCompleted": diagnostics_completed,
        "AIOSFinalIntegrationGateOpen": gate_open,
        "AIOSFinalIntegrationDiagnosticsPassed": diagnostics_passed,
        "AllLayersCompleted": all_layers_completed,
        "AllLayersSafe": all_layers_safe,
        "AllLayersRiskZero": all_layers_risk_zero,
        "AIOSFinalIntegrationCompleted": completed,
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
        "CurrentLevel": "safe_dry_run_ai_os_integrated_foundation",
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "HumanApproved": False,
        "Mode": "dry_run",
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": "Phase91 AI OS Unified Execution Bus",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"ai_os_final_integration_completion_report_{timestamp}.json"
    latest_json_path = BASE_DIR / "ai_os_final_integration_completion_report.json"
    txt_path = BASE_DIR / "ai_os_final_integration_completion_report.txt"

    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    latest_json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "=== AI OS Final Integration Completion Report ===",
        f"status: {report['status']}",
        f"phase: {report['phase']}",
        f"GateFound: {report['GateFound']}",
        f"DiagnosticsFound: {report['DiagnosticsFound']}",
        f"GateCompleted: {report['GateCompleted']}",
        f"DiagnosticsCompleted: {report['DiagnosticsCompleted']}",
        f"AIOSFinalIntegrationGateOpen: {report['AIOSFinalIntegrationGateOpen']}",
        f"AIOSFinalIntegrationDiagnosticsPassed: {report['AIOSFinalIntegrationDiagnosticsPassed']}",
        f"AllLayersCompleted: {report['AllLayersCompleted']}",
        f"AllLayersSafe: {report['AllLayersSafe']}",
        f"AllLayersRiskZero: {report['AllLayersRiskZero']}",
        f"AIOSFinalIntegrationCompleted: {report['AIOSFinalIntegrationCompleted']}",
        f"CurrentLevel: {report['CurrentLevel']}",
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