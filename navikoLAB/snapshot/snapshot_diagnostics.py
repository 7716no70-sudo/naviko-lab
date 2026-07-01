# ============================================================
# Phase68-2 Snapshot Diagnostics
# 復元ポイント診断コマンド
# ============================================================

from navikoLAB.snapshot.snapshot_manager import SnapshotManager


def main():
    manager = SnapshotManager()

    summary = manager.summary()
    latest = manager.latest()

    print("=== Snapshot Diagnostics ===")
    print("status:", summary.get("status"))
    print("snapshot_count:", summary.get("snapshot_count"))

    print("--- Latest Snapshot ---")
    print("latest_status:", latest.get("status"))

    snapshot = latest.get("snapshot")

    if snapshot:
        print("name:", snapshot.get("name"))
        print("path:", snapshot.get("path"))
        print("modified_at:", snapshot.get("modified_at"))
    else:
        print("name:", None)
        print("path:", None)
        print("modified_at:", None)


if __name__ == "__main__":
    main()