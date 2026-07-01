from pathlib import Path
import json
from datetime import datetime

class HumanReviewApprovalRecord:
    def __init__(self, record_dir=None):
        self.record_dir = Path(record_dir or Path(__file__).resolve().parent / "human_review_records")
        self.record_dir.mkdir(parents=True, exist_ok=True)

    def create_record(self, approved=False, reviewer="human", reason="pending"):
        record = {
            "status": "human_approved" if approved else "pending_human_review",
            "phase": "Post-v2.0 Phase2-27 Human Review Approval Record",
            "reviewer": reviewer,
            "approved": approved,
            "reason": reason,
            "approval_scope": [
                "PermissionPolicy",
                "Approval flow",
                "DecisionAwareExecutor",
                "AppOperatorDryRunPipeline",
                "Diagnostics",
                "Reflection/Experience",
                "Original adoption dry_run only",
            ],
            "original_adoption_allowed": False,
            "original_auto_write": False,
            "original_write_executed": False,
            "dry_run": True,
            "external_operation": False,
            "real_gui_operation": False,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        path = self.record_dir / f"human_review_approval_record_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        return record, str(path)