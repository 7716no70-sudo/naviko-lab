from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict


@dataclass
class EmotionStateReadResult:
    status: str
    phase: str
    emotion_file_found: bool
    emotion_path: str
    mood: str
    trust: float
    attachment: float
    curiosity: float
    fatigue: float
    confidence: float
    note: str
    emotion_state_ready: bool
    auto_response_injection: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class EmotionStateReader:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.personality_dir = self.root_dir / "personality"
        self.emotion_path = self.personality_dir / "emotion_state.json"

        self.personality_dir.mkdir(parents=True, exist_ok=True)

    def read(self) -> EmotionStateReadResult:
        emotion_file_found = self.emotion_path.exists()
        data = self._read_json(self.emotion_path)

        mood = str(data.get("mood", "")).strip()

        emotion_state_ready = (
            emotion_file_found
            and bool(mood)
        )

        return EmotionStateReadResult(
            status="completed" if emotion_state_ready else "blocked",
            phase="Phase6-4 Emotion State Reader",
            emotion_file_found=emotion_file_found,
            emotion_path=str(self.emotion_path),
            mood=mood,
            trust=self._to_float(data.get("trust", 0.0)),
            attachment=self._to_float(data.get("attachment", 0.0)),
            curiosity=self._to_float(data.get("curiosity", 0.0)),
            fatigue=self._to_float(data.get("fatigue", 0.0)),
            confidence=self._to_float(data.get("confidence", 0.0)),
            note=str(data.get("note", "")),
            emotion_state_ready=emotion_state_ready,
            auto_response_injection=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=emotion_state_ready,
        )

    def print_result(self, result: EmotionStateReadResult) -> None:
        print("=== Phase6-4 Emotion State Reader ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"EmotionFileFound: {result.emotion_file_found}")
        print(f"EmotionPath: {result.emotion_path}")
        print(f"Mood: {result.mood}")
        print(f"Trust: {result.trust}")
        print(f"Attachment: {result.attachment}")
        print(f"Curiosity: {result.curiosity}")
        print(f"Fatigue: {result.fatigue}")
        print(f"Confidence: {result.confidence}")
        print(f"EmotionStateReady: {result.emotion_state_ready}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")

        print("")
        print("[Emotion Note]")
        print(result.note if result.note else "なし")

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: EmotionStateReadResult) -> Dict[str, Any]:
        return asdict(result)

    def _to_float(self, value: Any) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

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


def run_phase6_4_test() -> None:
    reader = EmotionStateReader()
    result = reader.read()
    reader.print_result(result)


if __name__ == "__main__":
    run_phase6_4_test()