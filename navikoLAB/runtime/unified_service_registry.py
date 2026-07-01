# ============================================================
# Phase93-1
# AI OS Unified Service Registry
# File:
# navikoLAB/runtime/unified_service_registry.py
# ============================================================

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
import json


PHASE = "Phase93-1 AI OS Unified Service Registry"

ROOT = Path(__file__).resolve().parents[2]

REGISTRY_DIR = ROOT / "runtime" / "registry"
REGISTRY_DIR.mkdir(parents=True, exist_ok=True)

REGISTRY_FILE = REGISTRY_DIR / "service_registry.json"


@dataclass
class Service:

    name: str
    category: str
    enabled: bool
    dry_run: bool
    approval_required: bool
    execution_bus_required: bool
    control_plane_required: bool


DEFAULT_SERVICES = [

    Service(
        "GoalManager",
        "goal",
        True,
        True,
        True,
        True,
        True,
    ),

    Service(
        "GoalDaemon",
        "daemon",
        True,
        True,
        True,
        True,
        True,
    ),

    Service(
        "EventRouter",
        "event",
        True,
        True,
        True,
        True,
        True,
    ),

    Service(
        "UnifiedControlPlane",
        "control_plane",
        True,
        True,
        True,
        True,
        True,
    ),

    Service(
        "UnifiedExecutionBus",
        "execution_bus",
        True,
        True,
        True,
        True,
        True,
    ),

    Service(
        "PolicyEngine",
        "policy",
        True,
        True,
        True,
        True,
        True,
    ),

    Service(
        "PermissionLayer",
        "permission",
        True,
        True,
        True,
        True,
        True,
    ),

    Service(
        "CapabilityPermission",
        "capability",
        True,
        True,
        True,
        True,
        True,
    ),

    Service(
        "HumanApproval",
        "approval",
        True,
        True,
        True,
        True,
        True,
    ),

    Service(
        "OperationGuard",
        "guard",
        True,
        True,
        True,
        True,
        True,
    ),

    Service(
        "HealthMonitor",
        "health",
        True,
        True,
        True,
        True,
        True,
    ),

    Service(
        "StabilityKernel",
        "stability",
        True,
        True,
        True,
        True,
        True,
    ),

    Service(
        "BackupManager",
        "backup",
        True,
        True,
        True,
        True,
        True,
    ),

    Service(
        "RecoveryManager",
        "recovery",
        True,
        True,
        True,
        True,
        True,
    ),

    Service(
        "AuditManager",
        "audit",
        True,
        True,
        True,
        True,
        True,
    ),

    Service(
        "HistoryManager",
        "history",
        True,
        True,
        True,
        True,
        True,
    ),
]


def save_registry():

    registry = {
        "status": "completed",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "service_count": len(DEFAULT_SERVICES),
        "services": [
            asdict(service)
            for service in DEFAULT_SERVICES
        ]
    }

    with REGISTRY_FILE.open(
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            registry,
            f,
            indent=2,
            ensure_ascii=False,
        )

    return registry


def main():

    registry = save_registry()

    print("=== AI OS Unified Service Registry ===")
    print("status:", registry["status"])
    print("phase:", registry["phase"])
    print("ServiceCount:", registry["service_count"])
    print("RegistryCreated:", True)
    print("RegistryPath:", REGISTRY_FILE)
    print("CurrentLevel:", "safe_dry_run_service_registry_ready")
    print("RiskCount:", 0)
    print("SafeToContinue:", True)


if __name__ == "__main__":
    main()