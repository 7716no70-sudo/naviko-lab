from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

FEEDBACK_LOOP_DIR = ROOT / "workspace" / "feedback_loop"
REPORT_DIR = ROOT / "app_operator" / "reports"

PLANNER_PROFILE_PATH = FEEDBACK_LOOP_DIR / "planner_self_improvement_profile.json"
PLANNER_COMPLETION_PATH = REPORT_DIR / "planner_self_improvement_completion_report.json"
FEEDBACK_INDEX_PATH = FEEDBACK_LOOP_DIR / "feedback_loop_index.json"

OUTPUT_PATH = FEEDBACK_LOOP_DIR / "capability_connector_optimization_source.json"


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def collect_capability_connector_optimization_source():
    planner_profile = _load_json(PLANNER_PROFILE_PATH)
    planner_completion = _load_json(PLANNER_COMPLETION_PATH)
    feedback_index = _load_json(FEEDBACK_INDEX_PATH)

    planner_profile_found = isinstance(planner_profile, dict)
    planner_completion_found = isinstance(planner_completion, dict)
    feedback_index_found = isinstance(feedback_index, dict)

    capability_feedback_items = []
    connector_feedback_items = []

    if feedback_index_found:
        candidates = []
        candidates.extend(feedback_index.get("reflection_candidates", []))
        candidates.extend(feedback_index.get("experience_candidates", []))

        for item in candidates:
            data = item.get("data", {}) if isinstance(item, dict) else {}
            text = json.dumps(data, ensure_ascii=False).lower()

            if "capability" in text or "能力" in text:
                capability_feedback_items.append(item)

            if "connector" in text or "dispatcher" in text or "接続" in text:
                connector_feedback_items.append(item)

    source = {
        "status": "completed",
        "phase": "Phase16-1 Capability Connector Optimization Source Collector",
        "planner_profile_found": planner_profile_found,
        "planner_completion_found": planner_completion_found,
        "feedback_index_found": feedback_index_found,
        "mission_success_rate": (
            planner_profile.get("mission_success_rate", 0.0)
            if planner_profile_found
            else 0.0
        ),
        "planner_mode": (
            planner_profile.get("planner_mode", "unknown")
            if planner_profile_found
            else "unknown"
        ),
        "capability_feedback_count": len(capability_feedback_items),
        "connector_feedback_count": len(connector_feedback_items),
        "capability_feedback_items": capability_feedback_items,
        "connector_feedback_items": connector_feedback_items,
        "optimization_source_ready": (
            planner_profile_found
            and planner_completion_found
            and feedback_index_found
        ),
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "external_operation": False,
        "real_gui_operation": False,
        "risk_count": 0,
        "safe_to_continue": (
            planner_profile_found
            and planner_completion_found
            and feedback_index_found
        ),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "paths": {
            "planner_profile": str(PLANNER_PROFILE_PATH),
            "planner_completion": str(PLANNER_COMPLETION_PATH),
            "feedback_index": str(FEEDBACK_INDEX_PATH),
            "output": str(OUTPUT_PATH),
        },
    }

    FEEDBACK_LOOP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(source, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return source


if __name__ == "__main__":
    result = collect_capability_connector_optimization_source()

    print("=== Capability Connector Optimization Source Collector ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['phase']}")
    print(f"PlannerProfileFound: {result['planner_profile_found']}")
    print(f"PlannerCompletionFound: {result['planner_completion_found']}")
    print(f"FeedbackIndexFound: {result['feedback_index_found']}")
    print(f"MissionSuccessRate: {result['mission_success_rate']}")
    print(f"PlannerMode: {result['planner_mode']}")
    print(f"CapabilityFeedbackCount: {result['capability_feedback_count']}")
    print(f"ConnectorFeedbackCount: {result['connector_feedback_count']}")
    print(f"OptimizationSourceReady: {result['optimization_source_ready']}")
    print(f"WorkspaceOnly: {result['workspace_only']}")
    print(f"OriginalWrite: {result['original_write']}")
    print(f"FileDelete: {result['file_delete']}")
    print(f"ExternalOperation: {result['external_operation']}")
    print(f"RealGUIOperation: {result['real_gui_operation']}")
    print(f"RiskCount: {result['risk_count']}")
    print(f"SafeToContinue: {result['safe_to_continue']}")
    print(f"保存先: {OUTPUT_PATH}")