from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.analyzers.python_analyzer import PythonAnalyzer
from navikoLAB.analyzers.requirements_analyzer import RequirementsAnalyzer


class DependencyAnalyzer:
    """
    Python import と requirements.txt をもとに、
    プロジェクトの依存関係を読み取り専用で解析する基礎Analyzer。
    """

    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
        self.report_dir = self.root_dir / "navikoLAB" / "analyzers" / "reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)

        self.python_analyzer = PythonAnalyzer(root_dir=self.root_dir)
        self.requirements_analyzer = RequirementsAnalyzer(root_dir=self.root_dir)

    def classify_import(self, name: str) -> str:
        if not name:
            return "unknown"

        root_name = name.split(".")[0]

        local_prefixes = ["navikoLAB", "naviko"]
        stdlib_candidates = {
            "os", "sys", "json", "datetime", "pathlib", "ast", "shutil", "subprocess",
            "typing", "re", "time", "tempfile", "traceback", "collections", "itertools",
            "math", "random", "threading", "tkinter", "py_compile",
        }

        if root_name in local_prefixes:
            return "local"

        if root_name in stdlib_candidates:
            return "stdlib"

        return "external_or_unknown"

    def analyze(self, target_dir=None, max_files: int = 150) -> dict:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = Path(target_dir) if target_dir else self.root_dir

        python_report = self.python_analyzer.analyze_project(target_dir=target, max_files=max_files)
        requirements_report = self.requirements_analyzer.analyze(target_dir=target)

        import_counts = {}
        classified_counts = {
            "local": 0,
            "stdlib": 0,
            "external_or_unknown": 0,
            "unknown": 0,
        }

        for file_report in python_report.get("files", []):
            for import_name in file_report.get("imports", []):
                root_name = import_name.split(".")[0]
                import_counts[root_name] = import_counts.get(root_name, 0) + 1
                category = self.classify_import(import_name)
                classified_counts[category] = classified_counts.get(category, 0) + 1

        packages = requirements_report.get("packages", [])
        package_names = sorted({p.get("name") for p in packages if p.get("name")})

        external_imports = sorted(
            name for name in import_counts
            if self.classify_import(name) == "external_or_unknown"
        )

        possible_missing_requirements = [
            name for name in external_imports
            if name not in package_names
        ]

        report = {
            "title": "Dependency Analysis Report",
            "status": "completed",
            "created_at": now,
            "target": str(target),
            "python_file_count": python_report.get("python_file_count"),
            "requirements_file_count": requirements_report.get("requirements_file_count"),
            "package_count": len(package_names),
            "import_counts": import_counts,
            "classified_counts": classified_counts,
            "package_names": package_names,
            "external_imports": external_imports,
            "possible_missing_requirements": possible_missing_requirements,
            "mode": "read_only",
        }

        report_path = self.report_dir / f"dependency_analysis_{now}.json"
        report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        report["report_path"] = str(report_path)
        return report

    def diagnose(self) -> dict:
        report = self.analyze(target_dir=self.root_dir)

        return {
            "name": "DependencyAnalyzer",
            "status": "ready" if report.get("status") == "completed" else "failed",
            "python_file_count": report.get("python_file_count"),
            "requirements_file_count": report.get("requirements_file_count"),
            "package_count": report.get("package_count"),
            "external_import_count": len(report.get("external_imports", [])),
            "possible_missing_count": len(report.get("possible_missing_requirements", [])),
            "report_path": report.get("report_path"),
        }


def main() -> None:
    print("=== DependencyAnalyzer 診断 ===")

    analyzer = DependencyAnalyzer()
    report = analyzer.diagnose()

    print(f"状態: {report.get('status')}")
    print(f"Pythonファイル数: {report.get('python_file_count')}")
    print(f"requirements.txt数: {report.get('requirements_file_count')}")
    print(f"package数: {report.get('package_count')}")
    print(f"外部import候補数: {report.get('external_import_count')}")
    print(f"requirements不足候補数: {report.get('possible_missing_count')}")
    print(f"保存先: {report.get('report_path')}")


if __name__ == "__main__":
    main()