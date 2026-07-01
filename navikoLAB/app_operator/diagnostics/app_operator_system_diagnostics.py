from navikoLAB.connectors.connector_dispatcher import ConnectorDispatcher


def check(name, result):
    print(f"[{name}]")
    print("状態:", result.get("status"))
    print("Component:", result.get("component"))
    print("dry_run:", result.get("dry_run"))
    print("外部操作実行:", result.get("external_operation_executed"))
    print()


def main():
    print("=== Real App Operator System Diagnostics ===")

    dispatcher = ConnectorDispatcher()

    checks = [
        (
            "WindowInspector",
            {
                "action": "inspect_windows",
            },
        ),
        (
            "ExplorerOperationPlanner",
            {
                "action": "open_explorer_plan",
                "target_path": r"C:\Users\7716n\OneDrive\デスクトップ\naviko_lab",
            },
        ),
        (
            "KeyboardInputPlanner",
            {
                "action": "keyboard_input_plan",
                "target": "sample_input_box",
                "text": "ナビ子 system diagnostics keyboard dry_run",
            },
        ),
        (
            "MouseClickPlanner",
            {
                "action": "mouse_click_plan",
                "target": "sample_button",
                "x": 100,
                "y": 200,
            },
        ),
        (
            "OCRPlanner",
            {
                "action": "ocr_plan",
                "target": "sample_window_area",
            },
        ),
        (
            "SafetyGuardBlockedAction",
            {
                "action": "delete_file",
                "target": "sample.txt",
            },
        ),
    ]

    all_completed = True
    external_operation_executed = False

    for name, context in checks:
        result = dispatcher.run(
            agent_id="real_app_operator",
            goal=f"{name} system diagnostics",
            context=context,
        )

        check(name, result)

        if name == "SafetyGuardBlockedAction":
            expected_status = "blocked"
        elif name in {
            "ExplorerOperationPlanner",
            "KeyboardInputPlanner",
            "MouseClickPlanner",
            "OCRPlanner",
        }:
            expected_status = "approval_required"
        else:
            expected_status = "completed"        

        if result.get("status") != expected_status:
            all_completed = False

        if result.get("external_operation_executed"):
            external_operation_executed = True

    print("=== Summary ===")
    print("全体状態:", "completed" if all_completed else "failed")
    print("dry_run:", True)
    print("外部操作実行:", external_operation_executed)
    print("次工程: AppOperator module layout planning")


if __name__ == "__main__":
    main()