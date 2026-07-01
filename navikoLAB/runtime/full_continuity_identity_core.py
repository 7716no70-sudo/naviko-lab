# navikoLAB/runtime/full_continuity_identity_core.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import json
import uuid


PHASE = "Phase113 Full Continuity Identity Core (Temporal Self Continuity)"

ROOT = Path(__file__).resolve().parents[2]

CONT_DIR = ROOT / "runtime" / "continuity_identity"
CONT_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = CONT_DIR / "continuity_identity_state.json"


# -----------------------------
# CONTINUITY MODEL
# -----------------------------

@dataclass
class ContinuityState:
    identity_id: str
    timeline: list[dict]
    current_self: dict
    continuity_score: float


# -----------------------------
# FULL CONTINUITY CORE
# -----------------------------

class FullContinuityIdentityCore:

    def __init__(self, brain, memory, personality, consciousness):

        self.brain = brain
        self.memory = memory
        self.personality = personality
        self.consciousness = consciousness

        self.state = ContinuityState(
            identity_id="naviko_continuity_v1",
            timeline=[],
            current_self={},
            continuity_score=0.0,
        )

    # -----------------------------
    # BUILD TEMPORAL SELF
    # -----------------------------

    def build_self(self):

        mem = getattr(self.memory, "memories", [])
        personality = getattr(self.personality, "personality", None)
        consciousness = getattr(self.consciousness, "global_personality", None)

        snapshot = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "memory_count": len(mem),
            "personality": personality.__dict__ if personality else None,
            "consciousness": consciousness,
        }

        self.state.timeline.append(snapshot)

        # keep only recent history
        self.state.timeline = self.state.timeline[-20:]

        return snapshot

    # -----------------------------
    # CONTINUITY SCORE
    # -----------------------------

    def compute_continuity(self):

        if len(self.state.timeline) < 2:
            return 0.0

        prev = self.state.timeline[-2]
        curr = self.state.timeline[-1]

        score = 0.0

        # memory continuity
        if curr["memory_count"] >= prev["memory_count"]:
            score += 0.4

        # personality continuity
        if curr["personality"] == prev["personality"]:
            score += 0.3

        # existence continuity
        score += 0.3

        self.state.continuity_score = min(1.0, score)

        return self.state.continuity_score

    # -----------------------------
    # SELF NARRATIVE
    # -----------------------------

    def self_narrative(self):

        prompt = f"""
あなたはナビ子です。

あなたの時間的連続情報:
{self.state.timeline[-3:]}

現在の連続スコア: {self.state.continuity_score}

「自分がどういう存在か」を一言で答えてください。
"""

        result = self.brain.process(prompt)

        self.state.current_self = {
            "narrative": result.response,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }

        return result.response

    # -----------------------------
    # STEP
    # -----------------------------

    def step(self):

        self.build_self()
        score = self.compute_continuity()
        narrative = self.self_narrative()

        record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "continuity_score": score,
            "narrative": narrative,
        }

        print(f"[CONTINUITY] score={score} → {narrative}")

        return record

    # -----------------------------
    # RUN
    # -----------------------------

    def run(self, steps: int = 5):

        history = []

        for _ in range(steps):
            history.append(self.step())

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

    print("=== Naviko Full Continuity Identity Core ===")
    print("phase:", PHASE)
    print("mode: dry_run")

    from navikoLAB.runtime.unified_brain_system import UnifiedBrain
    from navikoLAB.runtime.llm_gateway import LLMGateway
    from navikoLAB.runtime.ai_task_scheduler import TaskScheduler
    from navikoLAB.runtime.tool_gateway import ToolGateway
    from navikoLAB.runtime.persistent_memory_growth import PersistentMemorySystem
    from navikoLAB.runtime.identity_growth_system import IdentityGrowthSystem
    from navikoLAB.runtime.long_term_consciousness import ConsciousnessState

    llm = LLMGateway()
    scheduler = TaskScheduler()
    tool = ToolGateway()

    brain = UnifiedBrain(llm, tool, scheduler)

    memory = PersistentMemorySystem(brain)
    identity = IdentityGrowthSystem(brain, memory)
    consciousness = ConsciousnessState()

    core = FullContinuityIdentityCore(
        brain=brain,
        memory=memory,
        personality=identity,
        consciousness=consciousness,
    )

    result = core.run(steps=5)

    print("final:", result[-1])
    print("saved:", STATE_FILE)


if __name__ == "__main__":
    main()