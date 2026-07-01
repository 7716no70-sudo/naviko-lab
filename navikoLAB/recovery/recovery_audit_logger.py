# ============================================================
# Phase71-1 Recovery Audit Logger
# 復旧監査ログ
# ============================================================

import json
from pathlib import Path
from datetime import datetime


class RecoveryAuditLogger:

    def __init__(self, log_dir="navikoLAB/recovery/audit_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def _timestamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def record(self, health_result, stability_result, policy_result, recovery_result):
        timestamp = self._timestamp()

        audit = {
            "timestamp": timestamp,
            "health": health_result,
            "stability": stability_result,
            "policy": policy_result,
            "recovery": recovery_result,
            "status": recovery_result.get("status", "unknown")
        }

        path = self.log_dir / f"recovery_audit_{timestamp}.json"

        with open(path, "w", encoding="utf-8") as f:
            json.dump(audit, f, ensure_ascii=False, indent=2)

        return {
            "status": "recorded",
            "path": str(path),
            "timestamp": timestamp
        }