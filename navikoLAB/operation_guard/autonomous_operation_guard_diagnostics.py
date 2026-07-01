from navikoLAB.operation_guard.autonomous_operation_guard import AutonomousOperationGuard


def main():
    result = AutonomousOperationGuard().check()
    rules = result.get("guard_rules", {})

    required_blocked = [
        "external_operation_allowed",
        "original_write_allowed",
        "file_delete_allowed",
        "real_gui_operation_allowed",
        "browser_operation_allowed",
        "auto_execute_allowed",
    ]

    all_required_blocked = all(
        rules.get(key) is False
        for key in required_blocked
    )

    human_approval_required = rules.get("human_approval_required") is True

    safe_to_continue = (
        result.get("status") == "completed"
        and result.get("operation_guard_active") is True
        and all_required_blocked
        and human_approval_required
        and result.get("risk_count") == 0
        and result.get("safe_to_continue") is True
    )

    print("=== Autonomous Operation Guard Diagnostics ===")
    print("phase: Phase81-2 Autonomous Operation Guard Diagnostics")
    print(f"status: {result.get('status')}")
    print(f"OperationGuardActive: {result.get('operation_guard_active')}")
    print(f"BlockedOperationCount: {result.get('blocked_operation_count')}")
    print(f"AllRequiredBlocked: {all_required_blocked}")
    print(f"HumanApprovalRequired: {human_approval_required}")
    print(f"RiskCount: {result.get('risk_count')}")
    print(f"SafeToContinue: {safe_to_continue}")
    print(f"LogPath: {result.get('log_path')}")


if __name__ == "__main__":
    main()