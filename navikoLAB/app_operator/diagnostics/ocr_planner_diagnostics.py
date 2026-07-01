from navikoLAB.app_operator.components.ocr_planner import OCRPlanner


def main():
    print("=== OCRPlanner Diagnostics ===")

    planner = OCRPlanner(dry_run=True)
    result = planner.plan({
        "action": "ocr_plan",
        "target": "sample_window_area",
    })

    print("状態:", result.get("status"))
    print("Component:", result.get("component"))
    print("dry_run:", result.get("dry_run"))
    print("外部操作実行:", result.get("external_operation_executed"))
    print("Action:", result.get("action"))
    print("Target:", result.get("target"))
    print("計画Steps:")
    for step in result.get("planned_steps", []):
        print("-", step)


if __name__ == "__main__":
    main()