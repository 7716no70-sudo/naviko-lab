from datetime import datetime
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
REQUEST_DIR = ROOT / "navikoLAB" / "approval" / "requests"


class ApprovalRequestManager:
    def __init__(self):
        REQUEST_DIR.mkdir(parents=True, exist_ok=True)

    def list_requests(self):
        return sorted(REQUEST_DIR.glob("approval_request_*.json"))

    def latest_request(self):
        requests = self.list_requests()
        return requests[-1] if requests else None

    def approve_latest(self):
        path = self.latest_request()
        if not path:
            return None, None

        data = json.loads(path.read_text(encoding="utf-8"))
        data["approved"] = True
        data["status"] = "approved_by_human"
        data["approved_at"] = datetime.now().isoformat()
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

        return data, path

    def reject_latest(self, reason="human rejected"):
        path = self.latest_request()
        if not path:
            return None, None

        data = json.loads(path.read_text(encoding="utf-8"))
        data["approved"] = False
        data["status"] = "rejected_by_human"
        data["rejected_at"] = datetime.now().isoformat()
        data["reject_reason"] = reason
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

        return data, path


if __name__ == "__main__":
    manager = ApprovalRequestManager()
    latest = manager.latest_request()

    print("=== ApprovalRequestManager ===")
    print("申請数:", len(manager.list_requests()))
    print("最新申請:", latest)