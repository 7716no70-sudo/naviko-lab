# navikoLAB/runtime/ai_os_multi_agent_feedback_loop.py

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json


PHASE = "Phase103-2 AI OS Multi-Agent Feedback Loop"

ROOT = Path(__file__).resolve().parents[2]

STATE_FILE = ROOT / "runtime" / "agents" / "multi_agent_state.json"
FEEDBACK_FILE = ROOT / "runtime" / "agents" / "multi_agent_feedback_state.json"

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


@dataclass
class Result:
    task_id: str
    output: str
    status: str


# -----------------------------
# Load State
# -----------------------------

def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# -----------------------------
# Feedback Engine
# -----------------------------

class FeedbackEngine:

    def analyze(self, evaluation):

        # simple scoring rule (dry_run)
        score = evaluation.get("quality_score", 0)

        if score >= 0.8:
            return "keep_strategy"
        elif score >= 0.5:
            return "adjust_strategy"
        else:
            return "replan_required"


# -----------------------------
# Multi-Agent Feedback Loop
# -----------------------------

class FeedbackLoopSystem:

    def __init__(self):

        self.feedback_engine = FeedbackEngine()
        self.history = []

    def run(self):

        state = load_json(STATE_FILE)

        if not state:
            print("missing agent state")
            return

        history = state.get("history", [])

        feedback_results = []

        for record in history:

            evaluation = record.get("evaluation", {})

            decision = self.feedback_engine.analyze(evaluation)

            feedback = {
                "task_id": record["task"]["task_id"],
                "decision": decision,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            }

            feedback_results.append(feedback)

            self.history.append({
                "record": record,
                "feedback": feedback
            })

        return {
            "feedback_count": len(feedback_results),
            "replan_required": len([f for f in feedback_results if f["decision"] == "replan_required"]),
            "adjust_strategy": len([f for f in feedback_results if f["decision"] == "adjust_strategy"]),
            "keep_strategy": len([f for f in feedback_results if f["decision"] == "keep_strategy"]),
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

        save_json(FEEDBACK_FILE, state)


# -----------------------------
# Entry Point
# -----------------------------

def main():

    system = FeedbackLoopSystem()

    summary = system.run()
    system.save()

    print("=== AI OS Multi-Agent Feedback Loop ===")
    print("phase:", PHASE)
    print("mode: dry_run")
    print("summary:", summary)
    print("safe: True")
    print("risk: 0")
    print("saved:", FEEDBACK_FILE)


if __name__ == "__main__":
    main()