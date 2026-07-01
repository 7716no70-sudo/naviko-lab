from datetime import datetime
from pathlib import Path
import json

from navikoLAB.connectors.connector_dispatcher import ConnectorDispatcher


def main():
    print("=== Real App Operator Phase2-2 Completion Report ===")

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = Path(__file__).resolve().parent / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    dispatcher = ConnectorDispatcher()

    window_result = dispatcher.run(
        agent_id="real_app_operator",
        goal="Phase2-2 WindowInspector completion check",
        context={"action": "inspect_windows"},
    )

    explorer_result = dispatcher.run(
        agent_id="real_app_operator",
        goal="Phase2-2 ExplorerOperationPlanner completion check",
        context={
            "action": "open_explorer_plan",
            "target_path": r"C:\Users\7716n\OneDrive\デスクトップ\naviko_lab",
        },
    )

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-2 WindowInspector / ExplorerOperationPlanner",
        "window_inspector_status": window_result.get("status"),
        "window_inspector_component": window_result.get("component"),
        "explorer_planner_status": explorer_result.get("status"),
        "explorer_planner_component": explorer_result.get("component"),
        "dry_run": True,
        "external_operation_executed": False,
        "completed_items": [
            "WindowInspector dry_run basis created",
            "ExplorerOperationPlanner dry_run basis created",
            "RealAppOperatorConnector component routing added",
            "ConnectorDispatcher context passthrough fixed",
            "Dispatcher to WindowInspector confirmed",
            "Dispatcher to ExplorerOperationPlanner confirmed",
        ],
        "remaining_tasks": [
            "KeyboardInputPlanner",
            "MouseClickPlanner",
            "GUIAutomationSafetyGuard",
            "HumanApproval gate before real GUI operation",
            "Real Explorer operation after explicit approval",
        ],
        "next_phase": "Post-v2.0 Phase2-3 KeyboardInputPlanner / MouseClickPlanner",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    report_path = report_dir / f"real_app_operator_phase2_2_completion_report_{now}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("WindowInspector:", report["window_inspector_status"], "/", report["window_inspector_component"])
    print("ExplorerOperationPlanner:", report["explorer_planner_status"], "/", report["explorer_planner_component"])
    print("dry_run:", report["dry_run"])
    print("外部操作実行:", report["external_operation_executed"])
    print("保存先:", report_path)
    print("次工程:", report["next_phase"])


if __name__ == "__main__":
    main()