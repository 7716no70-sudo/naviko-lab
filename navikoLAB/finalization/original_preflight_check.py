from __future__ import annotations

import py_compile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ORIGINAL_FILE = ROOT / "naviko.py"
LAB_FILE = ROOT / "naviko.py"


class OriginalPreflightCheck:
    def check_file_exists(self) -> bool:
        return ORIGINAL_FILE.exists()

    def check_syntax(self) -> tuple[bool, str]:
        if not ORIGINAL_FILE.exists():
            return False, "naviko.py not found"

        try:
            py_compile.compile(str(ORIGINAL_FILE), doraise=True)
            return True, "syntax_ok"
        except Exception as e:
            return False, str(e)

    def run(self) -> dict:
        exists = self.check_file_exists()
        syntax_ok, syntax_message = self.check_syntax()

        risks = []

        if not exists:
            risks.append("original_file_missing")

        if not syntax_ok:
            risks.append("original_syntax_error")

        return {
            "status": "passed" if not risks else "warning",
            "original_file": str(ORIGINAL_FILE),
            "exists": exists,
            "syntax_ok": syntax_ok,
            "syntax_message": syntax_message,
            "backup_required": True,
            "startup_check_required": True,
            "rollback_required": True,
            "risk_count": len(risks),
            "risks": risks,
        }


def main() -> None:
    result = OriginalPreflightCheck().run()

    print("=== Original Preflight Check ===")
    print(f"状態: {result['status']}")
    print(f"Original: {result['original_file']}")
    print(f"存在: {result['exists']}")
    print(f"構文OK: {result['syntax_ok']}")
    print(f"構文結果: {result['syntax_message']}")
    print(f"Risk数: {result['risk_count']}")

    for risk in result["risks"]:
        print(f"- {risk}")


if __name__ == "__main__":
    main()