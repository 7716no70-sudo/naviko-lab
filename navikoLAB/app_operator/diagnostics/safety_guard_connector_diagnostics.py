from navikoLAB.connectors.real_app_operator_connector import RealAppOperatorConnector


def main():
    print("=== SafetyGuard Connector Diagnostics ===")

    connector = RealAppOperatorConnector(dry_run=True)

    safe_result = connector.run({
        "action": "mouse_click_plan",
        "target": "sample_button",
        "x": 100,
        "y": 200,
    })

    blocked_result = connector.run({
        "action": "delete_file",
        "target": "sample.txt",
    })

    print("[Safe Routed Action]")
    print("状態:", safe_result.get("status"))
    print("Component:", safe_result.get("component"))
    print("blocked:", safe_result.get("blocked"))
    print("HumanApproval必須:", safe_result.get("requires_human_approval"))
    print("外部操作実行:", safe_result.get("external_operation_executed"))

    print("[Blocked Routed Action]")
    print("状態:", blocked_result.get("status"))
    print("Component:", blocked_result.get("component"))
    print("blocked:", blocked_result.get("blocked"))
    print("実行許可:", blocked_result.get("allowed_to_execute"))
    print("外部操作実行:", blocked_result.get("external_operation_executed"))


if __name__ == "__main__":
    main()