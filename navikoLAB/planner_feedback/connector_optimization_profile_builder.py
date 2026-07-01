from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_LOOP_DIR = ROOT / "workspace" / "feedback_loop"

SOURCE_PATH = FEEDBACK_LOOP_DIR / "capability_connector_optimization_source.json"
OUTPUT_PATH = FEEDBACK_LOOP_DIR / "connector_optimization_profile.json"


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def build_connector_optimization_profile():
    source = _load_json(SOURCE_PATH)
    source_found = isinstance(source, dict)

    mission_success_rate = 0.0
    planner_mode = "unknown"
    connector_feedback_count = 0

    if source_found:
        mission_success_rate = float(source.get("mission_success_rate", 0.0))
        planner_mode = source.get("planner_mode", "unknown")
        connector_feedback_count = int(source.get("connector_feedback_count", 0))

    connector_mode = "neutral"
    recommendations = []

    if not source_found:
        connector_mode = "missing_source"
        recommendations.append("Connector最適化Sourceが見つからないため、最適化を保留する")
    elif connector_feedback_count == 0:
        connector_mode = "data_collection"
        recommendations.append("Connector Feedbackが少ないため、接続選択ログをさらに蓄積する")
        recommendations.append("現段階ではConnectorDispatcherの判断を変更せず、読み取り分析のみ継続する")
    elif mission_success_rate >= 0.8:
        connector_mode = "reinforce_successful_connectors"
        recommendations.append("成功Missionで利用されたConnectorを優先候補として扱う")
    elif mission_success_rate >= 0.5:
        connector_mode = "balanced_connector_selection"
        recommendations.append("Connector選択は成功率と失敗傾向を比較して慎重に調整する")
        recommendations.append("失敗Signalがある場合は代替Connector候補も保持する")
    else:
        connector_mode = "cautious_connector_selection"
        recommendations.append("Connector選択は慎重モードにする")
        recommendations.append("外部接続はHumanApprovalとPermissionPolicy確認後のみ候補化する")

    profile_ready = source_found

    profile = {
        "status": "completed" if profile_ready else "incomplete",
        "phase": "Phase16-3 Connector Optimization Profile Builder",
        "source_found": source_found,
        "mission_success_rate": mission_success_rate,
        "planner_mode": planner_mode,
        "connector_feedback_count": connector_feedback_count,
        "connector_mode": connector_mode,
        "recommendations": recommendations,
        "connector_optimization_profile_ready": profile_ready,
        "connector_dispatcher_write_allowed": False,
        "connector_dispatcher_patch_allowed": False,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "external_operation": False,
        "real_gui_operation": False,
        "risk_count": 0,
        "safe_to_continue": profile_ready,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_path": str(SOURCE_PATH),
        "output_path": str(OUTPUT_PATH),
    }

    FEEDBACK_LOOP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(profile, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return profile


if __name__ == "__main__":
    result = build_connector_optimization_profile()

    print("=== Connector Optimization Profile Builder ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['phase']}")
    print(f"SourceFound: {result['source_found']}")
    print(f"MissionSuccessRate: {result['mission_success_rate']}")
    print(f"PlannerMode: {result['planner_mode']}")
    print(f"ConnectorFeedbackCount: {result['connector_feedback_count']}")
    print(f"ConnectorMode: {result['connector_mode']}")
    print(f"RecommendationCount: {len(result['recommendations'])}")
    print(f"ConnectorOptimizationProfileReady: {result['connector_optimization_profile_ready']}")
    print(f"ConnectorDispatcherWriteAllowed: {result['connector_dispatcher_write_allowed']}")
    print(f"ConnectorDispatcherPatchAllowed: {result['connector_dispatcher_patch_allowed']}")
    print(f"WorkspaceOnly: {result['workspace_only']}")
    print(f"OriginalWrite: {result['original_write']}")
    print(f"FileDelete: {result['file_delete']}")
    print(f"ExternalOperation: {result['external_operation']}")
    print(f"RealGUIOperation: {result['real_gui_operation']}")
    print(f"RiskCount: {result['risk_count']}")
    print(f"SafeToContinue: {result['safe_to_continue']}")
    print(f"保存先: {OUTPUT_PATH}")