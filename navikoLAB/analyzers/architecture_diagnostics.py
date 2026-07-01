from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.analyzers.dependency_analyzer import DependencyAnalyzer
from navikoLAB.analyzers.architecture_analyzer import ArchitectureAnalyzer


def run_architecture_diagnostics(root_dir=None) -> dict:
    root = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
    report_dir = root / "navikoLAB" / "analyzers" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    dependency_report = DependencyAnalyzer(root_dir=root).diagnose()
    architecture_report = ArchitectureAnalyzer(root_dir=root).diagnose()

    checks = {
        "dependency_analyzer_ready": dependency_report.get("status") == "ready",
        "architecture_analyzer_ready": architecture_report.get("status") == "ready",
        "python_syntax_safe": architecture_report.get("syntax_error_count", 0) == 0,
        "dependency_report_created": bool(dependency_report.get("report_path")),
        "architecture_report_created": bool(architecture_report.get("report_path")),
        "knowledge_saved": bool(architecture_report.get("knowledge_record")),
        "experience_saved": bool(architecture_report.get("experience_record")),
    }

    status = "passed" if all(checks.values()) else "failed"

    report = {
        "title": "Architecture / Dependency Diagnostics",
        "status": status,
        "created_at": now,
        "dependency_report": dependency_report,
        "architecture_report": architecture_report,
        "checks": checks,
    }

    report_path = report_dir / f"architecture_diagnostics_{now}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report["report_path"] = str(report_path)
    return report


def main() -> None:
    print("=== Architecture / Dependency Diagnostics ===")

    report = run_architecture_diagnostics()

    print(f"状態: {report.get('status')}")
    print("確認項目:")

    for name, ok in report.get("checks", {}).items():
        print(f"- {name}: {'OK' if ok else 'NG'}")

    architecture = report.get("architecture_report", {})
    dependency = report.get("dependency_report", {})

    print(f"構造: {architecture.get('architecture_style')}")
    print(f"requirements不足候補: {dependency.get('possible_missing_count')}")
    print(f"保存先: {report.get('report_path')}")


if __name__ == "__main__":
    main()