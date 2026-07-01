from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class ExperienceManager:
    """
    Mission / Research / Connector / Reflection の成功・失敗・学習履歴を保存する基礎Manager。
    KnowledgeBaseが「知識」を扱うのに対し、
    ExperienceManagerは「経験・実行結果・成功失敗パターン」を扱う。
    """

    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
        self.experience_dir = self.root_dir / "navikoLAB" / "experience"
        self.records_dir = self.experience_dir / "records"
        self.records_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.experience_dir / "experience_memory.json"

        if not self.index_path.exists():
            self.index_path.write_text(
                json.dumps({"experiences": []}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    def load_memory(self) -> dict:
        try:
            return json.loads(self.index_path.read_text(encoding="utf-8"))
        except Exception:
            return {"experiences": []}

    def save_memory(self, memory: dict) -> None:
        self.index_path.write_text(
            json.dumps(memory, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def add_experience(
        self,
        title: str,
        event_type: str,
        status: str,
        summary: str,
        source: str = "manual",
        metadata: dict | None = None,
    ) -> dict:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")

        record = {
            "id": f"experience_{now}",
            "title": title,
            "event_type": event_type,
            "status": status,
            "summary": summary,
            "source": source,
            "metadata": metadata or {},
            "created_at": now,
        }

        record_path = self.records_dir / f"{record['id']}.json"
        record_path.write_text(
            json.dumps(record, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        memory = self.load_memory()
        memory.setdefault("experiences", [])
        memory["experiences"].append(
            {
                "id": record["id"],
                "title": title,
                "event_type": event_type,
                "status": status,
                "source": source,
                "path": str(record_path),
                "created_at": now,
            }
        )
        self.save_memory(memory)

        record["path"] = str(record_path)
        return record

    def search(self, keyword: str) -> list[dict]:
        memory = self.load_memory()
        results = []

        for item in memory.get("experiences", []):
            haystack = " ".join(
                [
                    str(item.get("title", "")),
                    str(item.get("event_type", "")),
                    str(item.get("status", "")),
                    str(item.get("source", "")),
                ]
            )

            if keyword.lower() in haystack.lower():
                results.append(item)

        return results

    def diagnose(self) -> dict:
        sample = self.add_experience(
            title="ExperienceManager 診断",
            event_type="diagnostics",
            status="success",
            summary="ExperienceManager の保存・索引・検索テストです。",
            source="diagnostics",
            metadata={"test": True},
        )

        results = self.search("ExperienceManager")

        return {
            "name": "ExperienceManager",
            "status": "ready" if results else "failed",
            "sample_path": sample.get("path"),
            "search_count": len(results),
            "memory_path": str(self.index_path),
        }


def main() -> None:
    print("=== ExperienceManager 診断 ===")

    manager = ExperienceManager()
    report = manager.diagnose()

    print(f"状態: {report.get('status')}")
    print(f"検索件数: {report.get('search_count')}")
    print(f"Memory: {report.get('memory_path')}")
    print(f"保存先: {report.get('sample_path')}")


if __name__ == "__main__":
    main()