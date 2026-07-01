# navikoLAB/runtime/ai_os_evolution_kernel.py

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json
import uuid


PHASE = "Phase106-0 Naviko Evolution Kernel"

ROOT = Path(__file__).resolve().parents[2]

EVOLUTION_DIR = ROOT / "runtime" / "evolution"
EVOLUTION_DIR.mkdir(parents=True, exist_ok=True)

REGISTRY_FILE = EVOLUTION_DIR / "module_registry.json"
LOG_FILE = EVOLUTION_DIR / "evolution_log.json"


# -----------------------------
# Core Evolution Structures
# -----------------------------

@dataclass
class Module:
    module_id: str
    name: str
    enabled: bool
    description: str


@dataclass
class EvolutionEvent:
    event_id: str
    module_id: str
    action: str
    result: str
    timestamp: str


# -----------------------------
# Evolution Kernel
# -----------------------------

class EvolutionKernel:

    def __init__(self):

        self.modules: list[Module] = []
        self.history: list[EvolutionEvent] = []

        self.load_or_init()

    # -----------------------------
    # Module Registry
    # -----------------------------

    def load_or_init(self):

        if REGISTRY_FILE.exists():
            data = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
            self.modules = [Module(**m) for m in data.get("modules", [])]
        else:
            self.modules = [
                Module("scheduler", "Task Scheduler", True, "daily task generator"),
                Module("tool_gateway", "Tool Gateway", False, "external operations interface"),
                Module("media_identity", "Media Identity", False, "avatar / voice / 3D"),
                Module("ui_layer", "UI Layer", False, "UI and voice interface"),
            ]
            self.save_registry()

    def save_registry(self):

        data = {
            "phase": PHASE,
            "modules": [asdict(m) for m in self.modules],
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }

        REGISTRY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # -----------------------------
    # Evolution Operations
    # -----------------------------

    def enable_module(self, module_id: str):

        for m in self.modules:
            if m.module_id == module_id:
                m.enabled = True

                self.record_event(m.module_id, "enable", "success")

        self.save_registry()

    def disable_module(self, module_id: str):

        for m in self.modules:
            if m.module_id == module_id:
                m.enabled = False

                self.record_event(m.module_id, "disable", "success")

        self.save_registry()

    def record_event(self, module_id: str, action: str, result: str):

        event = EvolutionEvent(
            event_id=str(uuid.uuid4()),
            module_id=module_id,
            action=action,
            result=result,
            timestamp=datetime.now().isoformat(timespec="seconds"),
        )

        self.history.append(event)

    # -----------------------------
    # Learning Summary
    # -----------------------------

    def summary(self):

        return {
            "phase": PHASE,
            "modules_total": len(self.modules),
            "enabled": len([m for m in self.modules if m.enabled]),
            "disabled": len([m for m in self.modules if not m.enabled]),
            "events": len(self.history),
        }

    # -----------------------------
    # Save Logs
    # -----------------------------

    def save_logs(self):

        data = {
            "phase": PHASE,
            "history": [asdict(e) for e in self.history],
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }

        LOG_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# -----------------------------
# Entry Point
# -----------------------------

def main():

    kernel = EvolutionKernel()

    # --- initial evolution simulation ---
    kernel.enable_module("tool_gateway")
    kernel.enable_module("media_identity")
    kernel.disable_module("ui_layer")

    kernel.save_logs()

    summary = kernel.summary()

    print("=== Naviko Evolution Kernel ===")
    print("phase:", PHASE)
    print("summary:", summary)
    print("registry:", REGISTRY_FILE)
    print("log:", LOG_FILE)


if __name__ == "__main__":
    main()