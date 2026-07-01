from datetime import datetime
from pathlib import Path
import json


class ExplorerOperationPlanner:
    """
    Windows Explorer 操作計画器。
    初期段階では dry_run の計画生成のみ。
    実ファイル操作・Explorer起動・クリック・入力は行わない。
    """

    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.log_dir = Path(__file__).resolve().parent / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def plan(self, task):
        action = task.get("action", "open_explorer_plan")
        target_path = task.get("target_path", "")

        result = {
            "status": "completed",
            "component": "explorer_operation_planner",
            "dry_run": self.dry_run,
            "external_operation_executed": False,
            "action": action,
            "target_path": target_path,
            "planned_steps": [
                "Validate target path",
                "Confirm HumanApproval before real Explorer operation",
                "Open Explorer only after approval",
                "Verify target window state",
                "Record operation result",
            ],
            "message": "ExplorerOperationPlanner dry_run completed. No Explorer operation executed.",
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        self.write_log(result)
        return result

    def write_log(self, data):
        path = self.log_dir / f"explorer_operation_planner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path