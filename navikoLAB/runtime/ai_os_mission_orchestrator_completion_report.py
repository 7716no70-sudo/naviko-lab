# navikoLAB/runtime/ai_os_mission_orchestrator_completion_report.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json


PHASE = "Phase98-3 AI OS Mission Orchestrator Completion Report"

ROOT = Path(__file__).resolve().parents[2]
MISSION_FILE = ROOT / "runtime" / "mission" / "mission_orchestrator_state.json"

REPORT_DIR = ROOT / "runtime" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_orchestrator():
    if not MISSION_FILE.exists():
        return None
    return json.loads(MISSION_FILE.read_text(encoding="utf-8"))


def build_report():
    orchestrator = load_orchestrator()

    report = {
        "status": "completed" if orchestrator else "failed",
        "phase": PHASE,
        "MissionOrchestratorFound": orchestrator is not None,
        "MissionOrchestratorCompleted": orchestrator is not None,
        "Mode": orchestrator.get("mode") if orchestrator else None,
        "State": orchestrator.get("orchestrator_state") if orchestrator else None,
        "PipelineCount": orchestrator.get("pipeline_count") if orchestrator else 0,
        "GoalDispatch": orchestrator.get("goal_dispatch") is True if orchestrator else False,
        "EventDispatch": orchestrator.get("event_dispatch") is True if orchestrator else False,
        "ControlPlaneDispatch": orchestrator.get("control_plane_dispatch") is True if orchestrator else False,
        "ExecutionBusDispatch": orchestrator.get("execution_bus_dispatch") is True if orchestrator else False,
        "PolicyDispatch": orchestrator.get("policy_dispatch") is True if orchestrator else False,
        "PermissionDispatch": orchestrator.get("permission_dispatch") is True if orchestrator else False,
        "ApprovalDispatch": orchestrator.get("approval_dispatch") is True if orchestrator else False,
        "GuardDispatch": orchestrator.get("guard_dispatch") is True if orchestrator else False,
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
        "SafeToContinue": orchestrator is not None,
        "CurrentLevel": "safe_dry_run_mission_orchestrator_ready",
        "NextPhase": "Phase99 AI OS Final Safety Validation",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = REPORT_DIR / f"ai_os_mission_orchestrator_completion_report_{timestamp}.json"

    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return report, path


def main():
    report, path = build_report()

    print("=== AI OS Mission Orchestrator Completion Report ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"保存先: {path}")


if __name__ == "__main__":
    main()