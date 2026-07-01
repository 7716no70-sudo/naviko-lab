from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SUGGESTION_DIR = ROOT / "navikoLAB" / "improvement_suggestions"
PLAN_DIR = ROOT / "navikoLAB" / "refactoring_plans"


PRIORITY_SCORE = {
    "high": 3,
    "medium": 2,
    "low": 1,
}


class AutoRefactoringPlan:
    def __init__(self) -> None:
        SUGGESTION_DIR.mkdir(parents=True, exist_ok=True)
        PLAN_DIR.mkdir(parents=True, exist_ok=True)

    def load_latest_suggestion_file(self) -> dict:
        files = sorted(SUGGESTION_DIR.glob("auto_improvement_suggestions_*.json"))

        if not files:
            return {
                "status": "missing",
                "suggestions": [],
            }

        latest = files[-1]

        try:
            data = json.loads(latest.read_text(encoding="utf-8"))
            data["_source"] = str(latest)
            return data
        except Exception as e:
            return {
                "status": "read_failed",
                "error": str(e),
                "suggestions": [],
                "_source": str(latest),
            }

    def create_plan(self, suggestions: list[dict]) -> list[dict]:
        sorted_items = sorted(
            suggestions,
            key=lambda item: PRIORITY_SCORE.get(str(item.get("priority", "low")).lower(), 1),
            reverse=True,
        )

        plan = []

        for index, item in enumerate(sorted_items, start=1):
            plan.append({
                "step": index,
                "title": item.get("title", "unknown"),
                "target": item.get("target", "unknown"),
                "reason": item.get("reason", ""),
                "expected_effect": item.get("expected_effect", ""),
                "risk": item.get("risk", "unknown"),
                "priority": item.get("priority", "low"),
                "recommended_action": "小さな独立モジュールとして実装し、診断とCompletionReportで確認する。",
            })

        return plan

    def save(self, source: dict, plan: list[dict]) -> Path:
        output = PLAN_DIR / f"auto_refactoring_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        data = {
            "status": "completed",
            "stage": "第31工程 AutoRefactoringPlan",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "source": source.get("_source"),
            "plan_count": len(plan),
            "plan": plan,
        }

        output.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return output

    def run(self) -> dict:
        source = self.load_latest_suggestion_file()
        suggestions = source.get("suggestions", [])
        plan = self.create_plan(suggestions)
        output = self.save(source, plan)

        return {
            "status": "completed",
            "suggestion_count": len(suggestions),
            "plan_count": len(plan),
            "output": str(output),
        }


def main() -> None:
    result = AutoRefactoringPlan().run()

    print("=== AutoRefactoringPlan ===")
    print(f"状態: {result['status']}")
    print(f"改善候補数: {result['suggestion_count']}")
    print(f"計画数: {result['plan_count']}")
    print(f"保存先: {result['output']}")


if __name__ == "__main__":
    main()