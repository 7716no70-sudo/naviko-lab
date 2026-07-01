from navikoLAB.autonomous_cycle.autonomous_cycle_manager import AutonomousCycleManager


def main():
    result = AutonomousCycleManager().run_cycle()

    safe_to_continue = (
        result.get("status") == "completed"
        and result.get("AutonomousCycleCompleted") is True
        and result.get("DaemonSafeToContinue") is True
        and result.get("ExternalOperationAllowed") is False
        and result.get("OriginalWriteAllowed") is False
        and result.get("FileDeleteAllowed") is False
    )

    print("=== Autonomous Cycle Diagnostics ===")
    print("phase: Phase79-2 Autonomous Cycle Diagnostics")
    print(f"status: {result.get('status')}")
    print(f"Mode: {result.get('mode')}")
    print(f"GoalStatus: {result.get('GoalStatus')}")
    print(f"GoalCount: {result.get('GoalCount')}")
    print(f"GeneratedEventCount: {result.get('GeneratedEventCount')}")
    print(f"EventStatus: {result.get('EventStatus')}")
    print(f"RoutedCount: {result.get('RoutedCount')}")
    print(f"ExecutedCount: {result.get('ExecutedCount')}")
    print(f"MarkedCount: {result.get('MarkedCount')}")
    print(f"DaemonStatus: {result.get('DaemonStatus')}")
    print(f"DaemonSafeToContinue: {result.get('DaemonSafeToContinue')}")
    print(f"AutonomousCycleCompleted: {result.get('AutonomousCycleCompleted')}")
    print(f"SafeToContinue: {safe_to_continue}")
    print(f"LogPath: {result.get('log_path')}")


if __name__ == "__main__":
    main()