from pathlib import Path
import shutil


def main():
    print("=== Copy AppOperator Diagnostics ===")

    root = Path(__file__).resolve().parents[1]

    src = root / "connectors" / "real_app_operator_system_diagnostics.py"
    dst = root / "app_operator" / "diagnostics" / "app_operator_system_diagnostics.py"

    dst.parent.mkdir(parents=True, exist_ok=True)

    if not src.exists():
        print("状態: failed")
        print("Missing:", src)
        return

    shutil.copy2(src, dst)

    print("Copied:", src, "->", dst)
    print("状態: completed")
    print("次工程: Run app_operator system diagnostics")


if __name__ == "__main__":
    main()