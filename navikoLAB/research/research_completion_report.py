from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.research.research_diagnostics import run_research_diagnostics


def create_research_completion_report(root_dir=None) -> dict:
    root = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
    report_dir = root / "navikoLAB" / "research" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    diagnostics = run_research_diagnostics(root_dir=root)

    completed_items = [
        "BrowserConnector formal interface",
        "ConnectorDispatcher browser route",
        "BrowserDiagnostics",
        "ResearchManager",
        "KnowledgeBase",
        "ResearchManager to KnowledgeBase connection",
        "ExperienceManager",
        "ResearchManager to ExperienceManager connection",
        "ResearchDiagnostics",
    ]

    report = {
        "title": "Research / Knowledge / Experience Completion Report",
        "status": "completed" if diagnostics.get("status") == "passed" else "needs_review",
        "phase": "第26工程 Research / Knowledge 基盤構築",
        "created_at": now,
        "completed_items": completed_items,
        "diagnostics_status": diagnostics.get("status"),
        "diagnostics_report": diagnostics.get("report_path"),
        "next_recommended_phase": "第27工程 DeepSearch Engine / Knowledge Reflection",
        "architecture": {
            "mission_to_research": "MissionManager -> ResearchManager",
            "research_to_browser": "ResearchManager -> ConnectorDispatcher -> BrowserConnector",
            "research_to_knowledge": "ResearchManager -> KnowledgeBase",
            "research_to_experience": "ResearchManager -> ExperienceManager",
            "future_flow": "Mission -> Research -> Knowledge -> Experience -> Reflection -> Improvement",
        },
        "safety": {
            "external_browser_access": False,
            "mode": "safe_scaffold",
            "note": "外部検索やブラウザ操作はまだ実行しない。正式接続用の安全な基盤のみ完成。",
        },
    }

    report_path = report_dir / f"research_completion_report_{now}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report["report_path"] = str(report_path)
    return report


def main() -> None:
    print("=== Research / Knowledge / Experience Completion Report ===")

    report = create_research_completion_report()

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