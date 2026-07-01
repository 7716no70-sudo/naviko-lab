import json
from pathlib import Path
from datetime import datetime


class EventTestGenerator:
    def __init__(self):
        self.event_dir = Path("navikoLAB/event_trigger/events")
        self.log_dir = Path("navikoLAB/event_trigger/logs")
        self.event_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def generate(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        event = {
            "type": "daemon",
            "status": "pending",
            "safe": True,
            "mode": "dry_run",
            "created_at": timestamp,
            "description": "Phase76 safe daemon trigger test event",
            "external_operation_allowed": False,
            "original_write_allowed": False,
            "file_delete_allowed": False,
        }

        event_path = self.event_dir / f"safe_daemon_test_event_{timestamp}.json"

        with event_path.open("w", encoding="utf-8") as f:
            json.dump(event, f, ensure_ascii=False, indent=2)

        result = {
            "status": "completed",
            "phase": "Phase76-1 Event Test Generator",
            "timestamp": timestamp,
            "test_event_created": True,
            "event_path": str(event_path),
            "event_type": event["type"],
            "event_safe": event["safe"],
            "safe_to_continue": True,
        }

        log_path = self.log_dir / f"event_test_generator_{timestamp}.json"

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["log_path"] = str(log_path)
        return result


if __name__ == "__main__":
    generator = EventTestGenerator()
    report = generator.generate()

    print("=== Event Test Generator ===")
    for k, v in report.items():
        print(f"{k}: {v}")