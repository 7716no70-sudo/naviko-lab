# navikoLAB/runtime/daily_life_integration.py

from __future__ import annotations

from pathlib import Path
from datetime import datetime, date
import json


PHASE = "Phase109-1 Daily Life Integration Layer"

ROOT = Path(__file__).resolve().parents[2]

DAILY_DIR = ROOT / "runtime" / "daily_life"
DAILY_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = DAILY_DIR / "daily_state.json"


# -----------------------------
# DAILY CORE SYSTEM
# -----------------------------

class DailyLifeNaviko:

    def __init__(self, brain):

        self.brain = brain

        self.state = {
            "last_run_date": None,
            "daily_tasks": [],
            "reflection": None,
        }

    # -----------------------------
    # DAILY TASK GENERATION
    # -----------------------------

    def generate_daily_tasks(self):

        tasks = [
            "今日の振り返りを作成する",
            "1つ改善アイデアを出す",
            "ユーザーに短いアドバイスをする",
        ]

        self.state["daily_tasks"] = tasks

        return tasks

    # -----------------------------
    # DAILY RUN
    # -----------------------------

    def run_daily_cycle(self):

        today = str(date.today())

        if self.state["last_run_date"] == today:
            return "already_executed_today"

        tasks = self.generate_daily_tasks()

        outputs = []

        for t in tasks:

            result = self.brain.process(t)
            outputs.append(result.response)

        reflection = self.brain.process("今日の改善点を1つまとめて")

        self.state["reflection"] = reflection.response
        self.state["last_run_date"] = today

        return {
            "tasks": tasks,
            "outputs": outputs,
            "reflection": reflection.response,
        }

    # -----------------------------
    # SAVE STATE
    # -----------------------------

    def save(self):

        STATE_FILE.write_text(
            json.dumps(self.state, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# -----------------------------
# ENTRY POINT
# -----------------------------

def main():

    print("=== Naviko Daily Life Integration ===")
    print("phase:", PHASE)

    # import unified brain (already built system)
    from navikoLAB.runtime.unified_brain_system import UnifiedBrain
    from navikoLAB.runtime.llm_gateway import LLMGateway
    from navikoLAB.runtime.ai_task_scheduler import TaskScheduler
    from navikoLAB.runtime.tool_gateway import ToolGateway

    llm = LLMGateway()
    scheduler = TaskScheduler()
    tool = ToolGateway()

    brain = UnifiedBrain(
        llm_gateway=llm,
        tool_gateway=tool,
        scheduler=scheduler,
    )

    daily = DailyLifeNaviko(brain)

    result = daily.run_daily_cycle()

    print("tasks:", result["tasks"])
    print("reflection:", result["reflection"])

    daily.save()

    print("saved:", STATE_FILE)


if __name__ == "__main__":
    main()