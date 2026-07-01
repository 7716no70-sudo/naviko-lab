from pathlib import Path
import shutil
import json
from datetime import datetime

from navikoLAB.external_backup.external_backup_config import ExternalBackupConfig


class ExternalBackupManager:
    def __init__(self):
        self.config = ExternalBackupConfig()
        self.project_root = Path("navikoLAB")
        self.log_dir = Path("navikoLAB/external_backup/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def _read_config_status(self):
        if hasattr(self.config, "run"):
            return self.config.run()

        if hasattr(self.config, "diagnose"):
            return self.config.diagnose()

        if hasattr(self.config, "build"):
            return self.config.build()

        enabled = getattr(self.config, "enabled", False)
        path = getattr(self.config, "external_backup_path", None) or getattr(self.config, "path", None)

        return {
            "enabled": enabled,
            "path": path,
            "path_exists": Path(path).exists() if path else False,
        }

    def run(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        result = {
            "status": "blocked",
            "phase": "Phase72-2 ExternalBackupManager",
            "timestamp": timestamp,
            "external_backup_enabled": False,
            "external_path_found": False,
            "backup_created": False,
            "backup_path": None,
            "error": None,
        }

        config_status = self._read_config_status()

        result["external_backup_enabled"] = config_status.get("enabled", False)
        result["external_path_found"] = config_status.get("path_exists", False)

        if not result["external_backup_enabled"]:
            result["error"] = "external_backup_disabled"
            return self._save_log(result)

        if not result["external_path_found"]:
            result["error"] = "external_backup_path_not_found"
            return self._save_log(result)

        external_root = Path(config_status["path"])
        backup_root = external_root / "NavikoLAB_external_backups"
        backup_root.mkdir(parents=True, exist_ok=True)

        backup_path = backup_root / f"navikoLAB_backup_{timestamp}"

        ignore = shutil.ignore_patterns(
            "__pycache__",
            "*.pyc",
            ".git",
            ".venv",
            "venv",
            "node_modules",
        )

        shutil.copytree(
            self.project_root,
            backup_path,
            ignore=ignore,
        )

        result["status"] = "completed"
        result["backup_created"] = True
        result["backup_path"] = str(backup_path)

        return self._save_log(result)

    def _save_log(self, result):
        log_path = self.log_dir / f"external_backup_manager_{result['timestamp']}.json"

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["log_path"] = str(log_path)
        return result


if __name__ == "__main__":
    manager = ExternalBackupManager()
    report = manager.run()

    print("=== External Backup Manager ===")
    for k, v in report.items():
        print(f"{k}: {v}")