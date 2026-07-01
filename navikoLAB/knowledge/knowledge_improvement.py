from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.knowledge.knowledge_reflection import KnowledgeReflection
from navikoLAB.experience.experience_manager import ExperienceManager


class KnowledgeImprovement:
    """
    KnowledgeReflection の結果をもとに、
    改善候補を生成・保存する基礎Improvement。
    """

    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
        self.improvement_dir = self.root_dir / "navikoLAB" / "knowledge" / "improvement_reports"
        self.improvement_dir.mkdir(parents=True, exist_ok=True)

        self.reflection = KnowledgeReflection(root_dir=self.root_dir)
        self.experience_manager = ExperienceManager(root_dir=self.root_dir)

    def build_improvement_items(self, reflection_report: dict) -> list[dict]:
        items = []

        for recommendation in reflection_report.get("recommendations", []):
            rec_type = recommendation.get("type")

            if rec_type == "knowledge_gap":
                for area in recommendation.get("missing_areas", []):
                    items.append(
                        {
                            "type": "add_knowledge_area",
                            "priority": "medium",
                            "target": area,
                            "summary": f"{area} 領域の知識を追加する。",
                            "suggested_action": f"DeepSearchEngineで {area} 関連の調査を実行し、KnowledgeBaseへ保存する。",
                        }
                    )

            elif rec_type == "duplicate_knowledge":
                items.append(
                    {
                        "type": "review_duplicate_knowledge",
                        "priority": "low",
                        "target": "KnowledgeBase",
                        "summary": "重複している知識タイトルを確認する。",
                        "suggested_action": "重複タイトルを確認し、必要に応じて統合・整理する。",
                        "duplicates": recommendation.get("duplicates", {}),
                    }
                )

            elif rec_type == "stable":
                items.append(
                    {
                        "type": "maintain_current_state",
                        "priority": "low",
                        "target": "KnowledgeBase",
                        "summary": "現在のKnowledgeBaseは安定しています。",
                        "suggested_action": "新しいMissionやResearchのたびに継続的に知識を蓄積する。",
                    }
                )

        return items

    def create_improvement_plan(self) -> dict:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")

        reflection_report = self.reflection.reflect()
        improvement_items = self.build_improvement_items(reflection_report)

        plan = {
            "title": "Knowledge Improvement Plan",
            "status": "planned",
            "created_at": now,
            "source_reflection": reflection_report.get("report_path"),
            "improvement_count": len(improvement_items),
            "improvements": improvement_items,
        }

        report_path = self.improvement_dir / f"knowledge_improvement_{now}.json"
        report_path.write_text(
            json.dumps(plan, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        experience_record = self.experience_manager.add_experience(
            title="KnowledgeImprovement Plan Created",
            event_type="knowledge_improvement",
            status="planned",
            summary=f"{len(improvement_items)} 件のKnowledge改善候補を作成しました。",
            source="KnowledgeImprovement",
            metadata={
                "plan_path": str(report_path),
                "source_reflection": reflection_report.get("report_path"),
                "improvement_count": len(improvement_items),
            },
        )

        plan["report_path"] = str(report_path)
        plan["experience_record"] = {
            "id": experience_record.get("id"),
            "path": experience_record.get("path"),
        }

        return plan

    def diagnose(self) -> dict:
        plan = self.create_improvement_plan()

        return {
            "name": "KnowledgeImprovement",
            "status": "ready" if plan.get("status") == "planned" else "failed",
            "improvement_count": plan.get("improvement_count"),
            "report_path": plan.get("report_path"),
            "experience_record": plan.get("experience_record"),
        }


def main() -> None:
    print("=== KnowledgeImprovement 診断 ===")

    improvement = KnowledgeImprovement()
    report = improvement.diagnose()

    print(f"状態: {report.get('status')}")
    print(f"改善候補数: {report.get('improvement_count')}")
    print(f"保存先: {report.get('report_path')}")
    print(f"Experience保存: {report.get('experience_record')}")


if __name__ == "__main__":
    main()