from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

TARGET_FILES = [
    ROOT / "naviko.py",
    ROOT / "navikoLAB" / "original_adoption" / "original_bridge.py",
    ROOT / "navikoLAB" / "mission" / "mission_dashboard.py",
    ROOT / "navikoLAB" / "missions" / "mission_dashboard.py",
]


KEYWORDS = [
    "Mission Dashboard",
    "AIミッション開始",
    "ミッション",
    "Button",
    "tk.Button",
    "connector",
    "Connector",
]


def print_context(path, line_no, before=8, after=12):
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()

    start = max(1, line_no - before)
    end = min(len(lines), line_no + after)

    print("")
    print(f"--- {path} : L{line_no} ---")

    for i in range(start, end + 1):
        prefix = ">>" if i == line_no else "  "
        print(f"{prefix} {i}: {lines[i - 1]}")


def scan_file(path):
    if not path.exists():
        print(f"なし: {path}")
        return

    print("")
    print(f"=== scan: {path} ===")

    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    print(f"総行数: {len(lines)}")

    hit_count = 0

    for index, line in enumerate(lines, start=1):
        for keyword in KEYWORDS:
            if keyword in line:
                hit_count += 1
                print(
                    f"{path}:{index} "
                    f"[{keyword}] {line.strip()}"
                )

    if hit_count == 0:
        print("該当キーワードなし")

    shown = 0

    for index, line in enumerate(lines, start=1):
        if (
            "AIミッション開始" in line
            or "Mission Dashboard" in line
            or "tk.Button" in line
            or "Button(" in line
        ):
            print_context(path, index)
            shown += 1

        if shown >= 10:
            break


def main():
    print("=== Connector GUI Button Locator ===")

    for path in TARGET_FILES:
        scan_file(path)


if __name__ == "__main__":
    main()