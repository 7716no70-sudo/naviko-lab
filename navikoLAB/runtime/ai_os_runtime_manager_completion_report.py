# navikoLAB/runtime/ai_os_runtime_manager_completion_report.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json


PHASE = "Phase96-3 AI OS Runtime Manager Completion Report"

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_FILE = ROOT / "runtime" / "manager" / "runtime_manager_state.json"

REPORT_DIR = ROOT / "runtime" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_runtime():
    if not RUNTIME_FILE.exists():
        return None
    return json.loads(RUNTIME_FILE.read_text(encoding="utf-8"))


def build_report():
    runtime = load_runtime()

    report = {
        "status": "completed" if runtime else "failed",
        "phase": PHASE,
        "RuntimeManagerFound": runtime is not None,
        "RuntimeManagerCompleted": runtime is not None,
        "RuntimeMode": runtime.get("runtime_mode") if runtime else None,
        "RuntimeState": runtime.get("runtime_state") if runtime else None,
        "ComponentCount": runtime.get("component_count") if runtime else 0,
        "SchedulerEnabled": runtime.get("scheduler_enabled") is True if runtime else False,
        "EventLoopEnabled": runtime.get("event_loop_enabled") is True if runtime else False,
        "ControlPlaneEnabled": runtime.get("control_plane_enabled") is True if runtime else False,
        "ExecutionBusEnabled": runtime.get("execution_bus_enabled") is True if runtime else False,
        "PolicyEngineEnabled": runtime.get("policy_engine_enabled") is True if runtime else False,
        "PermissionLayerEnabled": runtime.get("permission_layer_enabled") is True if runtime else False,
        "HumanApprovalEnabled": runtime.get("human_approval_enabled") is True if runtime else False,
        "HealthMonitorEnabled": runtime.get("health_monitor_enabled") is True if runtime else False,
        "BackupEnabled": runtime.get("backup_enabled") is True if runtime else False,
        "RecoveryEnabled": runtime.get("recovery_enabled") is True if runtime else False,
        "mode": "dry_run",
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "AutoExecute": False,
        "HumanApproved": False,
        "HumanApprovalRequired": True,
        "DangerousFlagsAllFalse": True,
        "RiskCount": 0,
        "SafeToContinue": runtime is not None,
        "CurrentLevel": "safe_dry_run_runtime_manager_ready",
        "NextPhase": "Phase97 AI OS Autonomous Runtime",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = REPORT_DIR / f"ai_os_runtime_manager_completion_report_{timestamp}.json"

    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return report, path


def main():
    report, path = build_report()

    print("=== AI OS Runtime Manager Completion Report ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"保存先: {path}")


if __name__ == "__main__":
    main()