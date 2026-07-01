from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.original_adoption.app_operator_adoption_request import AppOperatorAdoptionRequest
from navikoLAB.app_operator.original_adoption.original_adoption_approval_gate import OriginalAdoptionApprovalGate

def main():
    adoption = AppOperatorAdoptionRequest()
    request, request_path = adoption.create_request(
        bridge_payload_path="phase2_19_test_bridge_payload"
    )

    gate = OriginalAdoptionApprovalGate()
    gate_result, gate_path = gate.evaluate(request)

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-19 HumanApproval Gate for Original Adoption",
        "adoption_request_path": request_path,
        "gate_path": gate_path,
        "gate_status": gate_result["gate_status"],
        "reason": gate_result["reason"],
        "requires_human_approval": gate_result["requires_human_approval"],
        "original_auto_write": gate_result["original_auto_write"],
        "original_write_executed": gate_result["original_write_executed"],
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "next_phase": "Phase2-20 AppOperator Adoption Final Safety Report",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / f"app_operator_phase2_19_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-19 Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("GateStatus:", report["gate_status"])
    print("Reason:", report["reason"])
    print("HumanApproval:", report["requires_human_approval"])
    print("OriginalAutoWrite:", report["original_auto_write"])
    print("OriginalWriteExecuted:", report["original_write_executed"])
    print("dry_run:", report["dry_run"])
    print("Real GUI Operation:", report["real_gui_operation"])
    print("外部操作実行:", report["external_operation"])
    print("Gate保存先:", gate_path)
    print("保存先:", out_path)
    print("次工程:", report["next_phase"])

if __name__ == "__main__":
    main()