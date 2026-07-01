# ============================================================
# Phase69-1 RecoveryManager
# 自動復旧管理
# ============================================================

from navikoLAB.snapshot.snapshot_manager import SnapshotManager
from navikoLAB.recovery_policy.recovery_policy import RecoveryPolicy
from navikoLAB.recovery.recovery_audit_logger import RecoveryAuditLogger


class RecoveryManager:

    def __init__(self):
        self.snapshot_manager = SnapshotManager()
        self.policy = RecoveryPolicy()
        self.audit_logger = RecoveryAuditLogger()
        self.recovery_log = []

    def should_recover(self, health_result, stability_result=None):
        system_health = health_result.get("system_health", "unknown")
        health_score = health_result.get("health_score", 0.5)
        warnings = health_result.get("warnings", [])

        if system_health == "critical":
            return True

        if health_score < 0.3:
            return True

        if "low_stability" in warnings:
            return True

        if stability_result and stability_result.get("stability", 0.5) < 0.25:
            return True

        return False

    def recover_to_latest_test(self):
        result = self.snapshot_manager.restore_latest_to(
            restore_root="navikoLAB/recovery_test"
        )

        self.recovery_log.append(result)

        return result

    def run(self, health_result, stability_result=None):
        snapshot_result = self.snapshot_manager.latest()

        policy_result = self.policy.evaluate(
            health_result,
            stability_result,
            snapshot_result
        )

        if not policy_result.get("allowed"):
            blocked_result = {
                "status": "blocked",
                "reason": "policy_blocked",
                "policy": policy_result
            }

            audit_result = self.audit_logger.record(
                health_result,
                stability_result,
                policy_result,
                blocked_result
            )

            blocked_result["audit"] = audit_result
            return blocked_result

        recovery_result = self.recover_to_latest_test()

        result = {
            "status": "recovery_test_completed",
            "policy": policy_result,
            "recovery": recovery_result
        }

        audit_result = self.audit_logger.record(
            health_result,
            stability_result,
            policy_result,
            result
        )

        result["audit"] = audit_result
        return result

    def latest(self):
        if not self.recovery_log:
            return {
                "status": "empty"
            }

        return self.recovery_log[-1]