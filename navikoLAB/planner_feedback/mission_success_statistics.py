from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"

HISTORY_PATH = WORKSPACE / "mission_success_history.json"
OUT_PATH = WORKSPACE / "mission_success_statistics.json"

def safe_rate(part, total):
    if total <= 0:
        return 0.0
    return round(part / total, 4)

def main():
    if not HISTORY_PATH.exists():
        output = {
            "status": "missing_history",
            "phase": "Phase17-2 Mission Success Statistics",
            "HistoryFound": False,
            "SafeToContinue": False,
        }
    else:
        history = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
        records = history.get("records", [])

        total = len(records)
        success = sum(1 for r in records if r.get("success_signal") == "success")
        failure = sum(1 for r in records if r.get("success_signal") == "failure")
        unknown = sum(1 for r in records if r.get("success_signal") == "unknown")

        known_total = success + failure

        output = {
            "status": "completed",
            "phase": "Phase17-2 Mission Success Statistics",
            "HistoryFound": True,
            "MissionSuccessStatisticsCreated": True,
            "RecordCount": total,
            "KnownRecordCount": known_total,
            "SuccessCount": success,
            "FailureCount": failure,
            "UnknownCount": unknown,
            "SuccessRate": safe_rate(success, known_total),
            "FailureRate": safe_rate(failure, known_total),
            "UnknownRate": safe_rate(unknown, total),
            "WorkspaceOnly": True,
            "OriginalWrite": False,
            "FileDelete": False,
            "ExternalOperation": False,
            "RealGUIOperation": False,
            "RiskCount": 0,
            "SafeToContinue": True,
            "NextPhase": "Phase17-3 Mission Success Trend Analyzer",
            "updated_at": datetime.now().isoformat(),
        }

    OUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== Mission Success Statistics ===")
    for k, v in output.items():
        print(f"{k}: {v}")
    print(f"保存先: {OUT_PATH}")

if __name__ == "__main__":
    main()