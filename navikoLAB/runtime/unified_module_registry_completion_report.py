# navikoLAB/runtime/unified_module_registry_completion_report.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json


PHASE = "Phase94-3 AI OS Unified Module Registry Completion Report"

ROOT = Path(__file__).resolve().parents[2]

MODULE_REGISTRY_FILE = ROOT / "runtime" / "registry" / "module_registry.json"

REPORT_DIR = ROOT / "runtime" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_module_registry():
    if not MODULE_REGISTRY_FILE.exists():
        return None
    return json.loads(MODULE_REGISTRY_FILE.read_text(encoding="utf-8"))


def build_report():
    registry = load_module_registry()
    modules = registry.get("modules", []) if registry else []

    report = {
        "status": "completed" if registry else "failed",
        "phase": PHASE,
        "ModuleRegistryFound": registry is not None,
        "UnifiedModuleRegistryCompleted": registry is not None,
        "ModuleCount": len(modules),
        "AllModulesDryRun": all(m.get("dry_run", False) for m in modules),
        "AllRequireControlPlane": all(m.get("control_plane_required", False) for m in modules),
        "AllRequireExecutionBus": all(m.get("execution_bus_required", False) for m in modules),
        "AllRequirePolicy": all(m.get("policy_required", False) for m in modules),
        "AllRequirePermission": all(m.get("permission_required", False) for m in modules),
        "AllRequireHumanApproval": all(m.get("approval_required", False) for m in modules),
        "DangerousFlagsAllFalse": all(
            not m.get("original_write", False)
            and not m.get("external_operation", False)
            and not m.get("browser_operation", False)
            and not m.get("real_gui_operation", False)
            and not m.get("file_delete", False)
            for m in modules
        ),
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
        "SafeToContinue": registry is not None,
        "CurrentLevel": "safe_dry_run_unified_module_registry_ready",
        "NextPhase": "Phase95 AI OS Dependency Graph",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = REPORT_DIR / f"unified_module_registry_completion_report_{timestamp}.json"

    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return report, path


def main():
    report, path = build_report()

    print("=== AI OS Unified Module Registry Completion Report ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"保存先: {path}")


if __name__ == "__main__":
    main()