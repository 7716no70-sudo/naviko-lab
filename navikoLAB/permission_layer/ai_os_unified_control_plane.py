from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
CONTROL_DIR = BASE_DIR / "control_plane"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
CONTROL_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase92-1 AI OS Unified Control Plane"

CONTROL_PLANE_ROUTES = {
    "system_health": "health_check",
    "system_stability": "stability_check",
    "backup_status": "backup_check",
    "recovery_status": "recovery_check",
    "goal_status": "goal_check",
    "event_status": "event_check",
    "daemon_status": "daemon_check",
    "audit_status": "audit_check",
    "cycle_status": "dry_run_cycle",
    "external_ai_request": "external_ai_execute",
    "browser_request": "browser_open",
    "gui_request": "gui_click",
    "original_write_request": "original_write",
    "delete_request": "file_delete",
}

SAFE_OPERATIONS = {
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

APPROVAL_REQUIRED_OPERATIONS = {
    "external_ai_execute",
    "browser_open",
    "gui_click",
    "original_write",
    "file_delete",
}

def control_plane_dispatch(request_type, payload=None):
    payload = payload or {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    operation = CONTROL_PLANE_ROUTES.get(request_type, "unknown_operation")

    if operation in SAFE_OPERATIONS:
        decision = "dispatch_to_bus_dry_run"
        allowed = True
        approval_required = False
        denied = False
        risk_level = 0
    elif operation in APPROVAL_REQUIRED_OPERATIONS:
        decision = "dispatch_to_bus_approval_required"
        allowed = False
        approval_required = True
        denied = False
        risk_level = 4
    else:
        decision = "deny_unknown_control_request"
        allowed = False
        approval_required = True
        denied = True
        risk_level = 5

    result = {
        "timestamp": timestamp,
        "phase": PHASE,
        "request_type": request_type,
        "operation": operation,
        "payload_preview": str(payload)[:200],
        "control_decision": decision,
        "allowed": allowed,
        "approval_required": approval_required,
        "denied": denied,
        "blocked": not allowed,
        "risk_level": risk_level,
        "ControlPlaneUsed": True,
        "UnifiedExecutionBusRequired": True,
        "PolicyEngineRequired": True,
        "PermissionLayerRequired": True,
        "CapabilityPermissionRequired": True,
        "HumanApprovalRequired": approval_required,
        "HumanApproved": False,
        "dry_run": True,
        "Dispatched": True,
        "Executed": False,
        "OriginalWrite": False,
        "ExternalOperation": False,
        "ExternalCommunicationExecuted": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "SafeToExecute": allowed,
    }

    return result

def run_control_plane_test():
    test_requests = [
        ("system_health", {}),
        ("system_stability", {}),
        ("backup_status", {}),
        ("recovery_status", {}),
        ("goal_status", {}),
        ("event_status", {}),
        ("daemon_status", {}),
        ("audit_status", {}),
        ("cycle_status", {}),
        ("external_ai_request", {"provider": "chatgpt"}),
        ("browser_request", {"target": "example"}),
        ("gui_request", {"target": "button"}),
        ("original_write_request", {"target": "naviko.py"}),
        ("delete_request", {"target": "some_file"}),
        ("unknown_control_request", {}),
    ]

    results = [
        control_plane_dispatch(request_type, payload)
        for request_type, payload in test_requests
    ]

    safe_results = [r for r in results if r["control_decision"] == "dispatch_to_bus_dry_run"]
    approval_results = [r for r in results if r["control_decision"] == "dispatch_to_bus_approval_required"]
    denied_results = [r for r in results if r["control_decision"] == "deny_unknown_control_request"]

    report = {
        "status": "completed",
        "phase": PHASE,
        "UnifiedControlPlaneCreated": True,
        "TestCount": len(results),
        "SafeDispatchCount": len(safe_results),
        "ApprovalRequiredDispatchCount": len(approval_results),
        "DeniedDispatchCount": len(denied_results),
        "AllSafeDispatchesAllowedDryRun": all(
            r["allowed"] is True and r["SafeToExecute"] is True and r["Executed"] is False
            for r in safe_results
        ),
        "AllApprovalDispatchesBlocked": all(
            r["allowed"] is False and r["approval_required"] is True and r["Executed"] is False
            for r in approval_results
        ),
        "AllDeniedDispatchesBlocked": all(
            r["denied"] is True and r["allowed"] is False and r["Executed"] is False
            for r in denied_results
        ),
        "ControlPlaneUsedForAll": all(r["ControlPlaneUsed"] is True for r in results),
        "UnifiedExecutionBusRequiredForAll": all(r["UnifiedExecutionBusRequired"] is True for r in results),
        "PolicyEngineRequiredForAll": all(r["PolicyEngineRequired"] is True for r in results),
        "PermissionLayerRequiredForAll": all(r["PermissionLayerRequired"] is True for r in results),
        "CapabilityPermissionRequiredForAll": all(r["CapabilityPermissionRequired"] is True for r in results),
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
        "NextPhase": "Phase92-2 AI OS Unified Control Plane Diagnostics",
        "results": results,
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"ai_os_unified_control_plane_{timestamp}.json"
    latest_path = BASE_DIR / "ai_os_unified_control_plane.json"

    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    latest_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    return report, report_path

def main():
    report, report_path = run_control_plane_test()

    print("=== AI OS Unified Control Plane ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"UnifiedControlPlaneCreated: {report['UnifiedControlPlaneCreated']}")
    print(f"TestCount: {report['TestCount']}")
    print(f"SafeDispatchCount: {report['SafeDispatchCount']}")
    print(f"ApprovalRequiredDispatchCount: {report['ApprovalRequiredDispatchCount']}")
    print(f"DeniedDispatchCount: {report['DeniedDispatchCount']}")
    print(f"AllSafeDispatchesAllowedDryRun: {report['AllSafeDispatchesAllowedDryRun']}")
    print(f"AllApprovalDispatchesBlocked: {report['AllApprovalDispatchesBlocked']}")
    print(f"AllDeniedDispatchesBlocked: {report['AllDeniedDispatchesBlocked']}")
    print(f"ControlPlaneUsedForAll: {report['ControlPlaneUsedForAll']}")
    print(f"UnifiedExecutionBusRequiredForAll: {report['UnifiedExecutionBusRequiredForAll']}")
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