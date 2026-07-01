from pathlib import Path
from datetime import datetime
import json
import platform
from navikoLAB.connectors.base_ai_connector import BaseAIConnector
from navikoLAB.app_operator.components.window_inspector import WindowInspector
from navikoLAB.app_operator.components.explorer_operation_planner import ExplorerOperationPlanner
from navikoLAB.app_operator.components.keyboard_input_planner import KeyboardInputPlanner
from navikoLAB.app_operator.components.mouse_click_planner import MouseClickPlanner
from navikoLAB.app_operator.components.gui_automation_safety_guard import GUIAutomationSafetyGuard
from navikoLAB.app_operator.components.ocr_planner import OCRPlanner
from navikoLAB.app_operator.components.human_approval_gate import HumanApprovalGate

class RealAppOperatorConnector(BaseAIConnector):
    connector_name = "real_app_operator"
    default_model = "windows_gui_dry_run"
    provider_key = "REAL_APP_OPERATOR"

    """
    Phase2 Real App Operator 基盤。
    初期段階では dry_run のみ。
    実クリック・実入力・外部操作は行わない。
    """

    def __init__(self, dry_run=True):
        super().__init__(
            model=self.default_model,
            api_key="dry_run_enabled",
        )
        self.dry_run = dry_run
        self.log_dir = Path(__file__).resolve().parent / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def run(self, task):
        action = task.get("action", "")

        guard = GUIAutomationSafetyGuard(dry_run=self.dry_run)
        guard_result = guard.check(task)

        if guard_result.get("blocked"):
            return guard_result

        if guard_result.get("requires_human_approval"):
            gate = HumanApprovalGate(dry_run=self.dry_run)
            return gate.request_approval(task)

        if action == "inspect_windows":
            inspector = WindowInspector(dry_run=self.dry_run)
            return inspector.inspect()

        if action == "open_explorer_plan":
            planner = ExplorerOperationPlanner(dry_run=self.dry_run)
            return planner.plan(task)

        if action == "keyboard_input_plan":
            planner = KeyboardInputPlanner(dry_run=self.dry_run)
            return planner.plan(task)

        if action == "mouse_click_plan":
            planner = MouseClickPlanner(dry_run=self.dry_run)
            return planner.plan(task)

        if action == "ocr_plan":
            planner = OCRPlanner(dry_run=self.dry_run)
            return planner.plan(task)

        result = {
            "status": "completed",
            "connector": self.connector_name,
            "dry_run": self.dry_run,
            "external_operation_executed": False,
            "os": platform.system(),
            "task": task,
            "supported_actions": [
                "inspect_windows",
                "open_explorer_plan",
                "keyboard_input_plan",
                "mouse_click_plan",
                "gui_automation_plan",
            ],
            "message": "Real App Operator dry_run completed. No real GUI operation executed.",
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }

        self.write_log(result)
        return result

    def write_log(self, data):
        path = self.log_dir / f"real_app_operator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path