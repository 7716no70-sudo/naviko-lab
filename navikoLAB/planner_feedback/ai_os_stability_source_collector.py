from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"
REPORT_DIRS = [
    ROOT / "navikoLAB" / "planner_feedback" / "reports",
    ROOT / "navikoLAB",
]

OUT_PATH = WORKSPACE / "ai_os_stability_source.json"

SOURCE_PATTERNS = {
    "phase14_feedback_loop": "feedback_loop_completion_report*.json",
    "phase15_planner_self_improvement": "planner_self_improvement_completion_report*.json",
    "phase16_capability_connector_optimization": "capability_connector_optimization_completion_report_*.json",
    "phase17_mission_success_learning": "mission_success_learning_completion_report_*.json",
    "phase18_mission_optimization_integration": "mission_optimization_integration_completion_report_*.json",
    "phase19_mission_policy_stabilization": "mission_policy_stabilization_completion_report_*.json",
}

def latest_file(pattern):
    candidates = []

    for base in REPORT_DIRS:
        if not base.exists():
            continue
        candidates.extend(base.rglob(pattern))

    files = sorted(
        set(candidates),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return files[0] if files else None

def load_json(path):
    if not path or not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def main():
    WORKSPACE.mkdir(parents=True, exist_ok=True)

    sources = {}
    found = {}

    for name, pattern in SOURCE_PATTERNS.items():
        path = latest_file(pattern)
        data = load_json(path)
        found[f"{name}_found"] = data is not None
        sources[name] = {
            "path": str(path) if path else None,
            "data": data,
        }

    required_ok = all(found.values())

    output = {
        "status": "completed" if required_ok else "missing_source",
        "phase": "Phase20-1 AI OS Stability Source Collector",
        **found,
        "RequiredOK": required_ok,
        "AIOSStabilitySourceCollected": required_ok,
        "SourceCount": sum(1 for v in found.values() if v),
        "ReadOnlyReference": True,
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "PlannerWriteAllowed": False,
        "CapabilityRouterWriteAllowed": False,
        "ConnectorDispatcherWriteAllowed": False,
        "FileDelete": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "RiskCount": 0,
        "SafeToContinue": required_ok,
        "NextPhase": "Phase20-2 AI OS Stability Profile Builder",
        "updated_at": datetime.now().isoformat(),
        "sources": sources,
    }

    OUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== AI OS Stability Source Collector ===")
    for k, v in output.items():
        if k != "sources":
            print(f"{k}: {v}")
    print(f"保存先: {OUT_PATH}")

if __name__ == "__main__":
    main()