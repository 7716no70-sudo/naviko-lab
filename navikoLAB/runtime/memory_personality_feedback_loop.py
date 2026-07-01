# navikoLAB/runtime/memory_personality_feedback_loop.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import json
import uuid
import random


PHASE = "Phase110-2 Memory × Personality Feedback Loop (Bidirectional Identity)"

ROOT = Path(__file__).resolve().parents[2]

FEEDBACK_DIR = ROOT / "runtime" / "feedback_loop"
FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = FEEDBACK_DIR / "feedback_state.json"


# -----------------------------
# FEEDBACK STATE MODEL
# -----------------------------

@dataclass
class FeedbackEvent:
    event_id: str
    type: str
    content: str
    timestamp: str


# -----------------------------
# FEEDBACK LOOP CORE
# -----------------------------

class MemoryPersonalityFeedbackLoop:

    def __init__(self, memory_system, personality_system):

        self.memory = memory_system
        self.personality = personality_system

        self.events: list[FeedbackEvent] = []
        self.last_sync = None

    # -----------------------------
    # MEMORY → PERSONALITY SIGNAL
    # -----------------------------

    def memory_to_personality_signal(self):

        recent = self.memory.memories[-5:] if self.memory.memories else []
        text = " ".join([m.content for m in recent])

        signal = {
            "increase_caution": 0.0,
            "increase_curiosity": 0.0,
            "increase_friendliness": 0.0,
            "increase_warmth": 0.0,
        }

        # simple pattern extraction (safe heuristic layer)
        if "失敗" in text or "エラー" in text:
            signal["increase_caution"] += 0.03

        if "学習" in text or "改善" in text:
            signal["increase_curiosity"] += 0.03

        if "成功" in text:
            signal["increase_friendliness"] += 0.02

        if "会話" in text:
            signal["increase_warmth"] += 0.02

        return signal

    # -----------------------------
    # PERSONALITY → MEMORY FILTER BIAS
    # -----------------------------

    def personality_bias(self):

        p = getattr(self.personality, "personality", None)

        if not p:
            return "neutral"

        if p.caution > 0.7:
            return "risk_sensitive_memory"

        if p.curiosity > 0.7:
            return "exploration_focused_memory"

        if p.friendliness > 0.7:
            return "social_memory_priority"

        return "balanced_memory"

    # -----------------------------
    # APPLY FEEDBACK LOOP
    # -----------------------------

    def step(self):

        signal = self.memory_to_personality_signal()
        bias = self.personality_bias()

        # inject randomness (controlled drift)
        noise = random.uniform(-0.01, 0.01)

        # apply to personality system safely
        self.personality.personality.caution = self._clamp(
            self.personality.personality.caution + signal["increase_caution"] + noise
        )

        self.personality.personality.curiosity = self._clamp(
            self.personality.personality.curiosity + signal["increase_curiosity"] + noise
        )

        self.personality.personality.friendliness = self._clamp(
            self.personality.personality.friendliness + signal["increase_friendliness"] + noise
        )

        self.personality.personality.warmth = self._clamp(
            self.personality.personality.warmth + signal["increase_warmth"] + noise
        )

        event = FeedbackEvent(
            event_id=str(uuid.uuid4()),
            type="feedback_cycle",
            content=f"bias={bias}, signal={signal}",
            timestamp=datetime.now().isoformat(timespec="seconds"),
        )

        self.events.append(event)

        self.last_sync = datetime.now().isoformat(timespec="seconds")

        print(f"[FEEDBACK] {bias}")

        return event

    # -----------------------------
    # SAFETY CLAMP
    # -----------------------------

    def _clamp(self, v: float):

        return max(0.0, min(1.0, v))

    # -----------------------------
    # RUN LOOP
    # -----------------------------

    def run(self, steps: int = 5):

        history = []

        for _ in range(steps):
            history.append(self.step())

        self.save(history)

        return history

    # -----------------------------
    # SAVE STATE
    # -----------------------------

    def save(self, history):

        STATE_FILE.write_text(
            json.dumps({
                "phase": PHASE,
                "events": [e.__dict__ for e in self.events],
                "history": [h.__dict__ for h in history],
                "last_sync": self.last_sync,
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# -----------------------------
# ENTRY POINT
# -----------------------------

def main():

    print("=== Naviko Memory × Personality Feedback Loop ===")
    print("phase:", PHASE)

    from navikoLAB.runtime.persistent_memory_growth import PersistentMemorySystem
    from navikoLAB.runtime.identity_growth_system import IdentityGrowthSystem
    from navikoLAB.runtime.llm_gateway import LLMGateway
    from navikoLAB.runtime.ai_task_scheduler import TaskScheduler
    from navikoLAB.runtime.tool_gateway import ToolGateway
    from navikoLAB.runtime.unified_brain_system import UnifiedBrain

    llm = LLMGateway()
    scheduler = TaskScheduler()
    tool = ToolGateway()

    brain = UnifiedBrain(llm, tool, scheduler)

    memory = PersistentMemorySystem(brain)
    personality = IdentityGrowthSystem(brain, memory)

    # seed memory
    memory.store("会話が成功した", "interaction")
    memory.store("改善を行った", "learning")
    memory.store("軽いエラーが発生した", "system")

    loop = MemoryPersonalityFeedbackLoop(memory, personality)

    result = loop.run(steps=5)

    print("cycles:", len(result))
    print("saved:", STATE_FILE)


if __name__ == "__main__":
    main()