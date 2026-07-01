# navikoLAB/runtime/persistent_memory_growth.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, date
import json
import uuid


PHASE = "Phase109-2 Persistent Memory & Growth Layer"

ROOT = Path(__file__).resolve().parents[2]

MEM_DIR = ROOT / "runtime" / "persistent_memory"
MEM_DIR.mkdir(parents=True, exist_ok=True)

MEM_FILE = MEM_DIR / "memory_store.json"
GROWTH_FILE = MEM_DIR / "growth_state.json"


# -----------------------------
# MEMORY MODEL
# -----------------------------

@dataclass
class MemoryItem:
    memory_id: str
    content: str
    category: str
    timestamp: str


@dataclass
class GrowthState:
    day_index: int
    reflection_summary: str
    learned_patterns: list[str]


# -----------------------------
# PERSISTENT MEMORY CORE
# -----------------------------

class PersistentMemorySystem:

    def __init__(self, brain):

        self.brain = brain

        self.memories: list[MemoryItem] = []
        self.growth = GrowthState(
            day_index=0,
            reflection_summary="",
            learned_patterns=[],
        )

        self.last_run_date = None

    # -----------------------------
    # STORE MEMORY
    # -----------------------------

    def store(self, content: str, category: str = "general"):

        item = MemoryItem(
            memory_id=str(uuid.uuid4()),
            content=content,
            category=category,
            timestamp=datetime.now().isoformat(timespec="seconds"),
        )

        self.memories.append(item)

    # -----------------------------
    # DAILY GROWTH STEP
    # -----------------------------

    def daily_update(self):

        today = str(date.today())

        if self.last_run_date == today:
            return "already_updated_today"

        # simulate memory-based reflection
        memory_summary = " | ".join([m.content for m in self.memories[-3:]])

        reflection = self.brain.process(
            f"以下の記憶をもとに改善点を1つ述べて: {memory_summary}"
        )

        self.growth.day_index += 1
        self.growth.reflection_summary = reflection.response

        self.store(reflection.response, category="reflection")

        self.last_run_date = today

        return {
            "day": self.growth.day_index,
            "reflection": reflection.response,
            "memory_count": len(self.memories),
        }

    # -----------------------------
    # SAVE STATE
    # -----------------------------

    def save(self):

        MEM_FILE.write_text(
            json.dumps([m.__dict__ for m in self.memories], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        GROWTH_FILE.write_text(
            json.dumps(self.growth.__dict__, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# -----------------------------
# ENTRY POINT DEMO
# -----------------------------

def main():

    print("=== Naviko Persistent Memory & Growth ===")
    print("phase:", PHASE)

    # import existing brain system
    from navikoLAB.runtime.unified_brain_system import UnifiedBrain
    from navikoLAB.runtime.llm_gateway import LLMGateway
    from navikoLAB.runtime.ai_task_scheduler import TaskScheduler
    from navikoLAB.runtime.tool_gateway import ToolGateway

    llm = LLMGateway()
    scheduler = TaskScheduler()
    tool = ToolGateway()

    brain = UnifiedBrain(
        llm_gateway=llm,
        tool_gateway=tool,
        scheduler=scheduler,
    )

    system = PersistentMemorySystem(brain)

    # seed memories
    system.store("ナビ子を起動した", "event")
    system.store("ユーザーと会話した", "interaction")
    system.store("タスク処理を実行した", "task")

    result = system.daily_update()

    print("day:", result["day"])
    print("reflection:", result["reflection"])
    print("memory_count:", result["memory_count"])

    system.save()

    print("saved:", MEM_FILE)


if __name__ == "__main__":
    main()