# navikoLAB/runtime/self_model_stabilization.py

from __future__ import annotations

from pathlib import Path
from datetime import datetime
import json


PHASE = "Phase112-2 Self Model Stabilization Layer (Self-Difference Awareness)"

ROOT = Path(__file__).resolve().parents[2]

STABLE_DIR = ROOT / "runtime" / "self_model"
STABLE_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = STABLE_DIR / "self_model_state.json"


# -----------------------------
# SELF MODEL STABILIZER
# -----------------------------

class SelfModelStabilizer:

    def __init__(self, self_aware_loop):

        self.loop = self_aware_loop

        self.last_snapshot = None
        self.differences = []

    # -----------------------------
    # CAPTURE CURRENT STATE
    # -----------------------------

    def snapshot(self):

        state = self.loop.state

        return {
            "cycle": state.cycle,
            "memory_size": state.memory_size,
            "awareness_score": state.awareness_score,
            "personality": state.personality_summary,
            "last_thought": state.last_thought,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }

    # -----------------------------
    # COMPARE STATES
    # -----------------------------

    def compare(self, prev, current):

        diff = {}

        keys = ["memory_size", "awareness_score"]

        for k in keys:
            diff[k] = current[k] - prev[k]

        # simple semantic change detection
        diff["thought_changed"] = prev["last_thought"] != current["last_thought"]

        return diff

    # -----------------------------
    # UPDATE SELF MODEL
    # -----------------------------

    def update(self):

        current = self.snapshot()

        if self.last_snapshot is None:
            self.last_snapshot = current
            return {
                "status": "initialized",
                "state": current,
            }

        diff = self.compare(self.last_snapshot, current)

        self.differences.append(diff)

        self.last_snapshot = current

        return {
            "status": "updated",
            "diff": diff,
        }

    # -----------------------------
    # RUN STABILIZATION LOOP
    # -----------------------------

    def run(self, steps: int = 5):

        history = []

        for _ in range(steps):
            history.append(self.update())

        self.save(history)

        return history

    # -----------------------------
    # SAVE STATE
    # -----------------------------

    def save(self, history):

        STATE_FILE.write_text(
            json.dumps({
                "phase": PHASE,
                "differences": self.differences,
                "history": history,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# -----------------------------
# ENTRY POINT
# -----------------------------

def main():

    print("=== Naviko Self Model Stabilization ===")
    print("phase:", PHASE)
    print("mode: dry_run")

    from navikoLAB.runtime.persistent_self_aware_loop import PersistentSelfAwareLoop
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

    stabilizer = SelfModelStabilizer(loop)

    # run self-aware loop first (to generate state)
    from navikoLAB.runtime.persistent_self_aware_loop import PersistentSelfAwareLoop
    loop.run(steps=5)

    result = stabilizer.run(steps=5)

    print("result:", result[-1])
    print("saved:", STATE_FILE)


if __name__ == "__main__":
    main()