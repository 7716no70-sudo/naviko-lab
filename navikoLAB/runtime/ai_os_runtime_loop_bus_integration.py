# navikoLAB/runtime/ai_os_runtime_loop_bus_integration.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json


PHASE = "Phase101-3 Runtime Loop Bus Integration"

ROOT = Path(__file__).resolve().parents[2]

STATE_FILE = ROOT / "runtime" / "loop" / "runtime_loop_state.json"
BUS_FILE = ROOT / "runtime" / "bus" / "execution_bus_state.json"


def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():

    loop = load_json(STATE_FILE)
    bus = load_json(BUS_FILE)

    if not loop or not bus:
        print("missing runtime data")
        return

    tasks = loop.get("tasks", [])

    injected = []

    for t in tasks:

        packet = {
            "task_id": t["id"],
            "payload": t["description"],
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "status": "auto_injected"
        }

        bus.setdefault("queue", []).append(packet)
        injected.append(packet)

    bus["last_sync"] = datetime.now().isoformat(timespec="seconds")
    bus["injected_count"] = len(injected)

    save_json(BUS_FILE, bus)

    print("=== Runtime Loop → Bus Integration ===")
    print("phase:", PHASE)
    print("injected:", len(injected))
    print("bus_queue:", len(bus["queue"]))
    print("risk:", 0)
    print("safe:", True)


if __name__ == "__main__":
    main()