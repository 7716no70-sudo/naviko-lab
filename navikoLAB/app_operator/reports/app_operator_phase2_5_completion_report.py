from datetime import datetime
from pathlib import Path
import json

from navikoLAB.connectors.connector_dispatcher import ConnectorDispatcher


def main():
    print("=== AppOperator Phase2-5 Completion Report ===")

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = Path(__file__).resolve().parent
    report_dir.mkdir(parents=True, exist_ok=True)

    dispatcher = ConnectorDispatcher()

    checks = {
        "ocr_planner": {
            "action": "ocr_plan",
            "target": "sample_window_area",
        },
        "safety_guard_safe_action": {
            "action": "mouse_click_plan",
            "target": "sample_button",
            "x": 100,
            "y": 200,
        },
        "safety_guard_blocked_action": {
            "action": "delete_file",
            "target": "sample.txt",
        },
    }

    results = {}

    for name, context in checks.items():
        results[name] = dispatcher.run(
            agent_id="real_app_operator",
            goal=f"{name} phase2-5 completion check",
            context=context,
        )

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-5 OCR Planner / GUI Automation Safety Guard",
        "ocr_status": results["ocr_planner"].get("status"),
        "ocr_component": results["ocr_planner"].get("component"),
        "safe_action_status": results["safety_guard_safe_action"].get("status"),
        "safe_action_component": results["safety_guard_safe_action"].get("component"),
        "blocked_action_status": results["safety_guard_blocked_action"].get("status"),
        "blocked_action_component": results["safety_guard_blocked_action"].get("component"),
        "dry_run": True,
        "external_operation_executed": False,
        "completed_items": [
            "OCRPlanner dry_run basis created",
            "OCRPlanner connected to RealAppOperatorConnector",
            "GUIAutomationSafetyGuard created",
            "SafetyGuard connected to RealAppOperatorConnector",
            "Dangerous GUI action block confirmed",
            "System diagnostics updated",
            "Blocked action treated as expected safe result",
        ],
        "remaining_tasks": [
            "HumanApproval gate implementation",
            "Real GUI operation permission model",
            "Window enumeration implementation",
            "Active window detection",
            "Real screen capture only after approval",
            "Real OCR execution only after approval",
        ],
        "next_phase": "Post-v2.0 Phase2-6 HumanApproval Gate for AppOperator",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    report_path = report_dir / f"app_operator_phase2_5_completion_report_{now}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("OCR:", report["ocr_status"], "/", report["ocr_component"])
    print("SafeAction:", report["safe_action_status"], "/", report["safe_action_component"])
    print("BlockedAction:", report["blocked_action_status"], "/", report["blocked_action_component"])
    print("dry_run:", report["dry_run"])
    print("外部操作実行:", report["external_operation_executed"])
    print("保存先:", report_path)
    print("次工程:", report["next_phase"])


if __name__ == "__main__":
    main()