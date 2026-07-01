from datetime import datetime
from pathlib import Path
import json


class HumanApprovalGate:
    """
    AppOperator用 HumanApproval Gate。
    実GUI操作前に人間承認を必須化する。
    初期段階では approval request を作成するのみ。
    """

    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.request_dir = Path(__file__).resolve().parents[1] / "approval_requests"
        self.request_dir.mkdir(parents=True, exist_ok=True)

    def request_approval(self, task):
        action = task.get("action", "")
        approval_id = datetime.now().strftime("app_operator_approval_%Y%m%d_%H%M%S")

        request = {
            "approval_id": approval_id,
            "status": "approval_required",
            "component": "human_approval_gate",
            "dry_run": self.dry_run,
            "external_operation_executed": False,
            "action": action,
            "task": task,
            "allowed_to_execute": False,
            "message": "Human approval is required before real AppOperator execution.",
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        path = self.request_dir / f"{approval_id}.json"
        path.write_text(
            json.dumps(request, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        request["approval_request_path"] = str(path)
        return request