from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NAVIKO_FILE = ROOT / "naviko.py"


KEYWORDS = [
    "def open_custom_chat_window():",
    "tk.Button",
    "Button(",
    "send",
    "chat",
    "command=",
    "pack(",
    "grid(",
]


def print_context(lines: list[str], index: int, radius: int = 8) -> None:
    start = max(0, index - radius)
    end = min(len(lines), index + radius + 1)

    for i in range(start, end):
        marker = ">>" if i == index else "  "
        print(f"{marker} {i + 1}: {lines[i].rstrip()}")


def main() -> None:
    print("=== GUIボタン挿入位置診断 ===")
    print(f"対象: {NAVIKO_FILE}")

    if not NAVIKO_FILE.exists():
        print("ERROR: naviko.py が見つかりません。")
        return

    lines = NAVIKO_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()
    print(f"総行数: {len(lines)}")
    print("")

    for keyword in KEYWORDS:
        print(f"--- 検索: {keyword} ---")
        count = 0

        for index, line in enumerate(lines):
            if keyword in line:
                print_context(lines, index)
                print("")
                count += 1

                if count >= 5:
                    print("※ 多いため5件で停止")
                    print("")
                    break

        if count == 0:
            print("見つかりませんでした。")
            print("")


if __name__ == "__main__":
    main()