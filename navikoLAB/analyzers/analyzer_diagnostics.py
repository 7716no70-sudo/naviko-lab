from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.analyzers.folder_analyzer import FolderAnalyzer
from navikoLAB.analyzers.python_analyzer import PythonAnalyzer
from navikoLAB.analyzers.app_analyzer import AppAnalyzer
from navikoLAB.analyzers.requirements_analyzer import RequirementsAnalyzer


def run_analyzer_diagnostics(root_dir=None) -> dict:
    root = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
    report_dir = root / "navikoLAB" / "analyzers" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    folder_report = FolderAnalyzer(root_dir=root).diagnose()
    python_report = PythonAnalyzer(root_dir=root).diagnose()
    app_report = AppAnalyzer(root_dir=root).diagnose()
    requirements_report = RequirementsAnalyzer(root_dir=root).diagnose()

    checks = {
        "folder_analyzer_ready": folder_report.get("status") == "ready",
        "python_analyzer_ready": python_report.get("status") == "ready",
        "app_analyzer_ready": app_report.get("status") == "ready",
        "requirements_analyzer_ready": requirements_report.get("status") == "ready",
        "python_syntax_safe": python_report.get("syntax_error_count", 0) == 0,
        "app_analysis_completed": app_report.get("analysis_status") in ["completed", "needs_review"],
    }

    status = "passed" if all(checks.values()) else "failed"

    report = {
        "title": "Analyzer Diagnostics",
        "status": status,
        "created_at": now,
        "folder_report": folder_report,
        "python_report": python_report,
        "app_report": app_report,
        "requirements_report": requirements_report,
        "checks": checks,
    }

    report_path = report_dir / f"analyzer_diagnostics_{now}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report["report_path"] = str(report_path)
    return report


def main() -> None:
    print("=== Analyzer Diagnostics ===")

    report = run_analyzer_diagnostics()

    print(f"状態: {report.get('status')}")
    print("確認項目:")

    for name, ok in report.get("checks", {}).items():
        print(f"- {name}: {'OK' if ok else 'NG'}")

    print(f"保存先: {report.get('report_path')}")


if __name__ == "__main__":
    main()