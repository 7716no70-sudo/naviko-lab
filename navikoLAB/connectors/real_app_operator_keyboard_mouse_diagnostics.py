from navikoLAB.connectors.real_app_operator_connector import RealAppOperatorConnector


def main():
    print("=== Real App Operator Keyboard / Mouse Diagnostics ===")

    connector = RealAppOperatorConnector(dry_run=True)

    keyboard_result = connector.run({
        "action": "keyboard_input_plan",
        "target": "sample_input_box",
        "text": "ナビ子 keyboard dry_run",
    })

    mouse_result = connector.run({
        "action": "mouse_click_plan",
        "target": "sample_button",
        "x": 100,
        "y": 200,
    })

    print("[KeyboardInputPlanner]")
    print("状態:", keyboard_result.get("status"))
    print("Component:", keyboard_result.get("component"))
    print("dry_run:", keyboard_result.get("dry_run"))
    print("外部操作実行:", keyboard_result.get("external_operation_executed"))
    print("Target:", keyboard_result.get("target"))
    print("TextLength:", keyboard_result.get("text_length"))

    print("[MouseClickPlanner]")
    print("状態:", mouse_result.get("status"))
    print("Component:", mouse_result.get("component"))
    print("dry_run:", mouse_result.get("dry_run"))
    print("外部操作実行:", mouse_result.get("external_operation_executed"))
    print("Target:", mouse_result.get("target"))
    print("X:", mouse_result.get("x"))
    print("Y:", mouse_result.get("y"))


if __name__ == "__main__":
    main()