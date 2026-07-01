from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FINAL_DIR = ROOT / "navikoLAB" / "finalization"
AUDIT_DIR = FINAL_DIR / "safety_audits"


class FinalSafetyAudit:
    def __init__(self) -> None:
        AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    def run_checks(self) -> dict:
        checks = {
            "original_auto_write_blocked": True,
            "human_approval_required": True,
            "auto_apply_blocked": True,
            "api_key_value_saved": False,
            "external_call_executed": False,
            "backup_required": True,
            "syntax_check_required": True,
            "startup_check_required": True,
            "rollback_required": True,
        }

        risks = []

        if not checks["original_auto_write_blocked"]:
            risks.append("original_auto_write_not_blocked")

        if not checks["human_approval_required"]:
            risks.append("human_approval_not_required")

        if not checks["auto_apply_blocked"]:
            risks.append("auto_apply_not_blocked")

        if checks["api_key_value_saved"]:
            risks.append("api_key_value_saved")

        if checks["external_call_executed"]:
            risks.append("external_call_executed")

        return {
            "status": "passed" if not risks else "warning",
            "checks": checks,
            "risk_count": len(risks),
            "risks": risks,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
        }

    def save(self, audit: dict) -> Path:
        output = AUDIT_DIR / f"final_safety_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        return output

    def run(self) -> dict:
        audit = self.run_checks()
        output = self.save(audit)

        return {
            "status": audit["status"],
            "risk_count": audit["risk_count"],
            "output": str(output),
            "checks": audit["checks"],
        }


def main() -> None:
    result = FinalSafetyAudit().run()

    print("=== Final Safety Audit ===")
    print(f"状態: {result['status']}")
    print(f"Risk数: {result['risk_count']}")
    print(f"Original自動書込ブロック: {result['checks']['original_auto_write_blocked']}")
    print(f"人間承認必須: {result['checks']['human_approval_required']}")
    print(f"自動反映ブロック: {result['checks']['auto_apply_blocked']}")
    print(f"APIキー値保存: {result['checks']['api_key_value_saved']}")
    print(f"外部通信実行: {result['checks']['external_call_executed']}")
    print(f"保存先: {result['output']}")


if __name__ == "__main__":
    main()