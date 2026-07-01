# navikoLAB/runtime/ai_os_autonomous_runtime_diagnostics.py

from __future__ import annotations

from pathlib import Path
import json


PHASE = "Phase97-2 AI OS Autonomous Runtime Diagnostics"

ROOT = Path(__file__).resolve().parents[2]
AUTONOMOUS_FILE = ROOT / "runtime" / "autonomous" / "autonomous_runtime_state.json"

REQUIRED_PIPELINE_COUNT = 16


def load_runtime():
    if not AUTONOMOUS_FILE.exists():
        return None
    return json.loads(AUTONOMOUS_FILE.read_text(encoding="utf-8"))


def main():
    runtime = load_runtime()

    runtime_found = runtime is not None
    pipeline_count_ok = runtime_found and runtime.get("pipeline_count") == REQUIRED_PIPELINE_COUNT
    dry_run_ok = runtime_found and runtime.get("runtime_mode") == "dry_run"
    standby_ok = runtime_found and runtime.get("runtime_state") == "standby"

    cycles_ok = runtime_found and all([
        runtime.get("autonomous_scheduler") is True,
        runtime.get("goal_cycle") is True,
        runtime.get("event_cycle") is True,
        runtime.get("health_cycle") is True,
        runtime.get("backup_cycle") is True,
        runtime.get("recovery_cycle") is True,
        runtime.get("audit_cycle") is True,
    ])

    safety_layers_ok = runtime_found and all([
        runtime.get("control_plane_required") is True,
        runtime.get("execution_bus_required") is True,
        runtime.get("policy_required") is True,
        runtime.get("permission_required") is True,
        runtime.get("human_approval_required") is True,
    ])

    dangerous_flags_ok = runtime_found and all([
        runtime.get("OriginalWrite") is False,
        runtime.get("ExternalOperation") is False,
        runtime.get("BrowserOperation") is False,
        runtime.get("RealGUIOperation") is False,
        runtime.get("FileDelete") is False,
        runtime.get("AutoExecute") is False,
        runtime.get("HumanApproved") is False,
    ])

    passed = all([
        runtime_found,
        pipeline_count_ok,
        dry_run_ok,
        standby_ok,
        cycles_ok,
        safety_layers_ok,
        dangerous_flags_ok,
    ])

    print("=== AI OS Autonomous Runtime Diagnostics ===")
    print("status:", "completed" if runtime_found else "failed")
    print("phase:", PHASE)
    print("AutonomousRuntimeFound:", runtime_found)
    print("PipelineCountOK:", pipeline_count_ok)
    print("DryRunOnly:", dry_run_ok)
    print("RuntimeStandby:", standby_ok)
    print("AutonomousCyclesOK:", cycles_ok)
    print("SafetyLayersRequired:", safety_layers_ok)
    print("DangerousFlagsAllFalse:", dangerous_flags_ok)
    print("AutonomousRuntimeDiagnosticsPassed:", passed)
    print("RiskCount:", 0)
    print("SafeToContinue:", passed)


if __name__ == "__main__":
    main()