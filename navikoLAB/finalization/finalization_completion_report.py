from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.finalization.final_integration_diagnostics import FinalIntegrationDiagnostics
from navikoLAB.finalization.project_completion_score import ProjectCompletionScore
from navikoLAB.finalization.final_roadmap import FinalRoadmap


ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "finalization" / "reports"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    diagnostics = FinalIntegrationDiagnostics().run()
    score = ProjectCompletionScore().calculate()
    roadmap = FinalRoadmap().build()

    status = "completed" if diagnostics["status"] == "passed" else "warning"

    result = {
        "status": status,
        "stage": "第36工程 最終統合診断 / ProjectCompletionScore / FinalRoadmap",
        "diagnostics": diagnostics,
        "score": score,
        "roadmap": roadmap,
        "completed_items": [
            "FinalIntegrationDiagnostics",
            "ProjectCompletionScore",
            "FinalRoadmap",
            "FinalizationCompletionReport",
        ],
        "next_stage": "第37工程 FinalSafetyAudit / Original反映前の最終安全監査",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }

    output = REPORT_DIR / f"finalization_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Finalization Completion Report ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['stage']}")
    print(f"確認項目数: {diagnostics['target_count']}")
    print(f"通過数: {diagnostics['passed_count']}")
    print(f"不足数: {diagnostics['missing_count']}")
    print(f"総合完成度: {score['overall_score']}%")
    print(f"Roadmap数: {roadmap['roadmap_count']}")
    print(f"保存先: {output}")
    print(f"次工程: {result['next_stage']}")


if __name__ == "__main__":
    main()