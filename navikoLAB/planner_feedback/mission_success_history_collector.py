from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"
OUT_PATH = WORKSPACE / "mission_success_history.json"

SOURCE_DIRS = [
    WORKSPACE / "mission_results",
    WORKSPACE / "feedback_loop",
]

def load_json_files(directory):
    if not directory.exists():
        return []

    records = []
    for path in directory.rglob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            records.append({
                "source_path": str(path),
                "data": data,
            })
        except Exception:
            continue

    return records

def extract_success_signal(data):
    if not isinstance(data, dict):
        return "unknown"

    for key in [
        "success",
        "Success",
        "MissionSuccess",
        "mission_success",
        "completed",
        "Completed",
        "status",
        "状態",
    ]:
        if key in data:
            value = data.get(key)
            if value is True:
                return "success"
            if value is False:
                return "failure"
            if isinstance(value, str):
                lower = value.lower()
                if lower in ["success", "completed", "passed"]:
                    return "success"
                if lower in ["failure", "failed", "error"]:
                    return "failure"

    return "unknown"

def main():
    WORKSPACE.mkdir(parents=True, exist_ok=True)

    collected = []
    for directory in SOURCE_DIRS:
        for item in load_json_files(directory):
            data = item["data"]

            collected.append({
                "source_path": item["source_path"],
                "success_signal": extract_success_signal(data),
                "planner": data.get("planner") or data.get("Planner"),
                "capability": data.get("capability") or data.get("Capability"),
                "connector": data.get("connector") or data.get("Connector"),
                "mission_id": data.get("mission_id") or data.get("MissionID"),
                "timestamp": data.get("timestamp") or data.get("created_at"),
            })

    success_count = sum(1 for r in collected if r["success_signal"] == "success")
    failure_count = sum(1 for r in collected if r["success_signal"] == "failure")
    unknown_count = sum(1 for r in collected if r["success_signal"] == "unknown")

    total_known = success_count + failure_count
    success_rate = success_count / total_known if total_known else 0.0

    output = {
        "status": "completed",
        "phase": "Phase17-1 Mission Success History Collector",
        "MissionSuccessHistoryCollected": True,
        "RecordCount": len(collected),
        "SuccessCount": success_count,
        "FailureCount": failure_count,
        "UnknownCount": unknown_count,
        "MissionSuccessRate": success_rate,
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "FileDelete": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "RiskCount": 0,
        "SafeToContinue": True,
        "NextPhase": "Phase17-2 Mission Success Statistics",
        "updated_at": datetime.now().isoformat(),
        "records": collected,
    }

    OUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== Mission Success History Collector ===")
    for key, value in output.items():
        if key != "records":
            print(f"{key}: {value}")
    print(f"保存先: {OUT_PATH}")

if __name__ == "__main__":
    main()