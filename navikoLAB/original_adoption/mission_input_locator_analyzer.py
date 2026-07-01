from pathlib import Path
from datetime import datetime
import json


def main():

    original_file = Path(__file__).resolve().parents[2] / "naviko.py"

    source = original_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    lines = source.splitlines()

    execute_line = None
    entry_get_lines = []
    groq_call_lines = []

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        if execute_line is None and stripped.startswith("def execute_groq_communication"):
            execute_line = i

        if ".get()" in stripped or ".get(" in stripped:
            if "e_box" in stripped or "entry" in stripped or "input" in stripped:
                entry_get_lines.append(i)

        if "requests.post" in stripped or "GROQ" in stripped or "groq" in stripped:
            groq_call_lines.append(i)

    report = {
        "status": "completed",
        "phase": "Phase5-6 Mission Input Locator Analyzer",
        "original_found": original_file.exists(),
        "execute_groq_communication_line": execute_line,
        "entry_get_candidate_lines": entry_get_lines[:20],
        "groq_call_candidate_lines": groq_call_lines[:20],
        "ready_for_mission_input_locator": execute_line is not None,
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "original_write": False,
    }

    report_dir = Path(__file__).parent / "reports"
    report_dir.mkdir(exist_ok=True)

    report_file = report_dir / (
        f"mission_input_locator_analyzer_{datetime.now():%Y%m%d_%H%M%S}.json"
    )

    report_file.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("=== Mission Input Locator Analyzer ===")

    for key, value in report.items():
        print(f"{key}: {value}")

    print("保存先:", report_file)


if __name__ == "__main__":
    main()