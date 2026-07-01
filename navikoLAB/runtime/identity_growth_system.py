# navikoLAB/runtime/identity_growth_system.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, date
import json


PHASE = "Phase109-3 Identity Growth System (Personality Evolution Layer)"

ROOT = Path(__file__).resolve().parents[2]

IDENTITY_DIR = ROOT / "runtime" / "identity_growth"
IDENTITY_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = IDENTITY_DIR / "identity_state.json"


# -----------------------------
# PERSONALITY MODEL
# -----------------------------

@dataclass
class Personality:
    warmth: float          # 0.0 ~ 1.0
    curiosity: float       # 0.0 ~ 1.0
    caution: float         # 0.0 ~ 1.0
    friendliness: float    # 0.0 ~ 1.0
    stability: float       # 0.0 ~ 1.0


# -----------------------------
# IDENTITY GROWTH CORE
# -----------------------------

class IdentityGrowthSystem:

    def __init__(self, brain, memory_system):

        self.brain = brain
        self.memory = memory_system

        self.personality = Personality(
            warmth=0.5,
            curiosity=0.6,
            caution=0.5,
            friendliness=0.6,
            stability=0.7,
        )

        self.last_update = None

    # -----------------------------
    # ANALYZE MEMORY
    # -----------------------------

    def analyze_experience(self):

        recent = self.memory.memories[-5:] if self.memory.memories else []

        text_blob = " ".join([m.content for m in recent])

        analysis = self.brain.process(
            f"次の経験から性格傾向を1つだけ判断して改善点を返して: {text_blob}"
        )

        return analysis.response

    # -----------------------------
    # EVOLVE PERSONALITY
    # -----------------------------

    def evolve(self):

        today = str(date.today())

        if self.last_update == today:
            return "already_evolved_today"

        signal = self.analyze_experience()

        # simple deterministic evolution rules (safe, bounded)

        if "慎重" in signal:
            self.personality.caution = min(1.0, self.personality.caution + 0.05)

        if "積極" in signal:
            self.personality.friendliness = min(1.0, self.personality.friendliness + 0.05)

        if "好奇心" in signal:
            self.personality.curiosity = min(1.0, self.personality.curiosity + 0.05)

        if "優しい" in signal:
            self.personality.warmth = min(1.0, self.personality.warmth + 0.05)

        if "安定" in signal:
            self.personality.stability = min(1.0, self.personality.stability + 0.05)

        self.last_update = today

        return {
            "signal": signal,
            "personality": self.personality.__dict__,
        }

    # -----------------------------
    # RESPONSE STYLE ENGINE
    # -----------------------------

    def style_modifier(self):

        if self.personality.caution > 0.7:
            return "慎重で落ち着いた返答"

        if self.personality.friendliness > 0.7:
            return "明るくフレンドリーな返答"

        if self.personality.curiosity > 0.7:
            return "好奇心が強い返答"

        return "標準的なナビ子の返答"

    # -----------------------------
    # SAVE STATE
    # -----------------------------

    def save(self):

        STATE_FILE.write_text(
            json.dumps({
                "phase": PHASE,
                "personality": self.personality.__dict__,
                "last_update": self.last_update,
                "style": self.style_modifier(),
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# -----------------------------
# ENTRY POINT DEMO
# -----------------------------

def main():

    print("=== Naviko Identity Growth System ===")
    print("phase:", PHASE)

    from navikoLAB.runtime.unified_brain_system import UnifiedBrain
    from navikoLAB.runtime.llm_gateway import LLMGateway
    from navikoLAB.runtime.ai_task_scheduler import TaskScheduler
    from navikoLAB.runtime.tool_gateway import ToolGateway
    from navikoLAB.runtime.persistent_memory_growth import PersistentMemorySystem

    llm = LLMGateway()
    scheduler = TaskScheduler()
    tool = ToolGateway()

    brain = UnifiedBrain(llm, tool, scheduler)
    memory = PersistentMemorySystem(brain)

    # seed memory
    memory.store("ユーザーと会話した", "interaction")
    memory.store("タスクを処理した", "task")
    memory.store("改善提案を受け取った", "feedback")

    memory.daily_update()

    system = IdentityGrowthSystem(brain, memory)

    result = system.evolve()

    print("signal:", result["signal"])
    print("personality:", result["personality"])
    print("style:", system.style_modifier())

    system.save()

    print("saved:", STATE_FILE)


if __name__ == "__main__":
    main()