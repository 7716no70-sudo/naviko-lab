# navikoLAB/runtime/ai_os_multi_agent_self_replanning.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json


PHASE = "Phase103-3 AI OS Multi-Agent Self-Replanning"

ROOT = Path(__file__).resolve().parents[2]

STATE_FILE = ROOT / "runtime" / "agents" / "multi_agent_state.json"
FEEDBACK_FILE = ROOT / "runtime" / "agents" / "multi_agent_feedback_state.json"
REPLAN_FILE = ROOT / "runtime" / "agents" / "multi_agent_replanned_state.json"

AGENT_DIR = STATE_FILE.parent
AGENT_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Data Models
# -----------------------------

@dataclass
class Task:
    task_id: str
    goal: str
    payload: str


# -----------------------------
# Load / Save
# -----------------------------

def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# -----------------------------
# Planner (Replanning Core)
# -----------------------------

class Replanner:

    def replan(self, goal: str, feedback_summary: dict):

        replan_required = feedback_summary.get("replan_required", 0)
        adjust = feedback_summary.get("adjust_strategy", 0)

        tasks = []

        # -----------------------------
        # SELF-REPLANNING RULES
        # -----------------------------

        if replan_required > 0:
            # aggressive replan
            tasks = [
                Task(task_id="r1", goal=goal, payload=f"{goal} - full replan strategy"),
                Task(task_id="r2", goal=goal, payload=f"{goal} - reset execution path"),
                Task(task_id="r3", goal=goal, payload=f"{goal} - validation pass"),
            ]

        elif adjust > 0:
            # partial adjustment
            tasks = [
                Task(task_id="a1", goal=goal, payload=f"{goal} - adjust execution flow"),
                Task(task_id="a2", goal=goal, payload=f"{goal} - optimize strategy"),
            ]

        else:
            # keep stable strategy
            tasks = [
                Task(task_id="k1", goal=goal, payload=f"{goal} - continue stable execution"),
            ]

        return tasks


# -----------------------------
# Self-Replanning System
# -----------------------------

class SelfReplanningSystem:

    def __init__(self):
        self.replanner = Replanner()
        self.history = []

    def run(self):

        state = load_json(STATE_FILE)
        feedback = load_json(FEEDBACK_FILE)

        if not state or not feedback:
            print("missing state or feedback")
            return

        goal = state["history"][0]["task"]["goal"]
        summary = feedback

        new_tasks = self.replanner.replan(goal, summary)

        self.history.append({
            "goal": goal,
            "feedback": summary,
            "replanned_tasks": [t.__dict__ for t in new_tasks],
        })

        return {
            "goal": goal,
            "new_task_count": len(new_tasks),
            "mode": "dry_run",
            "replan_mode": True,
        }

    def save(self):

        state = {
            "phase": PHASE,
            "mode": "dry_run",
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "history": self.history,
            "safe": True,
            "risk": 0,
        }

        save_json(REPLAN_FILE, state)


# -----------------------------
# Entry Point
# -----------------------------

def main():

    system = SelfReplanningSystem()

    summary = system.run()
    system.save()

    print("=== AI OS Self-Replanning System ===")
    print("phase:", PHASE)
    print("mode: dry_run")
    print("summary:", summary)
    print("safe: True")
    print("risk: 0")
    print("saved:", REPLAN_FILE)


if __name__ == "__main__":
    main()