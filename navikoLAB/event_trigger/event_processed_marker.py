import json
from pathlib import Path
from datetime import datetime


class EventProcessedMarker:
    def __init__(self):
        self.event_dir = Path("navikoLAB/event_trigger/events")
        self.log_dir = Path("navikoLAB/event_trigger/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def mark_processed(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        marked_events = []
        skipped_events = []

        for path in sorted(self.event_dir.glob("*.json")):
            try:
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)

                if data.get("status") == "pending" and data.get("safe") is True:
                    data["status"] = "processed"
                    data["processed_at"] = timestamp
                    data["processed_by"] = "Phase76-3 Event Processed Marker"

                    with path.open("w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)

                    marked_events.append(str(path))
                else:
                    skipped_events.append(str(path))

            except Exception as e:
                skipped_events.append({
                    "path": str(path),
                    "error": str(e),
                })

        result = {
            "status": "completed",
            "phase": "Phase76-3 Event Processed Marker",
            "timestamp": timestamp,
            "marked_count": len(marked_events),
            "skipped_count": len(skipped_events),
            "marked_events": marked_events,
            "skipped_events": skipped_events,
            "safe_to_continue": True,
        }

        log_path = self.log_dir / f"event_processed_marker_{timestamp}.json"

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["log_path"] = str(log_path)
        return result


if __name__ == "__main__":
    marker = EventProcessedMarker()
    report = marker.mark_processed()

    print("=== Event Processed Marker ===")
    for k, v in report.items():
        print(f"{k}: {v}")