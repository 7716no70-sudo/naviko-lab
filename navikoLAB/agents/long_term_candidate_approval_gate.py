from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ApprovalResult:
    status: str
    phase: str
    target_file: str
    approved: bool
    previous_status: str
    new_status: str
    message: str
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    auto_adoption: bool
    safe_to_continue: bool


class LongTermCandidateApprovalGate:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_dir = self.root_dir / "memory"
        self.candidate_dir = self.memory_dir / "long_term_candidates"
        self.report_dir = self.memory_dir / "reports"

        self.candidate_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def list_candidates(self) -> List[Path]:
        return sorted(self.candidate_dir.glob("*.json"))

    def approve_candidate_by_index(self, index: int) -> ApprovalResult:
        candidates = self.list_candidates()

        if index < 1 or index > len(candidates):
            return self._build_result(
                target_file="",
                approved=False,
                previous_status="not_found",
                new_status="not_found",
                message=f"指定された候補番号が存在しません: {index}",
            )

        target_path = candidates[index - 1]
        return self.approve_candidate_file(target_path)

    def approve_candidate_file(self, target_path: Path) -> ApprovalResult:
        data = self._read_json(target_path)

        if not data:
            return self._build_result(
                target_file=str(target_path),
                approved=False,
                previous_status="read_failed",
                new_status="read_failed",
                message="候補ファイルを読み込めませんでした。",
            )

        previous_status = str(data.get("status", "candidate"))

        data["approved"] = True
        data["status"] = "approved"
        data["approved_at"] = datetime.now().isoformat(timespec="seconds")
        data["approval_note"] = (
            "Phase4-12 human approval gate approved this candidate. "
            "This does not automatically adopt it into permanent long-term memory."
        )

        self._write_json(target_path, data)

        result = self._build_result(
            target_file=str(target_path),
            approved=True,
            previous_status=previous_status,
            new_status="approved",
            message="候補を承認済みに変更しました。正式な長期記憶への採用は次工程で行います。",
        )

        self.save_approval_report(result)
        return result

    def save_approval_report(self, result: ApprovalResult) -> Path:
        filename = f"long_term_candidate_approval_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = self.report_dir / filename

        with path.open("w", encoding="utf-8") as f:
            json.dump(asdict(result), f, ensure_ascii=False, indent=2)

        return path

    def print_candidates(self) -> None:
        candidates = self.list_candidates()

        print("[Long Term Memory Candidate List]")

        if not candidates:
            print("- 候補なし")
            return

        for index, path in enumerate(candidates, start=1):
            data = self._read_json(path)
            print(f"- Candidate {index}")
            print(f"  file: {path}")
            print(f"  text: {data.get('candidate_text', '')}")
            print(f"  importance: {data.get('importance', '')}")
            print(f"  score: {data.get('score', 0)}")
            print(f"  status: {data.get('status', 'candidate')}")
            print(f"  approved: {data.get('approved', False)}")

    def print_result(self, result: ApprovalResult) -> None:
        print("=== Phase4-12 Long Term Candidate Approval Gate ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"TargetFile: {result.target_file}")
        print(f"Approved: {result.approved}")
        print(f"PreviousStatus: {result.previous_status}")
        print(f"NewStatus: {result.new_status}")
        print(f"Message: {result.message}")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"AutoAdoption: {result.auto_adoption}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def _build_result(
        self,
        target_file: str,
        approved: bool,
        previous_status: str,
        new_status: str,
        message: str,
    ) -> ApprovalResult:
        return ApprovalResult(
            status="completed" if approved else "blocked",
            phase="Phase4-12 Long Term Memory Candidate Approval Gate",
            target_file=target_file,
            approved=approved,
            previous_status=previous_status,
            new_status=new_status,
            message=message,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            auto_adoption=False,
            safe_to_continue=True,
        )

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

    def _write_json(self, path: Path, data: Dict[str, Any]) -> None:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def run_phase4_12_test() -> None:
    gate = LongTermCandidateApprovalGate()

    print("=== Phase4-12 Long Term Candidate Approval Gate ===")
    gate.print_candidates()
    print("")

    result = gate.approve_candidate_by_index(1)
    gate.print_result(result)


if __name__ == "__main__":
    run_phase4_12_test()