# navikoLAB/runtime/naviko_full_integrated_system.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import json
import uuid


PHASE = "Phase107-2 Naviko FULL INTEGRATED SYSTEM"

ROOT = Path(__file__).resolve().parents[2]

FULL_DIR = ROOT / "runtime" / "full_system"
FULL_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = FULL_DIR / "naviko_full_state.json"


# -----------------------------
# FULL SYSTEM CORE
# -----------------------------

class NavikoFullSystem:

    def __init__(self, brain, ui, identity, tool, scheduler, llm):

        self.brain = brain
        self.ui = ui
        self.identity = identity
        self.tool = tool
        self.scheduler = scheduler
        self.llm = llm

        self.history = []

    # -----------------------------
    # SINGLE ENTRY POINT
    # -----------------------------

    def run(self, user_input: str):

        timestamp = datetime.now().isoformat(timespec="seconds")

        # 1. identity context injection
        identity = getattr(self.identity, "identity", None)

        # 2. brain processing
        brain_output = self.brain.process(user_input)

        # 3. tool execution simulation (if needed)
        tool_result = None

        if brain_output.intent == "task":

            tool_result = self.tool.log_note("task routed from full system")

        # 4. UI sync (state update simulation)
        ui_state = {
            "last_input": user_input,
            "last_output": brain_output.response,
        }

        # 5. log aggregation
        record = {
            "id": str(uuid.uuid4()),
            "timestamp": timestamp,
            "input": user_input,
            "intent": brain_output.intent,
            "response": brain_output.response,
            "used_llm": brain_output.used_llm,
            "tool_result": str(tool_result),
            "identity": str(identity),
            "ui_state": ui_state,
        }

        self.history.append(record)

        return record

    # -----------------------------
    # SAVE STATE
    # -----------------------------

    def save(self):

        STATE_FILE.write_text(
            json.dumps(self.history, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# -----------------------------
# ENTRY POINT DEMO
# -----------------------------

def main():

    print("=== Naviko FULL INTEGRATED SYSTEM ===")
    print("phase:", PHASE)
    print("mode: dry_run")

    # lazy imports (avoid circular dependency issues)
    from navikoLAB.runtime.unified_brain_system import UnifiedBrain
    from navikoLAB.runtime.llm_gateway import LLMGateway
    from navikoLAB.runtime.ai_task_scheduler import TaskScheduler
    from navikoLAB.runtime.tool_gateway import ToolGateway
    from navikoLAB.runtime.media_identity_layer import MediaIdentityLayer
    from navikoLAB.runtime.ui_layer import NavikoUI

    # initialize subsystems
    llm = LLMGateway()
    scheduler = TaskScheduler()
    tool = ToolGateway()
    identity = MediaIdentityLayer()

    # UI is optional (not launched automatically)
    ui = None

    brain = UnifiedBrain(
        llm_gateway=llm,
        tool_gateway=tool,
        scheduler=scheduler,
    )

    system = NavikoFullSystem(
        brain=brain,
        ui=ui,
        identity=identity,
        tool=tool,
        scheduler=scheduler,
        llm=llm,
    )

    # test runs
    inputs = [
        "ナビ子こんにちは",
        "タスクを実行して",
        "宿題を作って",
        "調子はどう？",
        "雑談しよう",
    ]

    for i in inputs:
        result = system.run(i)
        print(f"[{result['intent']}] {result['response']}")

    system.save()

    print("saved:", STATE_FILE)


if __name__ == "__main__":
    main()