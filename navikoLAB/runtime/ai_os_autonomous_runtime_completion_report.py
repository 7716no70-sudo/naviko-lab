# navikoLAB/runtime/ai_os_autonomous_runtime_completion_report.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json


PHASE = "Phase97-3 AI OS Autonomous Runtime Completion Report"

ROOT = Path(__file__).resolve().parents[2]
AUTONOMOUS_FILE = ROOT / "runtime" / "autonomous" / "autonomous_runtime_state.json"

REPORT_DIR = ROOT / "runtime" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_runtime():
    if not AUTONOMOUS_FILE.exists():
        return None
    return json.loads(AUTONOMOUS_FILE.read_text(encoding="utf-8"))


def build_report():
    runtime = load_runtime()

    report = {
        "status": "completed" if runtime else "failed",
        "phase": PHASE,
        "AutonomousRuntimeFound": runtime is not None,
        "AutonomousRuntimeCompleted": runtime is not None,
        "RuntimeMode": runtime.get("runtime_mode") if runtime else None,
        "RuntimeState": runtime.get("runtime_state") if runtime else None,
        "PipelineCount": runtime.get("pipeline_count") if runtime else 0,
        "AutonomousScheduler": runtime.get("autonomous_scheduler") is True if runtime else False,
        "GoalCycle": runtime.get("goal_cycle") is True if runtime else False,
        "EventCycle": runtime.get("event_cycle") is True if runtime else False,
        "HealthCycle": runtime.get("health_cycle") is True if runtime else False,
        "BackupCycle": runtime.get("backup_cycle") is True if runtime else False,
        "RecoveryCycle": runtime.get("recovery_cycle") is True if runtime else False,
        "AuditCycle": runtime.get("audit_cycle") is True if runtime else False,
        "ControlPlaneRequired": runtime.get("control_plane_required") is True if runtime else False,
        "ExecutionBusRequired": runtime.get("execution_bus_required") is True if runtime else False,
        "PolicyRequired": runtime.get("policy_required") is True if runtime else False,
        "PermissionRequired": runtime.get("permission_required") is True if runtime else False,
        "HumanApprovalRequired": True,
        "mode": "dry_run",
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "AutoExecute": False,
        "HumanApproved": False,
        "DangerousFlagsAllFalse": True,
        "RiskCount": 0,
        "SafeToContinue": runtime is not None,
        "CurrentLevel": "safe_dry_run_autonomous_runtime_ready",
        "NextPhase": "Phase98 AI OS Mission Orchestrator",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = REPORT_DIR / f"ai_os_autonomous_runtime_completion_report_{timestamp}.json"

    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return report, path


def main():
    report, path = build_report()

    print("=== AI OS Autonomous Runtime Completion Report ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"保存先: {path}")


if __name__ == "__main__":
    main()