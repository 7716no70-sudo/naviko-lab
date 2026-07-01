from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.analyzers.documentation_diagnostics import DocumentationDiagnostics


ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "analyzers" / "reports"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    diagnostics = DocumentationDiagnostics().run()

    result = {
        "status": "completed" if diagnostics["status"] == "passed" else "warning",
        "stage": "第30工程 AutoDocumentation / AutoTestGenerator",
        "diagnostics": diagnostics,
        "completed_items": [
            "AutoDocumentation",
            "AutoTestGenerator",
            "DocumentationDiagnostics",
            "DocumentationCompletionReport",
        ],
        "next_stage": "第31工程 AutoImprovementSuggestion / AutoRefactoringPlan / ArchitectureReflection",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }

    output = REPORT_DIR / f"documentation_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Documentation Completion Report ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['stage']}")
    print(f"Markdown数: {diagnostics['markdown_count']}")
    print(f"JSON数: {diagnostics['json_count']}")
    print(f"Test数: {diagnostics['test_count']}")
    print(f"不足候補: {len(diagnostics['missing'])}")
    print(f"保存先: {output}")
    print(f"次工程: {result['next_stage']}")


if __name__ == "__main__":
    main()