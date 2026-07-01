from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

TARGET_FILES = [
    ROOT / "navikoLAB" / "reflection" / "multi_ai_reflection.py",
    ROOT / "navikoLAB" / "improvements" / "multi_ai_improvement_request.py",
]


def print_context(lines, index, radius=6):
    start = max(0, index - radius)
    end = min(len(lines), index + radius + 1)

    for i in range(start, end):
        marker = ">>" if i == index else "  "
        print(f"{marker} {i + 1}: {lines[i].rstrip()}")


def inspect(path: Path):
    print(f"=== FILE: {path} ===")

    if not path.exists():
        print("見つかりません。")
        return

    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()

    for index, line in enumerate(lines):
        if "class " in line or "def " in line:
            print_context(lines, index)
            print("")


def main():
    print("=== MultiAI API確認 ===")
    for path in TARGET_FILES:
        inspect(path)


if __name__ == "__main__":
    main()