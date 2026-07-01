from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = ROOT / "navikoLAB" / "autonomous_core.py"


KEYWORDS = [
    "class AutonomousCore",
    "def ",
    "def run",
    "def execute",
    "def start",
    "AutonomousCapabilityFlow",
    "safe_simulation_completed",
]


def print_context(lines: list[str], index: int, radius: int = 6) -> None:
    start = max(0, index - radius)
    end = min(len(lines), index + radius + 1)

    for i in range(start, end):
        marker = ">>" if i == index else "  "
        print(f"{marker} {i + 1}: {lines[i].rstrip()}")


def main() -> None:
    print("=== AutonomousCore API確認 ===")
    print(f"対象: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print("ERROR: autonomous_core.py が見つかりません。")
        return

    lines = TARGET_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()
    print(f"総行数: {len(lines)}")
    print("")

    for keyword in KEYWORDS:
        print(f"--- 検索: {keyword} ---")
        found_count = 0

        for index, line in enumerate(lines):
            if keyword in line:
                print_context(lines, index)
                print("")
                found_count += 1

                if found_count >= 10:
                    print("※ 多いため10件で停止")
                    print("")
                    break

        if found_count == 0:
            print("見つかりませんでした。")
            print("")


if __name__ == "__main__":
    main()