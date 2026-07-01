from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"

HINT_PATH = WORKSPACE / "mission_self_optimization_hint.json"
OUT_PATH = WORKSPACE / "mission_self_optimization_integration_source.json"

def main():
    if not HINT_PATH.exists():
        output = {
            "status": "missing_hint",
            "phase": "Phase18-1 Mission Self Optimization Integration Source Adapter",
            "HintFound": False,
            "SafeToContinue": False,
        }
    else:
        hint = json.loads(HINT_PATH.read_text(encoding="utf-8"))

        output = {
            "status": "completed",
            "phase": "Phase18-1 Mission Self Optimization Integration Source Adapter",
            "HintFound": True,
            "IntegrationSourceCreated": True,
            "MissionLearningMode": hint.get("MissionLearningMode"),
            "Trend": hint.get("Trend"),
            "SuccessRate": hint.get("SuccessRate"),
            "FailureRate": hint.get("FailureRate"),
            "MissionSelfOptimizationHint": hint.get("MissionSelfOptimizationHint", {}),
            "PlannerIntegrationAllowed": True,
            "CapabilityIntegrationAllowed": True,
            "ConnectorIntegrationAllowed": True,
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
            "SafeToContinue": True,
            "NextPhase": "Phase18-2 Planner Mission Optimization Read Adapter",
            "updated_at": datetime.now().isoformat(),
        }

    OUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== Mission Self Optimization Integration Source Adapter ===")
    for k, v in output.items():
        print(f"{k}: {v}")
    print(f"保存先: {OUT_PATH}")

if __name__ == "__main__":
    main()