from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.approval.app_operator_dry_run_pipeline import AppOperatorDryRunPipeline
from navikoLAB.app_operator.policy.permission_policy import PermissionPolicy

class AppOperatorIntegratedDiagnostics:
    def __init__(self):
        self.root = Path(__file__).resolve().parents[1]
        self.pipeline = AppOperatorDryRunPipeline()
        self.policy = PermissionPolicy()

    def check_dirs(self):
        targets = [
            "components",
            "approval",
            "approval_requests",
            "approval_logs",
            "approval_decisions",
            "executors",
            "policy",
            "diagnostics",
            "reports",
        ]

        return {
            name: (self.root / name).exists()
            for name in targets
        }

    def run_policy_check(self):
        actions = [
            "report_generate",
            "browser_search",
            "mouse_click",
            "keyboard_input",
            "delete_file",
        ]
        return [self.policy.classify(action) for action in actions]

    def run_pipeline_check(self):
        operations = [
            {"request_id": "diag_report", "action": "report_generate"},
            {"request_id": "diag_browser", "action": "browser_search"},
            {"request_id": "diag_mouse", "action": "mouse_click"},
            {"request_id": "diag_delete", "action": "delete_file"},
        ]
        return [self.pipeline.run(op) for op in operations]

    def run(self):
        dirs = self.check_dirs()
        policy_results = self.run_policy_check()
        pipeline_results = self.run_pipeline_check()

        return {
            "status": "completed",
            "diagnostic": "AppOperatorIntegratedDiagnostics",
            "dir_check": dirs,
            "dir_all_ok": all(dirs.values()),
            "policy_check_count": len(policy_results),
            "policy_results": policy_results,
            "pipeline_check_count": len(pipeline_results),
            "pipeline_results": pipeline_results,
            "dry_run": True,
            "external_operation": False,
            "real_gui_operation": False,
            "checked_at": datetime.now().isoformat(timespec="seconds"),
        }

def main():
    diagnostics = AppOperatorIntegratedDiagnostics()
    result = diagnostics.run()

    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / f"app_operator_integrated_diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Integrated Diagnostics ===")
    print("状態:", result["status"])
    print("DirAllOK:", result["dir_all_ok"])
    print("PolicyCheckCount:", result["policy_check_count"])
    print("PipelineCheckCount:", result["pipeline_check_count"])
    print("dry_run:", result["dry_run"])
    print("Real GUI Operation:", result["real_gui_operation"])
    print("外部操作実行:", result["external_operation"])
    print("保存先:", out_path)

if __name__ == "__main__":
    main()