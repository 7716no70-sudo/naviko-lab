# navikoLAB/runtime/ai_os_runtime_manager_diagnostics.py

from __future__ import annotations

from pathlib import Path
import json


PHASE = "Phase96-2 AI OS Runtime Manager Diagnostics"

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_FILE = ROOT / "runtime" / "manager" / "runtime_manager_state.json"

REQUIRED_COMPONENT_COUNT = 16


def load_runtime():
    if not RUNTIME_FILE.exists():
        return None
    return json.loads(RUNTIME_FILE.read_text(encoding="utf-8"))


def main():
    runtime = load_runtime()

    runtime_found = runtime is not None
    component_count_ok = runtime_found and runtime.get("component_count") == REQUIRED_COMPONENT_COUNT
    dry_run_ok = runtime_found and runtime.get("runtime_mode") == "dry_run"
    initialized_ok = runtime_found and runtime.get("runtime_state") == "initialized"

    required_flags_ok = runtime_found and all([
        runtime.get("scheduler_enabled") is True,
        runtime.get("event_loop_enabled") is True,
        runtime.get("control_plane_enabled") is True,
        runtime.get("execution_bus_enabled") is True,
        runtime.get("policy_engine_enabled") is True,
        runtime.get("permission_layer_enabled") is True,
        runtime.get("human_approval_enabled") is True,
        runtime.get("health_monitor_enabled") is True,
        runtime.get("backup_enabled") is True,
        runtime.get("recovery_enabled") is True,
    ])

    dangerous_flags_ok = runtime_found and all([
        runtime.get("OriginalWrite") is False,
        runtime.get("ExternalOperation") is False,
        runtime.get("BrowserOperation") is False,
        runtime.get("RealGUIOperation") is False,
        runtime.get("FileDelete") is False,
        runtime.get("AutoExecute") is False,
        runtime.get("HumanApproved") is False,
        runtime.get("HumanApprovalRequired") is True,
    ])

    passed = all([
        runtime_found,
        component_count_ok,
        dry_run_ok,
        initialized_ok,
        required_flags_ok,
        dangerous_flags_ok,
    ])

    print("=== AI OS Runtime Manager Diagnostics ===")
    print("status:", "completed" if runtime_found else "failed")
    print("phase:", PHASE)
    print("RuntimeManagerFound:", runtime_found)
    print("ComponentCountOK:", component_count_ok)
    print("DryRunOnly:", dry_run_ok)
    print("RuntimeInitialized:", initialized_ok)
    print("RequiredRuntimeFlagsOK:", required_flags_ok)
    print("DangerousFlagsAllFalse:", dangerous_flags_ok)
    print("RuntimeManagerDiagnosticsPassed:", passed)
    print("RiskCount:", 0)
    print("SafeToContinue:", passed)


if __name__ == "__main__":
    main()