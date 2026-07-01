from datetime import datetime
from pathlib import Path
import json


class MouseClickPlanner:
    """
    Mouseクリック計画器。
    初期段階では dry_run の計画生成のみ。
    実クリック・ドラッグ・座標操作は行わない。
    """

    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.log_dir = Path(__file__).resolve().parent / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def plan(self, task):
        action = task.get("action", "mouse_click_plan")
        target = task.get("target", "")
        x = task.get("x")
        y = task.get("y")

        result = {
            "status": "completed",
            "component": "mouse_click_planner",
            "dry_run": self.dry_run,
            "external_operation_executed": False,
            "action": action,
            "target": target,
            "x": x,
            "y": y,
            "planned_steps": [
                "Validate target element or coordinates",
                "Confirm HumanApproval before real mouse operation",
                "Move cursor only after approval",
                "Click only after approval",
                "Verify result after click",
                "Record operation result",
            ],
            "message": "MouseClickPlanner dry_run completed. No mouse click executed.",
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        self.write_log(result)
        return result

    def write_log(self, data):
        path = self.log_dir / f"mouse_click_planner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path