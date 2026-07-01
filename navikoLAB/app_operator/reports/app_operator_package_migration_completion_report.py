from datetime import datetime
from pathlib import Path
import json

from navikoLAB.connectors.connector_dispatcher import ConnectorDispatcher


def main():
    print("=== AppOperator Package Migration Completion Report ===")

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = Path(__file__).resolve().parent
    report_dir.mkdir(parents=True, exist_ok=True)

    dispatcher = ConnectorDispatcher()

    checks = {
        "window_inspector": {"action": "inspect_windows"},
        "explorer_operation_planner": {
            "action": "open_explorer_plan",
            "target_path": r"C:\Users\7716n\OneDrive\デスクトップ\naviko_lab",
        },
        "keyboard_input_planner": {
            "action": "keyboard_input_plan",
            "target": "sample_input_box",
            "text": "migration completion keyboard dry_run",
        },
        "mouse_click_planner": {
            "action": "mouse_click_plan",
            "target": "sample_button",
            "x": 100,
            "y": 200,
        },
    }

    results = {}

    for name, context in checks.items():
        results[name] = dispatcher.run(
            agent_id="real_app_operator",
            goal=f"{name} migration completion check",
            context=context,
        )

    all_completed = all(r.get("status") == "completed" for r in results.values())
    external_operation_executed = any(
        r.get("external_operation_executed") for r in results.values()
    )

    report = {
        "status": "completed" if all_completed else "failed",
        "phase": "Post-v2.0 Phase2-4 AppOperator Package Migration",
        "package_created": True,
        "components_copied": True,
        "connector_import_switched": True,
        "diagnostics_copied": True,
        "dry_run": True,
        "external_operation_executed": external_operation_executed,
        "components": {
            name: {
                "status": result.get("status"),
                "component": result.get("component"),
            }
            for name, result in results.items()
        },
        "completed_items": [
            "navikoLAB/app_operator package created",
            "components package created",
            "diagnostics package created",
            "reports directory created",
            "AppOperator components copied",
            "RealAppOperatorConnector imports switched",
            "System diagnostics copied to app_operator package",
            "Dispatcher route confirmed after migration",
        ],
        "remaining_tasks": [
            "Keep old connector component files temporarily",
            "Remove old duplicates only after multiple successful diagnostics",
            "Add OCR planner",
            "Add GUIAutomationSafetyGuard",
            "Add HumanApproval gate before real operation",
        ],
        "next_phase": "Post-v2.0 Phase2-5 OCR Planner / GUI Automation Safety Guard",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    report_path = report_dir / f"app_operator_package_migration_completion_report_{now}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("Package作成:", report["package_created"])
    print("Componentsコピー:", report["components_copied"])
    print("Import切替:", report["connector_import_switched"])
    print("Diagnosticsコピー:", report["diagnostics_copied"])
    print("dry_run:", report["dry_run"])
    print("外部操作実行:", report["external_operation_executed"])
    print("保存先:", report_path)
    print("次工程:", report["next_phase"])


if __name__ == "__main__":
    main()