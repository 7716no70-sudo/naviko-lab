from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class MemoryAnalysisRecord:
    timestamp: str
    source: str
    input_text: str
    importance: str
    score: int
    reason: str
    long_term_candidate: bool


class MemoryAgentAnalysisSaver:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_dir = self.root_dir / "memory"
        self.analysis_dir = self.memory_dir / "analysis"
        self.candidate_dir = self.memory_dir / "long_term_candidates"

        self.analysis_dir.mkdir(parents=True, exist_ok=True)
        self.candidate_dir.mkdir(parents=True, exist_ok=True)

    def build_record(
        self,
        input_text: str,
        importance: str,
        score: int,
        reason: str,
        source: str = "MemoryAgent",
    ) -> MemoryAnalysisRecord:
        return MemoryAnalysisRecord(
            timestamp=datetime.now().isoformat(timespec="seconds"),
            source=source,
            input_text=input_text,
            importance=importance,
            score=score,
            reason=reason,
            long_term_candidate=self._is_long_term_candidate(importance, score),
        )

    def save_analysis(self, record: MemoryAnalysisRecord) -> Path:
        filename = f"memory_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = self.analysis_dir / filename

        with path.open("w", encoding="utf-8") as f:
            json.dump(asdict(record), f, ensure_ascii=False, indent=2)

        if record.long_term_candidate:
            self.save_long_term_candidate(record)

        return path

    def save_long_term_candidate(self, record: MemoryAnalysisRecord) -> Path:
        filename = f"long_term_candidate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = self.candidate_dir / filename

        candidate_data: Dict[str, Any] = {
            "timestamp": record.timestamp,
            "source": record.source,
            "candidate_text": record.input_text,
            "importance": record.importance,
            "score": record.score,
            "reason": record.reason,
            "status": "candidate",
            "approved": False,
            "note": "Phase4-10 generated long-term memory candidate. Human approval required before permanent adoption.",
        }

        with path.open("w", encoding="utf-8") as f:
            json.dump(candidate_data, f, ensure_ascii=False, indent=2)

        return path

    def save_from_analysis_result(self, analysis_result: Dict[str, Any]) -> Path:
        record = self.build_record(
            input_text=str(analysis_result.get("input_text", "")),
            importance=str(analysis_result.get("importance", "low")),
            score=int(analysis_result.get("score", 0)),
            reason=str(analysis_result.get("reason", "")),
            source=str(analysis_result.get("source", "MemoryAgent")),
        )
        return self.save_analysis(record)

    def _is_long_term_candidate(self, importance: str, score: int) -> bool:
        if importance == "high":
            return True
        if score >= 3:
            return True
        return False

    def list_saved_analysis(self) -> List[str]:
        return [str(path) for path in sorted(self.analysis_dir.glob("*.json"))]

    def list_long_term_candidates(self) -> List[str]:
        return [str(path) for path in sorted(self.candidate_dir.glob("*.json"))]


def run_phase4_10_test() -> None:
    print("=== Phase4-10 MemoryAgent Analysis Saver ===")

    saver = MemoryAgentAnalysisSaver()

    sample_result = {
        "source": "MemoryAgent",
        "input_text": "ナビ子はまず実際に起動して自然に会話できるAIになることを最優先にする",
        "importance": "high",
        "score": 3,
        "reason": "最重要目標に関係するため長期記憶候補",
    }

    saved_path = saver.save_from_analysis_result(sample_result)

    print("status: completed")
    print("phase: Phase4-10 MemoryAgent Analysis Result Save")
    print("AnalysisSaved: True")
    print("LongTermCandidateGenerated: True")
    print(f"SavedAnalysisPath: {saved_path}")
    print(f"AnalysisCount: {len(saver.list_saved_analysis())}")
    print(f"LongTermCandidateCount: {len(saver.list_long_term_candidates())}")
    print("SafeMode: True")
    print("ExternalAI: False")
    print("RealPCOperation: False")
    print("FileDelete: False")
    print("SafeToContinue: True")


if __name__ == "__main__":
    run_phase4_10_test()