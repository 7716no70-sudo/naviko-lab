import json
from pathlib import Path
from datetime import datetime

from navikoLAB.external_backup.external_backup_manager import ExternalBackupManager


def main():
    manager = ExternalBackupManager()
    result = manager.run()

    safe_to_continue = (
        result.get("status") == "completed"
        or result.get("error") in (
            "external_backup_disabled",
            "external_backup_path_not_found",
        )
    )

    report = {
        "status": "completed",
        "phase": "Phase72-4 External Backup Completion Report",
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "ExternalBackupEnabled": result.get("external_backup_enabled"),
        "ExternalPathFound": result.get("external_path_found"),
        "BackupCreated": result.get("backup_created"),
        "BackupPath": result.get("backup_path"),
        "LastStatus": result.get("status"),
        "LastError": result.get("error"),
        "SafeToContinue": safe_to_continue,
        "NextPhase": "Phase73 Backup Verification",
    }

    report_dir = Path("navikoLAB/external_backup/reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / (
        f"external_backup_completion_report_{report['timestamp']}.json"
    )

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("=== External Backup Completion Report ===")
    for key, value in report.items():
        print(f"{key}: {value}")

    print(f"ReportPath: {report_path}")


if __name__ == "__main__":
    main()