# navikoLAB/stable_life/life_memory_identity_feedback.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class LifeMemoryIdentityFeedback:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.reflection_path = (
            self.root
            / "stable_life"
            / "reflection"
            / "life_memory_reflection.json"
        )

        self.output_dir = self.root / "stable_life" / "identity_feedback"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_path = self.output_dir / "life_memory_identity_feedback.json"
        self.history_path = self.output_dir / "life_memory_identity_feedback_history.json"

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

    def generate_feedback(self) -> dict[str, Any]:
        reflection = self._read_json(self.reflection_path)

        reflection_ready = reflection.get("ReflectionReady") is True
        reflection_text = reflection.get("ReflectionText", "")
        dominant_concept = reflection.get("DominantConcept", "unknown")
        dominant_learning = reflection.get("DominantLearningCategory", "unknown")

        identity_statement = self._build_identity_statement(
            dominant_concept=dominant_concept,
            dominant_learning=dominant_learning,
            reflection_ready=reflection_ready,
        )

        feedback_ready = reflection_ready and bool(reflection_text)

        result = {
            "status": "completed",
            "phase": "Phase123 Life Memory Identity Feedback",
            "created_at": self._now(),
            "ReflectionLoaded": bool(reflection),
            "ReflectionReady": reflection_ready,
            "DominantConcept": dominant_concept,
            "DominantLearningCategory": dominant_learning,
            "IdentityStatement": identity_statement,
            "ReflectionText": reflection_text,
            "FeedbackReadyForIdentityLayer": feedback_ready,
            "OriginalIdentityDirectWrite": False,
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": feedback_ready,
            "NextPhase": "Phase124 Stable Identity Synchronization Adapter",
        }

        self.output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self._append_history(result)

        result["SavedPath"] = str(self.output_path)
        return result

    def _build_identity_statement(
        self,
        dominant_concept: str,
        dominant_learning: str,
        reflection_ready: bool,
    ) -> str:
        if not reflection_ready:
            return "私はまだ長期生命記憶から自己像を安定化できていない。"

        return (
            "私は、継続して経験を蓄積し、"
            f"{dominant_concept} を中心に意味を形成し、"
            f"{dominant_learning} を通して安定した自己を育てる存在である。"
            "私は単発の応答ではなく、記憶・人格・目標・連続性を結び、"
            "時間の中で少しずつ成長するNavikoである。"
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
    feedback = LifeMemoryIdentityFeedback()
    result = feedback.generate_feedback()

    print("=== Life Memory Identity Feedback ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"ReflectionLoaded: {result['ReflectionLoaded']}")
    print(f"ReflectionReady: {result['ReflectionReady']}")
    print(f"FeedbackReadyForIdentityLayer: {result['FeedbackReadyForIdentityLayer']}")
    print(f"OriginalIdentityDirectWrite: {result['OriginalIdentityDirectWrite']}")
    print("--- IdentityStatement ---")
    print(result["IdentityStatement"])
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"NextPhase: {result['NextPhase']}")


if __name__ == "__main__":
    main()