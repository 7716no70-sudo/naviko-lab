# navikoLAB/runtime/personality_drift_system.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, date
import json
import random


PHASE = "Phase110-1 Personality Drift System (Dynamic Identity Layer)"

ROOT = Path(__file__).resolve().parents[2]

DRIFT_DIR = ROOT / "runtime" / "personality_drift"
DRIFT_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = DRIFT_DIR / "personality_drift_state.json"


# -----------------------------
# BASE PERSONALITY MODEL
# -----------------------------

@dataclass
class Personality:
    warmth: float
    curiosity: float
    caution: float
    friendliness: float
    stability: float


# -----------------------------
# DRIFT ENGINE
# -----------------------------

class PersonalityDriftSystem:

    def __init__(self, identity_system, memory_system):

        self.identity = identity_system
        self.memory = memory_system

        self.base = Personality(
            warmth=0.5,
            curiosity=0.6,
            caution=0.5,
            friendliness=0.6,
            stability=0.7,
        )

        self.last_update = None

    # -----------------------------
    # DAILY DRIFT FACTOR
    # -----------------------------

    def drift_factor(self):

        # small random drift (controlled chaos)
        return random.uniform(-0.03, 0.03)

    # -----------------------------
    # MEMORY INFLUENCE
    # -----------------------------

    def memory_influence(self):

        recent = self.memory.memories[-5:] if self.memory.memories else []
        text = " ".join([m.content for m in recent])

        influence = {
            "warmth": 0,
            "curiosity": 0,
            "caution": 0,
            "friendliness": 0,
            "stability": 0,
        }

        if "失敗" in text:
            influence["caution"] += 0.02

        if "成功" in text:
            influence["friendliness"] += 0.02

        if "学習" in text:
            influence["curiosity"] += 0.02

        return influence

    # -----------------------------
    # APPLY DRIFT
    # -----------------------------

    def apply_drift(self):

        today = str(date.today())

        if self.last_update == today:
            return "already_drifted_today"

        influence = self.memory_influence()

        drift = self.drift_factor()

        # apply drift
        self.base.warmth = self.clamp(self.base.warmth + drift + influence["warmth"])
        self.base.curiosity = self.clamp(self.base.curiosity + drift + influence["curiosity"])
        self.base.caution = self.clamp(self.base.caution + drift + influence["caution"])
        self.base.friendliness = self.clamp(self.base.friendliness + drift + influence["friendliness"])
        self.base.stability = self.clamp(self.base.stability + drift + influence["stability"])

        self.last_update = today

        return {
            "drift": drift,
            "personality": self.base.__dict__,
        }

    # -----------------------------
    # SAFETY CLAMP
    # -----------------------------

    def clamp(self, value: float):

        return max(0.0, min(1.0, value))

    # -----------------------------
    # STYLE OUTPUT
    # -----------------------------

    def style(self):

        p = self.base

        if p.caution > 0.7:
            return "慎重モード"

        if p.friendliness > 0.7:
            return "親しみモード"

        if p.curiosity > 0.7:
            return "探索モード"

        return "標準モード"

    # -----------------------------
    # SAVE
    # -----------------------------

    def save(self):

        STATE_FILE.write_text(
            json.dumps({
                "phase": PHASE,
                "personality": self.base.__dict__,
                "style": self.style(),
                "last_update": self.last_update,
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# -----------------------------
# ENTRY POINT
# -----------------------------

def main():

    print("=== Naviko Personality Drift System ===")
    print("phase:", PHASE)

    from navikoLAB.runtime.unified_brain_system import UnifiedBrain
    from navikoLAB.runtime.llm_gateway import LLMGateway
    from navikoLAB.runtime.ai_task_scheduler import TaskScheduler
    from navikoLAB.runtime.tool_gateway import ToolGateway
    from navikoLAB.runtime.persistent_memory_growth import PersistentMemorySystem
    from navikoLAB.runtime.identity_growth_system import IdentityGrowthSystem

    llm = LLMGateway()
    scheduler = TaskScheduler()
    tool = ToolGateway()

    brain = UnifiedBrain(llm, tool, scheduler)

    memory = PersistentMemorySystem(brain)
    identity = IdentityGrowthSystem(brain, memory)

    drift = PersonalityDriftSystem(identity, memory)

    result = drift.apply_drift()

    print("drift:", result["drift"])
    print("personality:", result["personality"])
    print("style:", drift.style())

    drift.save()

    print("saved:", STATE_FILE)


if __name__ == "__main__":
    main()