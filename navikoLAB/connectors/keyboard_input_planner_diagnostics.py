from navikoLAB.connectors.keyboard_input_planner import KeyboardInputPlanner


def main():
    print("=== KeyboardInputPlanner Diagnostics ===")

    planner = KeyboardInputPlanner(dry_run=True)
    result = planner.plan({
        "action": "keyboard_input_plan",
        "target": "sample_input_box",
        "text": "ナビ子 Phase2-3 dry_run input test",
    })

    print("状態:", result.get("status"))
    print("Component:", result.get("component"))
    print("dry_run:", result.get("dry_run"))
    print("外部操作実行:", result.get("external_operation_executed"))
    print("Action:", result.get("action"))
    print("Target:", result.get("target"))
    print("TextLength:", result.get("text_length"))
    print("計画Steps:")
    for step in result.get("planned_steps", []):
        print("-", step)


if __name__ == "__main__":
    main()