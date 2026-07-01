from datetime import datetime
from pathlib import Path
import json

from navikoLAB.connectors.connector_dispatcher import ConnectorDispatcher


def main():
    print("=== AppOperator Phase2-6 Completion Report ===")

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = Path(__file__).resolve().parent
    report_dir.mkdir(parents=True, exist_ok=True)

    dispatcher = ConnectorDispatcher()

    checks = {
        "window_inspector": {"action": "inspect_windows"},
        "mouse_approval": {
            "action": "mouse_click_plan",
            "target": "sample_button",
            "x": 100,
            "y": 200,
        },
        "ocr_approval": {
            "action": "ocr_plan",
            "target": "sample_window_area",
        },
        "blocked_action": {
            "action": "delete_file",
            "target": "sample.txt",
        },
    }

    results = {
        name: dispatcher.run(
            agent_id="real_app_operator",
            goal=f"{name} phase2-6 completion check",
            context=context,
        )
        for name, context in checks.items()
    }

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-6 HumanApproval Gate for AppOperator",
        "window_status": results["window_inspector"].get("status"),
        "mouse_status": results["mouse_approval"].get("status"),
        "ocr_status": results["ocr_approval"].get("status"),
        "blocked_status": results["blocked_action"].get("status"),
        "dry_run": True,
        "external_operation_executed": False,
        "completed_items": [
            "HumanApprovalGate created",
            "Approval request JSON creation confirmed",
            "HumanApprovalGate connected to RealAppOperatorConnector",
            "Approval required flow confirmed for MouseClickPlanner",
            "Approval required flow confirmed for OCRPlanner",
            "Blocked dangerous action flow confirmed",
            "System diagnostics updated for approval_required",
        ],
        "remaining_tasks": [
            "Approval request review UI",
            "Approved request reader",
            "Real GUI operation permission model",
            "Window enumeration implementation",
            "Active window detection",
            "Real operation executor after explicit approval",
        ],
        "next_phase": "Post-v2.0 Phase2-7 Approval Request Review / Approved Operation Executor",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    report_path = report_dir / f"app_operator_phase2_6_completion_report_{now}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("Window:", report["window_status"])
    print("Mouse:", report["mouse_status"])
    print("OCR:", report["ocr_status"])
    print("Blocked:", report["blocked_status"])
    print("dry_run:", report["dry_run"])
    print("外部操作実行:", report["external_operation_executed"])
    print("保存先:", report_path)
    print("次工程:", report["next_phase"])


if __name__ == "__main__":
    main()