from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"

HISTORY_PATH = WORKSPACE / "mission_success_history.json"
STATISTICS_PATH = WORKSPACE / "mission_success_statistics.json"
TREND_PATH = WORKSPACE / "mission_success_trend.json"
OUT_PATH = WORKSPACE / "mission_long_term_learning_profile.json"

def load_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    history = load_json(HISTORY_PATH)
    statistics = load_json(STATISTICS_PATH)
    trend = load_json(TREND_PATH)

    required_ok = all([history, statistics, trend])

    if not required_ok:
        output = {
            "status": "missing_source",
            "phase": "Phase17-4 Mission Long-Term Learning Profile",
            "HistoryFound": history is not None,
            "StatisticsFound": statistics is not None,
            "TrendFound": trend is not None,
            "SafeToContinue": False,
        }
    else:
        learning_mode = trend.get("RecommendedMissionLearningMode", "observation")

        output = {
            "status": "completed",
            "phase": "Phase17-4 Mission Long-Term Learning Profile",
            "MissionLongTermLearningProfileCreated": True,
            "HistoryFound": True,
            "StatisticsFound": True,
            "TrendFound": True,
            "RecordCount": statistics.get("RecordCount", 0),
            "KnownRecordCount": statistics.get("KnownRecordCount", 0),
            "SuccessRate": statistics.get("SuccessRate", 0.0),
            "FailureRate": statistics.get("FailureRate", 0.0),
            "UnknownRate": statistics.get("UnknownRate", 0.0),
            "Trend": trend.get("Trend", "unclear"),
            "MissionLearningMode": learning_mode,
            "MissionOptimizationPolicy": {
                "mode": learning_mode,
                "planner_hint_allowed": True,
                "capability_hint_allowed": True,
                "connector_hint_allowed": True,
                "write_allowed": False,
                "patch_allowed": False,
                "auto_apply_allowed": False,
            },
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
            "NextPhase": "Phase17-5 Mission Self Optimization Read Adapter",
            "updated_at": datetime.now().isoformat(),
        }

    OUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== Mission Long-Term Learning Profile ===")
    for k, v in output.items():
        print(f"{k}: {v}")
    print(f"保存先: {OUT_PATH}")

if __name__ == "__main__":
    main()