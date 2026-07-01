# ============================================================
# Phase69-2 Recovery Diagnostics
# 自動復旧診断コマンド
# ============================================================

from navikoLAB.recovery.recovery_manager import RecoveryManager


def main():
    manager = RecoveryManager()

    healthy_case = {
        "system_health": "stable",
        "health_score": 0.9,
        "warnings": []
    }

    critical_case = {
        "system_health": "critical",
        "health_score": 0.2,
        "warnings": ["low_stability"]
    }

    healthy_result = manager.run(
        healthy_case,
        {"stability": 0.8}
    )

    critical_result = manager.run(
        critical_case,
        {"stability": 0.2}
    )

    print("=== Recovery Diagnostics ===")

    print("--- Healthy Case ---")
    print("status:", healthy_result.get("status"))
    print("reason:", healthy_result.get("reason"))

    print("--- Critical Case ---")
    print("status:", critical_result.get("status"))

    recovery = critical_result.get("recovery", {})
    print("recovery_status:", recovery.get("status"))
    print("source:", recovery.get("source"))
    print("restore_root:", recovery.get("restore_root"))
    print("snapshot_name:", recovery.get("snapshot_name"))


if __name__ == "__main__":
    main()