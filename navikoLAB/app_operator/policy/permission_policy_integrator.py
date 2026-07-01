from navikoLAB.app_operator.policy.permission_policy import PermissionPolicy

class PermissionPolicyIntegrator:
    def __init__(self):
        self.policy = PermissionPolicy()

    def apply(self, operation):
        action = operation.get("action", "unknown")
        policy_result = self.policy.classify(action)

        integrated = dict(operation)
        integrated.update({
            "permission_policy": policy_result,
            "permission_level": policy_result["permission_level"],
            "permission_type": policy_result["permission_type"],
            "requires_approval": policy_result["requires_approval"],
            "requires_strict_approval": policy_result["requires_strict_approval"],
            "dry_run": True,
            "external_operation": False,
        })

        if policy_result["permission_level"] == 1:
            integrated["route"] = "auto_dry_run"
        elif policy_result["permission_level"] == 2:
            integrated["route"] = "simple_approval_required"
        elif policy_result["permission_level"] == 3:
            integrated["route"] = "normal_approval_required"
        else:
            integrated["route"] = "strict_approval_required"

        return integrated