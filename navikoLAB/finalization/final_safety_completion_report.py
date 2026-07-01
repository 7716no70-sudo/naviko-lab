from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.finalization.final_safety_audit import FinalSafetyAudit
from navikoLAB.finalization.final_safety_diagnostics import FinalSafetyDiagnostics
from navikoLAB.finalization.original_preflight_check import OriginalPreflightCheck


ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "finalization" / "reports"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    audit = FinalSafetyAudit().run()
    preflight = OriginalPreflightCheck().run()
    diagnostics = FinalSafetyDiagnostics().run()

    status = (
        "completed"
        if audit["status"] == "passed"
        and diagnostics["status"] == "passed"
        and preflight["status"] == "passed"
        else "warning"
    )

    result = {
        "status": status,
        "stage": "第37工程 FinalSafetyAudit / Original反映前の最終安全監査",
        "audit": audit,
        "preflight": preflight,
        "diagnostics": diagnostics,
        "completed_items": [
            "FinalSafetyAudit",
            "OriginalPreflightCheck",
            "FinalSafetyDiagnostics",
            "FinalSafetyCompletionReport",
        ],
        "safety_policy": {
            "original_auto_write_allowed": False,
            "auto_apply_allowed": False,
            "human_approval_required": True,
            "backup_required": True,
            "syntax_check_required": True,
            "startup_check_required": True,
            "rollback_required": True,
        },
        "next_stage": "第38工程 OriginalNaviko Bridge / LAB統合パイプラインをOriginalへ渡す橋渡し層",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }

    output = REPORT_DIR / f"final_safety_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Final Safety Completion Report ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['stage']}")
    print(f"Audit数: {diagnostics['audit_count']}")
    print(f"Original存在: {preflight['exists']}")
    print(f"Original構文OK: {preflight['syntax_ok']}")
    print(f"Risk数: {audit['risk_count'] + preflight['risk_count']}")
    print(f"Original自動書込許可: {result['safety_policy']['original_auto_write_allowed']}")
    print(f"自動反映許可: {result['safety_policy']['auto_apply_allowed']}")
    print(f"人間承認必須: {result['safety_policy']['human_approval_required']}")
    print(f"保存先: {output}")
    print(f"次工程: {result['next_stage']}")


if __name__ == "__main__":
    main()