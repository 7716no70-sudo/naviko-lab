from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.analyzers.analyzer_diagnostics import run_analyzer_diagnostics


def create_analyzer_completion_report(root_dir=None) -> dict:
    root = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
    report_dir = root / "navikoLAB" / "analyzers" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    diagnostics = run_analyzer_diagnostics(root_dir=root)

    completed_items = [
        "FolderAnalyzer read-only project structure analysis",
        "PythonAnalyzer AST-based syntax/function/import analysis",
        "AppAnalyzer integrated app analysis",
        "RequirementsAnalyzer dependency file analysis",
        "Analyzer Diagnostics",
    ]

    report = {
        "title": "Analyzer Completion Report",
        "status": "completed" if diagnostics.get("status") == "passed" else "needs_review",
        "phase": "第28工程 AppAnalyzer / FolderAnalyzer / PythonAnalyzer",
        "created_at": now,
        "completed_items": completed_items,
        "diagnostics_status": diagnostics.get("status"),
        "diagnostics_report": diagnostics.get("report_path"),
        "next_recommended_phase": "第29工程 ArchitectureAnalyzer / DependencyAnalyzer",
        "architecture": {
            "folder_analysis": "FolderAnalyzer -> project structure summary",
            "python_analysis": "PythonAnalyzer -> AST syntax / functions / imports",
            "app_analysis": "AppAnalyzer -> FolderAnalyzer + PythonAnalyzer + KnowledgeBase + ExperienceManager",
            "requirements_analysis": "RequirementsAnalyzer -> requirements.txt / pyproject.toml scan",
            "future_flow": "AppAnalyzer -> ArchitectureAnalyzer -> DependencyAnalyzer -> AutoDocumentation -> AutoImprovementSuggestion",
        },
        "safety": {
            "mode": "read_only",
            "file_editing": False,
            "file_deletion": False,
            "external_access": False,
            "note": "第28工程のAnalyzerは読み取り専用。プロジェクト解析のみ実行。",
        },
    }

    report_path = report_dir / f"analyzer_completion_report_{now}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report["report_path"] = str(report_path)
    return report


def main() -> None:
    print("=== Analyzer Completion Report ===")

    report = create_analyzer_completion_report()

    print(f"状態: {report.get('status')}")
    print(f"工程: {report.get('phase')}")
    print(f"診断: {report.get('diagnostics_status')}")
    print("完成項目:")

    for item in report.get("completed_items", []):
        print(f"- {item}")

    print(f"保存先: {report.get('report_path')}")
    print(f"次工程: {report.get('next_recommended_phase')}")


if __name__ == "__main__":
    main()