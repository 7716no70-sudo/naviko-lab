from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "analyzers" / "reports"
REFLECTION_DIR = ROOT / "navikoLAB" / "architecture_reflection"


class ArchitectureReflection:
    def __init__(self) -> None:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        REFLECTION_DIR.mkdir(parents=True, exist_ok=True)

    def load_architecture_related_reports(self) -> dict:
        targets = {}

        for path in REPORT_DIR.glob("*.json"):
            name = path.stem.lower()

            if any(key in name for key in ["architecture", "dependency", "requirements", "documentation"]):
                try:
                    targets[path.stem] = json.loads(path.read_text(encoding="utf-8"))
                except Exception as e:
                    targets[path.stem] = {
                        "status": "read_failed",
                        "error": str(e),
                        "path": str(path),
                    }

        return targets

    def reflect(self, reports: dict) -> dict:
        findings = []
        recommendations = []

        if any("architecture" in name.lower() for name in reports):
            findings.append("ArchitectureAnalyzerの結果が存在する。")
            recommendations.append("設計診断結果を改善候補生成へ接続する。")

        if any("dependency" in name.lower() for name in reports):
            findings.append("DependencyAnalyzerの結果が存在する。")
            recommendations.append("依存関係とrequirements不足候補を継続監視する。")

        if any("documentation" in name.lower() for name in reports):
            findings.append("DocumentationCompletionReportが存在する。")
            recommendations.append("生成ドキュメントをKnowledgeBaseへ保存する導線を強化する。")

        if not findings:
            findings.append("設計反省に使えるレポートが不足している。")
            recommendations.append("Analyzer系CompletionReportの生成を優先する。")

        return {
            "status": "completed",
            "report_count": len(reports),
            "findings": findings,
            "recommendations": recommendations,
            "risk_level": "low",
            "next_action": "AutoImprovementSuggestionとAutoRefactoringPlanへ接続する。",
        }

    def save(self, reflection: dict) -> Path:
        output = REFLECTION_DIR / f"architecture_reflection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        data = {
            "stage": "第31工程 ArchitectureReflection",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            **reflection,
        }

        output.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return output

    def run(self) -> dict:
        reports = self.load_architecture_related_reports()
        reflection = self.reflect(reports)
        output = self.save(reflection)

        return {
            "status": reflection["status"],
            "report_count": reflection["report_count"],
            "finding_count": len(reflection["findings"]),
            "recommendation_count": len(reflection["recommendations"]),
            "output": str(output),
        }


def main() -> None:
    result = ArchitectureReflection().run()

    print("=== ArchitectureReflection ===")
    print(f"状態: {result['status']}")
    print(f"対象Report数: {result['report_count']}")
    print(f"Findings: {result['finding_count']}")
    print(f"Recommendations: {result['recommendation_count']}")
    print(f"保存先: {result['output']}")


if __name__ == "__main__":
    main()