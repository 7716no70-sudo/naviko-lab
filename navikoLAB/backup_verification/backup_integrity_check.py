from pathlib import Path
from datetime import datetime
import json


class BackupIntegrityCheck:
    def __init__(self):
        self.backup_dir = Path("navikoLAB/backup/backups")
        self.log_dir = Path("navikoLAB/backup_verification/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # バックアップ内に最低限存在してほしいディレクトリ
        self.required_items = [
            "memory",
            "goal",
            "identity",
            "stability",
            "monitoring",
        ]

    def run(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        result = {
            "status": "completed",
            "phase": "Phase73-3 Backup Integrity Check",
            "timestamp": timestamp,
            "backup_found": False,
            "latest_backup": None,
            "missing_items": [],
            "integrity_passed": False,
        }

        if not self.backup_dir.exists():
            return self._save(result)

        backups = sorted(
            [p for p in self.backup_dir.iterdir() if p.is_dir()],
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

        if not backups:
            return self._save(result)

        latest = backups[0]
        result["backup_found"] = True
        result["latest_backup"] = str(latest)

        missing = [
            item for item in self.required_items
            if not (latest / item).exists()
        ]

        result["missing_items"] = missing
        result["integrity_passed"] = len(missing) == 0

        return self._save(result)

    def _save(self, result):
        log_path = (
            self.log_dir /
            f"backup_integrity_check_{result['timestamp']}.json"
        )

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["log_path"] = str(log_path)
        return result


if __name__ == "__main__":
    checker = BackupIntegrityCheck()
    report = checker.run()

    print("=== Backup Integrity Check ===")
    for k, v in report.items():
        print(f"{k}: {v}")