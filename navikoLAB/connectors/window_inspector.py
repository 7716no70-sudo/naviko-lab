from datetime import datetime
from pathlib import Path
import json
import platform


class WindowInspector:
    """
    Phase2-2 WindowInspector 基盤。
    初期段階では安全な dry_run 情報のみ返す。
    実ウィンドウ操作・クリック・入力は行わない。
    """

    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.log_dir = Path(__file__).resolve().parent / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def inspect(self):
        result = {
            "status": "completed",
            "component": "window_inspector",
            "dry_run": self.dry_run,
            "external_operation_executed": False,
            "os": platform.system(),
            "supported_checks": [
                "os_check",
                "window_list_plan",
                "active_window_plan",
                "safe_gui_inspection_plan",
            ],
            "message": "WindowInspector dry_run completed. No real window operation executed.",
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        self.write_log(result)
        return result

    def write_log(self, data):
        path = self.log_dir / f"window_inspector_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path