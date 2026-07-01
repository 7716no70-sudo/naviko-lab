from navikoLAB.connectors.connector_dispatcher import ConnectorDispatcher


def main():
    print("=== Real App Operator Dispatch Keyboard / Mouse Diagnostics ===")

    dispatcher = ConnectorDispatcher()

    keyboard_result = dispatcher.run(
        agent_id="real_app_operator",
        goal="KeyboardInputPlanner dispatcher check",
        context={
            "action": "keyboard_input_plan",
            "target": "sample_input_box",
            "text": "ナビ子 dispatcher keyboard dry_run",
        },
    )

    mouse_result = dispatcher.run(
        agent_id="real_app_operator",
        goal="MouseClickPlanner dispatcher check",
        context={
            "action": "mouse_click_plan",
            "target": "sample_button",
            "x": 100,
            "y": 200,
        },
    )

    print("[Dispatcher → KeyboardInputPlanner]")
    print("状態:", keyboard_result.get("status"))
    print("Component:", keyboard_result.get("component"))
    print("dry_run:", keyboard_result.get("dry_run"))
    print("外部操作実行:", keyboard_result.get("external_operation_executed"))
    print("Target:", keyboard_result.get("target"))
    print("TextLength:", keyboard_result.get("text_length"))

    print("[Dispatcher → MouseClickPlanner]")
    print("状態:", mouse_result.get("status"))
    print("Component:", mouse_result.get("component"))
    print("dry_run:", mouse_result.get("dry_run"))
    print("外部操作実行:", mouse_result.get("external_operation_executed"))
    print("Target:", mouse_result.get("target"))
    print("X:", mouse_result.get("x"))
    print("Y:", mouse_result.get("y"))


if __name__ == "__main__":
    main()