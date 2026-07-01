# ============================================================
# Phase69-5 Recovery Force Test
# 強制Recoveryテスト診断
# ============================================================

from navikoLAB.recovery.recovery_manager import RecoveryManager


def main():
    manager = RecoveryManager()

    force_critical_health = {
        "system_health": "critical",
        "health_score": 0.1,
        "warnings": [
            "low_stability",
            "identity_unstable",
            "memory_growth_high"
        ]
    }

    force_stability = {
        "stability": 0.1,
        "expand_allowed": False
    }

    result = manager.run(
        force_critical_health,
        force_stability
    )

    print("=== Recovery Force Test ===")
    print("status:", result.get("status"))

    recovery = result.get("recovery", {})
    print("recovery_status:", recovery.get("status"))
    print("source:", recovery.get("source"))
    print("restore_root:", recovery.get("restore_root"))
    print("snapshot_name:", recovery.get("snapshot_name"))


if __name__ == "__main__":
    main()