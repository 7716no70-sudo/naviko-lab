from navikoLAB.connectors.connector_dispatcher import ConnectorDispatcher


def main():
    print("=== Real App Operator Dispatch Component Diagnostics ===")

    dispatcher = ConnectorDispatcher()

    window_result = dispatcher.run(
        agent_id="real_app_operator",
        goal="WindowInspector dispatcher check",
        context={
            "action": "inspect_windows",
        },
    )

    explorer_result = dispatcher.run(
        agent_id="real_app_operator",
        goal="ExplorerOperationPlanner dispatcher check",
        context={
            "action": "open_explorer_plan",
            "target_path": "C:\\Users\\7716n\\OneDrive\\デスクトップ\\naviko_lab",
        },
    )

    print("[Dispatcher -> WindowInspector]")
    print("状態:", window_result.get("status"))
    print("Component:", window_result.get("component"))
    print("dry_run:", window_result.get("dry_run"))
    print("外部操作実行:", window_result.get("external_operation_executed"))

    print("[Dispatcher -> ExplorerOperationPlanner]")
    print("状態:", explorer_result.get("status"))
    print("Component:", explorer_result.get("component"))
    print("dry_run:", explorer_result.get("dry_run"))
    print("外部操作実行:", explorer_result.get("external_operation_executed"))
    print("Target:", explorer_result.get("target_path"))


if __name__ == "__main__":
    main()