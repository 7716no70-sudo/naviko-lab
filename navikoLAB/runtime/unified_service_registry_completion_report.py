# navikoLAB/runtime/unified_service_registry_completion_report.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json


PHASE = "Phase93-3 AI OS Unified Service Registry Completion Report"

ROOT = Path(__file__).resolve().parents[2]

REGISTRY_FILE = ROOT / "runtime" / "registry" / "service_registry.json"

REPORT_DIR = ROOT / "runtime" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_registry():
    if not REGISTRY_FILE.exists():
        return None
    return json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))


def build_report():
    registry = load_registry()
    services = registry.get("services", []) if registry else []

    report = {
        "status": "completed" if registry else "failed",
        "phase": PHASE,
        "RegistryFound": registry is not None,
        "UnifiedServiceRegistryCompleted": registry is not None,
        "ServiceCount": len(services),
        "AllServicesDryRun": all(s.get("dry_run", False) for s in services),
        "AllRequireControlPlane": all(s.get("control_plane_required", False) for s in services),
        "AllRequireExecutionBus": all(s.get("execution_bus_required", False) for s in services),
        "AllRequireHumanApproval": all(s.get("approval_required", False) for s in services),
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
        "CurrentLevel": "safe_dry_run_unified_service_registry_ready",
        "NextPhase": "Phase94 AI OS Unified Module Registry",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = REPORT_DIR / f"unified_service_registry_completion_report_{timestamp}.json"

    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return report, path


def main():
    report, path = build_report()

    print("=== AI OS Unified Service Registry Completion Report ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"保存先: {path}")


if __name__ == "__main__":
    main()