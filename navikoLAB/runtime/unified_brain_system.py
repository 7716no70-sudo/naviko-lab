# navikoLAB/runtime/unified_brain_system.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import uuid
from datetime import datetime


PHASE = "Phase107-1 Naviko Unified Brain System (Dry Run Integration)"

ROOT = Path(__file__).resolve().parents[2]

BRAIN_DIR = ROOT / "runtime" / "unified_brain"
BRAIN_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = BRAIN_DIR / "brain_state.json"


# -----------------------------
# CORE INPUT STRUCTURE
# -----------------------------

@dataclass
class BrainInput:
    input_id: str
    text: str
    timestamp: str


@dataclass
class BrainOutput:
    input_id: str
    intent: str
    response: str
    used_llm: bool


# -----------------------------
# UNIFIED BRAIN SYSTEM
# -----------------------------

class UnifiedBrain:

    def __init__(self, llm_gateway, tool_gateway, scheduler):

        self.llm = llm_gateway
        self.tool = tool_gateway
        self.scheduler = scheduler

        self.memory: list[dict] = []

    # -----------------------------
    # INTENT DETECTION (LIGHT)
    # -----------------------------

    def detect_intent(self, text: str):

        t = text.lower()

        if any(x in t for x in ["こんにちは", "こんばんは", "hello"]):
            return "greeting"

        if "タスク" in t or "task" in t:
            return "task"

        if "宿題" in t or "やること" in t:
            return "schedule"

        if "状態" in t or "status" in t:
            return "status"

        return "general"

    # -----------------------------
    # MAIN PIPELINE
    # -----------------------------

    def process(self, text: str):

        input_obj = BrainInput(
            input_id=str(uuid.uuid4()),
            text=text,
            timestamp=datetime.now().isoformat(timespec="seconds"),
        )

        intent = self.detect_intent(text)

        # -------------------------
        # ROUTING LOGIC
        # -------------------------

        if intent == "task":

            response = "タスクをスケジューラに送信しました（dry_run）"
            used_llm = False

        elif intent == "schedule":

            tasks = self.scheduler.generate_daily_tasks()
            response = f"宿題を生成しました（{len(tasks)}件）"
            used_llm = False

        elif intent == "status":

            response = "Naviko OSはすべて正常動作中です"
            used_llm = False

        else:

            # LLM fallback
            response = self.llm.chat(text)
            used_llm = True

        output_obj = BrainOutput(
            input_id=input_obj.input_id,
            intent=intent,
            response=response,
            used_llm=used_llm,
        )

        self.memory.append({
            "input": input_obj.__dict__,
            "output": output_obj.__dict__,
        })

        return output_obj

    # -----------------------------
    # SAVE STATE
    # -----------------------------

    def save(self):

        STATE_FILE.write_text(
            json.dumps(self.memory, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# -----------------------------
# ENTRY POINT (DEMO)
# -----------------------------

def main():

    # lightweight mock injections (expected existing modules)
    from navikoLAB.runtime.llm_gateway import LLMGateway
    from navikoLAB.runtime.ai_task_scheduler import TaskScheduler
    from navikoLAB.runtime.tool_gateway import ToolGateway

    brain = UnifiedBrain(
        llm_gateway=LLMGateway(),
        tool_gateway=ToolGateway(),
        scheduler=TaskScheduler(),
    )

    print("=== Naviko Unified Brain System ===")
    print("phase:", PHASE)
    print("mode: dry_run")

    tests = [
        "ナビ子こんにちは",
        "今日のタスクを教えて",
        "宿題を作って",
        "状態は？",
        "雑談しよう",
    ]

    for t in tests:
        result = brain.process(t)
        print(f"[{result.intent}] {result.response} (LLM={result.used_llm})")

    brain.save()

    print("saved:", STATE_FILE)


if __name__ == "__main__":
    main()