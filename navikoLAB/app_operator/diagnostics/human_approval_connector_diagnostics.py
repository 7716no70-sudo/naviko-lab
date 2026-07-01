from navikoLAB.connectors.real_app_operator_connector import RealAppOperatorConnector


def main():
    print("=== HumanApproval Connector Diagnostics ===")

    connector = RealAppOperatorConnector(dry_run=True)

    result = connector.run({
        "action": "mouse_click_plan",
        "target": "sample_button",
        "x": 100,
        "y": 200,
    })

    print("状態:", result.get("status"))
    print("Component:", result.get("component"))
    print("ApprovalID:", result.get("approval_id"))
    print("dry_run:", result.get("dry_run"))
    print("実行許可:", result.get("allowed_to_execute"))
    print("外部操作実行:", result.get("external_operation_executed"))
    print("保存先:", result.get("approval_request_path"))


if __name__ == "__main__":
    main()