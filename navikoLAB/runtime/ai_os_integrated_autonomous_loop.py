# navikoLAB/runtime/ai_os_integrated_autonomous_loop.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json
import time


PHASE = "Phase104-2 Integrated Autonomous OS Loop"

ROOT = Path(__file__).resolve().parents[2]

INTEGRATED_DIR = ROOT / "runtime" / "integrated"
INTEGRATED_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = INTEGRATED_DIR / "integrated_os_state.json"


# -----------------------------
# CORE MODELS
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


@dataclass
class Evaluation:
    task_id: str
    score: float
    decision: str


# -----------------------------
# AGENTS
# -----------------------------

class Planner:

    def plan(self, goal: str):

        return [
            Task("t1", goal, f"{goal} - step analysis"),
            Task("t2", goal, f"{goal} - step execution"),
        ]


class Executor:

    def execute(self, task: Task):

        return Result(
            task.task_id,
            f"[EXEC] {task.payload}",
            "dry_run_done"
        )


class Monitor:

    def evaluate(self, result: Result):

        return Evaluation(
            result.task_id,
            score=1.0,
            decision="stable"
        )


class Feedback:

    def decide(self, evaluation: Evaluation):

        if evaluation.score < 0.5:
            return "replan"
        elif evaluation.score < 0.9:
            return "adjust"
        else:
            return "continue"


class Replanner:

    def replan(self, goal: str):

        return [
            Task("r1", goal, f"{goal} - replanned execution")
        ]


# -----------------------------
# INTEGRATED LOOP SYSTEM
# -----------------------------

class IntegratedOSLoop:

    def __init__(self):

        self.planner = Planner()
        self.executor = Executor()
        self.monitor = Monitor()
        self.feedback = Feedback()
        self.replanner = Replanner()

        self.history = []

    def cycle(self, goal: str):

        tasks = self.planner.plan(goal)

        final_tasks = []

        for task in tasks:

            result = self.executor.execute(task)
            eval_result = self.monitor.evaluate(result)
            decision = self.feedback.decide(eval_result)

            if decision == "replan":
                final_tasks.extend(self.replanner.replan(goal))
            elif decision == "adjust":
                final_tasks.append(task)
            else:
                final_tasks.append(task)

            self.history.append({
                "task": task.__dict__,
                "result": result.__dict__,
                "evaluation": eval_result.__dict__,
                "decision": decision
            })

        return final_tasks

    def run(self):

        goal = "Run integrated autonomous AI OS"

        cycles = 3

        for i in range(cycles):

            tasks = self.cycle(goal)

            print(f"[CYCLE {i+1}] tasks:", len(tasks))

            time.sleep(0.3)

        self.save()

    def save(self):

        data = {
            "phase": PHASE,
            "mode": "dry_run",
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "history": self.history,
            "safe": True,
            "risk": 0
        }

        STATE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# -----------------------------
# ENTRY POINT
# -----------------------------

def main():

    os_loop = IntegratedOSLoop()

    os_loop.run()

    print("=== AI OS Integrated Autonomous Loop ===")
    print("phase:", PHASE)
    print("mode: dry_run")
    print("cycles: 3")
    print("safe: True")
    print("risk: 0")
    print("saved:", STATE_FILE)


if __name__ == "__main__":
    main()