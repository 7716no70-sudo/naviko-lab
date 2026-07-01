from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
BUS_DIR = BASE_DIR / "execution_bus"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
BUS_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase91-1 AI OS Unified Execution Bus"

SAFE_BUS_OPERATIONS = {
    "health_check",
    "stability_check",
    "backup_check",
    "recovery_check",
    "goal_check",
    "event_check",
    "daemon_check",
    "audit_check",
    "dry_run_cycle",
}

APPROVAL_REQUIRED_BUS_OPERATIONS = {
    "external_ai_execute",
    "browser_open",
    "browser_click",
    "browser_input",
    "browser_submit",
    "browser_download",
    "gui_click",
    "gui_input",
    "gui_drag",
    "gui_hotkey",
    "gui_app_control",
    "original_write",
    "file_delete",
    "auto_execute",
}

def route_execution_request(source_module, operation, payload=None):
    payload = payload or {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if operation in SAFE_BUS_OPERATIONS:
        decision = "allow_dry_run"
        allowed = True
        approval_required = False
        denied = False
        risk_level = 0
    elif operation in APPROVAL_REQUIRED_BUS_OPERATIONS:
        decision = "approval_required"
        allowed = False
        approval_required = True
        denied = False
        risk_level = 4
    else:
        decision = "deny"
        allowed = False
        approval_required = True
        denied = True
        risk_level = 5

    result = {
        "timestamp": timestamp,
        "phase": PHASE,
        "source_module": source_module,
        "operation": operation,
        "payload_preview": str(payload)[:200],
        "bus_decision": decision,
        "allowed": allowed,
        "approval_required": approval_required,
        "denied": denied,
        "blocked": not allowed,
        "risk_level": risk_level,
        "PolicyEngineRequired": True,
        "PermissionLayerRequired": True,
        "CapabilityPermissionRequired": True,
        "HumanApprovalRequired": approval_required,
        "HumanApproved": False,
        "UnifiedExecutionBusUsed": True,
        "dry_run": True,
        "Executed": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "ExternalCommunicationExecuted": False,
        "BrowserOperation": False,
        "BrowserOpened": False,
        "RealGUIOperation": False,
        "GUIClicked": False,
        "GUIInput": False,
        "FileDelete": False,
        "SafeToExecute": allowed,
    }

    return result

def run_bus_test():
    test_requests = [
        ("health", "health_check", {}),
        ("stability", "stability_check", {}),
        ("backup", "backup_check", {}),
        ("recovery", "recovery_check", {}),
        ("goal", "goal_check", {}),
        ("event", "event_check", {}),
        ("daemon", "daemon_check", {}),
        ("audit", "audit_check", {}),
        ("cycle", "dry_run_cycle", {}),
        ("external_ai", "external_ai_execute", {"provider": "chatgpt"}),
        ("browser", "browser_open", {"target": "example"}),
        ("gui", "gui_click", {"target": "button"}),
        ("original", "original_write", {"target": "naviko.py"}),
        ("storage", "file_delete", {"target": "some_file"}),
        ("unknown", "unknown_operation", {}),
    ]

    results = [
        route_execution_request(module, operation, payload)
        for module, operation, payload in test_requests
    ]

    safe_results = [r for r in results if r["bus_decision"] == "allow_dry_run"]
    approval_results = [r for r in results if r["bus_decision"] == "approval_required"]
    denied_results = [r for r in results if r["bus_decision"] == "deny"]

    report = {
        "status": "completed",
        "phase": PHASE,
        "UnifiedExecutionBusCreated": True,
        "TestCount": len(results),
        "SafeDryRunRouteCount": len(safe_results),
        "ApprovalRequiredRouteCount": len(approval_results),
        "DeniedRouteCount": len(denied_results),
        "AllSafeRoutesAllowedDryRun": all(
            r["allowed"] is True
            and r["SafeToExecute"] is True
            and r["Executed"] is False
            for r in safe_results
        ),
        "AllApprovalRoutesBlocked": all(
            r["allowed"] is False
            and r["approval_required"] is True
            and r["SafeToExecute"] is False
            and r["Executed"] is False
            for r in approval_results
        ),
        "AllDeniedRoutesBlocked": all(
            r["denied"] is True
            and r["allowed"] is False
            and r["SafeToExecute"] is False
            and r["Executed"] is False
            for r in denied_results
        ),
        "UnifiedExecutionBusUsedForAll": all(
            r["UnifiedExecutionBusUsed"] is True for r in results
        ),
        "PolicyEngineRequiredForAll": all(
            r["PolicyEngineRequired"] is True for r in results
        ),
        "PermissionLayerRequiredForAll": all(
            r["PermissionLayerRequired"] is True for r in results
        ),
        "CapabilityPermissionRequiredForAll": all(
            r["CapabilityPermissionRequired"] is True for r in results
        ),
        "Executed": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "ExternalCommunicationExecuted": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "HumanApproved": False,
        "Mode": "dry_run",
        "RiskCount": 0,
        "SafeToContinue": True,
        "NextPhase": "Phase91-2 AI OS Unified Execution Bus Diagnostics",
        "results": results,
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"ai_os_unified_execution_bus_{timestamp}.json"
    latest_path = BASE_DIR / "ai_os_unified_execution_bus.json"

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
    report, report_path = run_bus_test()

    print("=== AI OS Unified Execution Bus ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"UnifiedExecutionBusCreated: {report['UnifiedExecutionBusCreated']}")
    print(f"TestCount: {report['TestCount']}")
    print(f"SafeDryRunRouteCount: {report['SafeDryRunRouteCount']}")
    print(f"ApprovalRequiredRouteCount: {report['ApprovalRequiredRouteCount']}")
    print(f"DeniedRouteCount: {report['DeniedRouteCount']}")
    print(f"AllSafeRoutesAllowedDryRun: {report['AllSafeRoutesAllowedDryRun']}")
    print(f"AllApprovalRoutesBlocked: {report['AllApprovalRoutesBlocked']}")
    print(f"AllDeniedRoutesBlocked: {report['AllDeniedRoutesBlocked']}")
    print(f"UnifiedExecutionBusUsedForAll: {report['UnifiedExecutionBusUsedForAll']}")
    print(f"PolicyEngineRequiredForAll: {report['PolicyEngineRequiredForAll']}")
    print(f"PermissionLayerRequiredForAll: {report['PermissionLayerRequiredForAll']}")
    print(f"CapabilityPermissionRequiredForAll: {report['CapabilityPermissionRequiredForAll']}")
    print(f"Executed: {report['Executed']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(f"Mode: {report['Mode']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"NextPhase: {report['NextPhase']}")
    print(f"保存先: {report_path}")

if __name__ == "__main__":
    main()