from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.policy.permission_policy_integrator import PermissionPolicyIntegrator
from navikoLAB.app_operator.executors.real_gui_operation_executor import RealGUIOperationExecutor

def main():
    integrator = PermissionPolicyIntegrator()
    executor = RealGUIOperationExecutor(dry_run=True)

    operations = [
        {"action": "report_generate", "source": "phase2_10_test"},
        {"action": "browser_search", "source": "phase2_10_test"},
        {"action": "mouse_click", "source": "phase2_10_test"},
        {"action": "keyboard_input", "source": "phase2_10_test"},
        {"action": "delete_file", "source": "phase2_10_test"},
    ]

    integrated = [integrator.apply(op) for op in operations]

    execution_results = []
    for op in integrated:
        if op["permission_level"] == 1:
            execution_results.append(executor.execute(op))
        else:
            execution_results.append({
                "action": op["action"],
                "status": op["route"],
                "permission_level": op["permission_level"],
                "permission_type": op["permission_type"],
                "dry_run": True,
                "external_operation": False,
                "real_gui_operation": False,
            })

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-10 PermissionPolicy integration with AppOperator",
        "integrated_count": len(integrated),
        "integrated_operations": integrated,
        "execution_results": execution_results,
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "next_phase": "Phase2-11 Approval UI / Approval Log Manager",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / f"app_operator_phase2_10_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-10 Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("IntegratedCount:", report["integrated_count"])
    print("dry_run:", report["dry_run"])
    print("Real GUI Operation:", report["real_gui_operation"])
    print("外部操作実行:", report["external_operation"])
    print("保存先:", out_path)
    print("次工程:", report["next_phase"])

if __name__ == "__main__":
    main()