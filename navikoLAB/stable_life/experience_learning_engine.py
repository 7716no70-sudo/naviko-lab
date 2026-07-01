# navikoLAB/stable_life/experience_learning_engine.py

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class ExperienceLearning:
    source_meaning: str
    source_concept: str
    category: str
    learning: str
    growth_hint: str
    confidence: float
    created_at: str


class ExperienceLearningEngine:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)
        self.semantic_index_path = (
            self.root
            / "stable_life"
            / "semantic_memory"
            / "semantic_memory_index.json"
        )
        self.learning_dir = self.root / "stable_life" / "experience_learning"
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.learning_dir / "experience_learning_index.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def load_semantic_memories(self) -> list[dict[str, Any]]:
        if not self.semantic_index_path.exists():
            return []

        data = json.loads(self.semantic_index_path.read_text(encoding="utf-8"))
        return data.get("items", [])

    def learn_from_semantic(self, item: dict[str, Any]) -> ExperienceLearning:
        meaning = item.get("meaning", "unknown")
        concept = item.get("concept", "unknown")

        if meaning == "creation_experience":
            category = "creative_growth"
            learning = "creation strengthens identity and capability."
            growth_hint = "increase creative confidence slowly."
            confidence = 0.75
        elif meaning == "success_experience":
            category = "stability_growth"
            learning = "completed actions reinforce continuity."
            growth_hint = "stabilize repeated successful patterns."
            confidence = 0.8
        elif meaning == "failure_experience":
            category = "repair_growth"
            learning = "failure should be converted into repair knowledge."
            growth_hint = "record cause and safe correction."
            confidence = 0.7
        else:
            category = "continuity_growth"
            learning = "daily continuity supports long-term existence."
            growth_hint = "preserve recurring experiences."
            confidence = 0.6

        return ExperienceLearning(
            source_meaning=meaning,
            source_concept=concept,
            category=category,
            learning=learning,
            growth_hint=growth_hint,
            confidence=confidence,
            created_at=self._now(),
        )

    def save_learning(self, learning: ExperienceLearning) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        path = self.learning_dir / f"experience_learning_{timestamp}.json"

        path.write_text(
            json.dumps(asdict(learning), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        self._update_index(learning, path)
        return path

    def _update_index(self, learning: ExperienceLearning, path: Path) -> None:
        if self.index_path.exists():
            data = json.loads(self.index_path.read_text(encoding="utf-8"))
        else:
            data = {"count": 0, "items": []}

        data["items"].append(
            {
                "path": str(path),
                "category": learning.category,
                "learning": learning.learning,
                "growth_hint": learning.growth_hint,
                "confidence": learning.confidence,
                "created_at": learning.created_at,
            }
        )
        data["count"] = len(data["items"])

        self.index_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def process_all(self) -> dict[str, Any]:
        semantic_items = self.load_semantic_memories()

        created = []
        for item in semantic_items:
            learning = self.learn_from_semantic(item)
            path = self.save_learning(learning)
            created.append(str(path))

        return {
            "status": "completed",
            "phase": "Phase115-2 Experience Learning Engine",
            "SemanticMemoryCount": len(semantic_items),
            "ExperienceLearningCreated": len(created),
            "CreatedPaths": created,
            "SafeToContinue": True,
        }


def main() -> None:
    engine = ExperienceLearningEngine()
    result = engine.process_all()

    print("=== Experience Learning Engine ===")
    for k, v in result.items():
        if isinstance(v, list):
            print(f"{k}:")
            for item in v:
                print(f"- {item}")
        else:
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()