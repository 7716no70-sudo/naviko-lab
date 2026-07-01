from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.autonomy.autonomy_diagnostics import AutonomyDiagnostics
from navikoLAB.autonomy.autonomy_safety_checker import AutonomySafetyChecker


ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "autonomy" / "reports"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    diagnostics = AutonomyDiagnostics().run()
    safety = AutonomySafetyChecker().run()

    status = "completed" if diagnostics["status"] == "passed" and safety["status"] == "passed" else "warning"

    result = {
        "status": status,
        "stage": "第33工程 自己改善自動ループ",
        "diagnostics": diagnostics,
        "safety": safety,
        "completed_items": [
            "SelfImprovementLoop",
            "AutonomySafetyChecker",
            "AutonomyDiagnostics",
            "AutonomyCompletionReport",
        ],
        "next_stage": "第34工程 Connector正式化 / ChatGPT API / Claude API / Gemini API / Grok API / Browser正式接続",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }

    output = REPORT_DIR / f"autonomy_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Autonomy Completion Report ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['stage']}")
    print(f"Loop数: {diagnostics['loop_count']}")
    print(f"安全状態: {safety['status']}")
    print(f"Original書込許可: {safety['original_write_allowed']}")
    print(f"自動反映許可: {safety['auto_apply_allowed']}")
    print(f"人間承認必須: {safety['human_approval_required']}")
    print(f"保存先: {output}")
    print(f"次工程: {result['next_stage']}")


if __name__ == "__main__":
    main()