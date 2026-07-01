from pathlib import Path
import shutil


def main():
    print("=== Copy AppOperator Components ===")

    root = Path(__file__).resolve().parents[1]
    src_dir = root / "connectors"
    dst_dir = root / "app_operator" / "components"
    dst_dir.mkdir(parents=True, exist_ok=True)

    files = [
        "window_inspector.py",
        "explorer_operation_planner.py",
        "keyboard_input_planner.py",
        "mouse_click_planner.py",
    ]

    for filename in files:
        src = src_dir / filename
        dst = dst_dir / filename

        if not src.exists():
            print("Missing:", src)
            continue

        shutil.copy2(src, dst)
        print("Copied:", src, "->", dst)

    print("状態: completed")
    print("次工程: Update RealAppOperatorConnector imports")


if __name__ == "__main__":
    main()