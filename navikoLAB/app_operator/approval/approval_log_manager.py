from pathlib import Path
import json
from datetime import datetime

class ApprovalLogManager:
    def __init__(self, log_dir=None):
        self.log_dir = Path(log_dir or Path(__file__).resolve().parents[1] / "approval_logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def save_log(self, approval_record):
        record = dict(approval_record)
        record["logged_at"] = datetime.now().isoformat(timespec="seconds")
        record["dry_run"] = True
        record["external_operation"] = False

        file_name = f"approval_log_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        path = self.log_dir / file_name
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(path)

    def summarize(self):
        files = sorted(self.log_dir.glob("*.json"))
        return {
            "log_count": len(files),
            "log_dir": str(self.log_dir),
            "latest_log": str(files[-1]) if files else None,
            "dry_run": True,
            "external_operation": False,
        }