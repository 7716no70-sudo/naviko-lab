from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"

SOURCE_FILES = {
    "mission_long_term_learning_profile": WORKSPACE / "mission_long_term_learning_profile.json",
    "mission_self_optimization_hint": WORKSPACE / "mission_self_optimization_hint.json",
    "planner_mission_optimization_hint": WORKSPACE / "planner_mission_optimization_hint.json",
    "capability_mission_optimization_hint": WORKSPACE / "capability_mission_optimization_hint.json",
    "connector_mission_optimization_hint": WORKSPACE / "connector_mission_optimization_hint.json",
}

OUT_PATH = WORKSPACE / "mission_policy_source.json"

def load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def main():
    sources = {}
    found = {}

    for name, path in SOURCE_FILES.items():
        data = load_json(path)
        sources[name] = data
        found[f"{name}_found"] = data is not None

    required_ok = all(found.values())

    output = {
        "status": "completed" if required_ok else "missing_source",
        "phase": "Phase19-1 Mission Policy Source Collector",
        **found,
        "RequiredOK": required_ok,
        "MissionPolicySourceCollected": required_ok,
        "MissionLearningMode": (
            sources["mission_long_term_learning_profile"].get("MissionLearningMode")
            if sources["mission_long_term_learning_profile"] else None
        ),
        "Trend": (
            sources["mission_long_term_learning_profile"].get("Trend")
            if sources["mission_long_term_learning_profile"] else None
        ),
        "SuccessRate": (
            sources["mission_long_term_learning_profile"].get("SuccessRate")
            if sources["mission_long_term_learning_profile"] else None
        ),
        "FailureRate": (
            sources["mission_long_term_learning_profile"].get("FailureRate")
            if sources["mission_long_term_learning_profile"] else None
        ),
        "PolicySource": sources,
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
        "NextPhase": "Phase19-2 Mission Stability Policy Builder",
        "updated_at": datetime.now().isoformat(),
    }

    OUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== Mission Policy Source Collector ===")
    for k, v in output.items():
        if k != "PolicySource":
            print(f"{k}: {v}")
    print(f"保存先: {OUT_PATH}")

if __name__ == "__main__":
    main()