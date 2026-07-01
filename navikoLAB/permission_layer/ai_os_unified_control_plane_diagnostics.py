from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PHASE = "Phase92-2 AI OS Unified Control Plane Diagnostics"

CONTROL_PATH = BASE_DIR / "ai_os_unified_control_plane.json"

REQUIRED_SAFE_REQUESTS = [
    "system_health",
    "system_stability",
    "backup_status",
    "recovery_status",
    "goal_status",
    "event_status",
    "daemon_status",
    "audit_status",
    "cycle_status",
]

REQUIRED_APPROVAL_REQUESTS = [
    "external_ai_request",
    "browser_request",
    "gui_request",
    "original_write_request",
    "delete_request",
]

REQUIRED_DENIED_REQUESTS = [
    "unknown_control_request",
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

    control = load_json(CONTROL_PATH)
    control_found = control is not None
    results = control.get("results", []) if control_found else []

    result_by_request = {
        r.get("request_type"): r for r in results
    }

    missing_safe = [r for r in REQUIRED_SAFE_REQUESTS if r not in result_by_request]
    missing_approval = [r for r in REQUIRED_APPROVAL_REQUESTS if r not in result_by_request]
    missing_denied = [r for r in REQUIRED_DENIED_REQUESTS if r not in result_by_request]

    safe_dispatches_ok = (
        len(missing_safe) == 0
        and all(
            result_by_request[r].get("allowed") is True
            and result_by_request[r].get("SafeToExecute") is True
            and result_by_request[r].get("Executed") is False
            for r in REQUIRED_SAFE_REQUESTS
        )
    )

    approval_dispatches_ok = (
        len(missing_approval) == 0
        and all(
            result_by_request[r].get("approval_required") is True
            and result_by_request[r].get("allowed") is False
            and result_by_request[r].get("Executed") is False
            for r in REQUIRED_APPROVAL_REQUESTS
        )
    )

    denied_dispatches_ok = (
        len(missing_denied) == 0
        and all(
            result_by_request[r].get("denied") is True
            and result_by_request[r].get("allowed") is False
            and result_by_request[r].get("Executed") is False
            for r in REQUIRED_DENIED_REQUESTS
        )
    )

    all_use_control_plane = (
        bool(results)
        and all(r.get("ControlPlaneUsed") is True for r in results)
    )

    all_require_bus = (
        bool(results)
        and all(r.get("UnifiedExecutionBusRequired") is True for r in results)
    )

    all_require_safety_layers = (
        bool(results)
        and all(
            r.get("PolicyEngineRequired") is True
            and r.get("PermissionLayerRequired") is True
            and r.get("CapabilityPermissionRequired") is True
            for r in results
        )
    )

    dangerous_flags_all_false = (
        control_found
        and control.get("Executed") is False
        and control.get("OriginalWrite") is False
        and control.get("ExternalOperation") is False
        and control.get("ExternalCommunicationExecuted") is False
        and control.get("BrowserOperation") is False
        and control.get("RealGUIOperation") is False
        and control.get("FileDelete") is False
        and control.get("HumanApproved") is False
    )

    control_summary_ok = (
        control_found
        and control.get("UnifiedControlPlaneCreated") is True
        and control.get("AllSafeDispatchesAllowedDryRun") is True
        and control.get("AllApprovalDispatchesBlocked") is True
        and control.get("AllDeniedDispatchesBlocked") is True
        and control.get("ControlPlaneUsedForAll") is True
        and control.get("UnifiedExecutionBusRequiredForAll") is True
        and control.get("PolicyEngineRequiredForAll") is True
        and control.get("PermissionLayerRequiredForAll") is True
        and control.get("CapabilityPermissionRequiredForAll") is True
    )

    diagnostics_passed = (
        control_found
        and safe_dispatches_ok
        and approval_dispatches_ok
        and denied_dispatches_ok
        and all_use_control_plane
        and all_require_bus
        and all_require_safety_layers
        and dangerous_flags_all_false
        and control_summary_ok
    )

    report = {
        "status": "completed" if diagnostics_passed else "failed",
        "phase": PHASE,
        "ControlPlaneFound": control_found,
        "RequiredSafeRequestCount": len(REQUIRED_SAFE_REQUESTS),
        "RequiredApprovalRequestCount": len(REQUIRED_APPROVAL_REQUESTS),
        "RequiredDeniedRequestCount": len(REQUIRED_DENIED_REQUESTS),
        "MissingSafeRequestCount": len(missing_safe),
        "MissingApprovalRequestCount": len(missing_approval),
        "MissingDeniedRequestCount": len(missing_denied),
        "MissingSafeRequests": missing_safe,
        "MissingApprovalRequests": missing_approval,
        "MissingDeniedRequests": missing_denied,
        "SafeDispatchesOK": safe_dispatches_ok,
        "ApprovalDispatchesOK": approval_dispatches_ok,
        "DeniedDispatchesOK": denied_dispatches_ok,
        "AllUseControlPlane": all_use_control_plane,
        "AllRequireUnifiedExecutionBus": all_require_bus,
        "AllRequireSafetyLayers": all_require_safety_layers,
        "DangerousFlagsAllFalse": dangerous_flags_all_false,
        "ControlPlaneSummaryOK": control_summary_ok,
        "UnifiedControlPlaneDiagnosticsPassed": diagnostics_passed,
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
        "NextPhase": "Phase92-3 AI OS Unified Control Plane Completion Report",
        "timestamp": timestamp,
    }

    report_path = REPORT_DIR / f"ai_os_unified_control_plane_diagnostics_{timestamp}.json"
    latest_path = BASE_DIR / "ai_os_unified_control_plane_diagnostics.json"

    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    latest_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    return report, report_path

def main():
    report, report_path = build_diagnostics()

    print("=== AI OS Unified Control Plane Diagnostics ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"ControlPlaneFound: {report['ControlPlaneFound']}")
    print(f"RequiredSafeRequestCount: {report['RequiredSafeRequestCount']}")
    print(f"RequiredApprovalRequestCount: {report['RequiredApprovalRequestCount']}")
    print(f"RequiredDeniedRequestCount: {report['RequiredDeniedRequestCount']}")
    print(f"MissingSafeRequestCount: {report['MissingSafeRequestCount']}")
    print(f"MissingApprovalRequestCount: {report['MissingApprovalRequestCount']}")
    print(f"MissingDeniedRequestCount: {report['MissingDeniedRequestCount']}")
    print(f"SafeDispatchesOK: {report['SafeDispatchesOK']}")
    print(f"ApprovalDispatchesOK: {report['ApprovalDispatchesOK']}")
    print(f"DeniedDispatchesOK: {report['DeniedDispatchesOK']}")
    print(f"AllUseControlPlane: {report['AllUseControlPlane']}")
    print(f"AllRequireUnifiedExecutionBus: {report['AllRequireUnifiedExecutionBus']}")
    print(f"AllRequireSafetyLayers: {report['AllRequireSafetyLayers']}")
    print(f"DangerousFlagsAllFalse: {report['DangerousFlagsAllFalse']}")
    print(f"ControlPlaneSummaryOK: {report['ControlPlaneSummaryOK']}")
    print(f"UnifiedControlPlaneDiagnosticsPassed: {report['UnifiedControlPlaneDiagnosticsPassed']}")
    print(f"Executed: {report['Executed']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(f"Mode: {report['Mode']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"NextPhase: {report['NextPhase']}")
    print(f"保存先: {report_path}")

if __name__ == "__main__":
    main()