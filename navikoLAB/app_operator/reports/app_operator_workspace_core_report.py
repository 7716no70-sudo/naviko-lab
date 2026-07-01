from pathlib import Path
from datetime import datetime
import json

from navikoLAB.app_operator.app_operator_workspace_core import run_workspace_core_diagnostics

ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    report = run_workspace_core_diagnostics()
    report["report_phase"] = "Phase8-3 Workspace Core Report"

    out = REPORT_DIR / f"app_operator_workspace_core_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Workspace Core Report ===")
    print("状態:", report["status"])
    print("工程:", report["report_phase"])
    print("WorkspaceInitialized:", report["workspace_initialized"])
    print("MissionResultSaved:", report["mission_result_saved"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("保存先:", out)

if __name__ == "__main__":
    main()