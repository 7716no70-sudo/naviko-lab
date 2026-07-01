from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"

SOURCE_PATH = WORKSPACE / "mission_self_optimization_integration_source.json"
OUT_PATH = WORKSPACE / "capability_mission_optimization_hint.json"

def main():
    if not SOURCE_PATH.exists():
        output = {
            "status": "missing_source",
            "phase": "Phase18-3 Capability Mission Optimization Read Adapter",
            "SourceFound": False,
            "SafeToContinue": False,
        }
    else:
        source = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
        hint = source.get("MissionSelfOptimizationHint", {})

        output = {
            "status": "completed",
            "phase": "Phase18-3 Capability Mission Optimization Read Adapter",
            "SourceFound": True,
            "CapabilityMissionOptimizationHintCreated": True,
            "MissionLearningMode": source.get("MissionLearningMode"),
            "Trend": source.get("Trend"),
            "SuccessRate": source.get("SuccessRate"),
            "FailureRate": source.get("FailureRate"),
            "CapabilityMissionOptimizationHint": {
                "capability_hint": hint.get(
                    "capability_hint",
                    "Continue collecting mission success data before capability selection changes."
                ),
                "optimization_mode": hint.get(
                    "optimization_mode",
                    source.get("MissionLearningMode", "observation")
                ),
                "capability_policy": "read_only_reference",
                "auto_modify_capability_router": False,
            },
            "ReadOnlyReference": True,
            "WorkspaceOnly": True,
            "OriginalWrite": False,
            "CapabilityRouterWriteAllowed": False,
            "CapabilityRouterPatchAllowed": False,
            "FileDelete": False,
            "ExternalOperation": False,
            "RealGUIOperation": False,
            "RiskCount": 0,
            "SafeToContinue": True,
            "NextPhase": "Phase18-4 Connector Mission Optimization Read Adapter",
            "updated_at": datetime.now().isoformat(),
        }

    OUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== Capability Mission Optimization Read Adapter ===")
    for k, v in output.items():
        print(f"{k}: {v}")
    print(f"保存先: {OUT_PATH}")

if __name__ == "__main__":
    main()