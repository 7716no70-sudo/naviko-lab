from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"

PROFILE_PATH = WORKSPACE / "mission_long_term_learning_profile.json"
OUT_PATH = WORKSPACE / "mission_self_optimization_hint.json"

def main():
    if not PROFILE_PATH.exists():
        output = {
            "status": "missing_profile",
            "phase": "Phase17-5 Mission Self Optimization Read Adapter",
            "ProfileFound": False,
            "SafeToContinue": False,
        }
    else:
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))

        learning_mode = profile.get("MissionLearningMode", "observation")
        trend = profile.get("Trend", "unclear")
        success_rate = profile.get("SuccessRate", 0.0)
        failure_rate = profile.get("FailureRate", 0.0)

        output = {
            "status": "completed",
            "phase": "Phase17-5 Mission Self Optimization Read Adapter",
            "ProfileFound": True,
            "MissionSelfOptimizationHintCreated": True,
            "MissionLearningMode": learning_mode,
            "Trend": trend,
            "SuccessRate": success_rate,
            "FailureRate": failure_rate,
            "MissionSelfOptimizationHint": {
                "planner_hint": (
                    "Prefer patterns from successful known mission records."
                    if learning_mode == "success_pattern_learning"
                    else "Continue collecting mission result data before changing planning behavior."
                ),
                "capability_hint": (
                    "Prefer capabilities associated with successful mission records."
                    if learning_mode == "success_pattern_learning"
                    else "Keep capability selection in observation mode."
                ),
                "connector_hint": (
                    "Prefer connector choices associated with successful mission records."
                    if learning_mode == "success_pattern_learning"
                    else "Keep connector selection in observation mode."
                ),
                "risk_hint": (
                    "Do not modify planner, capability router, or connector dispatcher automatically."
                ),
                "optimization_mode": learning_mode,
            },
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
            "NextPhase": "Phase17-6 Mission Self Optimization Diagnostics",
            "updated_at": datetime.now().isoformat(),
        }

    OUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== Mission Self Optimization Read Adapter ===")
    for k, v in output.items():
        print(f"{k}: {v}")
    print(f"保存先: {OUT_PATH}")

if __name__ == "__main__":
    main()