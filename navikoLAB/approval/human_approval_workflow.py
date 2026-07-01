from datetime import datetime
from pathlib import Path
import json
import shutil
import py_compile
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL_FILE = ROOT.parent / "naviko" / "naviko.py"
APPROVAL_DIR = ROOT / "navikoLAB" / "approval"
REQUEST_DIR = APPROVAL_DIR / "requests"
BACKUP_DIR = APPROVAL_DIR / "backups"
REPORT_DIR = APPROVAL_DIR / "reports"


class HumanApprovalWorkflow:
    def __init__(self):
        self.direct_write = False
        self.auto_apply = False
        self.human_approval_required = True

    def create_request(self, payload: dict):
        REQUEST_DIR.mkdir(parents=True, exist_ok=True)

        request = {
            "status": "pending_human_approval",
            "created_at": datetime.now().isoformat(),
            "payload": payload,
            "direct_write": False,
            "auto_apply": False,
            "human_approval_required": True,
            "approved": False,
        }

        path = REQUEST_DIR / f"approval_request_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")
        return request, path

    def approve_request(self, request_path: Path):
        data = json.loads(request_path.read_text(encoding="utf-8"))
        data["approved"] = True
        data["status"] = "approved_by_human"
        data["approved_at"] = datetime.now().isoformat()
        request_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return data

    def backup_original(self):
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

        if not ORIGINAL_FILE.exists():
            return None

        backup_path = BACKUP_DIR / f"naviko_backup_before_approval_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        shutil.copy2(ORIGINAL_FILE, backup_path)
        return backup_path

    def syntax_check_original(self):
        if not ORIGINAL_FILE.exists():
            return False, "Original naviko.py not found"

        try:
            py_compile.compile(str(ORIGINAL_FILE), doraise=True)
            return True, "syntax ok"
        except Exception as e:
            return False, str(e)

    def startup_check_original(self):
        if not ORIGINAL_FILE.exists():
            return False, "Original naviko.py not found"

        try:
            result = subprocess.run(
                [sys.executable, str(ORIGINAL_FILE), "--self-test"],
                capture_output=True,
                text=True,
                timeout=20,
            )
            return result.returncode == 0, result.stdout[-1000:] + result.stderr[-1000:]
        except Exception as e:
            return False, str(e)

    def run_pre_apply_checks(self):
        backup_path = self.backup_original()
        syntax_ok, syntax_message = self.syntax_check_original()
        startup_ok, startup_message = self.startup_check_original()

        result = {
            "status": "passed" if backup_path and syntax_ok and startup_ok else "failed",
            "backup_created": backup_path is not None,
            "backup_path": str(backup_path) if backup_path else None,
            "syntax_ok": syntax_ok,
            "syntax_message": syntax_message,
            "startup_ok": startup_ok,
            "startup_message": startup_message,
            "direct_write": False,
            "auto_apply": False,
            "human_approval_required": True,
            "rollback_required": True,
        }

        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        path = REPORT_DIR / f"pre_apply_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

        return result, path


if __name__ == "__main__":
    workflow = HumanApprovalWorkflow()

    request, request_path = workflow.create_request({
        "source": "Bridge",
        "target": "Original Naviko",
        "purpose": "diagnostic approval request",
    })

    check, check_path = workflow.run_pre_apply_checks()

    print("=== HumanApprovalWorkflow ===")
    print("申請状態:", request["status"])
    print("申請保存先:", request_path)
    print("事前確認:", check["status"])
    print("バックアップ:", check["backup_created"])
    print("構文チェック:", check["syntax_ok"])
    print("起動確認:", check["startup_ok"])
    print("Original直接書込:", check["direct_write"])
    print("自動反映:", check["auto_apply"])
    print("人間承認必須:", check["human_approval_required"])
    print("確認保存先:", check_path)