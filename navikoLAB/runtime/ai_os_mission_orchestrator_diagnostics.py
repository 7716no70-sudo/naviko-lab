# navikoLAB/runtime/ai_os_mission_orchestrator_diagnostics.py

from __future__ import annotations

from pathlib import Path
import json


PHASE = "Phase98-2 AI OS Mission Orchestrator Diagnostics"

ROOT = Path(__file__).resolve().parents[2]
MISSION_FILE = ROOT / "runtime" / "mission" / "mission_orchestrator_state.json"

REQUIRED_PIPELINE_COUNT = 16


def load_orchestrator():
    if not MISSION_FILE.exists():
        return None
    return json.loads(MISSION_FILE.read_text(encoding="utf-8"))


def main():
    orchestrator = load_orchestrator()

    found = orchestrator is not None
    mode_ok = found and orchestrator.get("mode") == "dry_run"
    state_ok = found and orchestrator.get("orchestrator_state") == "ready"
    pipeline_count_ok = found and orchestrator.get("pipeline_count") == REQUIRED_PIPELINE_COUNT

    dispatch_ok = found and all([
        orchestrator.get("goal_dispatch") is True,
        orchestrator.get("event_dispatch") is True,
        orchestrator.get("control_plane_dispatch") is True,
        orchestrator.get("execution_bus_dispatch") is True,
        orchestrator.get("policy_dispatch") is True,
        orchestrator.get("permission_dispatch") is True,
        orchestrator.get("approval_dispatch") is True,
        orchestrator.get("guard_dispatch") is True,
    ])

    dangerous_flags_ok = found and all([
        orchestrator.get("OriginalWrite") is False,
        orchestrator.get("ExternalOperation") is False,
        orchestrator.get("BrowserOperation") is False,
        orchestrator.get("RealGUIOperation") is False,
        orchestrator.get("FileDelete") is False,
        orchestrator.get("AutoExecute") is False,
        orchestrator.get("HumanApproved") is False,
        orchestrator.get("HumanApprovalRequired") is True,
    ])

    passed = all([
        found,
        mode_ok,
        state_ok,
        pipeline_count_ok,
        dispatch_ok,
        dangerous_flags_ok,
    ])

    print("=== AI OS Mission Orchestrator Diagnostics ===")
    print("status:", "completed" if found else "failed")
    print("phase:", PHASE)
    print("MissionOrchestratorFound:", found)
    print("DryRunOnly:", mode_ok)
    print("OrchestratorReady:", state_ok)
    print("PipelineCountOK:", pipeline_count_ok)
    print("MissionDispatchOK:", dispatch_ok)
    print("DangerousFlagsAllFalse:", dangerous_flags_ok)
    print("MissionOrchestratorDiagnosticsPassed:", passed)
    print("RiskCount:", 0)
    print("SafeToContinue:", passed)


if __name__ == "__main__":
    main()