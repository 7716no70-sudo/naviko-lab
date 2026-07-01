from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.search.search_integration_diagnostics import run_search_integration_diagnostics


def create_search_completion_report(root_dir=None) -> dict:
    root = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
    report_dir = root / "navikoLAB" / "search" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    diagnostics = run_search_integration_diagnostics(root_dir=root)

    completed_items = [
        "SearchDispatcher abstraction layer",
        "Browser provider route",
        "Search Diagnostics",
        "ResearchManager to SearchDispatcher connection",
        "DeepSearchEngine scaffold",
        "DeepSearch Diagnostics",
        "KnowledgeReflection",
        "KnowledgeImprovement",
        "Search / DeepSearch / Knowledge Integration Diagnostics",
    ]

    report = {
        "title": "Search / DeepSearch / KnowledgeReflection Completion Report",
        "status": "completed" if diagnostics.get("status") == "passed" else "needs_review",
        "phase": "第27工程 DeepSearch Engine / Knowledge Reflection",
        "created_at": now,
        "completed_items": completed_items,
        "diagnostics_status": diagnostics.get("status"),
        "diagnostics_report": diagnostics.get("report_path"),
        "knowledge_count": diagnostics.get("knowledge_count"),
        "experience_count": diagnostics.get("experience_count"),
        "improvement_count": diagnostics.get("improvement_count"),
        "next_recommended_phase": "第28工程 AppAnalyzer / FolderAnalyzer / PythonAnalyzer",
        "architecture": {
            "research_to_search": "ResearchManager -> SearchDispatcher",
            "search_to_browser": "SearchDispatcher -> ConnectorDispatcher -> BrowserConnector",
            "deep_search": "DeepSearchEngine -> SearchDispatcher -> Providers",
            "knowledge_reflection": "KnowledgeBase + ExperienceManager -> KnowledgeReflection",
            "knowledge_improvement": "KnowledgeReflection -> KnowledgeImprovement -> ExperienceManager",
            "future_flow": "Mission -> Research -> Search -> DeepSearch -> Knowledge -> Reflection -> Improvement",
        },
        "safety": {
            "external_browser_access": False,
            "mode": "safe_scaffold",
            "note": "SearchProvider抽象層とDeepSearch構造は完成。外部検索実行はまだ無効。",
        },
    }

    report_path = report_dir / f"search_completion_report_{now}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report["report_path"] = str(report_path)
    return report


def main() -> None:
    print("=== Search / DeepSearch / KnowledgeReflection Completion Report ===")

    report = create_search_completion_report()

    print(f"状態: {report.get('status')}")
    print(f"工程: {report.get('phase')}")
    print(f"診断: {report.get('diagnostics_status')}")
    print(f"Knowledge件数: {report.get('knowledge_count')}")
    print(f"Experience件数: {report.get('experience_count')}")
    print(f"改善候補数: {report.get('improvement_count')}")
    print("完成項目:")

    for item in report.get("completed_items", []):
        print(f"- {item}")

    print(f"保存先: {report.get('report_path')}")
    print(f"次工程: {report.get('next_recommended_phase')}")


if __name__ == "__main__":
    main()