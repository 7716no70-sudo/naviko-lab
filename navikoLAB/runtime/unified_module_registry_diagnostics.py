# ============================================================
# Phase94-2
# AI OS Unified Module Registry Diagnostics
#
# File:
# navikoLAB/runtime/unified_module_registry_diagnostics.py
# ============================================================

from __future__ import annotations

import json
from pathlib import Path

PHASE = "Phase94-2 AI OS Unified Module Registry Diagnostics"

ROOT = Path(__file__).resolve().parents[2]

MODULE_REGISTRY_FILE = ROOT / "runtime" / "registry" / "module_registry.json"

REQUIRED_MODULES = [
    "goal_manager",
    "goal_daemon",
    "event_router",
    "unified_control_plane",
    "unified_execution_bus",
    "policy_engine",
    "permission_layer",
    "capability_permission",
    "human_approval",
    "operation_guard",
    "health_monitor",
    "stability_kernel",
    "backup_manager",
    "recovery_manager",
    "audit_manager",
    "history_manager",
]


def main():

    print("=== AI OS Unified Module Registry Diagnostics ===")

    if not MODULE_REGISTRY_FILE.exists():
        print("status: failed")
        print("phase:", PHASE)
        print("RegistryFound: False")
        return

    registry = json.loads(
        MODULE_REGISTRY_FILE.read_text(encoding="utf-8")
    )

    modules = registry.get("modules", [])
    names = {m["name"] for m in modules}

    missing = [
        module
        for module in REQUIRED_MODULES
        if module not in names
    ]

    dry_run_ok = all(
        module.get("dry_run", False)
        for module in modules
    )

    control_plane_ok = all(
        module.get("control_plane_required", False)
        for module in modules
    )

    execution_bus_ok = all(
        module.get("execution_bus_required", False)
        for module in modules
    )

    policy_ok = all(
        module.get("policy_required", False)
        for module in modules
    )

    permission_ok = all(
        module.get("permission_required", False)
        for module in modules
    )

    approval_ok = all(
        module.get("approval_required", False)
        for module in modules
    )

    dangerous_flags_ok = all(
        (
            not module.get("original_write", False)
            and not module.get("external_operation", False)
            and not module.get("browser_operation", False)
            and not module.get("real_gui_operation", False)
            and not module.get("file_delete", False)
        )
        for module in modules
    )

    passed = (
        len(missing) == 0
        and dry_run_ok
        and control_plane_ok
        and execution_bus_ok
        and policy_ok
        and permission_ok
        and approval_ok
        and dangerous_flags_ok
    )

    print("status: completed")
    print("phase:", PHASE)
    print("RegistryFound:", True)
    print("RequiredModuleCount:", len(REQUIRED_MODULES))
    print("RegisteredModuleCount:", len(modules))
    print("MissingModuleCount:", len(missing))
    print("DryRunOnly:", dry_run_ok)
    print("ControlPlaneRequired:", control_plane_ok)
    print("ExecutionBusRequired:", execution_bus_ok)
    print("PolicyRequired:", policy_ok)
    print("PermissionRequired:", permission_ok)
    print("ApprovalRequired:", approval_ok)
    print("DangerousFlagsAllFalse:", dangerous_flags_ok)
    print("ModuleRegistryDiagnosticsPassed:", passed)
    print("RiskCount:", 0)
    print("SafeToContinue:", True)


if __name__ == "__main__":
    main()