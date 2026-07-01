from datetime import datetime
from pathlib import Path
import json


class GUIAutomationSafetyGuard:
    """
    GUI Automation Safety Guard。
    実GUI操作前の安全判定ゲート。
    初期段階では dry_run 判定のみで、実操作は行わない。
    """

    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.log_dir = Path(__file__).resolve().parents[1] / "reports"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.blocked_actions = {
            "shutdown",
            "restart",
            "delete_file",
            "format_disk",
            "install_software",
            "run_as_admin",
            "send_email",
            "purchase",
            "payment",
        }

        self.approval_required_actions = {
            "open_explorer_plan",
            "keyboard_input_plan",
            "mouse_click_plan",
            "ocr_plan",
            "gui_automation_plan",
        }

    def check(self, task):
        action = task.get("action", "")
        requires_approval = action in self.approval_required_actions
        blocked = action in self.blocked_actions

        result = {
            "status": "blocked" if blocked else "completed",
            "component": "gui_automation_safety_guard",
            "dry_run": self.dry_run,
            "external_operation_executed": False,
            "action": action,
            "blocked": blocked,
            "requires_human_approval": requires_approval,
            "allowed_to_execute": False,
            "reason": "blocked dangerous GUI action" if blocked else "dry_run safety check completed",
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        self.write_log(result)
        return result

    def write_log(self, data):
        path = self.log_dir / f"gui_automation_safety_guard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path