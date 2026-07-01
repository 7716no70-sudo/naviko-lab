from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase83-3 Permission Layer Integration Completion Report"

ROUTER_PATH = BASE_DIR / "permission_layer_integration_router.json"
DIAGNOSTICS_PATH = BASE_DIR / "permission_layer_integration_diagnostics.json"

def load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def build_report():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    router = load_json(ROUTER_PATH)
    diagnostics = load_json(DIAGNOSTICS_PATH)

    router_found = router is not None
    diagnostics_found = diagnostics is not None

    router_completed = router_found and router.get("status") == "completed"
    diagnostics_completed = diagnostics_found and diagnostics.get("status") == "completed"

    integration_router_created = (
        router_found
        and router.get("PermissionLayerIntegrationRouterCreated") is True
    )

    diagnostics_passed = (
        diagnostics_found
        and diagnostics.get("PermissionLayerIntegrationDiagnosticsPassed") is True
    )

    all_modules_routed = (
        diagnostics_found
        and diagnostics.get("AllModulesRouted") is True
    )

    all_routes_used_permission_layer = (
        diagnostics_found
        and diagnostics.get("AllModuleRoutesUsedPermissionLayer") is True
    )

    all_blocked_tests_blocked = (
        diagnostics_found
        and diagnostics.get("AllBlockedTestsBlocked") is True
    )

    dangerous_flags_all_false = (
        diagnostics_found
        and diagnostics.get("DangerousFlagsAllFalse") is True
    )

    completed = (
        router_completed
        and diagnostics_completed
        and integration_router_created
        and diagnostics_passed
        and all_modules_routed
        and all_routes_used_permission_layer
        and all_blocked_tests_blocked
        and dangerous_flags_all_false
    )

    report = {
        "status": "completed" if completed else "failed",
        "phase": PHASE,
        "RouterFound": router_found,
        "DiagnosticsFound": diagnostics_found,
        "RouterCompleted": router_completed,
        "DiagnosticsCompleted": diagnostics_completed,
        "PermissionLayerIntegrationRouterCreated": integration_router_created,
        "PermissionLayerIntegrationDiagnosticsPassed": diagnostics_passed,
        "AllModulesRouted": all_modules_routed,
        "AllRoutesUsedPermissionLayer": all_routes_used_permission_layer,
        "AllBlockedTestsBlocked": all_blocked_tests_blocked,
        "DangerousFlagsAllFalse": dangerous_flags_all_false,
        "IntegratedModules": [
            "health",
            "stability",
            "backup",
            "recovery",
            "goal",
            "event",
            "daemon",
            "audit",
            "cycle",
        ],
        "BlockedOperations": [
            "external_operation",
            "original_write",
            "file_delete",
            "real_gui_operation",
            "browser_operation",
            "auto_execute",
        ],
        "PermissionLayerIntegrationCompleted": completed,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": "Phase84 Human Approval Workflow",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"permission_layer_integration_completion_report_{timestamp}.json"
    latest_json_path = BASE_DIR / "permission_layer_integration_completion_report.json"
    txt_path = BASE_DIR / "permission_layer_integration_completion_report.txt"

    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    latest_json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    lines = [
        "=== Permission Layer Integration Completion Report ===",
        f"status: {report['status']}",
        f"phase: {report['phase']}",
        f"RouterFound: {report['RouterFound']}",
        f"DiagnosticsFound: {report['DiagnosticsFound']}",
        f"RouterCompleted: {report['RouterCompleted']}",
        f"DiagnosticsCompleted: {report['DiagnosticsCompleted']}",
        f"PermissionLayerIntegrationRouterCreated: {report['PermissionLayerIntegrationRouterCreated']}",
        f"PermissionLayerIntegrationDiagnosticsPassed: {report['PermissionLayerIntegrationDiagnosticsPassed']}",
        f"AllModulesRouted: {report['AllModulesRouted']}",
        f"AllRoutesUsedPermissionLayer: {report['AllRoutesUsedPermissionLayer']}",
        f"AllBlockedTestsBlocked: {report['AllBlockedTestsBlocked']}",
        f"DangerousFlagsAllFalse: {report['DangerousFlagsAllFalse']}",
        f"PermissionLayerIntegrationCompleted: {report['PermissionLayerIntegrationCompleted']}",
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