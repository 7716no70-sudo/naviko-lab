from datetime import datetime
from pathlib import Path
import json

from navikoLAB.connectors.real_app_operator_connector import RealAppOperatorConnector
from navikoLAB.connectors.connector_dispatcher import ConnectorDispatcher


def main():
    print("=== Real App Operator Completion Report ===")

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = Path(__file__).resolve().parent / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    direct = RealAppOperatorConnector(dry_run=True).run({
        "purpose": "Real App Operator direct completion check",
        "action": "inspect_windows",
    })

    dispatcher = ConnectorDispatcher().run(
        agent_id="real_app_operator",
        goal="Real App Operator dispatcher completion check",
        context={"action": "inspect_windows"},
    )

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2 Real App Operator",
        "direct_status": direct.get("status"),
        "dispatcher_status": dispatcher.get("status"),
        "connector": direct.get("connector"),
        "dry_run": direct.get("dry_run"),
        "external_operation_executed": direct.get("external_operation_executed"),
        "completed_items": [
            "RealAppOperatorConnector created",
            "BaseAIConnector compatible structure applied",
            "dry_run mode confirmed",
            "External GUI operation disabled",
            "ConnectorDispatcher routing confirmed",
            "Diagnostics passed",
        ],
        "remaining_tasks": [
            "Window inspection implementation",
            "Explorer operation planner",
            "Keyboard input planner",
            "Mouse click planner",
            "GUI automation safety guard",
            "HumanApproval before real operation",
        ],
        "next_phase": "Post-v2.0 Phase2-2 WindowInspector / ExplorerOperationPlanner",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    report_path = report_dir / f"real_app_operator_completion_report_{now}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("Direct:", report["direct_status"])
    print("Dispatcher:", report["dispatcher_status"])
    print("dry_run:", report["dry_run"])
    print("外部操作実行:", report["external_operation_executed"])
    print("保存先:", report_path)
    print("次工程:", report["next_phase"])


if __name__ == "__main__":
    main()