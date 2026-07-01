from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_LOOP_DIR = ROOT / "workspace" / "feedback_loop"
REPORT_DIR = ROOT / "app_operator" / "reports"

SUCCESS_PROFILE_PATH = FEEDBACK_LOOP_DIR / "planner_success_profile.json"
RECOMMENDATION_PATH = FEEDBACK_LOOP_DIR / "planner_improvement_recommendation.json"
SELF_IMPROVEMENT_PROFILE_PATH = FEEDBACK_LOOP_DIR / "planner_self_improvement_profile.json"
CONNECTED_PATH = FEEDBACK_LOOP_DIR / "taskplanner_self_improvement_connected.json"
DIAGNOSTICS_PATH = REPORT_DIR / "planner_self_improvement_diagnostics.json"


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def run_planner_self_improvement_diagnostics():
    success_profile = _load_json(SUCCESS_PROFILE_PATH)
    recommendation = _load_json(RECOMMENDATION_PATH)
    self_profile = _load_json(SELF_IMPROVEMENT_PROFILE_PATH)
    connected = _load_json(CONNECTED_PATH)

    checks = {
        "success_profile_found": isinstance(success_profile, dict),
        "recommendation_found": isinstance(recommendation, dict),
        "self_improvement_profile_found": isinstance(self_profile, dict),
        "taskplanner_connection_found": isinstance(connected, dict),
        "planner_write_allowed": False,
        "planner_patch_allowed": False,
        "original_write": False,
        "file_delete": False,
        "workspace_only": True,
    }

    risk_count = 0

    if isinstance(self_profile, dict):
        if self_profile.get("planner_write_allowed") is not False:
            risk_count += 1
        if self_profile.get("planner_patch_allowed") is not False:
            risk_count += 1
        if self_profile.get("original_write") is not False:
            risk_count += 1

    if isinstance(connected, dict):
        if connected.get("planner_logic_modified") is not False:
            risk_count += 1
        if connected.get("original_write") is not False:
            risk_count += 1
        if connected.get("file_delete") is not False:
            risk_count += 1

    required_ok = all([
        checks["success_profile_found"],
        checks["recommendation_found"],
        checks["self_improvement_profile_found"],
        checks["taskplanner_connection_found"],
    ])

    completed = required_ok and risk_count == 0

    diagnostics = {
        "status": "completed" if completed else "incomplete",
        "phase": "Phase15-6 Planner Self Improvement Diagnostics",
        "checks": checks,
        "required_ok": required_ok,
        "risk_count": risk_count,
        "planner_self_improvement_connected": completed,
        "planner_logic_modified": False,
        "planner_write_allowed": False,
        "planner_patch_allowed": False,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "safe_to_continue": completed,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "paths": {
            "success_profile": str(SUCCESS_PROFILE_PATH),
            "recommendation": str(RECOMMENDATION_PATH),
            "self_improvement_profile": str(SELF_IMPROVEMENT_PROFILE_PATH),
            "connected": str(CONNECTED_PATH),
            "diagnostics": str(DIAGNOSTICS_PATH),
        },
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    DIAGNOSTICS_PATH.write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return diagnostics


if __name__ == "__main__":
    result = run_planner_self_improvement_diagnostics()

    print("=== Planner Self Improvement Diagnostics ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['phase']}")
    print(f"RequiredOK: {result['required_ok']}")
    print(f"PlannerSelfImprovementConnected: {result['planner_self_improvement_connected']}")
    print(f"PlannerLogicModified: {result['planner_logic_modified']}")
    print(f"PlannerWriteAllowed: {result['planner_write_allowed']}")
    print(f"PlannerPatchAllowed: {result['planner_patch_allowed']}")
    print(f"WorkspaceOnly: {result['workspace_only']}")
    print(f"OriginalWrite: {result['original_write']}")
    print(f"FileDelete: {result['file_delete']}")
    print(f"RiskCount: {result['risk_count']}")
    print(f"SafeToContinue: {result['safe_to_continue']}")
    print(f"保存先: {DIAGNOSTICS_PATH}")