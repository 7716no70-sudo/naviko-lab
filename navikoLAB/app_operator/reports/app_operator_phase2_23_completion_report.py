from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.adoption_plan.original_adoption_plan_builder import OriginalAdoptionPlanBuilder

def main():
    builder = OriginalAdoptionPlanBuilder()
    plan, plan_path = builder.build_plan()

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-23 Original Adoption Plan Builder",
        "plan_status": plan["status"],
        "adoption_mode": plan["adoption_mode"],
        "adoption_allowed": plan["adoption_allowed"],
        "requires_human_approval": plan["requires_human_approval"],
        "original_auto_write": plan["original_auto_write"],
        "original_write_executed": plan["original_write_executed"],
        "adoption_item_count": len(plan["adoption_items"]),
        "blocked_until": plan["blocked_until"],
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "plan_path": plan_path,
        "next_phase": "Phase2-24 Original Adoption DryRun Validator",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / f"app_operator_phase2_23_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-23 Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("PlanStatus:", report["plan_status"])
    print("AdoptionMode:", report["adoption_mode"])
    print("AdoptionAllowed:", report["adoption_allowed"])
    print("AdoptionItemCount:", report["adoption_item_count"])
    print("HumanApproval:", report["requires_human_approval"])
    print("OriginalAutoWrite:", report["original_auto_write"])
    print("OriginalWriteExecuted:", report["original_write_executed"])
    print("dry_run:", report["dry_run"])
    print("Real GUI Operation:", report["real_gui_operation"])
    print("外部操作実行:", report["external_operation"])
    print("Plan保存先:", plan_path)
    print("保存先:", out_path)
    print("次工程:", report["next_phase"])

if __name__ == "__main__":
    main()