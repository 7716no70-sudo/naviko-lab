from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class AdoptionResult:
    status: str
    phase: str
    adopted_count: int
    skipped_count: int
    total_candidate_count: int
    long_term_memory_path: str
    report_path: str
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    human_approval_required: bool
    adopted_items: List[Dict[str, Any]]
    skipped_items: List[Dict[str, Any]]
    safe_to_continue: bool


class LongTermMemoryAdopter:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_dir = self.root_dir / "memory"
        self.candidate_dir = self.memory_dir / "long_term_candidates"
        self.report_dir = self.memory_dir / "reports"
        self.long_term_memory_path = self.memory_dir / "long_term_memory.json"

        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.candidate_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def load_candidates(self) -> List[Dict[str, Any]]:
        candidates: List[Dict[str, Any]] = []

        for path in sorted(self.candidate_dir.glob("*.json")):
            data = self._read_json(path)
            if data:
                data["_file_path"] = str(path)
                candidates.append(data)

        return candidates

    def load_long_term_memory(self) -> Dict[str, Any]:
        data = self._read_json(self.long_term_memory_path)

        if data:
            if "memories" not in data or not isinstance(data["memories"], list):
                data["memories"] = []
            return data

        return {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "source": "Naviko Memory System",
            "memories": [],
        }

    def adopt_approved_candidates(self) -> AdoptionResult:
        candidates = self.load_candidates()
        memory_data = self.load_long_term_memory()

        existing_texts = {
            str(item.get("text", ""))
            for item in memory_data.get("memories", [])
            if isinstance(item, dict)
        }

        adopted_items: List[Dict[str, Any]] = []
        skipped_items: List[Dict[str, Any]] = []

        for candidate in candidates:
            candidate_text = str(candidate.get("candidate_text", ""))
            approved = bool(candidate.get("approved", False))
            status = str(candidate.get("status", "candidate"))

            if not approved or status != "approved":
                skipped_items.append(
                    {
                        "file_path": candidate.get("_file_path", ""),
                        "reason": "not_approved",
                        "candidate_text": candidate_text,
                        "status": status,
                        "approved": approved,
                    }
                )
                continue

            if candidate_text in existing_texts:
                skipped_items.append(
                    {
                        "file_path": candidate.get("_file_path", ""),
                        "reason": "duplicate",
                        "candidate_text": candidate_text,
                        "status": status,
                        "approved": approved,
                    }
                )
                continue

            memory_item = {
                "id": f"ltm_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "text": candidate_text,
                "importance": candidate.get("importance", ""),
                "score": candidate.get("score", 0),
                "reason": candidate.get("reason", ""),
                "source": candidate.get("source", "MemoryAgent"),
                "candidate_file": candidate.get("_file_path", ""),
                "memory_type": "long_term",
                "safe_adopted": True,
            }

            memory_data["memories"].append(memory_item)
            existing_texts.add(candidate_text)
            adopted_items.append(memory_item)

            self._mark_candidate_adopted(candidate)

        memory_data["updated_at"] = datetime.now().isoformat(timespec="seconds")
        self._write_json(self.long_term_memory_path, memory_data)

        report_path = self._save_report(
            adopted_items=adopted_items,
            skipped_items=skipped_items,
            total_candidate_count=len(candidates),
        )

        return AdoptionResult(
            status="completed",
            phase="Phase4-13 Approved Long Term Memory Adoption",
            adopted_count=len(adopted_items),
            skipped_count=len(skipped_items),
            total_candidate_count=len(candidates),
            long_term_memory_path=str(self.long_term_memory_path),
            report_path=str(report_path),
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            human_approval_required=True,
            adopted_items=adopted_items,
            skipped_items=skipped_items,
            safe_to_continue=True,
        )

    def _mark_candidate_adopted(self, candidate: Dict[str, Any]) -> None:
        file_path = candidate.get("_file_path", "")
        if not file_path:
            return

        path = Path(file_path)
        data = self._read_json(path)

        if not data:
            return

        data["status"] = "adopted"
        data["adopted"] = True
        data["adopted_at"] = datetime.now().isoformat(timespec="seconds")
        data["adoption_note"] = "Phase4-13 adopted this approved candidate into long_term_memory.json."

        self._write_json(path, data)

    def _save_report(
        self,
        adopted_items: List[Dict[str, Any]],
        skipped_items: List[Dict[str, Any]],
        total_candidate_count: int,
    ) -> Path:
        filename = f"long_term_memory_adoption_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = self.report_dir / filename

        report = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "phase": "Phase4-13 Approved Long Term Memory Adoption",
            "status": "completed",
            "total_candidate_count": total_candidate_count,
            "adopted_count": len(adopted_items),
            "skipped_count": len(skipped_items),
            "long_term_memory_path": str(self.long_term_memory_path),
            "safe_mode": True,
            "external_ai": False,
            "real_pc_operation": False,
            "file_delete": False,
            "human_approval_required": True,
            "safe_to_continue": True,
            "adopted_items": adopted_items,
            "skipped_items": skipped_items,
        }

        with path.open("w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return path

    def print_result(self, result: AdoptionResult) -> None:
        print("=== Phase4-13 Long Term Memory Adopter ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"TotalCandidateCount: {result.total_candidate_count}")
        print(f"AdoptedCount: {result.adopted_count}")
        print(f"SkippedCount: {result.skipped_count}")
        print(f"LongTermMemoryPath: {result.long_term_memory_path}")
        print(f"ReportPath: {result.report_path}")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"HumanApprovalRequired: {result.human_approval_required}")

        print("")
        print("[Adopted Items]")
        if not result.adopted_items:
            print("- 採用なし")
        else:
            for index, item in enumerate(result.adopted_items, start=1):
                print(f"- Memory {index}")
                print(f"  text: {item.get('text', '')}")
                print(f"  importance: {item.get('importance', '')}")
                print(f"  score: {item.get('score', 0)}")
                print(f"  reason: {item.get('reason', '')}")

        print("")
        print(f"SafeToContinue: {result.safe_to_continue}")

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


def run_phase4_13_test() -> None:
    adopter = LongTermMemoryAdopter()
    result = adopter.adopt_approved_candidates()
    adopter.print_result(result)


if __name__ == "__main__":
    run_phase4_13_test()