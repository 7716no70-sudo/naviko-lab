from dataclasses import dataclass, asdict


@dataclass
class HumanApprovalDecision:
    mission_text: str
    operation_summary: str
    selected_action: str
    approved: bool
    rejected: bool
    show_details: bool
    reason: str


class HumanApprovalDialogCore:
    def evaluate(
        self,
        mission_text: str = "",
        operation_summary: str = "",
        selected_action: str = "reject",
    ) -> HumanApprovalDecision:
        approved = selected_action == "approve"
        rejected = selected_action == "reject"
        show_details = selected_action == "show_details"

        if approved:
            reason = "human_approved"
        elif show_details:
            reason = "details_requested"
        else:
            reason = "human_rejected_or_default_reject"

        return HumanApprovalDecision(
            mission_text=mission_text,
            operation_summary=operation_summary,
            selected_action=selected_action,
            approved=approved,
            rejected=rejected,
            show_details=show_details,
            reason=reason,
        )


def evaluate_human_approval(
    mission_text: str = "",
    operation_summary: str = "",
    selected_action: str = "reject",
) -> dict:
    core = HumanApprovalDialogCore()
    return asdict(
        core.evaluate(
            mission_text=mission_text,
            operation_summary=operation_summary,
            selected_action=selected_action,
        )
    )