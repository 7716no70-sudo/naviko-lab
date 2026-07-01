from navikoLAB.connectors.explorer_operation_planner import ExplorerOperationPlanner


def main():
    print("=== ExplorerOperationPlanner Diagnostics ===")

    planner = ExplorerOperationPlanner(dry_run=True)
    result = planner.plan({
        "action": "open_explorer_plan",
        "target_path": "C:\\Users\\7716n\\OneDrive\\デスクトップ\\naviko_lab",
    })

    print("状態:", result.get("status"))
    print("Component:", result.get("component"))
    print("dry_run:", result.get("dry_run"))
    print("外部操作実行:", result.get("external_operation_executed"))
    print("Action:", result.get("action"))
    print("Target:", result.get("target_path"))
    print("計画Steps:")
    for step in result.get("planned_steps", []):
        print("-", step)


if __name__ == "__main__":
    main()