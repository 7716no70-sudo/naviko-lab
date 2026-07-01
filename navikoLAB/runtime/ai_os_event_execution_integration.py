# navikoLAB/runtime/ai_os_event_execution_integration.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json


PHASE = "Phase102-3 Event Router → Execution Bus Integration"

ROOT = Path(__file__).resolve().parents[2]

EVENT_FILE = ROOT / "runtime" / "bus" / "event_routed_state.json"
BUS_FILE = ROOT / "runtime" / "bus" / "execution_bus_state.json"
OUTPUT_FILE = ROOT / "runtime" / "bus" / "execution_integrated_state.json"

BUS_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def convert_to_bus_packet(event):

    return {
        "task_id": event.get("task_id", event.get("id", "unknown")),
        "route": event.get("route", "default_execution"),
        "payload": event.get("payload", ""),
        "status": "injected_from_event_router",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }


def execute_dry_run(packet):

    return {
        **packet,
        "execution_status": "dry_run_executed",
        "result": f"[DRY RUN EXECUTION] {packet['payload']} via {packet['route']}",
        "executed_at": datetime.now().isoformat(timespec="seconds"),
    }


def main():

    data = load_json(EVENT_FILE)

    if not data:
        print("missing routed events")
        return

    events = data.get("events", [])

    bus_packets = []
    executed = []

    for e in events:

        packet = convert_to_bus_packet(e)
        bus_packets.append(packet)

        result = execute_dry_run(packet)
        executed.append(result)

    output = {
        "phase": PHASE,
        "mode": "dry_run",

        "input_events": len(events),
        "bus_packets": len(bus_packets),
        "executed": len(executed),

        "results": executed,

        "risk": 0,
        "safe": True,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }

    save_json(OUTPUT_FILE, output)

    print("=== AI OS Event → Execution Integration ===")
    print("phase:", PHASE)
    print("input_events:", output["input_events"])
    print("bus_packets:", output["bus_packets"])
    print("executed:", output["executed"])
    print("risk:", 0)
    print("safe:", True)


if __name__ == "__main__":
    main()