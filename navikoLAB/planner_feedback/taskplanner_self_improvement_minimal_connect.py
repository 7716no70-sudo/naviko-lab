from pathlib import Path
import json
from datetime import datetime

from navikoLAB.planner_feedback.taskplanner_self_improvement_read_adapter import (
    load_taskplanner_self_improvement_context,
)

ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_LOOP_DIR = ROOT / "workspace" / "feedback_loop"
OUTPUT_PATH = FEEDBACK_LOOP_DIR / "taskplanner_self_improvement_connected.json"


def connect_self_improvement_to_taskplanner(mission: str = "dry_run_mission"):
    context = load_taskplanner_self_improvement_context()

    connected_plan_context = {
        "status": "completed" if context.get("self_improvement_context_found") else "incomplete",
        "phase": "Phase15-5 TaskPlanner Self Improvement Minimal Connect",
        "mission": mission,
        "self_improvement_context_found": context.get("self_improvement_context_found", False),
        "mission_success_rate": context.get("mission_success_rate", 0.0),
        "planner_mode": context.get("planner_mode", "unknown"),
        "recommendations": context.get("recommendations", []),
        "taskplanner_hint": context.get("taskplanner_hint", ""),
        "connected_to_taskplanner": context.get("self_improvement_context_found", False),
        "connection_type": "read_only_reference",
        "planner_logic_modified": False,
        "planner_write_allowed": False,
        "planner_patch_allowed": False,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": context.get("safe_to_continue", False),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "output_path": str(OUTPUT_PATH),
    }

    FEEDBACK_LOOP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(connected_plan_context, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return connected_plan_context


if __name__ == "__main__":
    result = connect_self_improvement_to_taskplanner()

    print("=== TaskPlanner Self Improvement Minimal Connect ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['phase']}")
    print(f"Mission: {result['mission']}")
    print(f"SelfImprovementContextFound: {result['self_improvement_context_found']}")
    print(f"MissionSuccessRate: {result['mission_success_rate']}")
    print(f"PlannerMode: {result['planner_mode']}")
    print(f"RecommendationCount: {len(result['recommendations'])}")
    print(f"TaskPlannerHint: {result['taskplanner_hint']}")
    print(f"ConnectedToTaskPlanner: {result['connected_to_taskplanner']}")
    print(f"ConnectionType: {result['connection_type']}")
    print(f"PlannerLogicModified: {result['planner_logic_modified']}")
    print(f"PlannerWriteAllowed: {result['planner_write_allowed']}")
    print(f"PlannerPatchAllowed: {result['planner_patch_allowed']}")
    print(f"WorkspaceOnly: {result['workspace_only']}")
    print(f"OriginalWrite: {result['original_write']}")
    print(f"FileDelete: {result['file_delete']}")
    print(f"RiskCount: {result['risk_count']}")
    print(f"SafeToContinue: {result['safe_to_continue']}")
    print(f"保存先: {OUTPUT_PATH}")