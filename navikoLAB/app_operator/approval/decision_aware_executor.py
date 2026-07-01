from datetime import datetime

from navikoLAB.app_operator.executors.real_gui_operation_executor import RealGUIOperationExecutor

class DecisionAwareExecutor:
    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.real_executor = RealGUIOperationExecutor(dry_run=True)

    def execute_with_decision(self, decision_record):
        decision = decision_record.get("decision", "hold")
        action = decision_record.get("action", "unknown")

        if decision == "approve":
            result = self.real_executor.execute({
                "action": action,
                "request_id": decision_record.get("request_id"),
                "source": "decision_aware_executor",
            })
            result["approval_decision"] = decision
            result["status"] = "approved_dry_run_executed"
            return result

        return {
            "request_id": decision_record.get("request_id"),
            "action": action,
            "approval_decision": decision,
            "status": "execution_blocked_by_decision",
            "reason": decision_record.get("reason", "not approved"),
            "dry_run": True,
            "real_gui_operation": False,
            "external_operation": False,
            "executed_at": datetime.now().isoformat(timespec="seconds"),
        }