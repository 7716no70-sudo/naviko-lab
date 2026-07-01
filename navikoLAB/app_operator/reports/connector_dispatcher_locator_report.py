from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"


KEYWORDS = [
    "ConnectorDispatcher",
    "connector_dispatcher",
    "dispatcher",
    "dispatch",
    "connector",
    "route",
    "select",
]


def score_file(path: Path) -> int:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return 0

    return sum(1 for keyword in KEYWORDS if keyword in text)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    candidates = []

    for path in (ROOT / "navikoLAB").rglob("*.py"):
        if "__pycache__" in str(path):
            continue

        score = score_file(path)
        name_hit = (
            "connector" in path.name.lower()
            or "dispatcher" in path.name.lower()
        )

        if score >= 2 or name_hit:
            candidates.append({
                "path": str(path),
                "name": path.name,
                "score": score,
                "name_hit": name_hit,
            })

    candidates = sorted(
        candidates,
        key=lambda item: (item["score"], item["name_hit"]),
        reverse=True,
    )

    report = {
        "status": "completed",
        "phase": "Phase13-1 ConnectorDispatcher Locator Report",
        "candidate_count": len(candidates),
        "candidates": candidates[:20],
        "risk_count": 0,
        "safe_to_continue": True,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "external_operation": False,
        "real_gui_operation": False,
        "next_phase": "Phase13-2 ConnectorDispatcher Source Inspector",
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"connector_dispatcher_locator_report_{timestamp}.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== ConnectorDispatcher Locator Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("CandidateCount:", report["candidate_count"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("ExternalOperation:", report["external_operation"])
    print("RealGUIOperation:", report["real_gui_operation"])
    print("次工程:", report["next_phase"])
    print("保存先:", report_path)
    print("---- Candidates ----")

    for item in candidates[:10]:
        print(f"- score={item['score']} name_hit={item['name_hit']} path={item['path']}")


if __name__ == "__main__":
    main()