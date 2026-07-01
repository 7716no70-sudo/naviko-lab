from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "app_operator" / "reports"

DIAGNOSTICS_PATH = REPORT_DIR / "planner_self_improvement_diagnostics.json"
REPORT_PATH = REPORT_DIR / "planner_self_improvement_completion_report.json"


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def create_planner_self_improvement_completion_report():
    diagnostics = _load_json(DIAGNOSTICS_PATH)
    diagnostics_found = isinstance(diagnostics, dict)

    risk_count = 0
    safe_to_continue = False
    planner_connected = False
    planner_logic_modified = False

    if diagnostics_found:
        risk_count = int(diagnostics.get("risk_count", 0))
        safe_to_continue = bool(diagnostics.get("safe_to_continue", False))
        planner_connected = bool(
            diagnostics.get("planner_self_improvement_connected", False)
        )
        planner_logic_modified = bool(
            diagnostics.get("planner_logic_modified", False)
        )

    completed = (
        diagnostics_found
        and planner_connected
        and safe_to_continue
        and risk_count == 0
        and planner_logic_modified is False
    )

    report = {
        "status": "completed" if completed else "incomplete",
        "phase": "Phase15-7 Planner Self Improvement Completion Report",
        "phase15_completed": completed,
        "diagnostics_found": diagnostics_found,
        "planner_self_improvement_connected": planner_connected,
        "planner_logic_modified": planner_logic_modified,
        "planner_write_allowed": False,
        "planner_patch_allowed": False,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": risk_count,
        "safe_to_continue": completed,
        "next_phase": (
            "Phase16 Capability / Connector Self Optimization"
            if completed
            else "Phase15 review required"
        ),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "diagnostics_path": str(DIAGNOSTICS_PATH),
        "report_path": str(REPORT_PATH),
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return report


if __name__ == "__main__":
    result = create_planner_self_improvement_completion_report()

    print("=== Planner Self Improvement Completion Report ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['phase']}")
    print(f"Phase15Completed: {result['phase15_completed']}")
    print(f"DiagnosticsFound: {result['diagnostics_found']}")
    print(f"PlannerSelfImprovementConnected: {result['planner_self_improvement_connected']}")
    print(f"PlannerLogicModified: {result['planner_logic_modified']}")
    print(f"PlannerWriteAllowed: {result['planner_write_allowed']}")
    print(f"PlannerPatchAllowed: {result['planner_patch_allowed']}")
    print(f"WorkspaceOnly: {result['workspace_only']}")
    print(f"OriginalWrite: {result['original_write']}")
    print(f"FileDelete: {result['file_delete']}")
    print(f"RiskCount: {result['risk_count']}")
    print(f"SafeToContinue: {result['safe_to_continue']}")
    print(f"次工程: {result['next_phase']}")
    print(f"保存先: {REPORT_PATH}")