from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.connectors.connector_dispatcher import ConnectorDispatcher


class SearchDispatcher:
    """
    ResearchManager / DeepSearchEngine から検索要求を受け取り、
    検索Providerへ振り分ける抽象層。

    現段階では BrowserProvider 相当として
    ConnectorDispatcher -> BrowserConnector へ安全に接続する。
    """

    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
        self.search_dir = self.root_dir / "navikoLAB" / "search"
        self.log_dir = self.search_dir / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.connector_dispatcher = ConnectorDispatcher(root_dir=self.root_dir)

        self.provider_map = {
            "browser": self.search_with_browser,
        }

    def search(self, query: str, provider: str = "browser", context: dict | None = None) -> dict:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")

        if not query:
            result = {
                "status": "failed",
                "reason": "query_empty",
                "provider": provider,
                "query": query,
                "results": [],
                "created_at": now,
            }
        else:
            handler = self.provider_map.get(provider)

            if handler:
                result = handler(query=query, context=context or {})
            else:
                result = {
                    "status": "failed",
                    "reason": "unknown_search_provider",
                    "provider": provider,
                    "query": query,
                    "results": [],
                    "created_at": now,
                }

        result.setdefault("provider", provider)
        result.setdefault("query", query)
        result.setdefault("created_at", now)
        result["dispatcher"] = "SearchDispatcher"

        log_path = self.log_dir / f"search_dispatcher_{provider}_{now}.json"
        log_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        result["search_log"] = str(log_path)
        return result

    def search_with_browser(self, query: str, context: dict | None = None) -> dict:
        browser_result = self.connector_dispatcher.run(
            "browser",
            query,
            context={
                "source": "SearchDispatcher",
                "context": context or {},
            },
        )

        return {
            "status": browser_result.get("status", "unknown"),
            "provider": "browser",
            "query": query,
            "results": browser_result.get("results", []),
            "raw_result": browser_result,
        }

    def diagnose(self) -> dict:
        test = self.search(
            query="ナビ子 SearchDispatcher 診断",
            provider="browser",
            context={"source": "search_dispatcher_diagnostics"},
        )

        return {
            "name": "SearchDispatcher",
            "status": "ready" if test.get("status") in ["safe_skipped", "completed", "skipped"] else "failed",
            "provider": test.get("provider"),
            "search_log": test.get("search_log"),
            "raw_status": test.get("raw_result", {}).get("status"),
        }


def main() -> None:
    print("=== SearchDispatcher 診断 ===")

    dispatcher = SearchDispatcher()
    report = dispatcher.diagnose()

    print(f"状態: {report.get('status')}")
    print(f"Provider: {report.get('provider')}")
    print(f"Raw状態: {report.get('raw_status')}")
    print(f"保存先: {report.get('search_log')}")


if __name__ == "__main__":
    main()