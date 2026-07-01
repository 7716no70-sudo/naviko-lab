from pathlib import Path
import json
from datetime import datetime

class ApprovalDecisionManager:
    def __init__(self, request_dir=None):
        self.request_dir = Path(request_dir or Path(__file__).resolve().parents[1] / "approval_requests")

    def list_requests(self):
        self.request_dir.mkdir(parents=True, exist_ok=True)
        return sorted(self.request_dir.glob("*.json"))

    def review_requests(self):
        results = []
        for path in self.list_requests():
            data = json.loads(path.read_text(encoding="utf-8"))
            decision = {
                "request_file": str(path),
                "request_id": data.get("request_id", path.stem),
                "action": data.get("action"),
                "status": "pending_review",
                "decision": "dry_run_approved",
                "reason": "Phase2-7 dry_run approval review only",
                "decided_at": datetime.now().isoformat(timespec="seconds"),
                "dry_run": True,
                "external_operation": False,
            }
            results.append(decision)
        return results