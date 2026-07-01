from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.search.deep_search_engine import DeepSearchEngine
from navikoLAB.knowledge.knowledge_base import KnowledgeBase
from navikoLAB.experience.experience_manager import ExperienceManager


def run_deep_search_diagnostics(root_dir=None) -> dict:
    root = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
    report_dir = root / "navikoLAB" / "search" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    engine = DeepSearchEngine(root_dir=root)
    knowledge_base = KnowledgeBase(root_dir=root)
    experience_manager = ExperienceManager(root_dir=root)

    deep_result = engine.run_deep_search(
        query="ナビ子 DeepSearch Diagnostics",
        providers=["browser"],
        context={"source": "deep_search_diagnostics"},
    )

    knowledge_results = knowledge_base.search("DeepSearch")
    experience_results = experience_manager.search("DeepSearch")

    checks = {
        "deep_search_engine_ready": deep_result.get("status") == "completed",
        "browser_provider_used": "browser" in deep_result.get("providers", []),
        "results_normalized": deep_result.get("normalized_count", 0) >= 1,
        "results_deduped": deep_result.get("deduped_count", 0) >= 1,
        "knowledge_saved": bool(deep_result.get("knowledge_record")),
        "experience_saved": bool(deep_result.get("experience_record")),
        "knowledge_searchable": len(knowledge_results) > 0,
        "experience_searchable": len(experience_results) > 0,
        "deep_search_log_created": bool(deep_result.get("deep_search_log")),
    }

    status = "passed" if all(checks.values()) else "failed"

    report = {
        "title": "DeepSearch Diagnostics",
        "status": status,
        "created_at": now,
        "deep_result": deep_result,
        "knowledge_search_count": len(knowledge_results),
        "experience_search_count": len(experience_results),
        "checks": checks,
    }

    report_path = report_dir / f"deep_search_diagnostics_{now}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report["report_path"] = str(report_path)
    return report


def main() -> None:
    print("=== DeepSearch Diagnostics ===")

    report = run_deep_search_diagnostics()

    print(f"状態: {report.get('status')}")
    print("確認項目:")

    for name, ok in report.get("checks", {}).items():
        print(f"- {name}: {'OK' if ok else 'NG'}")

    print(f"Knowledge検索件数: {report.get('knowledge_search_count')}")
    print(f"Experience検索件数: {report.get('experience_search_count')}")
    print(f"保存先: {report.get('report_path')}")


if __name__ == "__main__":
    main()