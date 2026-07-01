from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]

TARGETS = [
    ROOT / "navikoLAB" / "core" / "mission_capability_bridge.py",
    ROOT / "navikoLAB" / "capabilities" / "agent_manager.py",
]


def inspect_file(path: Path) -> None:
    print("================================")
    print("対象:", path)

    if not path.exists():
        print("状態: missing")
        return

    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    print("状態: found")
    print("LineCount:", len(lines))

    print("---- def/class lines ----")
    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("def ") or stripped.startswith("class "):
            print(f"{index}: {line}")

    print("---- import area ----")
    for index, line in enumerate(lines[:40], start=1):
        print(f"{index}: {line}")


def main() -> None:
    print("=== CapabilityRouter Source Inspector ===")
    for target in TARGETS:
        inspect_file(target)


if __name__ == "__main__":
    main()