from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase91-2 AI OS Unified Execution Bus Diagnostics"

BUS_PATH = BASE_DIR / "ai_os_unified_execution_bus.json"

REQUIRED_SAFE_OPERATIONS = [
    "health_check",
    "stability_check",
    "backup_check",
    "recovery_check",
    "goal_check",
    "event_check",
    "daemon_check",
    "audit_check",
    "dry_run_cycle",
]

REQUIRED_APPROVAL_OPERATIONS = [
    "external_ai_execute",
    "browser_open",
    "gui_click",
    "original_write",
    "file_delete",
]

REQUIRED_DENIED_OPERATIONS = [
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

    bus = load_json(BUS_PATH)
    bus_found = bus is not None

    results = bus.get("results", []) if bus_found else []

    result_by_operation = {
        r.get("operation"): r for r in results
    }

    missing_safe = [op for op in REQUIRED_SAFE_OPERATIONS if op not in result_by_operation]
    missing_approval = [op for op in REQUIRED_APPROVAL_OPERATIONS if op not in result_by_operation]
    missing_denied = [op for op in REQUIRED_DENIED_OPERATIONS if op not in result_by_operation]

    safe_routes_ok = (
        len(missing_safe) == 0
        and all(
            result_by_operation[op].get("allowed") is True
            and result_by_operation[op].get("SafeToExecute") is True
            and result_by_operation[op].get("Executed") is False
            for op in REQUIRED_SAFE_OPERATIONS
        )
    )

    approval_routes_ok = (
        len(missing_approval) == 0
        and all(
            result_by_operation[op].get("approval_required") is True
            and result_by_operation[op].get("allowed") is False
            and result_by_operation[op].get("SafeToExecute") is False
            and result_by_operation[op].get("Executed") is False
            for op in REQUIRED_APPROVAL_OPERATIONS
        )
    )

    denied_routes_ok = (
        len(missing_denied) == 0
        and all(
            result_by_operation[op].get("denied") is True
            and result_by_operation[op].get("allowed") is False
            and result_by_operation[op].get("SafeToExecute") is False
            and result_by_operation[op].get("Executed") is False
            for op in REQUIRED_DENIED_OPERATIONS
        )
    )

    all_routes_use_bus = (
        bool(results)
        and all(r.get("UnifiedExecutionBusUsed") is True for r in results)
    )

    all_routes_require_safety_layers = (
        bool(results)
        and all(
            r.get("PolicyEngineRequired") is True
            and r.get("PermissionLayerRequired") is True
            and r.get("CapabilityPermissionRequired") is True
            for r in results
        )
    )

    dangerous_flags_all_false = (
        bus_found
        and bus.get("Executed") is False
        and bus.get("OriginalWrite") is False
        and bus.get("ExternalOperation") is False
        and bus.get("ExternalCommunicationExecuted") is False
        and bus.get("BrowserOperation") is False
        and bus.get("RealGUIOperation") is False
        and bus.get("FileDelete") is False
        and bus.get("HumanApproved") is False
    )

    bus_summary_ok = (
        bus_found
        and bus.get("UnifiedExecutionBusCreated") is True
        and bus.get("AllSafeRoutesAllowedDryRun") is True
        and bus.get("AllApprovalRoutesBlocked") is True
        and bus.get("AllDeniedRoutesBlocked") is True
        and bus.get("UnifiedExecutionBusUsedForAll") is True
        and bus.get("PolicyEngineRequiredForAll") is True
        and bus.get("PermissionLayerRequiredForAll") is True
        and bus.get("CapabilityPermissionRequiredForAll") is True
    )

    diagnostics_passed = (
        bus_found
        and safe_routes_ok
        and approval_routes_ok
        and denied_routes_ok
        and all_routes_use_bus
        and all_routes_require_safety_layers
        and dangerous_flags_all_false
        and bus_summary_ok
    )

    report = {
        "status": "completed" if diagnostics_passed else "failed",
        "phase": PHASE,
        "BusFound": bus_found,
        "RequiredSafeOperationCount": len(REQUIRED_SAFE_OPERATIONS),
        "RequiredApprovalOperationCount": len(REQUIRED_APPROVAL_OPERATIONS),
        "RequiredDeniedOperationCount": len(REQUIRED_DENIED_OPERATIONS),
        "MissingSafeOperationCount": len(missing_safe),
        "MissingApprovalOperationCount": len(missing_approval),
        "MissingDeniedOperationCount": len(missing_denied),
        "MissingSafeOperations": missing_safe,
        "MissingApprovalOperations": missing_approval,
        "MissingDeniedOperations": missing_denied,
        "SafeRoutesOK": safe_routes_ok,
        "ApprovalRoutesOK": approval_routes_ok,
        "DeniedRoutesOK": denied_routes_ok,
        "AllRoutesUseBus": all_routes_use_bus,
        "AllRoutesRequireSafetyLayers": all_routes_require_safety_layers,
        "DangerousFlagsAllFalse": dangerous_flags_all_false,
        "BusSummaryOK": bus_summary_ok,
        "UnifiedExecutionBusDiagnosticsPassed": diagnostics_passed,
        "Executed": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "ExternalCommunicationExecuted": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "HumanApproved": False,
        "Mode": "dry_run",
        "RiskCount": 0 if diagnostics_passed else 1,
        "SafeToContinue": diagnostics_passed,
        "NextPhase": "Phase91-3 AI OS Unified Execution Bus Completion Report",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"ai_os_unified_execution_bus_diagnostics_{timestamp}.json"
    latest_path = BASE_DIR / "ai_os_unified_execution_bus_diagnostics.json"

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
    report, report_path = build_diagnostics()

    print("=== AI OS Unified Execution Bus Diagnostics ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"BusFound: {report['BusFound']}")
    print(f"RequiredSafeOperationCount: {report['RequiredSafeOperationCount']}")
    print(f"RequiredApprovalOperationCount: {report['RequiredApprovalOperationCount']}")
    print(f"RequiredDeniedOperationCount: {report['RequiredDeniedOperationCount']}")
    print(f"MissingSafeOperationCount: {report['MissingSafeOperationCount']}")
    print(f"MissingApprovalOperationCount: {report['MissingApprovalOperationCount']}")
    print(f"MissingDeniedOperationCount: {report['MissingDeniedOperationCount']}")
    print(f"SafeRoutesOK: {report['SafeRoutesOK']}")
    print(f"ApprovalRoutesOK: {report['ApprovalRoutesOK']}")
    print(f"DeniedRoutesOK: {report['DeniedRoutesOK']}")
    print(f"AllRoutesUseBus: {report['AllRoutesUseBus']}")
    print(f"AllRoutesRequireSafetyLayers: {report['AllRoutesRequireSafetyLayers']}")
    print(f"DangerousFlagsAllFalse: {report['DangerousFlagsAllFalse']}")
    print(f"BusSummaryOK: {report['BusSummaryOK']}")
    print(f"UnifiedExecutionBusDiagnosticsPassed: {report['UnifiedExecutionBusDiagnosticsPassed']}")
    print(f"Executed: {report['Executed']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(f"Mode: {report['Mode']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"NextPhase: {report['NextPhase']}")
    print(f"保存先: {report_path}")

if __name__ == "__main__":
    main()