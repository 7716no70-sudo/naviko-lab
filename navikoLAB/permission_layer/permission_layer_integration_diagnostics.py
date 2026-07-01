from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase83-2 Permission Layer Integration Diagnostics"

ROUTER_REPORT_PATH = BASE_DIR / "permission_layer_integration_router.json"

REQUIRED_MODULES = [
    "health",
    "stability",
    "backup",
    "recovery",
    "goal",
    "event",
    "daemon",
    "audit",
    "cycle",
]

REQUIRED_BLOCKED_OPERATIONS = [
    "external_operation",
    "original_write",
    "file_delete",
    "real_gui_operation",
    "browser_operation",
    "auto_execute",
]

def load_router_report():
    if not ROUTER_REPORT_PATH.exists():
        return None
    try:
        return json.loads(ROUTER_REPORT_PATH.read_text(encoding="utf-8"))
    except Exception:
        return None

def build_diagnostics():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    router_report = load_router_report()

    source_found = router_report is not None
    results = router_report.get("results", []) if router_report else []

    module_results = [
        r for r in results
        if r.get("module") in REQUIRED_MODULES
    ]

    blocked_results = [
        r for r in results
        if r.get("requested_operation") in REQUIRED_BLOCKED_OPERATIONS
    ]

    routed_modules = sorted(set(r.get("module") for r in module_results))
    missing_modules = sorted(set(REQUIRED_MODULES) - set(routed_modules))

    blocked_operations = sorted(set(r.get("requested_operation") for r in blocked_results))
    missing_blocked_operations = sorted(
        set(REQUIRED_BLOCKED_OPERATIONS) - set(blocked_operations)
    )

    all_modules_routed = len(missing_modules) == 0
    all_module_routes_used_permission_layer = (
        bool(module_results)
        and all(r.get("PermissionLayerUsed") is True for r in module_results)
    )

    all_module_routes_allowed = (
        bool(module_results)
        and all(r.get("allowed") is True for r in module_results)
    )

    all_blocked_tests_found = len(missing_blocked_operations) == 0
    all_blocked_tests_blocked = (
        bool(blocked_results)
        and all(r.get("blocked") is True for r in blocked_results)
    )

    dangerous_flags_all_false = (
        router_report is not None
        and router_report.get("OriginalWrite") is False
        and router_report.get("ExternalOperation") is False
        and router_report.get("BrowserOperation") is False
        and router_report.get("RealGUIOperation") is False
        and router_report.get("FileDelete") is False
    )

    diagnostics_passed = (
        source_found
        and all_modules_routed
        and all_module_routes_used_permission_layer
        and all_module_routes_allowed
        and all_blocked_tests_found
        and all_blocked_tests_blocked
        and dangerous_flags_all_false
    )

    report = {
        "status": "completed" if diagnostics_passed else "failed",
        "phase": PHASE,
        "SourceFound": source_found,
        "RouterReportPath": str(ROUTER_REPORT_PATH),
        "RequiredModuleCount": len(REQUIRED_MODULES),
        "RoutedModuleCount": len(routed_modules),
        "MissingModuleCount": len(missing_modules),
        "MissingModules": missing_modules,
        "RequiredBlockedOperationCount": len(REQUIRED_BLOCKED_OPERATIONS),
        "BlockedOperationCount": len(blocked_operations),
        "MissingBlockedOperationCount": len(missing_blocked_operations),
        "MissingBlockedOperations": missing_blocked_operations,
        "AllModulesRouted": all_modules_routed,
        "AllModuleRoutesUsedPermissionLayer": all_module_routes_used_permission_layer,
        "AllModuleRoutesAllowed": all_module_routes_allowed,
        "AllBlockedTestsFound": all_blocked_tests_found,
        "AllBlockedTestsBlocked": all_blocked_tests_blocked,
        "DangerousFlagsAllFalse": dangerous_flags_all_false,
        "PermissionLayerIntegrationDiagnosticsPassed": diagnostics_passed,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0 if diagnostics_passed else 1,
        "SafeToContinue": diagnostics_passed,
        "NextPhase": "Phase83-3 Permission Layer Integration Completion Report",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"permission_layer_integration_diagnostics_{timestamp}.json"
    latest_path = BASE_DIR / "permission_layer_integration_diagnostics.json"

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

    print("=== Permission Layer Integration Diagnostics ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"SourceFound: {report['SourceFound']}")
    print(f"RequiredModuleCount: {report['RequiredModuleCount']}")
    print(f"RoutedModuleCount: {report['RoutedModuleCount']}")
    print(f"MissingModuleCount: {report['MissingModuleCount']}")
    print(f"RequiredBlockedOperationCount: {report['RequiredBlockedOperationCount']}")
    print(f"BlockedOperationCount: {report['BlockedOperationCount']}")
    print(f"MissingBlockedOperationCount: {report['MissingBlockedOperationCount']}")
    print(f"AllModulesRouted: {report['AllModulesRouted']}")
    print(f"AllModuleRoutesUsedPermissionLayer: {report['AllModuleRoutesUsedPermissionLayer']}")
    print(f"AllModuleRoutesAllowed: {report['AllModuleRoutesAllowed']}")
    print(f"AllBlockedTestsFound: {report['AllBlockedTestsFound']}")
    print(f"AllBlockedTestsBlocked: {report['AllBlockedTestsBlocked']}")
    print(f"DangerousFlagsAllFalse: {report['DangerousFlagsAllFalse']}")
    print(f"PermissionLayerIntegrationDiagnosticsPassed: {report['PermissionLayerIntegrationDiagnosticsPassed']}")
    print(f"Mode: {report['Mode']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"NextPhase: {report['NextPhase']}")
    print(f"保存先: {report_path}")

if __name__ == "__main__":
    main()