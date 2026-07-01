from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"

POLICY_PATH = WORKSPACE / "mission_stability_policy.json"
OUT_PATH = WORKSPACE / "mission_policy_hint.json"

def main():
    if not POLICY_PATH.exists():
        output = {
            "status": "missing_policy",
            "phase": "Phase19-3 Mission Policy Read Adapter",
            "PolicyFound": False,
            "SafeToContinue": False,
        }
    else:
        policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        stability = policy.get("MissionStabilityPolicy", {})

        output = {
            "status": "completed",
            "phase": "Phase19-3 Mission Policy Read Adapter",
            "PolicyFound": True,
            "MissionPolicyHintCreated": True,
            "MissionLearningMode": policy.get("MissionLearningMode"),
            "Trend": policy.get("Trend"),
            "SuccessRate": policy.get("SuccessRate"),
            "FailureRate": policy.get("FailureRate"),
            "MissionPolicyHint": {
                "policy_mode": stability.get("policy_mode", "observation_only"),
                "use_success_patterns": stability.get("use_success_patterns", False),
                "planner_hint_allowed": stability.get("allow_planner_hint", False),
                "capability_hint_allowed": stability.get("allow_capability_hint", False),
                "connector_hint_allowed": stability.get("allow_connector_hint", False),
                "auto_write_allowed": False,
                "auto_patch_allowed": False,
                "external_operation_allowed": False,
                "real_gui_operation_allowed": False,
                "human_approval_required": True,
                "permission_policy_required": True,
                "reference_mode": "read_only",
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
            "NextPhase": "Phase19-4 Mission Policy Diagnostics",
            "updated_at": datetime.now().isoformat(),
        }

    OUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== Mission Policy Read Adapter ===")
    for k, v in output.items():
        print(f"{k}: {v}")
    print(f"保存先: {OUT_PATH}")

if __name__ == "__main__":
    main()