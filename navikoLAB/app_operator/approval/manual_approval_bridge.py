from pathlib import Path
import json
from datetime import datetime

class ManualApprovalBridge:
    VALID_DECISIONS = {"approve", "reject", "hold"}

    def __init__(self, decision_dir=None):
        self.decision_dir = Path(decision_dir or Path(__file__).resolve().parents[1] / "approval_decisions")
        self.decision_dir.mkdir(parents=True, exist_ok=True)

    def create_decision(self, request_id, action, decision="hold", reason="manual review pending"):
        if decision not in self.VALID_DECISIONS:
            decision = "hold"
            reason = "invalid decision converted to hold"

        record = {
            "request_id": request_id,
            "action": action,
            "decision": decision,
            "reason": reason,
            "dry_run": True,
            "external_operation": False,
            "real_gui_operation": False,
            "decided_at": datetime.now().isoformat(timespec="seconds"),
        }

        file_name = f"approval_decision_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        path = self.decision_dir / file_name
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        return record, str(path)

    def summarize(self):
        files = sorted(self.decision_dir.glob("*.json"))
        return {
            "decision_count": len(files),
            "decision_dir": str(self.decision_dir),
            "latest_decision": str(files[-1]) if files else None,
            "dry_run": True,
            "external_operation": False,
        }