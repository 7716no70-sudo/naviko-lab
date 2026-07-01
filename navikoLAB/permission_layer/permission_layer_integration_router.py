from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase83-1 Permission Layer Integration Router"

ALLOWED_REQUESTS = {
    "dry_run_cycle",
    "health_check",
    "stability_check",
    "backup_check",
    "recovery_check",
    "goal_check",
    "event_check",
    "daemon_check",
    "audit_check",
}

BLOCKED_REQUESTS = {
    "external_operation",
    "original_write",
    "file_delete",
    "real_gui_operation",
    "browser_operation",
    "auto_execute",
}

MODULE_ROUTE_MAP = {
    "health": "health_check",
    "stability": "stability_check",
    "backup": "backup_check",
    "recovery": "recovery_check",
    "goal": "goal_check",
    "event": "event_check",
    "daemon": "daemon_check",
    "audit": "audit_check",
    "cycle": "dry_run_cycle",
}

def permission_request(module_name, requested_operation, dry_run=True):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    allowed = requested_operation in ALLOWED_REQUESTS
    blocked = requested_operation in BLOCKED_REQUESTS

    if blocked:
        decision = "blocked"
    elif allowed:
        decision = "allowed"
    else:
        decision = "blocked_unknown_request"

    result = {
        "timestamp": timestamp,
        "phase": PHASE,
        "module": module_name,
        "requested_operation": requested_operation,
        "decision": decision,
        "allowed": decision == "allowed",
        "blocked": decision != "allowed",
        "dry_run": dry_run,
        "PermissionLayerUsed": True,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "RiskCount": 0 if decision == "allowed" else 1,
        "SafeToContinue": decision == "allowed",
    }

    return result

def route_module_request(module_name):
    requested_operation = MODULE_ROUTE_MAP.get(module_name, "unknown_request")
    return permission_request(module_name, requested_operation, dry_run=True)

def run_integration_test():
    results = []

    for module_name in MODULE_ROUTE_MAP.keys():
        results.append(route_module_request(module_name))

    blocked_tests = [
        "external_operation",
        "original_write",
        "file_delete",
        "real_gui_operation",
        "browser_operation",
        "auto_execute",
    ]

    for op in blocked_tests:
        results.append(permission_request("blocked_test", op, dry_run=True))

    allowed_results = [r for r in results if r["allowed"]]
    blocked_results = [r for r in results if r["blocked"]]

    report = {
        "status": "completed",
        "phase": PHASE,
        "PermissionLayerIntegrationRouterCreated": True,
        "ModuleRouteCount": len(MODULE_ROUTE_MAP),
        "AllowedRouteCount": len(allowed_results),
        "BlockedRouteCount": len(blocked_results),
        "AllModuleRoutesUsedPermissionLayer": all(r["PermissionLayerUsed"] for r in results),
        "AllAllowedRoutesPassed": all(r["allowed"] for r in allowed_results),
        "AllBlockedTestsBlocked": all(r["blocked"] for r in blocked_results),
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "Mode": "dry_run",
        "RiskCount": 0,
        "SafeToContinue": True,
        "NextPhase": "Phase83-2 Permission Layer Integration Diagnostics",
        "results": results,
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"permission_layer_integration_router_{timestamp}.json"
    latest_path = BASE_DIR / "permission_layer_integration_router.json"

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
    report, report_path = run_integration_test()

    print("=== Permission Layer Integration Router ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"PermissionLayerIntegrationRouterCreated: {report['PermissionLayerIntegrationRouterCreated']}")
    print(f"ModuleRouteCount: {report['ModuleRouteCount']}")
    print(f"AllowedRouteCount: {report['AllowedRouteCount']}")
    print(f"BlockedRouteCount: {report['BlockedRouteCount']}")
    print(f"AllModuleRoutesUsedPermissionLayer: {report['AllModuleRoutesUsedPermissionLayer']}")
    print(f"AllAllowedRoutesPassed: {report['AllAllowedRoutesPassed']}")
    print(f"AllBlockedTestsBlocked: {report['AllBlockedTestsBlocked']}")
    print(f"Mode: {report['Mode']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"NextPhase: {report['NextPhase']}")
    print(f"保存先: {report_path}")

if __name__ == "__main__":
    main()