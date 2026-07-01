import json
from pathlib import Path
from datetime import datetime

from navikoLAB.backup_verification.backup_verification_manager import BackupVerificationManager
from navikoLAB.backup_verification.backup_integrity_check import BackupIntegrityCheck


def main():
    verification = BackupVerificationManager().verify()
    integrity = BackupIntegrityCheck().run()

    safe_to_continue = (
        verification.get("status") == "completed"
        and integrity.get("status") == "completed"
    )

    report = {
        "status": "completed",
        "phase": "Phase73-4 Backup Verification Completion Report",
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "BackupDirectoryExists": verification.get("backup_directory_exists"),
        "BackupCount": verification.get("backup_count"),
        "LatestBackup": verification.get("latest_backup"),
        "VerificationPassed": verification.get("verification_passed"),
        "BackupFound": integrity.get("backup_found"),
        "IntegrityPassed": integrity.get("integrity_passed"),
        "MissingItems": integrity.get("missing_items"),
        "SafeToContinue": safe_to_continue,
        "NextPhase": "Phase74 Autonomous Daemon Loop",
    }

    report_dir = Path("navikoLAB/backup_verification/reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / (
        f"backup_verification_completion_report_{report['timestamp']}.json"
    )

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("=== Backup Verification Completion Report ===")
    for k, v in report.items():
        print(f"{k}: {v}")

    print(f"ReportPath: {report_path}")


if __name__ == "__main__":
    main()