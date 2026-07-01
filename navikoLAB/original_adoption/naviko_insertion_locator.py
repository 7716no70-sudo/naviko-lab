from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NAVIKO_FILE = ROOT / "naviko.py"


SEARCH_KEYWORDS = [
    "import ",
    "from ",
    "def open_custom_chat_window",
    "def build_system_prompt",
    "def remember_conversation",
    "def analyze_self_status",
    "if __name__ == \"__main__\"",
    "if __name__ == '__main__'",
]


def print_context(lines: list[str], line_index: int, radius: int = 5) -> None:
    start = max(0, line_index - radius)
    end = min(len(lines), line_index + radius + 1)

    for i in range(start, end):
        marker = ">>" if i == line_index else "  "
        print(f"{marker} {i + 1}: {lines[i].rstrip()}")


def main() -> None:
    print("=== naviko.py 挿入位置診断 ===")
    print(f"対象: {NAVIKO_FILE}")

    if not NAVIKO_FILE.exists():
        print("ERROR: naviko.py が見つかりません。")
        return

    lines = NAVIKO_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()

    print(f"総行数: {len(lines)}")
    print("")

    for keyword in SEARCH_KEYWORDS:
        print(f"--- 検索: {keyword} ---")
        found = False

        for index, line in enumerate(lines):
            if keyword in line:
                found = True
                print_context(lines, index)
                print("")
                break

        if not found:
            print("見つかりませんでした。")
            print("")


if __name__ == "__main__":
    main()