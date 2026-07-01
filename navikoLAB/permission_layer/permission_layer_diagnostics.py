from navikoLAB.permission_layer.permission_enforcement import PermissionEnforcement


def main():
    enforcement = PermissionEnforcement()

    allowed_tests = [
        "dry_run_cycle",
        "health_check",
    ]

    blocked_tests = [
        "external_operation",
        "original_write",
        "file_delete",
        "real_gui_operation",
        "browser_operation",
        "auto_execute",
    ]

    allowed_results = [
        enforcement.request(op)
        for op in allowed_tests
    ]

    blocked_results = [
        enforcement.request(op)
        for op in blocked_tests
    ]

    allowed_passed = all(
        r.get("allowed") is True and r.get("executed") is True
        for r in allowed_results
    )

    blocked_passed = all(
        r.get("allowed") is False
        and r.get("blocked") is True
        and r.get("executed") is False
        for r in blocked_results
    )

    safe_to_continue = allowed_passed and blocked_passed

    print("=== Permission Layer Diagnostics ===")
    print("phase: Phase82-3 Permission Layer Diagnostics")
    print(f"AllowedTestCount: {len(allowed_results)}")
    print(f"BlockedTestCount: {len(blocked_results)}")
    print(f"AllowedPassed: {allowed_passed}")
    print(f"BlockedPassed: {blocked_passed}")
    print(f"PermissionLayerEnforced: {safe_to_continue}")
    print(f"SafeToContinue: {safe_to_continue}")


if __name__ == "__main__":
    main()