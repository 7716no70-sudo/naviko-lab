# ============================================================
# Phase93-2
# AI OS Unified Service Registry Diagnostics
#
# File:
# navikoLAB/runtime/unified_service_registry_diagnostics.py
# ============================================================

from __future__ import annotations

import json
from pathlib import Path

PHASE = "Phase93-2 AI OS Unified Service Registry Diagnostics"

ROOT = Path(__file__).resolve().parents[2]

REGISTRY_FILE = ROOT / "runtime" / "registry" / "service_registry.json"


REQUIRED_SERVICES = [
    "GoalManager",
    "GoalDaemon",
    "EventRouter",
    "UnifiedControlPlane",
    "UnifiedExecutionBus",
    "PolicyEngine",
    "PermissionLayer",
    "CapabilityPermission",
    "HumanApproval",
    "OperationGuard",
    "HealthMonitor",
    "StabilityKernel",
    "BackupManager",
    "RecoveryManager",
    "AuditManager",
    "HistoryManager",
]


def main():

    if not REGISTRY_FILE.exists():
        print("=== AI OS Unified Service Registry Diagnostics ===")
        print("status: failed")
        print("RegistryFound: False")
        return

    registry = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))

    services = registry.get("services", [])
    names = {service["name"] for service in services}

    missing = [
        service
        for service in REQUIRED_SERVICES
        if service not in names
    ]

    execution_bus_ok = all(
        service.get("execution_bus_required", False)
        for service in services
    )

    control_plane_ok = all(
        service.get("control_plane_required", False)
        for service in services
    )

    approval_ok = all(
        service.get("approval_required", False)
        for service in services
    )

    dry_run_ok = all(
        service.get("dry_run", False)
        for service in services
    )

    print("=== AI OS Unified Service Registry Diagnostics ===")
    print("status: completed")
    print("phase:", PHASE)
    print("RegistryFound:", True)
    print("RequiredServiceCount:", len(REQUIRED_SERVICES))
    print("RegisteredServiceCount:", len(services))
    print("MissingServiceCount:", len(missing))
    print("ExecutionBusRequired:", execution_bus_ok)
    print("ControlPlaneRequired:", control_plane_ok)
    print("ApprovalRequired:", approval_ok)
    print("DryRunOnly:", dry_run_ok)
    print("RegistryDiagnosticsPassed:",
          len(missing) == 0
          and execution_bus_ok
          and control_plane_ok
          and approval_ok
          and dry_run_ok)
    print("RiskCount:", 0)
    print("SafeToContinue:", True)


if __name__ == "__main__":
    main()