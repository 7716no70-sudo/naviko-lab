from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.search.search_dispatcher import SearchDispatcher
from navikoLAB.knowledge.knowledge_base import KnowledgeBase
from navikoLAB.experience.experience_manager import ExperienceManager


class DeepSearchEngine:
    """
    複数SearchProviderを横断して検索し、
    結果をKnowledgeBase / ExperienceManagerへ保存する基礎エンジン。

    現段階では browser provider のみ接続。
    将来 ChatGPT / Gemini / Claude / LocalKnowledge / HDDKnowledge を追加する。
    """

    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
        self.search_dir = self.root_dir / "navikoLAB" / "search"
        self.log_dir = self.search_dir / "deep_search_logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.search_dispatcher = SearchDispatcher(root_dir=self.root_dir)
        self.knowledge_base = KnowledgeBase(root_dir=self.root_dir)
        self.experience_manager = ExperienceManager(root_dir=self.root_dir)

        self.default_providers = ["browser"]

    def normalize_results(self, provider_results: list[dict]) -> list[dict]:
        normalized = []

        for item in provider_results:
            provider = item.get("provider", "unknown")
            results = item.get("results", [])

            if results:
                for result in results:
                    normalized.append(
                        {
                            "provider": provider,
                            "title": result.get("title", ""),
                            "url": result.get("url", ""),
                            "snippet": result.get("snippet", ""),
                            "raw": result,
                        }
                    )
            else:
                normalized.append(
                    {
                        "provider": provider,
                        "title": f"{provider} result placeholder",
                        "url": "",
                        "snippet": item.get("status", "no results"),
                        "raw": item,
                    }
                )

        return normalized

    def deduplicate_results(self, results: list[dict]) -> list[dict]:
        seen = set()
        deduped = []

        for result in results:
            key = (
                result.get("url")
                or result.get("title")
                or json.dumps(result.get("raw", {}), ensure_ascii=False, sort_keys=True)
            )

            if key in seen:
                continue

            seen.add(key)
            deduped.append(result)

        return deduped

    def run_deep_search(
        self,
        query: str,
        providers: list[str] | None = None,
        context: dict | None = None,
    ) -> dict:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        providers = providers or self.default_providers

        provider_results = []

        for provider in providers:
            result = self.search_dispatcher.search(
                query=query,
                provider=provider,
                context={
                    "source": "DeepSearchEngine",
                    "context": context or {},
                },
            )
            provider_results.append(result)

        normalized = self.normalize_results(provider_results)
        deduped = self.deduplicate_results(normalized)

        status = "completed" if provider_results else "failed"

        deep_record = {
            "status": status,
            "mode": "safe_deep_search_scaffold",
            "query": query,
            "providers": providers,
            "provider_results": provider_results,
            "normalized_count": len(normalized),
            "deduped_count": len(deduped),
            "results": deduped,
            "created_at": now,
        }

        knowledge_record = self.knowledge_base.add_knowledge(
            title=f"DeepSearch: {query}",
            content=json.dumps(deep_record, ensure_ascii=False, indent=2),
            source="DeepSearchEngine",
            tags=["deep_search", "search", "knowledge"],
            metadata={
                "query": query,
                "providers": providers,
                "deduped_count": len(deduped),
            },
        )

        experience_record = self.experience_manager.add_experience(
            title=f"DeepSearch Experience: {query}",
            event_type="deep_search",
            status=status,
            summary=f"DeepSearchEngine executed query: {query}",
            source="DeepSearchEngine",
            metadata={
                "providers": providers,
                "knowledge_id": knowledge_record.get("id"),
                "knowledge_path": knowledge_record.get("path"),
                "deduped_count": len(deduped),
            },
        )

        deep_record["knowledge_record"] = {
            "id": knowledge_record.get("id"),
            "path": knowledge_record.get("path"),
        }
        deep_record["experience_record"] = {
            "id": experience_record.get("id"),
            "path": experience_record.get("path"),
        }

        log_path = self.log_dir / f"deep_search_{now}.json"
        log_path.write_text(
            json.dumps(deep_record, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        deep_record["deep_search_log"] = str(log_path)
        return deep_record

    def diagnose(self) -> dict:
        test = self.run_deep_search(
            query="ナビ子 DeepSearchEngine 診断",
            providers=["browser"],
            context={"source": "deep_search_diagnostics"},
        )

        return {
            "name": "DeepSearchEngine",
            "status": "ready" if test.get("status") == "completed" else "failed",
            "providers": test.get("providers"),
            "result_count": test.get("deduped_count"),
            "knowledge_record": test.get("knowledge_record"),
            "experience_record": test.get("experience_record"),
            "deep_search_log": test.get("deep_search_log"),
        }


def main() -> None:
    print("=== DeepSearchEngine 診断 ===")

    engine = DeepSearchEngine()
    report = engine.diagnose()

    print(f"状態: {report.get('status')}")
    print(f"Providers: {report.get('providers')}")
    print(f"結果件数: {report.get('result_count')}")
    print(f"Knowledge保存: {report.get('knowledge_record')}")
    print(f"Experience保存: {report.get('experience_record')}")
    print(f"保存先: {report.get('deep_search_log')}")


if __name__ == "__main__":
    main()