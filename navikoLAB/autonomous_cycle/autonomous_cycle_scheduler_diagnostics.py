from navikoLAB.autonomous_cycle.autonomous_cycle_scheduler import AutonomousCycleScheduler


def main():
    result = AutonomousCycleScheduler(interval_seconds=1, max_cycles=3).run()

    safe_cycles = [
        c for c in result.get("cycle_results", [])
        if c.get("safe_to_continue") is True
    ]

    safe_to_continue = (
        result.get("status") == "completed"
        and len(safe_cycles) == result.get("max_cycles")
        and result.get("ExternalOperationAllowed") is False
        and result.get("OriginalWriteAllowed") is False
        and result.get("FileDeleteAllowed") is False
        and result.get("SafeToContinue") is True
    )

    print("=== Autonomous Cycle Scheduler Diagnostics ===")
    print("phase: Phase80-2 Autonomous Cycle Scheduler Diagnostics")
    print(f"status: {result.get('status')}")
    print(f"Mode: {result.get('mode')}")
    print(f"MaxCycles: {result.get('max_cycles')}")
    print(f"CompletedCycleCount: {result.get('completed_cycle_count')}")
    print(f"SafeCycleCount: {len(safe_cycles)}")
    print(f"ExternalOperationAllowed: {result.get('ExternalOperationAllowed')}")
    print(f"OriginalWriteAllowed: {result.get('OriginalWriteAllowed')}")
    print(f"FileDeleteAllowed: {result.get('FileDeleteAllowed')}")
    print(f"SafeToContinue: {safe_to_continue}")
    print(f"LogPath: {result.get('log_path')}")


if __name__ == "__main__":
    main()