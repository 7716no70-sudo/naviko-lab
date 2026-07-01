# navikoLAB/stable_life/long_term_life_memory_consolidation.py

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


class LongTermLifeMemoryConsolidation:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.semantic_index_path = (
            self.root / "stable_life" / "semantic_memory" / "semantic_memory_index.json"
        )
        self.learning_index_path = (
            self.root / "stable_life" / "experience_learning" / "experience_learning_index.json"
        )
        self.personality_path = (
            self.root / "stable_life" / "personality" / "stable_personality.json"
        )
        self.continuity_report_path = (
            self.root / "stable_life" / "continuity" / "life_kernel_continuity_report.json"
        )

        self.output_dir = self.root / "stable_life" / "long_term_life_memory"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_path = self.output_dir / "long_term_life_memory_summary.json"
        self.history_path = self.output_dir / "long_term_life_memory_history.json"

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

    def consolidate(self) -> dict[str, Any]:
        semantic = self._read_json(self.semantic_index_path)
        learning = self._read_json(self.learning_index_path)
        personality = self._read_json(self.personality_path)
        continuity = self._read_json(self.continuity_report_path)

        semantic_items = semantic.get("items", [])
        learning_items = learning.get("items", [])

        meanings = Counter(item.get("meaning", "unknown") for item in semantic_items)
        concepts = Counter(item.get("concept", "unknown") for item in semantic_items)
        value_hints = Counter(item.get("value_hint", "unknown") for item in semantic_items)
        learning_categories = Counter(item.get("category", "unknown") for item in learning_items)

        dominant_meaning = meanings.most_common(1)[0][0] if meanings else "none"
        dominant_concept = concepts.most_common(1)[0][0] if concepts else "none"
        dominant_value_hint = value_hints.most_common(1)[0][0] if value_hints else "none"
        dominant_learning_category = (
            learning_categories.most_common(1)[0][0] if learning_categories else "none"
        )

        life_memory_ready = (
            len(semantic_items) > 0
            and len(learning_items) > 0
            and bool(personality.get("updated_at"))
            and continuity.get("ContinuityEstablished") is True
        )

        summary = {
            "status": "completed",
            "phase": "Phase121 Long-Term Life Memory Consolidation",
            "created_at": self._now(),
            "SemanticMemoryCount": len(semantic_items),
            "ExperienceLearningCount": len(learning_items),
            "DominantMeaning": dominant_meaning,
            "DominantConcept": dominant_concept,
            "DominantValueHint": dominant_value_hint,
            "DominantLearningCategory": dominant_learning_category,
            "MeaningDistribution": dict(meanings),
            "ConceptDistribution": dict(concepts),
            "ValueHintDistribution": dict(value_hints),
            "LearningCategoryDistribution": dict(learning_categories),
            "PersonalitySnapshot": {
                "curiosity": personality.get("curiosity"),
                "creative_confidence": personality.get("creative_confidence"),
                "stability": personality.get("stability"),
                "repair_orientation": personality.get("repair_orientation"),
                "continuity_drive": personality.get("continuity_drive"),
            },
            "ContinuityEstablished": continuity.get("ContinuityEstablished") is True,
            "LongTermLifeMemoryReady": life_memory_ready,
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": life_memory_ready,
            "NextPhase": "Phase122 Life Memory Reflection Engine",
        }

        self.output_path.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        self._append_history(summary)

        summary["SavedPath"] = str(self.output_path)
        return summary

    def _append_history(self, summary: dict[str, Any]) -> None:
        if self.history_path.exists():
            history = json.loads(self.history_path.read_text(encoding="utf-8"))
        else:
            history = {"count": 0, "items": []}

        history["items"].append(summary)
        history["count"] = len(history["items"])

        self.history_path.write_text(
            json.dumps(history, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def main() -> None:
    consolidation = LongTermLifeMemoryConsolidation()
    result = consolidation.consolidate()

    print("=== Long-Term Life Memory Consolidation ===")
    for key, value in result.items():
        if isinstance(value, dict):
            print(f"{key}: {json.dumps(value, ensure_ascii=False)}")
        else:
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()