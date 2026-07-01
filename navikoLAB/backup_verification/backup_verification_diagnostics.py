from navikoLAB.backup_verification.backup_verification_manager import BackupVerificationManager


def main():
    manager = BackupVerificationManager()
    result = manager.verify()

    safe_to_continue = (
        result.get("status") == "completed"
    )

    print("=== Backup Verification Diagnostics ===")
    print("phase: Phase73-2 Backup Verification Diagnostics")
    print(f"status: {result.get('status')}")
    print(f"BackupDirectoryExists: {result.get('backup_directory_exists')}")
    print(f"BackupCount: {result.get('backup_count')}")
    print(f"LatestBackup: {result.get('latest_backup')}")
    print(f"VerificationPassed: {result.get('verification_passed')}")
    print(f"LogPath: {result.get('log_path')}")
    print(f"SafeToContinue: {safe_to_continue}")


if __name__ == "__main__":
    main()