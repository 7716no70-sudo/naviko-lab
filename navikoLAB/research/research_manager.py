from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.search.search_dispatcher import SearchDispatcher
from navikoLAB.knowledge.knowledge_base import KnowledgeBase
from navikoLAB.experience.experience_manager import ExperienceManager


class ResearchManager:
    """
    Mission / Goal から調査要求を受け取り、
    Browser Connector 経由で安全に調査フローを実行する基礎Manager。
    """

    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
        self.research_dir = self.root_dir / "navikoLAB" / "research" / "logs"
        self.research_dir.mkdir(parents=True, exist_ok=True)
        self.search_dispatcher = SearchDispatcher(root_dir=self.root_dir)
        self.knowledge_base = KnowledgeBase(root_dir=self.root_dir)
        self.experience_manager = ExperienceManager(root_dir=self.root_dir)

    def build_query(self, goal: str, context: dict | None = None) -> str:
        context = context or {}

        keywords = context.get("keywords", [])
        if isinstance(keywords, list) and keywords:
            return f"{goal} " + " ".join(str(k) for k in keywords)

        return goal

    def run_research(self, goal: str, context: dict | None = None) -> dict:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        query = self.build_query(goal, context=context)

        browser_result = self.search_dispatcher.search(
            query=query,
            provider="browser",
            context={
                "source": "ResearchManager",
                "goal": goal,
                "context": context or {},
            },
        )

        research_record = {
            "status": "completed" if browser_result.get("status") in ["safe_skipped", "completed", "skipped"] else "failed",
            "mode": "safe_research_scaffold",
            "goal": goal,
            "query": query,
            "browser_result": browser_result,
            "created_at": now,
        }

        knowledge_record = self.knowledge_base.add_knowledge(
            title=f"Research: {goal}",
            content=json.dumps(
                {
                    "goal": goal,
                    "query": query,
                    "browser_result": browser_result,
                },
                ensure_ascii=False,
                indent=2,
            ),
            source="ResearchManager",
            tags=["research", "browser", "safe_scaffold"],
            metadata={
                "research_created_at": now,
                "browser_status": browser_result.get("status"),
            },
        )

        experience_record = self.experience_manager.add_experience(
            title=f"Research Experience: {goal}",
            event_type="research",
            status=research_record["status"],
            summary=f"ResearchManager executed browser research scaffold for: {goal}",
            source="ResearchManager",
            metadata={
                "query": query,
                "browser_status": browser_result.get("status"),
                "knowledge_id": knowledge_record.get("id"),
                "knowledge_path": knowledge_record.get("path"),
            },
        )

        research_record["experience_record"] = {
            "id": experience_record.get("id"),
            "path": experience_record.get("path"),
        }

        research_record["knowledge_record"] = {
            "id": knowledge_record.get("id"),
            "path": knowledge_record.get("path"),
        }

        log_path = self.research_dir / f"research_{now}.json"
        log_path.write_text(
            json.dumps(research_record, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        research_record["research_log"] = str(log_path)
        return research_record

    def diagnose(self) -> dict:
        test = self.run_research(
            "ナビ子 ResearchManager 診断",
            context={"keywords": ["BrowserConnector", "KnowledgeBase"]},
        )

        return {
            "name": "ResearchManager",
            "status": "ready" if test.get("status") == "completed" else "failed",
            "research_log": test.get("research_log"),
            "browser_status": test.get("browser_result", {}).get("status"),
            "knowledge_record": test.get("knowledge_record"),
            "experience_record": test.get("experience_record"),
        }


def main() -> None:
    print("=== ResearchManager 診断 ===")

    manager = ResearchManager()
    report = manager.diagnose()

    print(f"状態: {report.get('status')}")
    print(f"Browser状態: {report.get('browser_status')}")
    print(f"保存先: {report.get('research_log')}")
    print(f"Knowledge保存: {report.get('knowledge_record')}")
    print(f"Experience保存: {report.get('experience_record')}")


if __name__ == "__main__":
    main()