from navikoLAB.connectors.mouse_click_planner import MouseClickPlanner


def main():
    print("=== MouseClickPlanner Diagnostics ===")

    planner = MouseClickPlanner(dry_run=True)
    result = planner.plan({
        "action": "mouse_click_plan",
        "target": "sample_button",
        "x": 100,
        "y": 200,
    })

    print("状態:", result.get("status"))
    print("Component:", result.get("component"))
    print("dry_run:", result.get("dry_run"))
    print("外部操作実行:", result.get("external_operation_executed"))
    print("Action:", result.get("action"))
    print("Target:", result.get("target"))
    print("X:", result.get("x"))
    print("Y:", result.get("y"))
    print("計画Steps:")
    for step in result.get("planned_steps", []):
        print("-", step)


if __name__ == "__main__":
    main()