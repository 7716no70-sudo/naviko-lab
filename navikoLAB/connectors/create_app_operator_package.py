from pathlib import Path


def main():
    print("=== Create AppOperator Package Folders ===")

    root = Path(__file__).resolve().parents[1]

    folders = [
        root / "app_operator",
        root / "app_operator" / "components",
        root / "app_operator" / "diagnostics",
        root / "app_operator" / "reports",
    ]

    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
        print("Folder OK:", folder)

    init_files = [
        root / "app_operator" / "__init__.py",
        root / "app_operator" / "components" / "__init__.py",
        root / "app_operator" / "diagnostics" / "__init__.py",
    ]

    for init_file in init_files:
        if not init_file.exists():
            init_file.write_text("", encoding="utf-8")
        print("Init OK:", init_file)

    print("状態: completed")
    print("次工程: Copy AppOperator components")


if __name__ == "__main__":
    main()