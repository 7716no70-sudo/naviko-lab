from navikoLAB.app_operator.components.gui_automation_safety_guard import GUIAutomationSafetyGuard


def main():
    print("=== GUIAutomationSafetyGuard Diagnostics ===")

    guard = GUIAutomationSafetyGuard(dry_run=True)

    safe_result = guard.check({
        "action": "mouse_click_plan",
        "target": "sample_button",
    })

    blocked_result = guard.check({
        "action": "delete_file",
        "target": "sample.txt",
    })

    print("[Safe Action]")
    print("状態:", safe_result.get("status"))
    print("Component:", safe_result.get("component"))
    print("Action:", safe_result.get("action"))
    print("blocked:", safe_result.get("blocked"))
    print("HumanApproval必須:", safe_result.get("requires_human_approval"))
    print("実行許可:", safe_result.get("allowed_to_execute"))
    print("外部操作実行:", safe_result.get("external_operation_executed"))

    print("[Blocked Action]")
    print("状態:", blocked_result.get("status"))
    print("Component:", blocked_result.get("component"))
    print("Action:", blocked_result.get("action"))
    print("blocked:", blocked_result.get("blocked"))
    print("HumanApproval必須:", blocked_result.get("requires_human_approval"))
    print("実行許可:", blocked_result.get("allowed_to_execute"))
    print("外部操作実行:", blocked_result.get("external_operation_executed"))


if __name__ == "__main__":
    main()