from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "navikoLAB" / "capabilities" / "capability_router.py"


def main():
    print("=== CapabilityRouter Core Inspector ===")
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
    for i, line in enumerate(lines[:40], 1):
        print(f"{i}: {line}")


if __name__ == "__main__":
    main()