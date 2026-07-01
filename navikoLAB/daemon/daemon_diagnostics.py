from navikoLAB.daemon.daemon_scheduler import DaemonScheduler


def main():
    scheduler = DaemonScheduler(interval_seconds=1, max_cycles=3)
    result = scheduler.run()

    completed_cycles = [
        c for c in result.get("cycle_results", [])
        if c.get("status") == "completed"
    ]

    safe_cycles = [
        c for c in result.get("cycle_results", [])
        if c.get("safe_to_continue") is True
    ]

    all_cycles_completed = len(completed_cycles) == result.get("max_cycles")
    all_cycles_safe = len(safe_cycles) == result.get("max_cycles")

    safe_to_continue = (
        result.get("status") == "completed"
        and all_cycles_completed
        and all_cycles_safe
        and result.get("autonomous_execution_allowed") is False
        and result.get("external_operation_allowed") is False
        and result.get("original_write_allowed") is False
        and result.get("file_delete_allowed") is False
    )

    print("=== Daemon Diagnostics ===")
    print("phase: Phase74-3 Daemon Diagnostics")
    print(f"status: {result.get('status')}")
    print(f"Mode: {result.get('mode')}")
    print(f"MaxCycles: {result.get('max_cycles')}")
    print(f"CompletedCycles: {len(completed_cycles)}")
    print(f"SafeCycles: {len(safe_cycles)}")
    print(f"AllCyclesCompleted: {all_cycles_completed}")
    print(f"AllCyclesSafe: {all_cycles_safe}")
    print(f"AutonomousExecutionAllowed: {result.get('autonomous_execution_allowed')}")
    print(f"ExternalOperationAllowed: {result.get('external_operation_allowed')}")
    print(f"OriginalWriteAllowed: {result.get('original_write_allowed')}")
    print(f"FileDeleteAllowed: {result.get('file_delete_allowed')}")
    print(f"SafeToContinue: {safe_to_continue}")
    print(f"LogPath: {result.get('log_path')}")


if __name__ == "__main__":
    main()