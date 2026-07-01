from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "navikoLAB" / "task_planner.py"


def main() -> None:
    print("=== TaskPlanner Source Inspector ===")
    print("対象:", TARGET)

    if not TARGET.exists():
        print("状態: missing")
        return

    text = TARGET.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    print("状態: found")
    print("LineCount:", len(lines))
    print("---- def lines ----")

    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("def ") or stripped.startswith("class "):
            print(f"{index}: {line}")

    print("---- import area ----")
    for index, line in enumerate(lines[:40], start=1):
        print(f"{index}: {line}")


if __name__ == "__main__":
    main()