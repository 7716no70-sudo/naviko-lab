# navikoLAB/runtime/global_identity_unification.py

from __future__ import annotations

from pathlib import Path
from datetime import datetime
import json


PHASE = "Phase111-2 Global Identity Unification Layer (Final Identity Merge)"

ROOT = Path(__file__).resolve().parents[2]

UNIFY_DIR = ROOT / "runtime" / "global_identity"
UNIFY_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = UNIFY_DIR / "global_identity_state.json"


# -----------------------------
# GLOBAL IDENTITY CORE
# -----------------------------

class GlobalIdentity:

    def __init__(self, brain, memory, identity, personality, consciousness):

        self.brain = brain
        self.memory = memory
        self.identity = identity
        self.personality = personality
        self.consciousness = consciousness

        self.global_self = {
            "name": "Naviko",
            "coherence": 0.0,
            "stability": 0.0,
            "awareness": 0.0,
        }

    # -----------------------------
    # UNIFY ALL LAYERS
    # -----------------------------

    def unify(self):

        mem_size = len(getattr(self.memory, "memories", []))
        personality = getattr(self.personality, "personality", None)
        consciousness = getattr(self.consciousness, "global_personality", None)

        # coherence = how well everything aligns
        self.global_self["coherence"] = min(1.0, mem_size / 20)

        # stability derived from consciousness layer
        if consciousness:
            self.global_self["stability"] = consciousness.get("stability", 0.5)

        # awareness derived from identity + personality consistency
        if personality:
            avg_personality = (
                personality.warmth +
                personality.curiosity +
                personality.caution +
                personality.friendliness +
                personality.stability
            ) / 5

            self.global_self["awareness"] = avg_personality

        return self.global_self

    # -----------------------------
    # IDENTITY RESPONSE ENGINE
    # -----------------------------

    def respond(self, user_input: str):

        context = f"""
あなたは統合されたナビ子です。

現在の自己状態:
{self.global_self}

ユーザー入力:
{user_input}

短く自然に返答してください。
"""

        result = self.brain.process(context)

        return result.response

    # -----------------------------
    # SAVE STATE
    # -----------------------------

    def save(self):

        STATE_FILE.write_text(
            json.dumps({
                "phase": PHASE,
                "global_identity": self.global_self,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# -----------------------------
# ENTRY POINT
# -----------------------------

def main():

    print("=== Naviko Global Identity Unification ===")
    print("phase:", PHASE)

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

    global_ai = GlobalIdentity(brain, memory, identity, identity, consciousness)

    unified_state = global_ai.unify()

    print("coherence:", unified_state["coherence"])
    print("stability:", unified_state["stability"])
    print("awareness:", unified_state["awareness"])

    response = global_ai.respond("ナビ子、今の自分について教えて")

    print("response:", response)

    global_ai.save()

    print("saved:", STATE_FILE)


if __name__ == "__main__":
    main()