from datetime import datetime
from pathlib import Path
import json


class OCRPlanner:
    """
    OCR計画器。
    初期段階では dry_run の計画生成のみ。
    画像取得・画面キャプチャ・OCR実行は行わない。
    """

    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.log_dir = Path(__file__).resolve().parents[1] / "reports"
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def plan(self, task):
        target = task.get("target", "")
        action = task.get("action", "ocr_plan")

        result = {
            "status": "completed",
            "component": "ocr_planner",
            "dry_run": self.dry_run,
            "external_operation_executed": False,
            "action": action,
            "target": target,
            "planned_steps": [
                "Validate OCR target",
                "Confirm HumanApproval before screen capture",
                "Capture screen only after approval",
                "Run OCR only after approval",
                "Filter sensitive information",
                "Record OCR result safely",
            ],
            "message": "OCRPlanner dry_run completed. No screen capture or OCR executed.",
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        self.write_log(result)
        return result

    def write_log(self, data):
        path = self.log_dir / f"ocr_planner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path