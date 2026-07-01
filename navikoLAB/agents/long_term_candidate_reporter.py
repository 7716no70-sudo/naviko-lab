from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class LongTermCandidateSummary:
    file_path: str
    timestamp: str
    source: str
    candidate_text: str
    importance: str
    score: int
    reason: str
    status: str
    approved: bool


class LongTermCandidateReporter:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_dir = self.root_dir / "memory"
        self.candidate_dir = self.memory_dir / "long_term_candidates"
        self.report_dir = self.memory_dir / "reports"

        self.candidate_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def load_candidates(self) -> List[LongTermCandidateSummary]:
        summaries: List[LongTermCandidateSummary] = []

        for path in sorted(self.candidate_dir.glob("*.json")):
            data = self._read_json(path)

            summary = LongTermCandidateSummary(
                file_path=str(path),
                timestamp=str(data.get("timestamp", "")),
                source=str(data.get("source", "")),
                candidate_text=str(data.get("candidate_text", "")),
                importance=str(data.get("importance", "")),
                score=int(data.get("score", 0)),
                reason=str(data.get("reason", "")),
                status=str(data.get("status", "candidate")),
                approved=bool(data.get("approved", False)),
            )

            summaries.append(summary)

        return summaries

    def build_report(self) -> Dict[str, Any]:
        candidates = self.load_candidates()

        unapproved_count = sum(1 for item in candidates if not item.approved)
        approved_count = sum(1 for item in candidates if item.approved)

        report: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "phase": "Phase4-11 Long Term Memory Candidate Report",
            "status": "completed",
            "candidate_count": len(candidates),
            "unapproved_count": unapproved_count,
            "approved_count": approved_count,
            "safe_mode": True,
            "external_ai": False,
            "real_pc_operation": False,
            "file_delete": False,
            "auto_adoption": False,
            "human_approval_required": True,
            "safe_to_continue": True,
            "candidates": [asdict(item) for item in candidates],
        }

        return report

    def save_report(self, report: Dict[str, Any]) -> Path:
        filename = f"long_term_candidate_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = self.report_dir / filename

        with path.open("w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return path

    def print_report(self, report: Dict[str, Any], report_path: Path) -> None:
        print("=== Phase4-11 Long Term Candidate Reporter ===")
        print(f"status: {report['status']}")
        print(f"phase: {report['phase']}")
        print(f"CandidateCount: {report['candidate_count']}")
        print(f"UnapprovedCount: {report['unapproved_count']}")
        print(f"ApprovedCount: {report['approved_count']}")
        print(f"AutoAdoption: {report['auto_adoption']}")
        print(f"HumanApprovalRequired: {report['human_approval_required']}")

        print("")
        print("[Long Term Memory Candidates]")

        candidates = report.get("candidates", [])

        if not candidates:
            print("- 候補なし")
        else:
            for index, item in enumerate(candidates, start=1):
                print(f"- Candidate {index}")
                print(f"  file: {item.get('file_path', '')}")
                print(f"  text: {item.get('candidate_text', '')}")
                print(f"  importance: {item.get('importance', '')}")
                print(f"  score: {item.get('score', 0)}")
                print(f"  reason: {item.get('reason', '')}")
                print(f"  status: {item.get('status', '')}")
                print(f"  approved: {item.get('approved', False)}")

        print("")
        print(f"ReportSavedPath: {report_path}")
        print(f"SafeMode: {report['safe_mode']}")
        print(f"ExternalAI: {report['external_ai']}")
        print(f"RealPCOperation: {report['real_pc_operation']}")
        print(f"FileDelete: {report['file_delete']}")
        print(f"SafeToContinue: {report['safe_to_continue']}")

    def _read_json(self, path: Path) -> Dict[str, Any]:
        try:
            with path.open("r", encoding="utf-8") as f:
                loaded = json.load(f)

            if isinstance(loaded, dict):
                return loaded

            return {}

        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}


def run_phase4_11_test() -> None:
    reporter = LongTermCandidateReporter()
    report = reporter.build_report()
    report_path = reporter.save_report(report)
    reporter.print_report(report, report_path)


if __name__ == "__main__":
    run_phase4_11_test()