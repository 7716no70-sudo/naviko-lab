from datetime import datetime
from pathlib import Path
import json


class KeyboardInputPlanner:
    """
    Keyboard入力計画器。
    初期段階では dry_run の計画生成のみ。
    実入力・貼り付け・ショートカット送信は行わない。
    """

    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.log_dir = Path(__file__).resolve().parent / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def plan(self, task):
        text = task.get("text", "")
        target = task.get("target", "")
        action = task.get("action", "keyboard_input_plan")

        result = {
            "status": "completed",
            "component": "keyboard_input_planner",
            "dry_run": self.dry_run,
            "external_operation_executed": False,
            "action": action,
            "target": target,
            "text_length": len(text),
            "planned_steps": [
                "Validate target input field",
                "Confirm HumanApproval before real keyboard input",
                "Prepare text safely",
                "Send keyboard input only after approval",
                "Verify result after input",
                "Record operation result",
            ],
            "message": "KeyboardInputPlanner dry_run completed. No keyboard input executed.",
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        self.write_log(result)
        return result

    def write_log(self, data):
        path = self.log_dir / f"keyboard_input_planner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path