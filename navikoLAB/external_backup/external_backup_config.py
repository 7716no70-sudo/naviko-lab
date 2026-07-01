# ============================================================
# Phase72-1 External Backup Config
# 外付けHDDバックアップ設定
# ============================================================

from pathlib import Path


class ExternalBackupConfig:

    def __init__(self):
        self.enabled = False
        self.external_backup_root = None

    def set_path(self, path):
        backup_path = Path(path)

        return {
            "status": "configured",
            "enabled": self.enabled,
            "path": str(backup_path),
            "exists": backup_path.exists(),
            "ready": backup_path.exists() and backup_path.is_dir()
        }

    def enable(self, path):
        backup_path = Path(path)

        if not backup_path.exists() or not backup_path.is_dir():
            return {
                "status": "failed",
                "reason": "external_path_not_found",
                "path": str(backup_path),
                "enabled": False
            }

        self.enabled = True
        self.external_backup_root = backup_path

        return {
            "status": "enabled",
            "path": str(backup_path),
            "enabled": True
        }

    def disable(self):
        self.enabled = False
        self.external_backup_root = None

        return {
            "status": "disabled",
            "enabled": False
        }

    def status(self):
        return {
            "enabled": self.enabled,
            "path": str(self.external_backup_root) if self.external_backup_root else None
        }