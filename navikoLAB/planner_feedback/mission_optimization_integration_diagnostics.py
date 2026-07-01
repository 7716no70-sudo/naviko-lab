from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_FILES = {
    "IntegrationSourceFound": WORKSPACE / "mission_self_optimization_integration_source.json",
    "PlannerHintFound": WORKSPACE / "planner_mission_optimization_hint.json",
    "CapabilityHintFound": WORKSPACE / "capability_mission_optimization_hint.json",
    "ConnectorHintFound": WORKSPACE / "connector_mission_optimization_hint.json",
}

def load_json(path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def main():
    found = {name: path.exists() for name, path in REQUIRED_FILES.items()}
    required_ok = all(found.values())

    planner = load_json(REQUIRED_FILES["PlannerHintFound"])
    capability = load_json(REQUIRED_FILES["CapabilityHintFound"])
    connector = load_json(REQUIRED_FILES["ConnectorHintFound"])

    risk_flags = [
        planner.get("PlannerWriteAllowed") is True,
        planner.get("PlannerPatchAllowed") is True,
        capability.get("CapabilityRouterWriteAllowed") is True,
        capability.get("CapabilityRouterPatchAllowed") is True,
        connector.get("ConnectorDispatcherWriteAllowed") is True,
        connector.get("ConnectorDispatcherPatchAllowed") is True,
        planner.get("OriginalWrite") is True,
        capability.get("OriginalWrite") is True,
        connector.get("OriginalWrite") is True,
        planner.get("ExternalOperation") is True,
        capability.get("ExternalOperation") is True,
        connector.get("ExternalOperation") is True,
        planner.get("RealGUIOperation") is True,
        capability.get("RealGUIOperation") is True,
        connector.get("RealGUIOperation") is True,
        planner.get("FileDelete") is True,
        capability.get("FileDelete") is True,
        connector.get("FileDelete") is True,
    ]

    risk_count = sum(1 for flag in risk_flags if flag)

    output = {
        "status": "completed" if required_ok and risk_count == 0 else "blocked",
        "phase": "Phase18-5 Mission Optimization Integration Diagnostics",
        **found,
        "RequiredOK": required_ok,
        "MissionOptimizationIntegrationReady": required_ok and risk_count == 0,
        "PlannerReadOnly": planner.get("ReadOnlyReference", False),
        "CapabilityReadOnly": capability.get("ReadOnlyReference", False),
        "ConnectorReadOnly": connector.get("ReadOnlyReference", False),
        "MissionLearningMode": planner.get("MissionLearningMode"),
        "Trend": planner.get("Trend"),
        "SuccessRate": planner.get("SuccessRate"),
        "FailureRate": planner.get("FailureRate"),
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "PlannerWriteAllowed": False,
        "PlannerPatchAllowed": False,
        "CapabilityRouterWriteAllowed": False,
        "CapabilityRouterPatchAllowed": False,
        "ConnectorDispatcherWriteAllowed": False,
        "ConnectorDispatcherPatchAllowed": False,
        "FileDelete": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "RiskCount": risk_count,
        "SafeToContinue": required_ok and risk_count == 0,
        "NextPhase": "Phase18-6 Mission Optimization Integration Completion Report",
        "updated_at": datetime.now().isoformat(),
    }

    out_path = REPORT_DIR / f"mission_optimization_integration_diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== Mission Optimization Integration Diagnostics ===")
    for k, v in output.items():
        print(f"{k}: {v}")
    print(f"保存先: {out_path}")

if __name__ == "__main__":
    main()