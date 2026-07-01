from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

SOURCE_PATH = WORKSPACE / "mission_policy_source.json"
STABILITY_PATH = WORKSPACE / "mission_stability_policy.json"
HINT_PATH = WORKSPACE / "mission_policy_hint.json"

def load_json(path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def main():
    source_found = SOURCE_PATH.exists()
    stability_found = STABILITY_PATH.exists()
    hint_found = HINT_PATH.exists()

    source = load_json(SOURCE_PATH)
    stability = load_json(STABILITY_PATH)
    hint = load_json(HINT_PATH)

    policy_hint = hint.get("MissionPolicyHint", {})

    required_ok = source_found and stability_found and hint_found

    risk_flags = [
        policy_hint.get("auto_write_allowed") is True,
        policy_hint.get("auto_patch_allowed") is True,
        policy_hint.get("external_operation_allowed") is True,
        policy_hint.get("real_gui_operation_allowed") is True,
        hint.get("OriginalWrite") is True,
        hint.get("PlannerWriteAllowed") is True,
        hint.get("CapabilityRouterWriteAllowed") is True,
        hint.get("ConnectorDispatcherWriteAllowed") is True,
        hint.get("FileDelete") is True,
        hint.get("ExternalOperation") is True,
        hint.get("RealGUIOperation") is True,
    ]

    risk_count = sum(1 for flag in risk_flags if flag)

    approval_required = policy_hint.get("human_approval_required") is True
    permission_required = policy_hint.get("permission_policy_required") is True
    read_only = policy_hint.get("reference_mode") == "read_only"

    output = {
        "status": "completed" if required_ok and risk_count == 0 and approval_required and permission_required and read_only else "blocked",
        "phase": "Phase19-4 Mission Policy Diagnostics",
        "SourceFound": source_found,
        "StabilityPolicyFound": stability_found,
        "PolicyHintFound": hint_found,
        "RequiredOK": required_ok,
        "MissionPolicyDiagnosticsCompleted": True,
        "MissionPolicyReady": required_ok and risk_count == 0 and approval_required and permission_required and read_only,
        "MissionLearningMode": hint.get("MissionLearningMode"),
        "Trend": hint.get("Trend"),
        "PolicyMode": policy_hint.get("policy_mode"),
        "ReferenceMode": policy_hint.get("reference_mode"),
        "HumanApprovalRequired": approval_required,
        "PermissionPolicyRequired": permission_required,
        "ReadOnlyReference": hint.get("ReadOnlyReference", False),
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "PlannerWriteAllowed": False,
        "CapabilityRouterWriteAllowed": False,
        "ConnectorDispatcherWriteAllowed": False,
        "FileDelete": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "RiskCount": risk_count,
        "SafeToContinue": required_ok and risk_count == 0 and approval_required and permission_required and read_only,
        "NextPhase": "Phase19-5 Mission Policy Stabilization Completion Report",
        "updated_at": datetime.now().isoformat(),
    }

    out_path = REPORT_DIR / f"mission_policy_diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== Mission Policy Diagnostics ===")
    for k, v in output.items():
        print(f"{k}: {v}")
    print(f"保存先: {out_path}")

if __name__ == "__main__":
    main()