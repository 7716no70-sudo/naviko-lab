from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.knowledge.knowledge_base import KnowledgeBase
from navikoLAB.experience.experience_manager import ExperienceManager


class KnowledgeReflection:
    """
    KnowledgeBase と ExperienceManager を読み取り、
    知識の件数・重複・不足・成功/失敗傾向を分析する基礎Reflection。
    """

    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
        self.report_dir = self.root_dir / "navikoLAB" / "knowledge" / "reflection_reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)

        self.knowledge_base = KnowledgeBase(root_dir=self.root_dir)
        self.experience_manager = ExperienceManager(root_dir=self.root_dir)

    def load_knowledge_items(self) -> list[dict]:
        index = self.knowledge_base.load_index()
        return index.get("items", [])

    def load_experience_items(self) -> list[dict]:
        memory = self.experience_manager.load_memory()
        return memory.get("experiences", [])

    def detect_duplicate_titles(self, items: list[dict]) -> dict:
        title_counts = {}

        for item in items:
            title = item.get("title", "")
            if not title:
                continue
            title_counts[title] = title_counts.get(title, 0) + 1

        duplicates = {
            title: count
            for title, count in title_counts.items()
            if count >= 2
        }

        return duplicates

    def count_by_source(self, items: list[dict]) -> dict:
        source_counts = {}

        for item in items:
            source = item.get("source", "unknown")
            source_counts[source] = source_counts.get(source, 0) + 1

        return source_counts

    def count_experience_status(self, items: list[dict]) -> dict:
        status_counts = {}

        for item in items:
            status = item.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

        return status_counts

    def find_missing_knowledge_areas(self, knowledge_items: list[dict]) -> list[str]:
        required_keywords = [
            "Research",
            "DeepSearch",
            "Mission",
            "Connector",
            "Reflection",
            "Improvement",
        ]

        titles = " ".join(str(item.get("title", "")) for item in knowledge_items)

        missing = [
            keyword
            for keyword in required_keywords
            if keyword.lower() not in titles.lower()
        ]

        return missing

    def reflect(self) -> dict:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")

        knowledge_items = self.load_knowledge_items()
        experience_items = self.load_experience_items()

        duplicate_titles = self.detect_duplicate_titles(knowledge_items)
        knowledge_by_source = self.count_by_source(knowledge_items)
        experience_by_status = self.count_experience_status(experience_items)
        missing_areas = self.find_missing_knowledge_areas(knowledge_items)

        recommendations = []

        if missing_areas:
            recommendations.append(
                {
                    "type": "knowledge_gap",
                    "summary": "不足している知識領域があります。",
                    "missing_areas": missing_areas,
                }
            )

        if duplicate_titles:
            recommendations.append(
                {
                    "type": "duplicate_knowledge",
                    "summary": "重複している知識タイトルがあります。",
                    "duplicates": duplicate_titles,
                }
            )

        if not recommendations:
            recommendations.append(
                {
                    "type": "stable",
                    "summary": "現在のKnowledgeBaseは基礎診断上、安定しています。",
                }
            )

        report = {
            "title": "Knowledge Reflection Report",
            "status": "completed",
            "created_at": now,
            "knowledge_count": len(knowledge_items),
            "experience_count": len(experience_items),
            "knowledge_by_source": knowledge_by_source,
            "experience_by_status": experience_by_status,
            "duplicate_titles": duplicate_titles,
            "missing_areas": missing_areas,
            "recommendations": recommendations,
        }

        report_path = self.report_dir / f"knowledge_reflection_{now}.json"
        report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        report["report_path"] = str(report_path)
        return report

    def diagnose(self) -> dict:
        report = self.reflect()

        return {
            "name": "KnowledgeReflection",
            "status": "ready" if report.get("status") == "completed" else "failed",
            "knowledge_count": report.get("knowledge_count"),
            "experience_count": report.get("experience_count"),
            "recommendation_count": len(report.get("recommendations", [])),
            "report_path": report.get("report_path"),
        }


def main() -> None:
    print("=== KnowledgeReflection 診断 ===")

    reflection = KnowledgeReflection()
    report = reflection.diagnose()

    print(f"状態: {report.get('status')}")
    print(f"Knowledge件数: {report.get('knowledge_count')}")
    print(f"Experience件数: {report.get('experience_count')}")
    print(f"提案件数: {report.get('recommendation_count')}")
    print(f"保存先: {report.get('report_path')}")


if __name__ == "__main__":
    main()