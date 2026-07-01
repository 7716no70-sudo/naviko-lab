# navikoLAB/stable_life/semantic_memory_engine.py

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class SemanticMemory:
    source_text: str
    meaning: str
    concept: str
    value_hint: str
    created_at: str


class SemanticMemoryEngine:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)
        self.memory_dir = self.root / "stable_life" / "semantic_memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.memory_dir / "semantic_memory_index.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def interpret(self, text: str) -> SemanticMemory:
        lowered = text.lower()

        if any(k in text for k in ["作る", "作り", "制作", "生成", "開発", "実装", "構築", "動画", "コード"]):
            meaning = "creation_experience"
            concept = "creative_activity"
            value_hint = "creation_is_important"
        elif any(k in lowered for k in ["create", "build", "develop", "implement", "code"]):
            meaning = "creation_experience"
            concept = "creative_activity"
            value_hint = "creation_is_important"
        elif any(k in text for k in ["失敗", "エラー", "不具合", "壊れ", "問題", "修正"]):
            meaning = "failure_experience"
            concept = "repair_and_learning"
            value_hint = "safety_and_improvement_are_important"
        elif any(k in lowered for k in ["error", "bug", "failed", "failure", "broken", "fix"]):
            meaning = "failure_experience"
            concept = "repair_and_learning"
            value_hint = "safety_and_improvement_are_important"
        elif any(k in text for k in ["確認", "成功", "完了", "通過", "正常"]):
            meaning = "success_experience"
            concept = "stable_progress"
            value_hint = "continuity_and_completion_are_important"
        elif any(k in lowered for k in ["success", "completed", "passed", "ok"]):
            meaning = "success_experience"
            concept = "stable_progress"
            value_hint = "continuity_and_completion_are_important"
        else:
            meaning = "general_experience"
            concept = "daily_continuity"
            value_hint = "existence_continuity_is_important"

        return SemanticMemory(
            source_text=text,
            meaning=meaning,
            concept=concept,
            value_hint=value_hint,
            created_at=self._now(),
        )

    def save(self, memory: SemanticMemory) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.memory_dir / f"semantic_memory_{timestamp}.json"

        path.write_text(
            json.dumps(asdict(memory), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        self._update_index(memory, path)
        return path

    def _update_index(self, memory: SemanticMemory, path: Path) -> None:
        if self.index_path.exists():
            data = json.loads(self.index_path.read_text(encoding="utf-8"))
        else:
            data = {"count": 0, "items": []}

        data["items"].append(
            {
                "path": str(path),
                "meaning": memory.meaning,
                "concept": memory.concept,
                "value_hint": memory.value_hint,
                "created_at": memory.created_at,
            }
        )
        data["count"] = len(data["items"])

        self.index_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def process(self, text: str) -> dict[str, Any]:
        memory = self.interpret(text)
        path = self.save(memory)

        return {
            "status": "completed",
            "phase": "Phase115-1 Semantic Memory Engine",
            "SemanticMemoryCreated": True,
            "Meaning": memory.meaning,
            "Concept": memory.concept,
            "ValueHint": memory.value_hint,
            "SavedPath": str(path),
            "SafeToContinue": True,
        }


def main() -> None:
    engine = SemanticMemoryEngine()

    sample = "今日はNavikoのStable Life Kernelを作り始めた"
    result = engine.process(sample)

    print("=== Semantic Memory Engine ===")
    for k, v in result.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()