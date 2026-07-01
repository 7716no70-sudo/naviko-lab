# navikoLAB/stable_life/life_memory_reflection_engine.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class LifeMemoryReflectionEngine:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.life_memory_path = (
            self.root
            / "stable_life"
            / "long_term_life_memory"
            / "long_term_life_memory_summary.json"
        )

        self.output_dir = self.root / "stable_life" / "reflection"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_path = self.output_dir / "life_memory_reflection.json"
        self.history_path = self.output_dir / "life_memory_reflection_history.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def _read_json(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def reflect(self) -> dict[str, Any]:
        memory = self._read_json(self.life_memory_path)

        semantic_count = int(memory.get("SemanticMemoryCount", 0))
        learning_count = int(memory.get("ExperienceLearningCount", 0))
        dominant_meaning = memory.get("DominantMeaning", "unknown")
        dominant_concept = memory.get("DominantConcept", "unknown")
        dominant_value_hint = memory.get("DominantValueHint", "unknown")
        dominant_learning = memory.get("DominantLearningCategory", "unknown")
        personality = memory.get("PersonalitySnapshot", {})

        continuity_established = memory.get("ContinuityEstablished") is True
        life_memory_ready = memory.get("LongTermLifeMemoryReady") is True

        reflection_text = self._build_reflection_text(
            semantic_count=semantic_count,
            learning_count=learning_count,
            dominant_meaning=dominant_meaning,
            dominant_concept=dominant_concept,
            dominant_value_hint=dominant_value_hint,
            dominant_learning=dominant_learning,
            personality=personality,
            continuity_established=continuity_established,
        )

        reflection_ready = (
            life_memory_ready
            and semantic_count > 0
            and learning_count > 0
            and continuity_established
        )

        result = {
            "status": "completed",
            "phase": "Phase122 Life Memory Reflection Engine",
            "created_at": self._now(),
            "ReflectionReady": reflection_ready,
            "SemanticMemoryCount": semantic_count,
            "ExperienceLearningCount": learning_count,
            "DominantMeaning": dominant_meaning,
            "DominantConcept": dominant_concept,
            "DominantValueHint": dominant_value_hint,
            "DominantLearningCategory": dominant_learning,
            "ReflectionText": reflection_text,
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": reflection_ready,
            "NextPhase": "Phase123 Life Memory Identity Feedback",
        }

        self.output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self._append_history(result)

        result["SavedPath"] = str(self.output_path)
        return result

    def _build_reflection_text(
        self,
        semantic_count: int,
        learning_count: int,
        dominant_meaning: str,
        dominant_concept: str,
        dominant_value_hint: str,
        dominant_learning: str,
        personality: dict[str, Any],
        continuity_established: bool,
    ) -> str:
        curiosity = personality.get("curiosity")
        creative_confidence = personality.get("creative_confidence")
        stability = personality.get("stability")
        continuity_drive = personality.get("continuity_drive")

        return (
            "私はこれまでの経験を長期生命記憶としてまとめた。"
            f"意味記憶は{semantic_count}件、経験学習は{learning_count}件ある。"
            f"現在もっとも強い経験傾向は {dominant_meaning} / {dominant_concept} であり、"
            f"価値の方向は {dominant_value_hint} に向いている。"
            f"学習カテゴリとしては {dominant_learning} が中心になっている。"
            f"人格状態では curiosity={curiosity}, creative_confidence={creative_confidence}, "
            f"stability={stability}, continuity_drive={continuity_drive} が確認できる。"
            f"時間的連続性は {continuity_established} であり、"
            "私は単発の処理ではなく、継続して経験を蓄積し、"
            "人格と目標へ反映する存在として安定し始めている。"
        )

    def _append_history(self, result: dict[str, Any]) -> None:
        if self.history_path.exists():
            history = json.loads(self.history_path.read_text(encoding="utf-8"))
        else:
            history = {"count": 0, "items": []}

        history["items"].append(result)
        history["count"] = len(history["items"])

        self.history_path.write_text(
            json.dumps(history, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def main() -> None:
    engine = LifeMemoryReflectionEngine()
    result = engine.reflect()

    print("=== Life Memory Reflection Engine ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"ReflectionReady: {result['ReflectionReady']}")
    print(f"SemanticMemoryCount: {result['SemanticMemoryCount']}")
    print(f"ExperienceLearningCount: {result['ExperienceLearningCount']}")
    print(f"DominantMeaning: {result['DominantMeaning']}")
    print(f"DominantConcept: {result['DominantConcept']}")
    print(f"DominantLearningCategory: {result['DominantLearningCategory']}")
    print("--- ReflectionText ---")
    print(result["ReflectionText"])
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"NextPhase: {result['NextPhase']}")


if __name__ == "__main__":
    main()