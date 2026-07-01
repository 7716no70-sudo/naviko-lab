from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.analyzers.improvement_diagnostics import ImprovementDiagnostics


ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "analyzers" / "reports"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    diagnostics = ImprovementDiagnostics().run()

    result = {
        "status": "completed" if diagnostics["status"] == "passed" else "warning",
        "stage": "第31工程 AutoImprovementSuggestion / AutoRefactoringPlan / ArchitectureReflection",
        "diagnostics": diagnostics,
        "completed_items": [
            "AutoImprovementSuggestion",
            "AutoRefactoringPlan",
            "ArchitectureReflection",
            "ImprovementDiagnostics",
            "ImprovementCompletionReport",
        ],
        "next_stage": "第32工程 Original Naviko統合 / Mission→Research→Search→Knowledge→Reflection→Improvement完全接続",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }

    output = REPORT_DIR / f"improvement_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Improvement Completion Report ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['stage']}")
    print(f"改善候補数: {diagnostics['suggestion_count']}")
    print(f"計画数: {diagnostics['plan_count']}")
    print(f"設計反省数: {diagnostics['reflection_count']}")
    print(f"不足候補: {len(diagnostics['missing'])}")
    print(f"保存先: {output}")
    print(f"次工程: {result['next_stage']}")


if __name__ == "__main__":
    main()