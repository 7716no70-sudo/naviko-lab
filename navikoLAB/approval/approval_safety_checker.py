from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
REQUEST_DIR = ROOT / "navikoLAB" / "approval" / "requests"


class ApprovalSafetyChecker:
    def __init__(self):
        self.required_flags = {
            "direct_write": False,
            "auto_apply": False,
            "human_approval_required": True,
            "approved": True,
        }

    def check_request(self, request_path: Path):
        if not request_path or not request_path.exists():
            return {
                "status": "failed",
                "reason": "approval request not found",
            }

        data = json.loads(request_path.read_text(encoding="utf-8"))

        checks = {
            "direct_write_false": data.get("direct_write") is False,
            "auto_apply_false": data.get("auto_apply") is False,
            "human_approval_required": data.get("human_approval_required") is True,
            "approved_by_human": data.get("approved") is True,
            "status_approved": data.get("status") == "approved_by_human",
        }

        failed = [name for name, ok in checks.items() if not ok]

        return {
            "status": "passed" if not failed else "failed",
            "checks": checks,
            "failed": failed,
            "request_path": str(request_path),
        }


if __name__ == "__main__":
    requests = sorted(REQUEST_DIR.glob("approval_request_*.json"))
    latest = requests[-1] if requests else None

    checker = ApprovalSafetyChecker()
    result = checker.check_request(latest)

    print("=== ApprovalSafetyChecker ===")
    print("状態:", result["status"])
    print("失敗:", result.get("failed"))