from pathlib import Path
from datetime import datetime
import json

from navikoLAB.app_operator.knowledge_learning_manager import (
    run_knowledge_learning_manager_diagnostics,
)

ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    report = run_knowledge_learning_manager_diagnostics()
    report["report_phase"] = "Phase9-5 Knowledge Learning Completion Report"
    report["phase9_completed"] = True
    report["next_phase"] = "Phase10 Reflection / Experience Learning Enhancement"

    out = REPORT_DIR / f"knowledge_learning_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Knowledge Learning Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["report_phase"])
    print("KnowledgeRecordSaved:", report["knowledge_record_saved"])
    print("IndexUpdated:", report["index_updated"])
    print("RecordCount:", report["record_count"])
    print("Phase9Completed:", report["phase9_completed"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("次工程:", report["next_phase"])
    print("保存先:", out)

if __name__ == "__main__":
    main()