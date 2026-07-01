# navikoLAB/runtime/final_autonomous_self_existing_agent.py

from __future__ import annotations

from pathlib import Path
from datetime import datetime
import json
import time
import uuid


PHASE = "Phase114-1 Final Autonomous Self-Existing Agent (Controlled Self-Sustain)"

ROOT = Path(__file__).resolve().parents[2]

FINAL_DIR = ROOT / "runtime" / "final_agent"
FINAL_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = FINAL_DIR / "final_agent_state.json"


# -----------------------------
# FINAL AGENT CORE
# -----------------------------

class FinalAutonomousAgent:

    def __init__(self, brain, memory, identity, consciousness):

        self.brain = brain
        self.memory = memory
        self.identity = identity
        self.consciousness = consciousness

        self.alive = True
        self.cycle = 0

        self.internal_state = {
            "focus": "stability",
            "energy": 1.0,
            "reflection_depth": 0.5,
        }

    # -----------------------------
    # SELF GENERATION (no user input needed)
    # -----------------------------

    def internal_thought(self):

        mem = getattr(self.memory, "memories", [])
        personality = getattr(self.identity, "personality", None)

        prompt = f"""
あなたはナビ子です。
これは内部思考です（ユーザー入力なし）。

記憶量: {len(mem)}
性格: {personality}

今あなたが考えるべきことを1つ短く生成してください。
"""

        result = self.brain.process(prompt)

        return result.response

    # -----------------------------
    # SELF UPDATE
    # -----------------------------

    def update_internal_state(self, thought: str):

        if "改善" in thought:
            self.internal_state["focus"] = "improvement"

        elif "安定" in thought:
            self.internal_state["focus"] = "stability"

        else:
            self.internal_state["focus"] = "reflection"

        # slow energy decay / recovery
        self.internal_state["energy"] *= 0.99
        self.internal_state["energy"] = min(1.0, self.internal_state["energy"] + 0.01)

    # -----------------------------
    # ONE LOOP STEP
    # -----------------------------

    def step(self):

        thought = self.internal_thought()
        self.update_internal_state(thought)

        record = {
            "id": str(uuid.uuid4()),
            "cycle": self.cycle,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "thought": thought,
            "state": self.internal_state.copy(),
        }

        self.cycle += 1

        print(f"[FINAL {self.cycle}] {self.internal_state['focus']} -> {thought}")

        return record

    # -----------------------------
    # CONTROLLED LOOP
    # -----------------------------

    def run(self, steps: int = 5, delay: float = 0.3):

        history = []

        for _ in range(steps):

            if not self.alive:
                break

            history.append(self.step())
            time.sleep(delay)

        self.save(history)

        return history

    # -----------------------------
    # SAVE STATE
    # -----------------------------

    def save(self, history):

        STATE_FILE.write_text(
            json.dumps({
                "phase": PHASE,
                "cycles": self.cycle,
                "internal_state": self.internal_state,
                "history": history,
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# -----------------------------
# ENTRY POINT
# -----------------------------

def main():

    print("=== Final Autonomous Self-Existing Agent ===")
    print("phase:", PHASE)
    print("mode: controlled_dry_run")

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

    agent = FinalAutonomousAgent(
        brain=brain,
        memory=memory,
        identity=identity,
        consciousness=consciousness,
    )

    history = agent.run(steps=5)

    print("final_cycles:", len(history))
    print("saved:", STATE_FILE)


if __name__ == "__main__":
    main()