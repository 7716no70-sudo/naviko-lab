from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"


KEYWORDS = [
    "CapabilityRouter",
    "capability_router",
    "capability",
    "route",
    "select",
    "dispatch",
    "agent",
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
            "capability" in path.name.lower()
            or "router" in path.name.lower()
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
        "phase": "Phase12-3A CapabilityRouter Locator Report",
        "candidate_count": len(candidates),
        "candidates": candidates[:20],
        "risk_count": 0,
        "safe_to_continue": True,
        "original_write": False,
        "file_delete": False,
        "next_phase": "Phase12-3B CapabilityRouter Source Inspector",
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"capability_router_locator_report_{timestamp}.json"

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== CapabilityRouter Locator Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("CandidateCount:", report["candidate_count"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("次工程:", report["next_phase"])
    print("保存先:", report_path)
    print("---- Candidates ----")

    for item in candidates[:10]:
        print(f"- score={item['score']} name_hit={item['name_hit']} path={item['path']}")


if __name__ == "__main__":
    main()