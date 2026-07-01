from navikoLAB.external_backup.external_backup_manager import ExternalBackupManager


def main():
    manager = ExternalBackupManager()
    result = manager.run()

    print("=== External Backup Diagnostics ===")
    print(f"status: {result.get('status')}")
    print("phase: Phase72-3 External Backup Diagnostics")
    print(f"ExternalBackupEnabled: {result.get('external_backup_enabled')}")
    print(f"ExternalPathFound: {result.get('external_path_found')}")
    print(f"BackupCreated: {result.get('backup_created')}")
    print(f"BackupPath: {result.get('backup_path')}")
    print(f"Error: {result.get('error')}")
    print(f"LogPath: {result.get('log_path')}")

    safe_to_continue = (
        result.get("status") == "completed"
        or result.get("error") == "external_backup_disabled"
        or result.get("error") == "external_backup_path_not_found"
    )

    print(f"SafeToContinue: {safe_to_continue}")


if __name__ == "__main__":
    main()