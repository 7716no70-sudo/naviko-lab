from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.research.research_manager import ResearchManager
from navikoLAB.knowledge.knowledge_base import KnowledgeBase
from navikoLAB.experience.experience_manager import ExperienceManager


def run_research_diagnostics(root_dir=None) -> dict:
    root = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
    report_dir = root / "navikoLAB" / "research" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    research_manager = ResearchManager(root_dir=root)
    knowledge_base = KnowledgeBase(root_dir=root)
    experience_manager = ExperienceManager(root_dir=root)

    research_report = research_manager.diagnose()
    knowledge_results = knowledge_base.search("Research")
    experience_results = experience_manager.search("Research")

    checks = {
        "research_manager_ready": research_report.get("status") == "ready",
        "browser_connected": research_report.get("browser_status") in ["safe_skipped", "completed", "skipped"],
        "knowledge_saved": bool(research_report.get("knowledge_record")),
        "experience_saved": bool(research_report.get("experience_record")),
        "knowledge_searchable": len(knowledge_results) > 0,
        "experience_searchable": len(experience_results) > 0,
    }

    status = "passed" if all(checks.values()) else "failed"

    report = {
        "title": "Research Diagnostics",
        "status": status,
        "created_at": now,
        "research_report": research_report,
        "knowledge_search_count": len(knowledge_results),
        "experience_search_count": len(experience_results),
        "checks": checks,
    }

    report_path = report_dir / f"research_diagnostics_{now}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report["report_path"] = str(report_path)
    return report


def main() -> None:
    print("=== Research Diagnostics ===")

    report = run_research_diagnostics()

    print(f"状態: {report.get('status')}")
    print("確認項目:")

    for name, ok in report.get("checks", {}).items():
        print(f"- {name}: {'OK' if ok else 'NG'}")

    print(f"Knowledge検索件数: {report.get('knowledge_search_count')}")
    print(f"Experience検索件数: {report.get('experience_search_count')}")
    print(f"保存先: {report.get('report_path')}")


if __name__ == "__main__":
    main()