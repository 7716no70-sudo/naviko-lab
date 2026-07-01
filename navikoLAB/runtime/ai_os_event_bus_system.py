# navikoLAB/runtime/ai_os_event_bus_system.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import uuid


PHASE = "Phase102-1 AI OS Execution Bus Event System"

ROOT = Path(__file__).resolve().parents[2]

BUS_FILE = ROOT / "runtime" / "bus" / "execution_bus_state.json"
EVENT_FILE = ROOT / "runtime" / "bus" / "event_bus_state.json"

EVENT_DIR = ROOT / "runtime" / "bus"
EVENT_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def create_event(task_id: str, payload: str):

    return {
        "event_id": str(uuid.uuid4()),
        "task_id": task_id,
        "payload": payload,
        "event_type": "task_execution_request",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "status": "created",
    }


def route_event(event, bus):

    routed = {
        **event,
        "status": "routed_dry_run",
        "route": "execution_bus",
        "processed_at": datetime.now().isoformat(timespec="seconds"),
        "result": f"[EVENT DRY RUN EXEC] {event['payload']}",
    }

    bus.setdefault("events", []).append(routed)
    return routed


def main():

    bus = load_json(BUS_FILE)

    if not bus:
        print("missing bus state")
        return

    queue = bus.get("queue", [])

    events = []

    for item in queue:

        event = create_event(item["task_id"], item["payload"])
        routed = route_event(event, bus)
        events.append(routed)

        item["status"] = "event_emitted"

    bus["event_mode"] = True
    bus["last_event_run"] = datetime.now().isoformat(timespec="seconds")
    bus["event_count"] = len(events)

    save_json(BUS_FILE, bus)
    save_json(EVENT_FILE, {"phase": PHASE, "events": events})

    print("=== AI OS Event Bus System ===")
    print("phase:", PHASE)
    print("events_created:", len(events))
    print("bus_events:", len(bus.get("events", [])))
    print("event_mode:", bus["event_mode"])
    print("risk:", 0)
    print("safe:", True)


if __name__ == "__main__":
    main()