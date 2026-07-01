from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase90-2 AI OS Final Integration Diagnostics"

GATE_PATH = BASE_DIR / "ai_os_final_integration_gate.json"

REQUIRED_LAYERS = [
    "permission_layer",
    "permission_layer_integration",
    "human_approval",
    "policy_engine",
    "capability_permission",
    "external_ai_permission",
    "browser_permission",
    "gui_permission",
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
    gate = load_json(GATE_PATH)

    gate_found = gate is not None
    gate_completed = gate_found and gate.get("status") == "completed"

    report_status = gate.get("ReportStatus", {}) if gate_found else {}

    missing_layers = [
        layer for layer in REQUIRED_LAYERS
        if layer not in report_status
    ]

    all_layers_found = (
        len(missing_layers) == 0
        and all(report_status[layer].get("found") is True for layer in REQUIRED_LAYERS)
    )

    all_layers_completed = (
        len(missing_layers) == 0
        and all(report_status[layer].get("completed") is True for layer in REQUIRED_LAYERS)
    )

    all_layers_safe = (
        len(missing_layers) == 0
        and all(report_status[layer].get("safe_to_continue") is True for layer in REQUIRED_LAYERS)
    )

    all_layers_risk_zero = (
        len(missing_layers) == 0
        and all(report_status[layer].get("risk_count") == 0 for layer in REQUIRED_LAYERS)
    )

    gate_summary_ok = (
        gate_found
        and gate.get("AllReportsFound") is True
        and gate.get("AllReportsCompleted") is True
        and gate.get("AllSafeToContinue") is True
        and gate.get("AllRiskZero") is True
        and gate.get("DangerousFlagsAllFalse") is True
        and gate.get("AIOSFinalIntegrationGateOpen") is True
        and gate.get("OriginalWrite") is False
        and gate.get("ExternalOperation") is False
        and gate.get("BrowserOperation") is False
        and gate.get("RealGUIOperation") is False
        and gate.get("FileDelete") is False
        and gate.get("HumanApproved") is False
    )

    diagnostics_passed = (
        gate_found
        and gate_completed
        and all_layers_found
        and all_layers_completed
        and all_layers_safe
        and all_layers_risk_zero
        and gate_summary_ok
    )

    report = {
        "status": "completed" if diagnostics_passed else "failed",
        "phase": PHASE,
        "GateFound": gate_found,
        "GateCompleted": gate_completed,
        "RequiredLayerCount": len(REQUIRED_LAYERS),
        "MissingLayerCount": len(missing_layers),
        "MissingLayers": missing_layers,
        "AllLayersFound": all_layers_found,
        "AllLayersCompleted": all_layers_completed,
        "AllLayersSafe": all_layers_safe,
        "AllLayersRiskZero": all_layers_risk_zero,
        "GateSummaryOK": gate_summary_ok,
        "AIOSFinalIntegrationDiagnosticsPassed": diagnostics_passed,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "HumanApproved": False,
        "Mode": "dry_run",
        "RiskCount": 0 if diagnostics_passed else 1,
        "SafeToContinue": diagnostics_passed,
        "NextPhase": "Phase90-3 AI OS Final Integration Completion Report",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"ai_os_final_integration_diagnostics_{timestamp}.json"
    latest_path = BASE_DIR / "ai_os_final_integration_diagnostics.json"

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

    print("=== AI OS Final Integration Diagnostics ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"GateFound: {report['GateFound']}")
    print(f"GateCompleted: {report['GateCompleted']}")
    print(f"RequiredLayerCount: {report['RequiredLayerCount']}")
    print(f"MissingLayerCount: {report['MissingLayerCount']}")
    print(f"AllLayersFound: {report['AllLayersFound']}")
    print(f"AllLayersCompleted: {report['AllLayersCompleted']}")
    print(f"AllLayersSafe: {report['AllLayersSafe']}")
    print(f"AllLayersRiskZero: {report['AllLayersRiskZero']}")
    print(f"GateSummaryOK: {report['GateSummaryOK']}")
    print(f"AIOSFinalIntegrationDiagnosticsPassed: {report['AIOSFinalIntegrationDiagnosticsPassed']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(f"Mode: {report['Mode']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"NextPhase: {report['NextPhase']}")
    print(f"保存先: {report_path}")

if __name__ == "__main__":
    main()