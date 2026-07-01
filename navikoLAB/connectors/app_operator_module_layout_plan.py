from datetime import datetime
from pathlib import Path
import json


def main():
    print("=== AppOperator Module Layout Plan ===")

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = Path(__file__).resolve().parent / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    plan = {
        "status": "planned",
        "phase": "Post-v2.0 Phase2-4 AppOperator module layout planning",
        "policy": {
            "no_file_move_in_this_step": True,
            "dry_run_only": True,
            "external_operation_executed": False,
            "keep_connector_dispatcher_compatibility": True,
        },
        "current_files": [
            "navikoLAB/connectors/real_app_operator_connector.py",
            "navikoLAB/connectors/window_inspector.py",
            "navikoLAB/connectors/explorer_operation_planner.py",
            "navikoLAB/connectors/keyboard_input_planner.py",
            "navikoLAB/connectors/mouse_click_planner.py",
        ],
        "planned_layout": {
            "connector_entry": "navikoLAB/connectors/real_app_operator_connector.py",
            "app_operator_root": "navikoLAB/app_operator",
            "components": [
                "navikoLAB/app_operator/components/window_inspector.py",
                "navikoLAB/app_operator/components/explorer_operation_planner.py",
                "navikoLAB/app_operator/components/keyboard_input_planner.py",
                "navikoLAB/app_operator/components/mouse_click_planner.py",
            ],
            "diagnostics": [
                "navikoLAB/app_operator/diagnostics/app_operator_system_diagnostics.py"
            ],
            "reports": [
                "navikoLAB/app_operator/reports/"
            ],
        },
        "migration_steps": [
            "Create navikoLAB/app_operator package folders",
            "Copy current component files into app_operator/components",
            "Update real_app_operator_connector imports",
            "Run unified system diagnostics",
            "Keep old connector component files temporarily",
            "Remove old duplicates only after full confirmation",
        ],
        "risk_level": "low",
        "next_phase": "Post-v2.0 Phase2-4 Create AppOperator package folders",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    report_path = report_dir / f"app_operator_module_layout_plan_{now}.json"
    report_path.write_text(
        json.dumps(plan, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("状態:", plan["status"])
    print("工程:", plan["phase"])
    print("dry_run:", plan["policy"]["dry_run_only"])
    print("外部操作実行:", plan["policy"]["external_operation_executed"])
    print("リスク:", plan["risk_level"])
    print("保存先:", report_path)
    print("次工程:", plan["next_phase"])


if __name__ == "__main__":
    main()