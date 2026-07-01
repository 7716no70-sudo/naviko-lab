from datetime import datetime


class BrowserConnector:
    """
    Browser Connector 正式版の基礎実装。

    現段階では安全のため、実ブラウザ操作や外部通信は行わない。
    ResearchManager / ConnectorDispatcher から呼び出せる共通形式だけを整える。
    """

    def __init__(self):
        self.name = "browser"
        self.connector_type = "research"
        self.enabled = True
        self.status = "ready"

    def diagnose(self):
        return {
            "name": self.name,
            "connector_type": self.connector_type,
            "enabled": self.enabled,
            "status": self.status,
            "external_access": False,
            "checked_at": datetime.now().isoformat(timespec="seconds"),
        }

    def search(self, query, limit=5):
        if not query:
            return {
                "status": "failed",
                "reason": "query_empty",
                "results": [],
            }

        return {
            "status": "safe_skipped",
            "reason": "external_browser_access_not_enabled_yet",
            "query": query,
            "limit": limit,
            "results": [],
            "message": "BrowserConnector formal interface is ready. External search is disabled for safety.",
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

    def run(self, request):
        action = request.get("action", "search")

        if action == "diagnose":
            return self.diagnose()

        if action == "search":
            return self.search(
                query=request.get("query", ""),
                limit=request.get("limit", 5),
            )

        return {
            "status": "failed",
            "reason": "unknown_browser_action",
            "action": action,
        }