from dataclasses import dataclass, asdict


@dataclass
class PermissionDecision:
    action: str
    allowed: bool
    reason: str
    real_gui_operation: bool = False
    external_operation: bool = False
    original_write: bool = False


class PermissionPolicyCore:
    def evaluate(self, action: str, human_approved: bool = False) -> PermissionDecision:
        safe_actions = {
            "read_only_check": True,
            "dry_run_app_operation": True,
            "real_gui_operation": False,
            "external_operation": False,
            "original_write": False,
        }

        base_allowed = safe_actions.get(action, False)
        allowed = bool(base_allowed and human_approved)

        if not human_approved:
            reason = "human_approval_required"
        elif not base_allowed:
            reason = "permission_policy_blocked"
        else:
            reason = "allowed"

        return PermissionDecision(
            action=action,
            allowed=allowed,
            reason=reason,
            real_gui_operation=action == "real_gui_operation" and allowed,
            external_operation=action == "external_operation" and allowed,
            original_write=action == "original_write" and allowed,
        )


def evaluate_permission(action: str, human_approved: bool = False) -> dict:
    policy = PermissionPolicyCore()
    return asdict(policy.evaluate(action, human_approved))