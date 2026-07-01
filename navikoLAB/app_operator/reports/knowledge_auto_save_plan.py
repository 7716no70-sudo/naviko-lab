from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    report = {
        "status": "planned",
        "phase": "Phase9-1 Knowledge Auto Save Plan",
        "target": "enhance Workspace knowledge save into structured learning records",
        "write_scope": "navikoLAB/workspace/knowledge only",
        "original_write": False,
        "file_delete": False,
        "external_operation": False,
        "real_gui_operation": False,
        "requires_human_approval": True,
        "requires_permission_policy": True,
        "planned_features": [
            "structured knowledge record",
            "mission summary extraction",
            "pipeline status preservation",
            "risk and safety metadata preservation",
            "future learning index base",
        ],
        "risk_count": 0,
        "safe_to_continue": True,
        "next_phase": "Phase9-2 Knowledge Auto Save Core",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"knowledge_auto_save_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Knowledge Auto Save Plan ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("Target:", report["target"])
    print("WriteScope:", report["write_scope"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("次工程:", report["next_phase"])
    print("保存先:", out)

if __name__ == "__main__":
    main()