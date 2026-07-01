from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.original_adoption.human_review_approval_record import HumanReviewApprovalRecord

def main():
    recorder = HumanReviewApprovalRecord()

    record, record_path = recorder.create_record(
        approved=True,
        reviewer="human",
        reason="Phase2-27 records human approval for dry_run adoption only"
    )

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-27 Human Review Approval Record",
        "record_status": record["status"],
        "approved": record["approved"],
        "record_path": record_path,
        "original_adoption_allowed": record["original_adoption_allowed"],
        "original_auto_write": record["original_auto_write"],
        "original_write_executed": record["original_write_executed"],
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "next_phase": "Phase2-28 Original Adoption DryRun Package Builder",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_path = Path(__file__).resolve().parent / f"app_operator_phase2_27_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-27 Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("RecordStatus:", report["record_status"])
    print("Approved:", report["approved"])
    print("OriginalAdoptionAllowed:", report["original_adoption_allowed"])
    print("OriginalAutoWrite:", report["original_auto_write"])
    print("OriginalWriteExecuted:", report["original_write_executed"])
    print("dry_run:", report["dry_run"])
    print("Real GUI Operation:", report["real_gui_operation"])
    print("外部操作実行:", report["external_operation"])
    print("Record保存先:", record_path)
    print("保存先:", out_path)
    print("次工程:", report["next_phase"])

if __name__ == "__main__":
    main()