from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "navikoLAB" / "connectors" / "connector_dispatcher.py"


def main() -> None:
    print("=== ConnectorDispatcher Source Inspector ===")
    print("対象:", TARGET)

    if not TARGET.exists():
        print("状態: missing")
        return

    text = TARGET.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    print("状態: found")
    print("LineCount:", len(lines))

    print("---- def/class ----")
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("def ") or line.strip().startswith("class "):
            print(f"{i}: {line}")

    print("---- import area ----")
    for i, line in enumerate(lines[:50], 1):
        print(f"{i}: {line}")


if __name__ == "__main__":
    main()