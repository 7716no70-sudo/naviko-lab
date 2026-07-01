import json
from pathlib import Path
from datetime import datetime


class EventTriggerManager:
    def __init__(self):
        self.event_dir = Path("navikoLAB/event_trigger/events")
        self.log_dir = Path("navikoLAB/event_trigger/logs")

        self.event_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def scan_events(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        event_files = sorted(self.event_dir.glob("*.json"))

        events = []
        for path in event_files:
            try:
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)

                events.append({
                    "path": str(path),
                    "type": data.get("type", "unknown"),
                    "status": data.get("status", "pending"),
                    "safe": data.get("safe", False),
                })
            except Exception as e:
                events.append({
                    "path": str(path),
                    "type": "invalid_json",
                    "status": "error",
                    "safe": False,
                    "error": str(e),
                })

        safe_events = [
            e for e in events
            if e.get("status") == "pending" and e.get("safe") is True
        ]

        result = {
            "status": "completed",
            "phase": "Phase75-1 Event Trigger Manager",
            "timestamp": timestamp,
            "event_directory_exists": self.event_dir.exists(),
            "event_count": len(events),
            "safe_event_count": len(safe_events),
            "events": events,
            "trigger_allowed": len(safe_events) > 0,
            "safe_to_continue": True,
        }

        log_path = self.log_dir / f"event_trigger_manager_{timestamp}.json"

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["log_path"] = str(log_path)
        return result


if __name__ == "__main__":
    manager = EventTriggerManager()
    report = manager.scan_events()

    print("=== Event Trigger Manager ===")
    for k, v in report.items():
        print(f"{k}: {v}")