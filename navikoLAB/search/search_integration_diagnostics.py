from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.search.search_diagnostics import run_search_diagnostics
from navikoLAB.search.deep_search_diagnostics import run_deep_search_diagnostics
from navikoLAB.knowledge.knowledge_reflection import KnowledgeReflection
from navikoLAB.knowledge.knowledge_improvement import KnowledgeImprovement


def run_search_integration_diagnostics(root_dir=None) -> dict:
    root = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
    report_dir = root / "navikoLAB" / "search" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    search_report = run_search_diagnostics(root_dir=root)
    deep_search_report = run_deep_search_diagnostics(root_dir=root)

    reflection = KnowledgeReflection(root_dir=root)
    reflection_report = reflection.reflect()

    improvement = KnowledgeImprovement(root_dir=root)
    improvement_plan = improvement.create_improvement_plan()

    checks = {
        "search_diagnostics_passed": search_report.get("status") == "passed",
        "deep_search_diagnostics_passed": deep_search_report.get("status") == "passed",
        "knowledge_reflection_completed": reflection_report.get("status") == "completed",
        "knowledge_improvement_planned": improvement_plan.get("status") == "planned",
        "knowledge_count_positive": reflection_report.get("knowledge_count", 0) > 0,
        "experience_count_positive": reflection_report.get("experience_count", 0) > 0,
        "improvement_count_positive": improvement_plan.get("improvement_count", 0) > 0,
    }

    status = "passed" if all(checks.values()) else "failed"

    report = {
        "title": "Search / DeepSearch / Knowledge Integration Diagnostics",
        "status": status,
        "created_at": now,
        "search_report": search_report.get("report_path"),
        "deep_search_report": deep_search_report.get("report_path"),
        "reflection_report": reflection_report.get("report_path"),
        "improvement_plan": improvement_plan.get("report_path"),
        "knowledge_count": reflection_report.get("knowledge_count"),
        "experience_count": reflection_report.get("experience_count"),
        "improvement_count": improvement_plan.get("improvement_count"),
        "checks": checks,
    }

    report_path = report_dir / f"search_integration_diagnostics_{now}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report["report_path"] = str(report_path)
    return report


def main() -> None:
    print("=== Search / DeepSearch / Knowledge Integration Diagnostics ===")

    report = run_search_integration_diagnostics()

    print(f"状態: {report.get('status')}")
    print("確認項目:")

    for name, ok in report.get("checks", {}).items():
        print(f"- {name}: {'OK' if ok else 'NG'}")

    print(f"Knowledge件数: {report.get('knowledge_count')}")
    print(f"Experience件数: {report.get('experience_count')}")
    print(f"改善候補数: {report.get('improvement_count')}")
    print(f"保存先: {report.get('report_path')}")


if __name__ == "__main__":
    main()