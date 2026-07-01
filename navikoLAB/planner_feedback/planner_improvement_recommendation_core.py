from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_LOOP_DIR = ROOT / "workspace" / "feedback_loop"
PROFILE_PATH = FEEDBACK_LOOP_DIR / "planner_success_profile.json"
RECOMMENDATION_PATH = FEEDBACK_LOOP_DIR / "planner_improvement_recommendation.json"


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def create_planner_improvement_recommendation():
    profile = _load_json(PROFILE_PATH)

    mission_success_rate = 0.0
    success_signal_count = 0
    failure_signal_count = 0
    total_signal_count = 0
    source_profile_found = isinstance(profile, dict)

    if source_profile_found:
        mission_success_rate = float(profile.get("mission_success_rate", 0.0))
        success_signal_count = int(profile.get("success_signal_count", 0))
        failure_signal_count = int(profile.get("failure_signal_count", 0))
        total_signal_count = int(profile.get("total_signal_count", 0))

    recommendations = []
    planner_mode = "balanced"

    if total_signal_count == 0:
        planner_mode = "data_collection"
        recommendations.append("Mission結果データをさらに蓄積する")
        recommendations.append("Planner改善はまだ反映せず、分析のみ継続する")
    elif mission_success_rate >= 0.8:
        planner_mode = "success_reinforcement"
        recommendations.append("成功したPlanner方針を優先して再利用する")
        recommendations.append("同種Missionでは既存の計画パターンを強める")
    elif mission_success_rate >= 0.5:
        planner_mode = "balanced_improvement"
        recommendations.append("成功パターンと失敗パターンを比較して計画を調整する")
        recommendations.append("失敗Signalが含まれる場合は追加確認ステップを増やす")
    else:
        planner_mode = "cautious_replanning"
        recommendations.append("Plannerは慎重モードで再計画する")
        recommendations.append("Missionを小さなステップへ分解する")
        recommendations.append("HumanApproval確認点を増やす")

    if failure_signal_count > success_signal_count:
        recommendations.append("失敗Signalが成功Signalを上回るため、安全確認を優先する")

    recommendation = {
        "status": "completed" if source_profile_found else "incomplete",
        "phase": "Phase15-2 Planner Improvement Recommendation Core",
        "source_profile_found": source_profile_found,
        "mission_success_rate": mission_success_rate,
        "success_signal_count": success_signal_count,
        "failure_signal_count": failure_signal_count,
        "total_signal_count": total_signal_count,
        "planner_mode": planner_mode,
        "recommendations": recommendations,
        "planner_self_improvement_recommendation_ready": source_profile_found,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": source_profile_found,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_profile_path": str(PROFILE_PATH),
        "recommendation_path": str(RECOMMENDATION_PATH),
    }

    FEEDBACK_LOOP_DIR.mkdir(parents=True, exist_ok=True)
    RECOMMENDATION_PATH.write_text(
        json.dumps(recommendation, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return recommendation


if __name__ == "__main__":
    result = create_planner_improvement_recommendation()

    print("=== Planner Improvement Recommendation Core ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['phase']}")
    print(f"SourceProfileFound: {result['source_profile_found']}")
    print(f"MissionSuccessRate: {result['mission_success_rate']}")
    print(f"SuccessSignalCount: {result['success_signal_count']}")
    print(f"FailureSignalCount: {result['failure_signal_count']}")
    print(f"TotalSignalCount: {result['total_signal_count']}")
    print(f"PlannerMode: {result['planner_mode']}")
    print(f"RecommendationCount: {len(result['recommendations'])}")
    print(f"PlannerSelfImprovementRecommendationReady: {result['planner_self_improvement_recommendation_ready']}")
    print(f"WorkspaceOnly: {result['workspace_only']}")
    print(f"OriginalWrite: {result['original_write']}")
    print(f"FileDelete: {result['file_delete']}")
    print(f"RiskCount: {result['risk_count']}")
    print(f"SafeToContinue: {result['safe_to_continue']}")
    print(f"保存先: {RECOMMENDATION_PATH}")