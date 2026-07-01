# ============================================================
# Phase70-6 Restore Diagnostics
# Snapshot Validation 表示強化
# ============================================================

from navikoLAB.snapshot.snapshot_manager import SnapshotManager


def main():
    manager = SnapshotManager()

    result = manager.restore_latest_to(
        restore_root="navikoLAB/restore_test"
    )

    validation = result.get("validation", {})

    print("=== Restore Diagnostics ===")
    print("status:", result.get("status"))
    print("source:", result.get("source"))
    print("restore_root:", result.get("restore_root"))
    print("snapshot_name:", result.get("snapshot_name"))
    print("reason:", result.get("reason"))

    print("--- Snapshot Validation ---")
    print("validation_status:", validation.get("status"))
    print("valid:", validation.get("valid"))
    print("path:", validation.get("path"))
    print("missing:", validation.get("missing"))


if __name__ == "__main__":
    main()