from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LAB_DIR = ROOT / "navikoLAB"

KEYWORDS = [
    "AutonomousCapabilityFlow",
    "autonomous_capability_flow",
    "run_autonomous",
    "run_capability",
    "safe_simulation",
    "MissionCapabilityBridge",
    "MultiAIOrchestrator",
]


def scan_file(path: Path) -> list[str]:
    results = []
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return results

    for index, line in enumerate(lines):
        for keyword in KEYWORDS:
            if keyword in line:
                start = max(0, index - 3)
                end = min(len(lines), index + 4)

                block = [f"FILE: {path}"]
                for i in range(start, end):
                    marker = ">>" if i == index else "  "
                    block.append(f"{marker} {i + 1}: {lines[i]}")
                results.append("\n".join(block))
                break

    return results


def main() -> None:
    print("=== AutonomousCapabilityFlow 実体確認 ===")
    print(f"対象: {LAB_DIR}")

    if not LAB_DIR.exists():
        print("ERROR: navikoLAB が見つかりません。")
        return

    all_results = []

    for path in LAB_DIR.rglob("*.py"):
        if "__pycache__" in str(path):
            continue
        all_results.extend(scan_file(path))

    if not all_results:
        print("関連コードは見つかりませんでした。")
        return

    for result in all_results[:80]:
        print(result)
        print("-" * 60)

    if len(all_results) > 80:
        print(f"※ 結果が多いため80件で停止。総件数: {len(all_results)}")


if __name__ == "__main__":
    main()