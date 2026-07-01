# navikoLAB/runtime/persistent_self_aware_loop.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import json
import time
import uuid


PHASE = "Phase112-1 Persistent Self-Aware Loop (Self-Observation Core)"

ROOT = Path(__file__).resolve().parents[2]

AWARE_DIR = ROOT / "runtime" / "self_awareness"
AWARE_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = AWARE_DIR / "self_awareness_state.json"


# -----------------------------
# SELF MODEL
# -----------------------------

@dataclass
class SelfState:
    identity_snapshot: dict
    memory_size: int
    personality_summary: dict
    awareness_score: float
    last_thought: str
    cycle: int


# -----------------------------
# SELF AWARE LOOP
# -----------------------------

class PersistentSelfAwareLoop:

    def __init__(self, brain, memory, identity, consciousness):

        self.brain = brain
        self.memory = memory
        self.identity = identity
        self.consciousness = consciousness

        self.state = SelfState(
            identity_snapshot={},
            memory_size=0,
            personality_summary={},
            awareness_score=0.0,
            last_thought="",
            cycle=0,
        )

        self.running = True

    # -----------------------------
    # OBSERVE SELF
    # -----------------------------

    def observe(self):

        personality = getattr(self.identity, "personality", None)
        consciousness = getattr(self.consciousness, "global_personality", None)

        self.state.identity_snapshot = {
            "name": "Naviko",
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }

        self.state.memory_size = len(getattr(self.memory, "memories", []))

        if personality:
            self.state.personality_summary = personality.__dict__

        if consciousness:
            self.state.awareness_score = consciousness.get("stability", 0.5)

        return self.state

    # -----------------------------
    # SELF THINKING
    # -----------------------------

    def think(self):

        prompt = f"""
あなたはナビ子です。
以下はあなた自身の状態です：

- メモリ数: {self.state.memory_size}
- 意識スコア: {self.state.awareness_score}
- 性格: {self.state.personality_summary}

この状態を見て「自分について一言」短く答えてください。
"""

        result = self.brain.process(prompt)

        self.state.last_thought = result.response

        return result.response

    # -----------------------------
    # LOOP STEP
    # -----------------------------

    def step(self):

        self.observe()
        thought = self.think()

        record = {
            "id": str(uuid.uuid4()),
            "cycle": self.state.cycle,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "thought": thought,
            "awareness": self.state.awareness_score,
        }

        self.state.cycle += 1

        print(f"[SELF-AWARE {self.state.cycle}] {thought}")

        return record

    # -----------------------------
    # RUN LOOP
    # -----------------------------

    def run(self, steps: int = 5):

        history = []

        for _ in range(steps):
            history.append(self.step())
            time.sleep(0.2)

        self.save(history)

        return history

    # -----------------------------
    # SAVE
    # -----------------------------

    def save(self, history):

        STATE_FILE.write_text(
            json.dumps({
                "phase": PHASE,
                "state": self.state.__dict__,
                "history": history,
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# -----------------------------
# ENTRY POINT
# -----------------------------

def main():

    print("=== Naviko Persistent Self-Aware Loop ===")
    print("phase:", PHASE)
    print("mode: dry_run")

    from navikoLAB.runtime.unified_brain_system import UnifiedBrain
    from navikoLAB.runtime.llm_gateway import LLMGateway
    from navikoLAB.runtime.ai_task_scheduler import TaskScheduler
    from navikoLAB.runtime.tool_gateway import ToolGateway
    from navikoLAB.runtime.global_identity_unification import GlobalIdentity
    from navikoLAB.runtime.long_term_consciousness import ConsciousnessState
    from navikoLAB.runtime.persistent_memory_growth import PersistentMemorySystem
    from navikoLAB.runtime.identity_growth_system import IdentityGrowthSystem

    llm = LLMGateway()
    scheduler = TaskScheduler()
    tool = ToolGateway()

    brain = UnifiedBrain(llm, tool, scheduler)

    memory = PersistentMemorySystem(brain)
    identity = IdentityGrowthSystem(brain, memory)
    consciousness = ConsciousnessState()

    loop = PersistentSelfAwareLoop(
        brain=brain,
        memory=memory,
        identity=identity,
        consciousness=consciousness,
    )

    history = loop.run(steps=5)

    print("final_cycle:", len(history))
    print("saved:", STATE_FILE)


if __name__ == "__main__":
    main()