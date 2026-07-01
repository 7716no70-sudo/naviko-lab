from pathlib import Path
from datetime import datetime
import json

from navikoLAB.app_operator.pipeline_workspace_save_adapter import (
    run_pipeline_workspace_save_adapter_diagnostics,
)

ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    report = run_pipeline_workspace_save_adapter_diagnostics()
    report["report_phase"] = "Phase8-9 Pipeline Workspace Save Adapter Report"

    out = REPORT_DIR / f"pipeline_workspace_save_adapter_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Pipeline Workspace Save Adapter Report ===")
    print("状態:", report["status"])
    print("工程:", report["report_phase"])
    print("MissionSaved:", report["mission_saved"])
    print("KnowledgeSaved:", report["knowledge_saved"])
    print("ReflectionSaved:", report["reflection_saved"])
    print("ExperienceSaved:", report["experience_saved"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("保存先:", out)

if __name__ == "__main__":
    main()