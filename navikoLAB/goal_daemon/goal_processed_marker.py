import json
from pathlib import Path
from datetime import datetime


class GoalProcessedMarker:
    def __init__(self):
        self.goal_dir = Path("navikoLAB/goal_daemon/goals")
        self.log_dir = Path("navikoLAB/goal_daemon/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def mark_processed(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        marked_goals = []
        skipped_goals = []

        for path in sorted(self.goal_dir.glob("*.json")):
            try:
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)

                if data.get("status") == "pending" and data.get("safe") is True:
                    data["status"] = "processed"
                    data["processed_at"] = timestamp
                    data["processed_by"] = "Phase78-4 Goal Processed Marker"

                    with path.open("w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)

                    marked_goals.append(str(path))
                else:
                    skipped_goals.append(str(path))

            except Exception as e:
                skipped_goals.append({
                    "path": str(path),
                    "error": str(e),
                })

        result = {
            "status": "completed",
            "phase": "Phase78-4 Goal Processed Marker",
            "timestamp": timestamp,
            "marked_count": len(marked_goals),
            "skipped_count": len(skipped_goals),
            "marked_goals": marked_goals,
            "skipped_goals": skipped_goals,
            "safe_to_continue": True,
        }

        log_path = self.log_dir / f"goal_processed_marker_{timestamp}.json"

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["log_path"] = str(log_path)
        return result


if __name__ == "__main__":
    marker = GoalProcessedMarker()
    report = marker.mark_processed()

    print("=== Goal Processed Marker ===")
    for k, v in report.items():
        print(f"{k}: {v}")