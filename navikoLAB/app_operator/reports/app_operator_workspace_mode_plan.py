from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def build_report():
    return {
        "status": "planned",
        "phase": "Phase8-1 AppOperator Workspace Mode Plan",
        "workspace_mode": True,
        "allowed_write_scope": "navikoLAB/workspace only",
        "original_write_allowed": False,
        "external_operation_allowed": False,
        "real_gui_operation_allowed": False,
        "file_delete_allowed": False,
        "requires_human_approval": True,
        "requires_permission_policy": True,
        "planned_outputs": [
            "Mission result save",
            "Knowledge auto save",
            "Reflection auto save",
            "Experience auto save",
            "Workspace artifact generation",
        ],
        "risk_count": 0,
        "safe_to_continue": True,
        "next_phase": "Phase8-2 AppOperator Workspace Core",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }

def main():
    report = build_report()
    out = REPORT_DIR / f"app_operator_workspace_mode_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Workspace Mode Plan ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("WorkspaceMode:", report["workspace_mode"])
    print("AllowedWriteScope:", report["allowed_write_scope"])
    print("OriginalWriteAllowed:", report["original_write_allowed"])
    print("ExternalOperationAllowed:", report["external_operation_allowed"])
    print("RealGUIOperationAllowed:", report["real_gui_operation_allowed"])
    print("FileDeleteAllowed:", report["file_delete_allowed"])
    print("HumanApprovalRequired:", report["requires_human_approval"])
    print("PermissionPolicyRequired:", report["requires_permission_policy"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("次工程:", report["next_phase"])
    print("保存先:", out)

if __name__ == "__main__":
    main()