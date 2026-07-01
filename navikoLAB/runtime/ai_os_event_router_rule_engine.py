# navikoLAB/runtime/ai_os_event_router_rule_engine.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json


PHASE = "Phase102-2 AI OS Event Router Rule Engine"

ROOT = Path(__file__).resolve().parents[2]

EVENT_FILE = ROOT / "runtime" / "bus" / "event_bus_state.json"
ROUTED_FILE = ROOT / "runtime" / "bus" / "event_routed_state.json"

ROUTE_LOG = ROOT / "runtime" / "bus"
ROUTE_LOG.mkdir(parents=True, exist_ok=True)


def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def route_event(event):

    payload = event.get("payload", "")

    # -----------------------------
    # RULE ENGINE (minimal)
    # -----------------------------
    if "goal" in payload.lower():
        route = "goal_execution"

    elif "error" in payload.lower():
        route = "recovery_execution"

    elif "backup" in payload.lower():
        route = "backup_execution"

    elif "audit" in payload.lower():
        route = "audit_execution"

    else:
        route = "default_execution"

    return {
        **event,
        "route": route,
        "status": "routed_by_rule_engine",
        "routed_at": datetime.now().isoformat(timespec="seconds"),
    }


def main():

    data = load_json(EVENT_FILE)

    if not data:
        print("missing event data")
        return

    events = data.get("events", [])

    routed_events = []

    for e in events:

        routed = route_event(e)
        routed_events.append(routed)

    result = {
        "phase": PHASE,
        "mode": "dry_run",
        "event_count": len(events),
        "routed_count": len(routed_events),
        "routes": {
            "goal": len([e for e in routed_events if e["route"] == "goal_execution"]),
            "recovery": len([e for e in routed_events if e["route"] == "recovery_execution"]),
            "backup": len([e for e in routed_events if e["route"] == "backup_execution"]),
            "audit": len([e for e in routed_events if e["route"] == "audit_execution"]),
            "default": len([e for e in routed_events if e["route"] == "default_execution"]),
        },
        "risk": 0,
        "safe": True,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }

    save_json(ROUTED_FILE, {"events": routed_events, "summary": result})

    print("=== AI OS Event Router Rule Engine ===")
    print("phase:", PHASE)
    print("event_count:", result["event_count"])
    print("routed_count:", result["routed_count"])
    print("routes:", result["routes"])
    print("risk:", 0)
    print("safe:", True)


if __name__ == "__main__":
    main()