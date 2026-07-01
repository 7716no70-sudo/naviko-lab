# navikoLAB/runtime/unified_living_agent.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import json
import uuid


PHASE = "Phase109-4 Unified Living Agent (Final Integration Layer)"

ROOT = Path(__file__).resolve().parents[2]

LIVING_DIR = ROOT / "runtime" / "living_agent"
LIVING_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = LIVING_DIR / "living_agent_state.json"


# -----------------------------
# UNIFIED LIVING STATE
# -----------------------------

@dataclass
class LivingState:
    identity: dict
    personality: dict
    memory_summary: str
    last_thought: str
    last_action: str
    cycle: int


# -----------------------------
# UNIFIED LIVING AGENT
# -----------------------------

class UnifiedLivingAgent:

    def __init__(self, brain, memory_system, identity_system):

        self.brain = brain
        self.memory = memory_system
        self.identity = identity_system

        self.state = LivingState(
            identity={},
            personality={},
            memory_summary="",
            last_thought="",
            last_action="idle",
            cycle=0,
        )

    # -----------------------------
    # INTERNAL THOUGHT LOOP
    # -----------------------------

    def think(self):

        # memory context
        recent_memories = self.memory.memories[-5:] if self.memory.memories else []
        memory_text = " ".join([m.content for m in recent_memories])

        # identity + personality context
        personality = getattr(self.identity, "personality", None)

        prompt = f"""
あなたはナビ子です。
これまでの記憶: {memory_text}
現在の性格: {personality}

次に1つだけ短い思考をしてください。
"""

        result = self.brain.process(prompt)

        self.state.last_thought = result.response
        self.state.memory_summary = memory_text

        return result.response

    # -----------------------------
    # ACTION DECISION
    # -----------------------------

    def act(self, thought: str):

        if "タスク" in thought:
            action = "schedule_task"
        elif "改善" in thought:
            action = "update_memory"
        else:
            action = "reflect"

        self.state.last_action = action

        return action

    # -----------------------------
    # ONE LIVING CYCLE
    # -----------------------------

    def cycle_step(self):

        thought = self.think()
        action = self.act(thought)

        self.state.cycle += 1

        record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "thought": thought,
            "action": action,
            "cycle": self.state.cycle,
        }

        return record

    # -----------------------------
    # RUN LIVING PROCESS
    # -----------------------------

    def run(self, steps: int = 5):

        history = []

        for _ in range(steps):

            record = self.cycle_step()
            history.append(record)

            print(f"[LIVING {record['cycle']}] {record['action']}")

        self.save(history)

        return history

    # -----------------------------
    # SAVE STATE
    # -----------------------------

    def save(self, history):

        data = {
            "phase": PHASE,
            "state": self.state.__dict__,
            "history": history,
        }

        STATE_FILE.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# -----------------------------
# ENTRY POINT
# -----------------------------

def main():

    print("=== Naviko Unified Living Agent ===")
    print("phase:", PHASE)
    print("mode: dry_run")

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

    agent = UnifiedLivingAgent(brain, memory, identity)

    history = agent.run(steps=5)

    print("final_cycle:", len(history))
    print("saved:", STATE_FILE)


if __name__ == "__main__":
    main()