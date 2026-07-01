from __future__ import annotations

import ast
import json
from datetime import datetime
from pathlib import Path


class PythonAnalyzer:
    """
    Pythonファイルを読み取り専用で解析する基礎Analyzer。
    構文、関数、クラス、importを抽出する。
    """

    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
        self.report_dir = self.root_dir / "navikoLAB" / "analyzers" / "reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def analyze_file(self, file_path) -> dict:
        path = Path(file_path)

        result = {
            "path": str(path),
            "exists": path.exists(),
            "syntax_ok": False,
            "functions": [],
            "classes": [],
            "imports": [],
            "error": None,
        }

        if not path.exists():
            result["error"] = "file_not_found"
            return result

        try:
            source = path.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(source)
            result["syntax_ok"] = True

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    result["functions"].append(
                        {
                            "name": node.name,
                            "line": node.lineno,
                            "args": [arg.arg for arg in node.args.args],
                        }
                    )

                elif isinstance(node, ast.ClassDef):
                    result["classes"].append(
                        {
                            "name": node.name,
                            "line": node.lineno,
                        }
                    )

                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        result["imports"].append(alias.name)

                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        result["imports"].append(f"{module}.{alias.name}")

        except Exception as e:
            result["error"] = str(e)

        return result

    def analyze_project(self, target_dir=None, max_files: int = 100) -> dict:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = Path(target_dir) if target_dir else self.root_dir

        python_files = list(target.rglob("*.py"))[:max_files]

        file_reports = []
        syntax_ok_count = 0
        syntax_error_count = 0
        total_functions = 0
        total_classes = 0

        for file_path in python_files:
            report = self.analyze_file(file_path)
            file_reports.append(report)

            if report.get("syntax_ok"):
                syntax_ok_count += 1
            else:
                syntax_error_count += 1

            total_functions += len(report.get("functions", []))
            total_classes += len(report.get("classes", []))

        project_report = {
            "title": "Python Analysis Report",
            "status": "completed",
            "target": str(target),
            "created_at": now,
            "python_file_count": len(python_files),
            "syntax_ok_count": syntax_ok_count,
            "syntax_error_count": syntax_error_count,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "files": file_reports,
            "limited": len(python_files) >= max_files,
            "mode": "read_only",
        }

        report_path = self.report_dir / f"python_analysis_{now}.json"
        report_path.write_text(
            json.dumps(project_report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        project_report["report_path"] = str(report_path)
        return project_report

    def diagnose(self) -> dict:
        report = self.analyze_project(target_dir=self.root_dir, max_files=100)

        return {
            "name": "PythonAnalyzer",
            "status": "ready" if report.get("status") == "completed" else "failed",
            "python_file_count": report.get("python_file_count"),
            "syntax_ok_count": report.get("syntax_ok_count"),
            "syntax_error_count": report.get("syntax_error_count"),
            "total_functions": report.get("total_functions"),
            "total_classes": report.get("total_classes"),
            "report_path": report.get("report_path"),
        }


def main() -> None:
    print("=== PythonAnalyzer 診断 ===")

    analyzer = PythonAnalyzer()
    report = analyzer.diagnose()

    print(f"状態: {report.get('status')}")
    print(f"Pythonファイル数: {report.get('python_file_count')}")
    print(f"構文OK: {report.get('syntax_ok_count')}")
    print(f"構文NG: {report.get('syntax_error_count')}")
    print(f"関数数: {report.get('total_functions')}")
    print(f"クラス数: {report.get('total_classes')}")
    print(f"保存先: {report.get('report_path')}")


if __name__ == "__main__":
    main()