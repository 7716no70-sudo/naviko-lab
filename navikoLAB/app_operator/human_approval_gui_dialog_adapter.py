from dataclasses import asdict

from navikoLAB.app_operator.human_approval_dialog_core import (
    HumanApprovalDialogCore,
)


def request_human_approval_gui(
    parent_window=None,
    mission_text="",
    operation_summary="",
    enable_gui_dialog=False,
):
    selected_action = "reject"

    if enable_gui_dialog:
        try:
            from tkinter import messagebox

            message = (
                "以下の操作を承認しますか？\n\n"
                f"Mission:\n{mission_text}\n\n"
                f"Operation:\n{operation_summary}\n\n"
                "承認すると次の安全判定へ進みます。"
            )

            approved = messagebox.askyesno(
                "HumanApproval",
                message,
                parent=parent_window,
            )

            selected_action = "approve" if approved else "reject"

        except Exception:
            selected_action = "reject"

    core = HumanApprovalDialogCore()
    return asdict(
        core.evaluate(
            mission_text=mission_text,
            operation_summary=operation_summary,
            selected_action=selected_action,
        )
    )