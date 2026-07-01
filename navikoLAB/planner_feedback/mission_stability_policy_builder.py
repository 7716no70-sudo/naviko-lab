from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"

SOURCE_PATH = WORKSPACE / "mission_policy_source.json"
OUT_PATH = WORKSPACE / "mission_stability_policy.json"

def main():
    if not SOURCE_PATH.exists():
        output = {
            "status": "missing_source",
            "phase": "Phase19-2 Mission Stability Policy Builder",
            "SourceFound": False,
            "SafeToContinue": False,
        }
    else:
        source = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))

        learning_mode = source.get("MissionLearningMode", "observation")
        trend = source.get("Trend", "unclear")
        success_rate = source.get("SuccessRate", 0.0)
        failure_rate = source.get("FailureRate", 0.0)

        policy_mode = (
            "stable_success_reference"
            if learning_mode == "success_pattern_learning" and trend == "stable_success"
            else "observation_only"
        )

        output = {
            "status": "completed",
            "phase": "Phase19-2 Mission Stability Policy Builder",
            "SourceFound": True,
            "MissionStabilityPolicyCreated": True,
            "MissionLearningMode": learning_mode,
            "Trend": trend,
            "SuccessRate": success_rate,
            "FailureRate": failure_rate,
            "MissionStabilityPolicy": {
                "policy_mode": policy_mode,
                "use_success_patterns": policy_mode == "stable_success_reference",
                "allow_planner_hint": True,
                "allow_capability_hint": True,
                "allow_connector_hint": True,
                "allow_auto_write": False,
                "allow_auto_patch": False,
                "allow_external_operation": False,
                "allow_real_gui_operation": False,
                "require_human_approval": True,
                "require_permission_policy": True,
                "stability_note": (
                    "Use mission success patterns only as read-only reference hints."
                ),
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
            "NextPhase": "Phase19-3 Mission Policy Read Adapter",
            "updated_at": datetime.now().isoformat(),
        }

    OUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== Mission Stability Policy Builder ===")
    for k, v in output.items():
        print(f"{k}: {v}")
    print(f"保存先: {OUT_PATH}")

if __name__ == "__main__":
    main()