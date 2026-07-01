from pathlib import Path
from datetime import datetime
import json


class BackupVerificationManager:
    def __init__(self):
        self.backup_dir = Path("navikoLAB/backup/backups")
        self.log_dir = Path("navikoLAB/backup_verification/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def verify(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        result = {
            "status": "completed",
            "phase": "Phase73-1 Backup Verification Manager",
            "timestamp": timestamp,
            "backup_directory_exists": False,
            "backup_count": 0,
            "latest_backup": None,
            "verification_passed": False,
        }

        if self.backup_dir.exists():
            result["backup_directory_exists"] = True

            backups = sorted(
                [p for p in self.backup_dir.iterdir() if p.is_dir()],
                key=lambda x: x.stat().st_mtime,
                reverse=True,
            )

            result["backup_count"] = len(backups)

            if backups:
                result["latest_backup"] = str(backups[0])
                result["verification_passed"] = True

        log_path = (
            self.log_dir
            / f"backup_verification_{timestamp}.json"
        )

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["log_path"] = str(log_path)

        return result


if __name__ == "__main__":
    manager = BackupVerificationManager()
    report = manager.verify()

    print("=== Backup Verification Manager ===")
    for k, v in report.items():
        print(f"{k}: {v}")