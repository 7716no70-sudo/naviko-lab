from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "analyzers" / "reports"
IMPROVEMENT_DIR = ROOT / "navikoLAB" / "improvement_suggestions"


class AutoImprovementSuggestion:
    def __init__(self) -> None:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        IMPROVEMENT_DIR.mkdir(parents=True, exist_ok=True)

    def load_reports(self) -> dict:
        reports = {}

        for path in REPORT_DIR.glob("*.json"):
            try:
                reports[path.stem] = json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                reports[path.stem] = {
                    "status": "read_failed",
                    "error": str(e),
                    "path": str(path),
                }

        return reports

    def create_suggestions(self, reports: dict) -> list[dict]:
        suggestions = []

        report_names = " ".join(reports.keys()).lower()

        if "architecture" in report_names:
            suggestions.append({
                "title": "ArchitectureReflection連携の強化",
                "reason": "ArchitectureAnalyzerの結果を改善判断へ活用できる段階に入っているため。",
                "expected_effect": "設計理解から改善候補生成までの自動化が進む。",
                "risk": "low",
                "priority": "high",
                "target": "navikoLAB/analyzers",
            })

        if "dependency" in report_names:
            suggestions.append({
                "title": "依存関係の改善候補抽出",
                "reason": "DependencyAnalyzerの結果から依存方向や不足requirementsを評価できるため。",
                "expected_effect": "保守性と環境再現性が向上する。",
                "risk": "low",
                "priority": "high",
                "target": "navikoLAB/analyzers",
            })

        if "documentation" in report_names:
            suggestions.append({
                "title": "Documentation結果のKnowledge保存強化",
                "reason": "AutoDocumentationが生成したMarkdown/JSONを長期知識へ接続できるため。",
                "expected_effect": "ナビ子が過去の解析結果を参照しやすくなる。",
                "risk": "low",
                "priority": "medium",
                "target": "navikoLAB/docs",
            })

        if not suggestions:
            suggestions.append({
                "title": "解析レポート収集基盤の安定化",
                "reason": "改善候補を作るための入力レポートが不足している可能性があるため。",
                "expected_effect": "後続の改善判断が安定する。",
                "risk": "low",
                "priority": "medium",
                "target": "navikoLAB/analyzers/reports",
            })

        return suggestions

    def save(self, suggestions: list[dict]) -> Path:
        output = IMPROVEMENT_DIR / f"auto_improvement_suggestions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        data = {
            "status": "completed",
            "stage": "第31工程 AutoImprovementSuggestion",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "suggestion_count": len(suggestions),
            "suggestions": suggestions,
        }

        output.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return output

    def run(self) -> dict:
        reports = self.load_reports()
        suggestions = self.create_suggestions(reports)
        output = self.save(suggestions)

        return {
            "status": "completed",
            "report_count": len(reports),
            "suggestion_count": len(suggestions),
            "output": str(output),
        }


def main() -> None:
    result = AutoImprovementSuggestion().run()

    print("=== AutoImprovementSuggestion ===")
    print(f"状態: {result['status']}")
    print(f"Report数: {result['report_count']}")
    print(f"改善候補数: {result['suggestion_count']}")
    print(f"保存先: {result['output']}")


if __name__ == "__main__":
    main()