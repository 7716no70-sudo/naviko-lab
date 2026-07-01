from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    result = {
        "phase": "Phase6-6",
        "name": "HumanApproval Approved Simulation",
        "status": "simulated",
        "human_approved_simulation": True,
        "real_execution_allowed": False,
        "reason": "approval_simulation_only",
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "original_write": False,
        "next_phase": "Phase6-7 PermissionPolicy Approved Simulation",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"human_approval_approved_simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== HumanApproval Approved Simulation ===")
    print("状態: simulated")
    print("工程: Phase6-6 HumanApproval Approved Simulation")
    print("HumanApprovedSimulation: True")
    print("RealExecutionAllowed: False")
    print("Reason: approval_simulation_only")
    print("dry_run: True")
    print("外部操作実行: False")
    print("Real GUI Operation: False")
    print("Original書込: False")
    print("次工程: Phase6-7 PermissionPolicy Approved Simulation")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()