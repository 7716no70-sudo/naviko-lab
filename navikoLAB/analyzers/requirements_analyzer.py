from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class RequirementsAnalyzer:
    """
    requirements.txt / pyproject.toml など依存関係ファイルを読み取り専用で解析する基礎Analyzer。
    """

    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
        self.report_dir = self.root_dir / "navikoLAB" / "analyzers" / "reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def parse_requirements_txt(self, path: Path) -> list[dict]:
        packages = []

        if not path.exists():
            return packages

        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            raw = line.strip()

            if not raw or raw.startswith("#"):
                continue

            packages.append(
                {
                    "raw": raw,
                    "name": raw.split("==")[0].split(">=")[0].split("<=")[0].split("~=")[0].strip(),
                }
            )

        return packages

    def analyze(self, target_dir=None) -> dict:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = Path(target_dir) if target_dir else self.root_dir

        requirements_files = list(target.rglob("requirements.txt"))
        pyproject_files = list(target.rglob("pyproject.toml"))

        packages = []
        for req in requirements_files:
            packages.extend(self.parse_requirements_txt(req))

        report = {
            "title": "Requirements Analysis Report",
            "status": "completed",
            "created_at": now,
            "target": str(target),
            "requirements_file_count": len(requirements_files),
            "pyproject_file_count": len(pyproject_files),
            "package_count": len(packages),
            "packages": packages,
            "requirements_files": [str(p) for p in requirements_files[:30]],
            "pyproject_files": [str(p) for p in pyproject_files[:30]],
            "mode": "read_only",
        }

        report_path = self.report_dir / f"requirements_analysis_{now}.json"
        report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        report["report_path"] = str(report_path)
        return report

    def diagnose(self) -> dict:
        report = self.analyze(target_dir=self.root_dir)

        return {
            "name": "RequirementsAnalyzer",
            "status": "ready" if report.get("status") == "completed" else "failed",
            "requirements_file_count": report.get("requirements_file_count"),
            "pyproject_file_count": report.get("pyproject_file_count"),
            "package_count": report.get("package_count"),
            "report_path": report.get("report_path"),
        }


def main() -> None:
    print("=== RequirementsAnalyzer 診断 ===")

    analyzer = RequirementsAnalyzer()
    report = analyzer.diagnose()

    print(f"状態: {report.get('status')}")
    print(f"requirements.txt数: {report.get('requirements_file_count')}")
    print(f"pyproject.toml数: {report.get('pyproject_file_count')}")
    print(f"package数: {report.get('package_count')}")
    print(f"保存先: {report.get('report_path')}")


if __name__ == "__main__":
    main()