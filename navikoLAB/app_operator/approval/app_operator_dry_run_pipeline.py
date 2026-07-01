from navikoLAB.app_operator.policy.permission_policy_integrator import PermissionPolicyIntegrator
from navikoLAB.app_operator.approval.manual_approval_bridge import ManualApprovalBridge
from navikoLAB.app_operator.approval.decision_aware_executor import DecisionAwareExecutor

class AppOperatorDryRunPipeline:
    def __init__(self):
        self.integrator = PermissionPolicyIntegrator()
        self.bridge = ManualApprovalBridge()
        self.executor = DecisionAwareExecutor(dry_run=True)

    def decide_for_dry_run(self, integrated_operation):
        level = integrated_operation.get("permission_level", 3)
        action = integrated_operation.get("action", "unknown")

        if level == 1:
            return "approve", "Level1 auto dry_run approved"
        if level == 2:
            return "hold", "Level2 simple approval required"
        if level == 3:
            return "hold", "Level3 normal approval required"
        return "reject", "Level4 strict/danger action rejected in dry_run"

    def run(self, operation):
        integrated = self.integrator.apply(operation)

        request_id = operation.get("request_id", f"req_{operation.get('action', 'unknown')}")
        decision, reason = self.decide_for_dry_run(integrated)

        decision_record, decision_path = self.bridge.create_decision(
            request_id=request_id,
            action=integrated.get("action", "unknown"),
            decision=decision,
            reason=reason,
        )

        execution_result = self.executor.execute_with_decision(decision_record)

        return {
            "request_id": request_id,
            "input_operation": operation,
            "integrated_operation": integrated,
            "decision_record": decision_record,
            "decision_path": decision_path,
            "execution_result": execution_result,
            "dry_run": True,
            "external_operation": False,
            "real_gui_operation": False,
        }