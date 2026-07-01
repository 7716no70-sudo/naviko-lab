from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ANALYZER_DIR = ROOT / "navikoLAB" / "analyzers"
REPORT_DIR = ANALYZER_DIR / "reports"
DOC_DIR = ROOT / "navikoLAB" / "docs"


class AutoDocumentation:
    def __init__(self) -> None:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        DOC_DIR.mkdir(parents=True, exist_ok=True)

    def collect_latest_reports(self) -> dict:
        reports = {}

        for path in REPORT_DIR.glob("*.json"):
            key = path.stem
            try:
                reports[key] = json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                reports[key] = {
                    "status": "read_failed",
                    "error": str(e),
                    "path": str(path),
                }

        return reports

    def generate_markdown(self, reports: dict) -> Path:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output = DOC_DIR / f"auto_documentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        lines = [
            "# Naviko Auto Documentation",
            "",
            f"Generated: {now}",
            "",
            "## Summary",
            "",
            f"- Report count: {len(reports)}",
            "",
            "## Analyzer Reports",
            "",
        ]

        for name, data in reports.items():
            lines.append(f"### {name}")
            lines.append("")
            if isinstance(data, dict):
                status = data.get("status") or data.get("状態") or "unknown"
                lines.append(f"- status: {status}")
                lines.append("")
                lines.append("```json")
                lines.append(json.dumps(data, ensure_ascii=False, indent=2))
                lines.append("```")
            else:
                lines.append(str(data))
            lines.append("")

        output.write_text("\n".join(lines), encoding="utf-8")
        return output

    def generate_json_summary(self, reports: dict) -> Path:
        output = DOC_DIR / f"analysis_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        summary = {
            "status": "completed",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "report_count": len(reports),
            "reports": reports,
        }

        output.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return output

    def run(self) -> dict:
        reports = self.collect_latest_reports()
        markdown_path = self.generate_markdown(reports)
        json_path = self.generate_json_summary(reports)

        return {
            "status": "completed",
            "report_count": len(reports),
            "markdown": str(markdown_path),
            "json": str(json_path),
        }


def main() -> None:
    result = AutoDocumentation().run()

    print("=== AutoDocumentation ===")
    print(f"状態: {result['status']}")
    print(f"Report数: {result['report_count']}")
    print(f"Markdown: {result['markdown']}")
    print(f"JSON: {result['json']}")


if __name__ == "__main__":
    main()