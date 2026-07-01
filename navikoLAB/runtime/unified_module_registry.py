# navikoLAB/runtime/unified_module_registry.py

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json


PHASE = "Phase94-1 AI OS Unified Module Registry"

ROOT = Path(__file__).resolve().parents[2]

REGISTRY_DIR = ROOT / "runtime" / "registry"
REGISTRY_DIR.mkdir(parents=True, exist_ok=True)

MODULE_REGISTRY_FILE = REGISTRY_DIR / "module_registry.json"


@dataclass
class ModuleEntry:
    name: str
    layer: str
    service: str
    enabled: bool
    dry_run: bool
    control_plane_required: bool
    execution_bus_required: bool
    policy_required: bool
    permission_required: bool
    approval_required: bool
    original_write: bool
    external_operation: bool
    browser_operation: bool
    real_gui_operation: bool
    file_delete: bool


DEFAULT_MODULES = [
    ModuleEntry("goal_manager", "goal", "GoalManager", True, True, True, True, True, True, True, False, False, False, False, False),
    ModuleEntry("goal_daemon", "daemon", "GoalDaemon", True, True, True, True, True, True, True, False, False, False, False, False),
    ModuleEntry("event_router", "event", "EventRouter", True, True, True, True, True, True, True, False, False, False, False, False),
    ModuleEntry("unified_control_plane", "control_plane", "UnifiedControlPlane", True, True, True, True, True, True, True, False, False, False, False, False),
    ModuleEntry("unified_execution_bus", "execution_bus", "UnifiedExecutionBus", True, True, True, True, True, True, True, False, False, False, False, False),
    ModuleEntry("policy_engine", "policy", "PolicyEngine", True, True, True, True, True, True, True, False, False, False, False, False),
    ModuleEntry("permission_layer", "permission", "PermissionLayer", True, True, True, True, True, True, True, False, False, False, False, False),
    ModuleEntry("capability_permission", "capability", "CapabilityPermission", True, True, True, True, True, True, True, False, False, False, False, False),
    ModuleEntry("human_approval", "approval", "HumanApproval", True, True, True, True, True, True, True, False, False, False, False, False),
    ModuleEntry("operation_guard", "guard", "OperationGuard", True, True, True, True, True, True, True, False, False, False, False, False),
    ModuleEntry("health_monitor", "health", "HealthMonitor", True, True, True, True, True, True, True, False, False, False, False, False),
    ModuleEntry("stability_kernel", "stability", "StabilityKernel", True, True, True, True, True, True, True, False, False, False, False, False),
    ModuleEntry("backup_manager", "backup", "BackupManager", True, True, True, True, True, True, True, False, False, False, False, False),
    ModuleEntry("recovery_manager", "recovery", "RecoveryManager", True, True, True, True, True, True, True, False, False, False, False, False),
    ModuleEntry("audit_manager", "audit", "AuditManager", True, True, True, True, True, True, True, False, False, False, False, False),
    ModuleEntry("history_manager", "history", "HistoryManager", True, True, True, True, True, True, True, False, False, False, False, False),
]


def build_module_registry():
    registry = {
        "status": "completed",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "module_count": len(DEFAULT_MODULES),
        "modules": [asdict(module) for module in DEFAULT_MODULES],
        "mode": "dry_run",
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "AutoExecute": False,
        "HumanApproved": False,
        "HumanApprovalRequired": True,
        "RiskCount": 0,
        "SafeToContinue": True,
        "CurrentLevel": "safe_dry_run_unified_module_registry_ready",
    }

    MODULE_REGISTRY_FILE.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return registry


def main():
    registry = build_module_registry()

    print("=== AI OS Unified Module Registry ===")
    print("status:", registry["status"])
    print("phase:", registry["phase"])
    print("ModuleCount:", registry["module_count"])
    print("ModuleRegistryCreated:", True)
    print("ModuleRegistryPath:", MODULE_REGISTRY_FILE)
    print("CurrentLevel:", registry["CurrentLevel"])
    print("RiskCount:", registry["RiskCount"])
    print("SafeToContinue:", registry["SafeToContinue"])


if __name__ == "__main__":
    main()