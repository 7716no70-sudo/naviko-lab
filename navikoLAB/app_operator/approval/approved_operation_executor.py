from datetime import datetime

class ApprovedOperationExecutor:
    def execute(self, decision):
        return {
            "request_id": decision.get("request_id"),
            "action": decision.get("action"),
            "decision": decision.get("decision"),
            "status": "dry_run_executed",
            "executed_at": datetime.now().isoformat(timespec="seconds"),
            "dry_run": True,
            "external_operation": False,
            "real_gui_operation": False,
        }