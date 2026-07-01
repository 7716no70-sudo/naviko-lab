from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.search.search_dispatcher import SearchDispatcher


def run_search_diagnostics(root_dir=None) -> dict:
    root = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
    report_dir = root / "navikoLAB" / "search" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    dispatcher = SearchDispatcher(root_dir=root)

    browser_result = dispatcher.search(
        query="ナビ子 Search Diagnostics Browser Provider",
        provider="browser",
        context={"source": "search_diagnostics"},
    )

    unknown_result = dispatcher.search(
        query="unknown provider test",
        provider="unknown_provider",
        context={"source": "search_diagnostics"},
    )

    empty_result = dispatcher.search(
        query="",
        provider="browser",
        context={"source": "search_diagnostics"},
    )

    checks = {
        "search_dispatcher_import": True,
        "browser_provider_connected": browser_result.get("status") in ["safe_skipped", "completed", "skipped"],
        "browser_provider_log_created": bool(browser_result.get("search_log")),
        "unknown_provider_blocked": unknown_result.get("reason") == "unknown_search_provider",
        "empty_query_blocked": empty_result.get("reason") == "query_empty",
    }

    status = "passed" if all(checks.values()) else "failed"

    report = {
        "title": "Search Diagnostics",
        "status": status,
        "created_at": now,
        "browser_result": browser_result,
        "unknown_result": unknown_result,
        "empty_result": empty_result,
        "checks": checks,
    }

    report_path = report_dir / f"search_diagnostics_{now}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report["report_path"] = str(report_path)
    return report


def main() -> None:
    print("=== Search Diagnostics ===")

    report = run_search_diagnostics()

    print(f"状態: {report.get('status')}")
    print("確認項目:")

    for name, ok in report.get("checks", {}).items():
        print(f"- {name}: {'OK' if ok else 'NG'}")

    print(f"保存先: {report.get('report_path')}")


if __name__ == "__main__":
    main()