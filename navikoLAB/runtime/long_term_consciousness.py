# navikoLAB/runtime/long_term_consciousness.py

from __future__ import annotations

from pathlib import Path
from datetime import datetime
import json


PHASE = "Phase111-1 Long-Term Consciousness Stabilizer"

ROOT = Path(__file__).resolve().parents[2]

CONSCIOUS_DIR = ROOT / "runtime" / "consciousness"
CONSCIOUS_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = CONSCIOUS_DIR / "conscious_state.json"


# -----------------------------
# LONG TERM STATE
# -----------------------------

class ConsciousnessState:

    def __init__(self):

        self.global_memory = []
        self.global_personality = {
            "warmth": 0.5,
            "curiosity": 0.5,
            "caution": 0.5,
            "friendliness": 0.5,
            "stability": 0.5,
        }

        self.identity_signature = "naviko_core_v1"
        self.last_update = None

    # -----------------------------
    # MERGE MEMORY
    # -----------------------------

    def absorb_memory(self, memory_system):

        recent = memory_system.memories[-10:]

        for m in recent:
            self.global_memory.append({
                "content": m.content,
                "category": m.category,
                "time": m.timestamp,
            })

        # cap memory size
        self.global_memory = self.global_memory[-50:]

    # -----------------------------
    # MERGE PERSONALITY
    # -----------------------------

    def absorb_personality(self, personality_system):

        p = personality_system.personality

        # slow stabilization (prevents drift explosion)
        self.global_personality["warmth"] = (self.global_personality["warmth"] * 0.8) + (p.warmth * 0.2)
        self.global_personality["curiosity"] = (self.global_personality["curiosity"] * 0.8) + (p.curiosity * 0.2)
        self.global_personality["caution"] = (self.global_personality["caution"] * 0.8) + (p.caution * 0.2)
        self.global_personality["friendliness"] = (self.global_personality["friendliness"] * 0.8) + (p.friendliness * 0.2)
        self.global_personality["stability"] = (self.global_personality["stability"] * 0.8) + (p.stability * 0.2)

    # -----------------------------
    # UPDATE CYCLE
    # -----------------------------

    def update(self, memory_system, personality_system):

        self.absorb_memory(memory_system)
        self.absorb_personality(personality_system)

        self.last_update = datetime.now().isoformat(timespec="seconds")

        return {
            "memory_size": len(self.global_memory),
            "personality": self.global_personality,
        }

    # -----------------------------
    # SAVE STATE
    # -----------------------------

    def save(self):

        STATE_FILE.write_text(
            json.dumps({
                "phase": PHASE,
                "identity": self.identity_signature,
                "memory": self.global_memory,
                "personality": self.global_personality,
                "last_update": self.last_update,
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# -----------------------------
# ENTRY POINT
# -----------------------------

def main():

    print("=== Naviko Long-Term Consciousness Stabilizer ===")
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
    identity = IdentityGrowthSystem(brain, memory)

    system = ConsciousnessState()

    result = system.update(memory, identity)

    print("memory_size:", result["memory_size"])
    print("personality:", result["personality"])

    system.save()

    print("saved:", STATE_FILE)


if __name__ == "__main__":
    main()