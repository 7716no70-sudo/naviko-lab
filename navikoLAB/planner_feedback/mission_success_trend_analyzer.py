from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"

HISTORY_PATH = WORKSPACE / "mission_success_history.json"
STATISTICS_PATH = WORKSPACE / "mission_success_statistics.json"
OUT_PATH = WORKSPACE / "mission_success_trend.json"

def detect_trend(success_rate, failure_rate, known_count):
    if known_count < 3:
        return "insufficient_data"
    if success_rate >= 0.8 and failure_rate <= 0.2:
        return "stable_success"
    if success_rate >= 0.5:
        return "mixed_but_positive"
    if failure_rate > success_rate:
        return "failure_dominant"
    return "unclear"

def main():
    history_found = HISTORY_PATH.exists()
    statistics_found = STATISTICS_PATH.exists()

    if not history_found or not statistics_found:
        output = {
            "status": "missing_source",
            "phase": "Phase17-3 Mission Success Trend Analyzer",
            "HistoryFound": history_found,
            "StatisticsFound": statistics_found,
            "SafeToContinue": False,
        }
    else:
        history = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
        statistics = json.loads(STATISTICS_PATH.read_text(encoding="utf-8"))

        records = history.get("records", [])
        known_records = [
            r for r in records
            if r.get("success_signal") in ["success", "failure"]
        ]

        success_rate = statistics.get("SuccessRate", 0.0)
        failure_rate = statistics.get("FailureRate", 0.0)
        known_count = statistics.get("KnownRecordCount", 0)
        unknown_count = statistics.get("UnknownCount", 0)

        trend = detect_trend(success_rate, failure_rate, known_count)

        output = {
            "status": "completed",
            "phase": "Phase17-3 Mission Success Trend Analyzer",
            "HistoryFound": True,
            "StatisticsFound": True,
            "MissionSuccessTrendAnalyzed": True,
            "KnownRecordCount": known_count,
            "UnknownCount": unknown_count,
            "SuccessRate": success_rate,
            "FailureRate": failure_rate,
            "Trend": trend,
            "TrendHint": {
                "stable_success": "Known mission records are consistently successful.",
                "mixed_but_positive": "Mission outcomes are mixed but leaning positive.",
                "failure_dominant": "Failures dominate known records; planning should become more cautious.",
                "insufficient_data": "More mission records are needed before optimization.",
                "unclear": "Trend is unclear and should remain in observation mode.",
            }.get(trend, "Trend could not be determined."),
            "RecommendedMissionLearningMode": (
                "success_pattern_learning"
                if trend == "stable_success"
                else "observation"
            ),
            "WorkspaceOnly": True,
            "OriginalWrite": False,
            "FileDelete": False,
            "ExternalOperation": False,
            "RealGUIOperation": False,
            "RiskCount": 0,
            "SafeToContinue": True,
            "NextPhase": "Phase17-4 Mission Long-Term Learning Profile",
            "updated_at": datetime.now().isoformat(),
            "known_records": known_records,
        }

    OUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== Mission Success Trend Analyzer ===")
    for k, v in output.items():
        if k != "known_records":
            print(f"{k}: {v}")
    print(f"保存先: {OUT_PATH}")

if __name__ == "__main__":
    main()