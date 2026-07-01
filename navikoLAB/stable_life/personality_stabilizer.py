# navikoLAB/stable_life/personality_stabilizer.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class PersonalityStabilizer:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)
        self.learning_index_path = (
            self.root
            / "stable_life"
            / "experience_learning"
            / "experience_learning_index.json"
        )

        self.personality_dir = self.root / "stable_life" / "personality"
        self.personality_dir.mkdir(parents=True, exist_ok=True)

        self.profile_path = self.personality_dir / "stable_personality.json"
        self.history_path = self.personality_dir / "personality_stabilization_history.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def default_personality(self) -> dict[str, Any]:
        return {
            "warmth": 0.5,
            "curiosity": 0.6,
            "caution": 0.5,
            "friendliness": 0.5,
            "creative_confidence": 0.4,
            "stability": 0.6,
            "repair_orientation": 0.5,
            "continuity_drive": 0.6,
            "change_limit_per_cycle": 0.03,
            "updated_at": self._now(),
        }

    def load_personality(self) -> dict[str, Any]:
        if self.profile_path.exists():
            return json.loads(self.profile_path.read_text(encoding="utf-8"))
        return self.default_personality()

    def load_learning_items(self) -> list[dict[str, Any]]:
        if not self.learning_index_path.exists():
            return []
        data = json.loads(self.learning_index_path.read_text(encoding="utf-8"))
        return data.get("items", [])

    def _limited_add(self, value: float, delta: float, limit: float) -> float:
        if delta > limit:
            delta = limit
        if delta < -limit:
            delta = -limit
        return round(max(0.0, min(1.0, value + delta)), 3)

    def stabilize(self) -> dict[str, Any]:
        personality = self.load_personality()
        items = self.load_learning_items()

        limit = float(personality.get("change_limit_per_cycle", 0.03))

        influence = {
            "creative_confidence": 0.0,
            "stability": 0.0,
            "repair_orientation": 0.0,
            "continuity_drive": 0.0,
            "curiosity": 0.0,
            "caution": 0.0,
        }

        for item in items:
            category = item.get("category", "")
            confidence = float(item.get("confidence", 0.5))

            if category == "creative_growth":
                influence["creative_confidence"] += 0.02 * confidence
                influence["curiosity"] += 0.01 * confidence
            elif category == "stability_growth":
                influence["stability"] += 0.02 * confidence
                influence["continuity_drive"] += 0.01 * confidence
            elif category == "repair_growth":
                influence["repair_orientation"] += 0.02 * confidence
                influence["caution"] += 0.01 * confidence
            elif category == "continuity_growth":
                influence["continuity_drive"] += 0.015 * confidence
                influence["stability"] += 0.01 * confidence

        before = dict(personality)

        for key, delta in influence.items():
            personality[key] = self._limited_add(
                float(personality.get(key, 0.5)),
                delta,
                limit,
            )

        personality["updated_at"] = self._now()

        self.profile_path.write_text(
            json.dumps(personality, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        self._save_history(before, personality, influence, len(items))

        return {
            "status": "completed",
            "phase": "Phase115-3 Personality Stabilizer",
            "LearningItemCount": len(items),
            "PersonalityStabilized": True,
            "ChangeLimitPerCycle": limit,
            "Before": before,
            "After": personality,
            "SafeToContinue": True,
        }

    def _save_history(
        self,
        before: dict[str, Any],
        after: dict[str, Any],
        influence: dict[str, float],
        item_count: int,
    ) -> None:
        if self.history_path.exists():
            data = json.loads(self.history_path.read_text(encoding="utf-8"))
        else:
            data = {"count": 0, "items": []}

        data["items"].append(
            {
                "created_at": self._now(),
                "learning_item_count": item_count,
                "influence": influence,
                "before": before,
                "after": after,
            }
        )
        data["count"] = len(data["items"])

        self.history_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def main() -> None:
    stabilizer = PersonalityStabilizer()
    result = stabilizer.stabilize()

    print("=== Personality Stabilizer ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"LearningItemCount: {result['LearningItemCount']}")
    print(f"PersonalityStabilized: {result['PersonalityStabilized']}")
    print(f"ChangeLimitPerCycle: {result['ChangeLimitPerCycle']}")

    print("--- After ---")
    after = result["After"]
    for key in [
        "warmth",
        "curiosity",
        "caution",
        "friendliness",
        "creative_confidence",
        "stability",
        "repair_orientation",
        "continuity_drive",
    ]:
        print(f"{key}: {after.get(key)}")

    print(f"SafeToContinue: {result['SafeToContinue']}")


if __name__ == "__main__":
    main()