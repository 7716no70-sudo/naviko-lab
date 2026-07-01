# ============================================================
# Phase70-2 RecoveryPolicy Diagnostics
# 復旧許可ポリシー診断
# ============================================================

from navikoLAB.recovery_policy.recovery_policy import RecoveryPolicy


def main():
    policy = RecoveryPolicy()

    healthy_case = {
        "system_health": "stable",
        "health_score": 0.9,
        "warnings": []
    }

    critical_case = {
        "system_health": "critical",
        "health_score": 0.1,
        "warnings": ["low_stability"]
    }

    healthy_result = policy.evaluate(
        healthy_case,
        {"stability": 0.8},
        {"status": "found"}
    )

    critical_result = policy.evaluate(
        critical_case,
        {"stability": 0.1},
        {"status": "found"}
    )

    no_snapshot_result = policy.evaluate(
        critical_case,
        {"stability": 0.1},
        {"status": "empty"}
    )

    print("=== RecoveryPolicy Diagnostics ===")

    print("--- Healthy Case ---")
    print("status:", healthy_result.get("status"))
    print("allowed:", healthy_result.get("allowed"))
    print("reasons:", healthy_result.get("reasons"))

    print("--- Critical Case ---")
    print("status:", critical_result.get("status"))
    print("allowed:", critical_result.get("allowed"))
    print("reasons:", critical_result.get("reasons"))

    print("--- No Snapshot Case ---")
    print("status:", no_snapshot_result.get("status"))
    print("allowed:", no_snapshot_result.get("allowed"))
    print("reasons:", no_snapshot_result.get("reasons"))


if __name__ == "__main__":
    main()