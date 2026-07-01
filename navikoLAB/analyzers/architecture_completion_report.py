from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.analyzers.architecture_diagnostics import run_architecture_diagnostics


def create_architecture_completion_report(root_dir=None) -> dict:
    root = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
    report_dir = root / "navikoLAB" / "analyzers" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    diagnostics = run_architecture_diagnostics(root_dir=root)

    architecture_report = diagnostics.get("architecture_report", {})
    dependency_report = diagnostics.get("dependency_report", {})

    completed_items = [
        "DependencyAnalyzer import / requirements analysis",
        "ArchitectureAnalyzer layer / architecture style analysis",
        "Architecture / Dependency Diagnostics",
        "Architecture knowledge save",
        "Architecture experience save",
    ]

    report = {
        "title": "Architecture / Dependency Completion Report",
        "status": "completed" if diagnostics.get("status") == "passed" else "needs_review",
        "phase": "第29工程 ArchitectureAnalyzer / DependencyAnalyzer",
        "created_at": now,
        "completed_items": completed_items,
        "diagnostics_status": diagnostics.get("status"),
        "diagnostics_report": diagnostics.get("report_path"),
        "architecture_style": architecture_report.get("architecture_style"),
        "syntax_error_count": architecture_report.get("syntax_error_count"),
        "possible_missing_requirements_count": dependency_report.get("possible_missing_count"),
        "next_recommended_phase": "第30工程 AutoDocumentation / AutoTestGenerator",
        "architecture": {
            "dependency_analysis": "PythonAnalyzer + RequirementsAnalyzer -> DependencyAnalyzer",
            "architecture_analysis": "FolderAnalyzer + PythonAnalyzer + DependencyAnalyzer -> ArchitectureAnalyzer",
            "knowledge_flow": "ArchitectureAnalyzer -> KnowledgeBase",
            "experience_flow": "ArchitectureAnalyzer -> ExperienceManager",
            "future_flow": "ArchitectureAnalyzer -> AutoDocumentation -> AutoTestGenerator -> AutoImprovementSuggestion",
        },
        "safety": {
            "mode": "read_only",
            "file_editing": False,
            "file_deletion": False,
            "external_access": False,
            "note": "第29工程は読み取り専用。設計構造と依存関係の解析のみ実行。",
        },
    }

    report_path = report_dir / f"architecture_completion_report_{now}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report["report_path"] = str(report_path)
    return report


def main() -> None:
    print("=== Architecture / Dependency Completion Report ===")

    report = create_architecture_completion_report()

    print(f"状態: {report.get('status')}")
    print(f"工程: {report.get('phase')}")
    print(f"診断: {report.get('diagnostics_status')}")
    print(f"構造: {report.get('architecture_style')}")
    print(f"構文NG: {report.get('syntax_error_count')}")
    print(f"requirements不足候補: {report.get('possible_missing_requirements_count')}")
    print("完成項目:")

    for item in report.get("completed_items", []):
        print(f"- {item}")

    print(f"保存先: {report.get('report_path')}")
    print(f"次工程: {report.get('next_recommended_phase')}")


if __name__ == "__main__":
    main()