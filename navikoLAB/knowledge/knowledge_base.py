from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class KnowledgeBase:
    """
    ResearchManager や Reflection から得た知識を保存・検索する基礎KnowledgeBase。
    """

    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
        self.knowledge_dir = self.root_dir / "navikoLAB" / "knowledge"
        self.records_dir = self.knowledge_dir / "records"
        self.records_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.knowledge_dir / "knowledge_index.json"

        if not self.index_path.exists():
            self.index_path.write_text(
                json.dumps({"items": []}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    def load_index(self) -> dict:
        try:
            return json.loads(self.index_path.read_text(encoding="utf-8"))
        except Exception:
            return {"items": []}

    def save_index(self, index: dict) -> None:
        self.index_path.write_text(
            json.dumps(index, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def add_knowledge(
        self,
        title: str,
        content: str,
        source: str = "manual",
        tags: list[str] | None = None,
        metadata: dict | None = None,
    ) -> dict:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")

        record = {
            "id": f"knowledge_{now}",
            "title": title,
            "content": content,
            "source": source,
            "tags": tags or [],
            "metadata": metadata or {},
            "created_at": now,
        }

        record_path = self.records_dir / f"{record['id']}.json"
        record.write_text if False else None
        record_path.write_text(
            json.dumps(record, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        index = self.load_index()
        index.setdefault("items", [])
        index["items"].append(
            {
                "id": record["id"],
                "title": title,
                "source": source,
                "tags": tags or [],
                "path": str(record_path),
                "created_at": now,
            }
        )
        self.save_index(index)

        record["path"] = str(record_path)
        return record

    def search(self, keyword: str) -> list[dict]:
        index = self.load_index()
        results = []

        for item in index.get("items", []):
            haystack = " ".join(
                [
                    str(item.get("title", "")),
                    str(item.get("source", "")),
                    " ".join(item.get("tags", [])),
                ]
            )

            if keyword.lower() in haystack.lower():
                results.append(item)

        return results

    def diagnose(self) -> dict:
        sample = self.add_knowledge(
            title="KnowledgeBase 診断",
            content="KnowledgeBase の保存・索引・検索テストです。",
            source="diagnostics",
            tags=["knowledge", "diagnostics"],
        )

        results = self.search("KnowledgeBase")

        return {
            "name": "KnowledgeBase",
            "status": "ready" if results else "failed",
            "sample_path": sample.get("path"),
            "search_count": len(results),
            "index_path": str(self.index_path),
        }


def main() -> None:
    print("=== KnowledgeBase 診断 ===")

    kb = KnowledgeBase()
    report = kb.diagnose()

    print(f"状態: {report.get('status')}")
    print(f"検索件数: {report.get('search_count')}")
    print(f"索引: {report.get('index_path')}")
    print(f"保存先: {report.get('sample_path')}")


if __name__ == "__main__":
    main()