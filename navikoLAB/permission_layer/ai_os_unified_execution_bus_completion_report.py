from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase91-3 AI OS Unified Execution Bus Completion Report"

BUS_PATH = BASE_DIR / "ai_os_unified_execution_bus.json"
DIAGNOSTICS_PATH = BASE_DIR / "ai_os_unified_execution_bus_diagnostics.json"

def load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def build_report():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    bus = load_json(BUS_PATH)
    diagnostics = load_json(DIAGNOSTICS_PATH)

    bus_found = bus is not None
    diagnostics_found = diagnostics is not None

    bus_completed = bus_found and bus.get("status") == "completed"
    diagnostics_completed = diagnostics_found and diagnostics.get("status") == "completed"

    bus_created = bus_found and bus.get("UnifiedExecutionBusCreated") is True
    diagnostics_passed = diagnostics_found and diagnostics.get("UnifiedExecutionBusDiagnosticsPassed") is True

    all_routes_use_bus = diagnostics_found and diagnostics.get("AllRoutesUseBus") is True
    all_routes_require_safety_layers = diagnostics_found and diagnostics.get("AllRoutesRequireSafetyLayers") is True
    dangerous_flags_all_false = diagnostics_found and diagnostics.get("DangerousFlagsAllFalse") is True
    bus_summary_ok = diagnostics_found and diagnostics.get("BusSummaryOK") is True

    completed = (
        bus_completed
        and diagnostics_completed
        and bus_created
        and diagnostics_passed
        and all_routes_use_bus
        and all_routes_require_safety_layers
        and dangerous_flags_all_false
        and bus_summary_ok
    )

    report = {
        "status": "completed" if completed else "failed",
        "phase": PHASE,
        "BusFound": bus_found,
        "DiagnosticsFound": diagnostics_found,
        "BusCompleted": bus_completed,
        "DiagnosticsCompleted": diagnostics_completed,
        "UnifiedExecutionBusCreated": bus_created,
        "UnifiedExecutionBusDiagnosticsPassed": diagnostics_passed,
        "AllRoutesUseBus": all_routes_use_bus,
        "AllRoutesRequireSafetyLayers": all_routes_require_safety_layers,
        "DangerousFlagsAllFalse": dangerous_flags_all_false,
        "BusSummaryOK": bus_summary_ok,
        "UnifiedExecutionBusCompletionConfirmed": completed,
        "CurrentLevel": "safe_dry_run_unified_execution_bus_ready",
        "Executed": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "ExternalCommunicationExecuted": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "HumanApproved": False,
        "Mode": "dry_run",
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": "Phase92 AI OS Unified Control Plane",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"ai_os_unified_execution_bus_completion_report_{timestamp}.json"
    latest_json_path = BASE_DIR / "ai_os_unified_execution_bus_completion_report.json"
    txt_path = BASE_DIR / "ai_os_unified_execution_bus_completion_report.txt"

    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    latest_json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "=== AI OS Unified Execution Bus Completion Report ===",
        f"status: {report['status']}",
        f"phase: {report['phase']}",
        f"BusFound: {report['BusFound']}",
        f"DiagnosticsFound: {report['DiagnosticsFound']}",
        f"BusCompleted: {report['BusCompleted']}",
        f"DiagnosticsCompleted: {report['DiagnosticsCompleted']}",
        f"UnifiedExecutionBusCreated: {report['UnifiedExecutionBusCreated']}",
        f"UnifiedExecutionBusDiagnosticsPassed: {report['UnifiedExecutionBusDiagnosticsPassed']}",
        f"AllRoutesUseBus: {report['AllRoutesUseBus']}",
        f"AllRoutesRequireSafetyLayers: {report['AllRoutesRequireSafetyLayers']}",
        f"DangerousFlagsAllFalse: {report['DangerousFlagsAllFalse']}",
        f"BusSummaryOK: {report['BusSummaryOK']}",
        f"UnifiedExecutionBusCompletionConfirmed: {report['UnifiedExecutionBusCompletionConfirmed']}",
        f"CurrentLevel: {report['CurrentLevel']}",
        f"Executed: {report['Executed']}",
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