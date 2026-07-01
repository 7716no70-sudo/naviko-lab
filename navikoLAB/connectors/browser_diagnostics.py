from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.connectors.browser_connector import BrowserConnector
from navikoLAB.connectors.connector_dispatcher import ConnectorDispatcher


def run_browser_diagnostics(root_dir=None) -> dict:
    root = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
    report_dir = root / "navikoLAB" / "connectors" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    connector = BrowserConnector()
    connector_diag = connector.diagnose()

    dispatcher = ConnectorDispatcher(root_dir=root)
    dispatcher_result = dispatcher.run(
        "browser",
        "ナビ子 ResearchManager のためのBrowser診断",
        context={"source": "browser_diagnostics"},
    )

    checks = {
        "browser_connector_import": True,
        "browser_connector_ready": connector_diag.get("status") == "ready",
        "external_access_disabled": connector_diag.get("external_access") is False,
        "dispatcher_connected": dispatcher_result.get("dispatcher") == "ConnectorDispatcher",
        "dispatcher_status_safe": dispatcher_result.get("status") in ["safe_skipped", "completed", "skipped"],
        "dispatcher_log_created": bool(dispatcher_result.get("dispatcher_log")),
    }

    status = "passed" if all(checks.values()) else "failed"

    report = {
        "title": "Browser Connector Diagnostics",
        "status": status,
        "created_at": now,
        "connector": connector_diag,
        "dispatcher_result": dispatcher_result,
        "checks": checks,
    }

    report_path = report_dir / f"browser_diagnostics_{now}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report["report_path"] = str(report_path)
    return report


def main() -> None:
    print("=== Browser Connector Diagnostics ===")

    report = run_browser_diagnostics()

    print(f"状態: {report.get('status')}")
    print("確認項目:")

    for name, ok in report.get("checks", {}).items():
        print(f"- {name}: {'OK' if ok else 'NG'}")

    print(f"保存先: {report.get('report_path')}")


if __name__ == "__main__":
    main()