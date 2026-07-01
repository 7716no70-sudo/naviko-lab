# ============================================================
# Phase68-1 SnapshotManager
# 復元ポイント管理
# ============================================================

from pathlib import Path
from datetime import datetime
from pathlib import Path
from datetime import datetime
import shutil

class SnapshotManager:

    def __init__(self, backup_root="navikoLAB/backups"):
        self.backup_root = Path(backup_root)
        self.snapshot_index = []

    def scan_snapshots(self):
        if not self.backup_root.exists():
            return []

        snapshots = [
            p for p in self.backup_root.iterdir()
            if p.is_dir() and "snapshot_" in p.name
        ]

        snapshots.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        self.snapshot_index = [
            {
                "name": p.name,
                "path": str(p),
                "modified_at": datetime.fromtimestamp(
                    p.stat().st_mtime
                ).strftime("%Y%m%d_%H%M%S")
            }
            for p in snapshots
        ]

        return self.snapshot_index

    def latest(self):
        snapshots = self.scan_snapshots()

        if not snapshots:
            return {
                "status": "empty",
                "snapshot": None
            }

        return {
            "status": "found",
            "snapshot": snapshots[0]
        }

    def validate_snapshot(self, snapshot_path):
        snapshot_path = Path(snapshot_path)

        required_dirs = [
            "memory",
            "goal",
            "identity",
            "planning",
            "evolution",
            "monitoring",
            "stability",
            "autonomy"
        ]

        missing = []

        if not snapshot_path.exists():
            return {
                "status": "invalid",
                "valid": False,
                "reason": "snapshot_path_not_found",
                "path": str(snapshot_path),
                "missing": required_dirs
            }

        for dirname in required_dirs:
            if not (snapshot_path / dirname).exists():
                missing.append(dirname)

        valid = len(missing) == 0

        return {
            "status": "valid" if valid else "invalid",
            "valid": valid,
            "path": str(snapshot_path),
            "required": required_dirs,
            "missing": missing
        }

    def restore_latest_to(self, restore_root="navikoLAB/restore_test"):
        latest = self.latest()

        if latest.get("status") != "found":
            return {
                "status": "failed",
                "reason": "no_snapshot_found"
            }

        snapshot = latest.get("snapshot")
        snapshot_path = Path(snapshot.get("path"))
        restore_root = Path(restore_root)

        validation = self.validate_snapshot(snapshot_path)

        if not validation.get("valid"):
            return {
                "status": "failed",
                "reason": "invalid_snapshot",
                "validation": validation
            }

        if restore_root.exists():
            shutil.rmtree(restore_root)

        shutil.copytree(snapshot_path, restore_root)

        return {
            "status": "completed",
            "source": str(snapshot_path),
            "restore_root": str(restore_root),
            "snapshot_name": snapshot.get("name"),
            "validation": validation
        }

    def summary(self):
        snapshots = self.scan_snapshots()

        return {
            "status": "completed",
            "snapshot_count": len(snapshots),
            "latest": snapshots[0] if snapshots else None
        }