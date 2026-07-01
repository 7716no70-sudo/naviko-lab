from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TARGET_FILES = [
    ROOT / "navikoLAB" / "capabilities" / "agent_executor.py",
    ROOT / "navikoLAB" / "capabilities" / "agent_manager.py",
    ROOT / "navikoLAB" / "capabilities" / "capability_registry.py",
    ROOT / "navikoLAB" / "capabilities" / "capability_router.py",
]


KEYWORDS = [
    "class AgentExecutor",
    "def ",
    "execute",
    "run",
    "chatgpt",
    "app_operator",
    "mock",
    "agent_id",
    "capability",
]


def print_context(lines: list[str], index: int, radius: int = 5) -> None:
    start = max(0, index - radius)
    end = min(len(lines), index + radius + 1)

    for i in range(start, end):
        marker = ">>" if i == index else "  "
        print(f"{marker} {i + 1}: {lines[i].rstrip()}")


def inspect_file(path: Path) -> None:
    print(f"=== FILE: {path} ===")

    if not path.exists():
        print("見つかりません。")
        print("")
        return

    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    print(f"総行数: {len(lines)}")

    for keyword in KEYWORDS:
        print(f"--- 検索: {keyword} ---")
        count = 0

        for index, line in enumerate(lines):
            if keyword in line:
                print_context(lines, index)
                print("")
                count += 1

                if count >= 8:
                    print("※ 多いため8件で停止")
                    print("")
                    break

        if count == 0:
            print("見つかりませんでした。")
            print("")


def main() -> None:
    print("=== AgentExecutor / Capability 接続構造確認 ===")
    for path in TARGET_FILES:
        inspect_file(path)


if __name__ == "__main__":
    main()