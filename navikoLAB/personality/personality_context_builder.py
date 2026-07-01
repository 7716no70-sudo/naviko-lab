from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from navikoLAB.personality.personality_profile_reader import PersonalityProfileReader
from navikoLAB.personality.tone_profile_reader import ToneProfileReader
from navikoLAB.personality.emotion_state_reader import EmotionStateReader


@dataclass
class PersonalityContextBuildResult:
    status: str
    phase: str
    personality_profile_ready: bool
    tone_profile_ready: bool
    emotion_state_ready: bool
    context_created: bool
    context_path: str
    latest_context_path: str
    auto_response_injection: bool
    conversation_engine_modified: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class PersonalityContextBuilder:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.personality_dir = self.root_dir / "personality"
        self.context_dir = self.personality_dir / "contexts"

        self.personality_dir.mkdir(parents=True, exist_ok=True)
        self.context_dir.mkdir(parents=True, exist_ok=True)

        self.profile_reader = PersonalityProfileReader(root_dir=root_dir)
        self.tone_reader = ToneProfileReader(root_dir=root_dir)
        self.emotion_reader = EmotionStateReader(root_dir=root_dir)

    def build_context(self) -> PersonalityContextBuildResult:
        profile_result = self.profile_reader.read()
        tone_result = self.tone_reader.read()
        emotion_result = self.emotion_reader.read()

        ready = (
            profile_result.personality_profile_ready
            and tone_result.tone_profile_ready
            and emotion_result.emotion_state_ready
        )

        context_data = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "phase": "Phase6-5 Personality Context Builder",
            "purpose": "ナビ子が自然な会話を行うための人格参照コンテキスト",
            "auto_response_injection": False,
            "conversation_engine_modified": False,
            "safe_mode": True,
            "external_ai": False,
            "real_pc_operation": False,
            "file_delete": False,
            "personality_context": {
                "profile": {
                    "name": profile_result.name,
                    "role": profile_result.role,
                    "primary_goal": profile_result.primary_goal,
                    "personality_traits": profile_result.personality_traits,
                    "core_rules": profile_result.core_rules,
                },
                "tone": {
                    "base_tone": tone_result.base_tone,
                    "user_name": tone_result.user_name,
                    "speech_style": tone_result.speech_style,
                    "sample_phrases": tone_result.sample_phrases,
                },
                "emotion": {
                    "mood": emotion_result.mood,
                    "trust": emotion_result.trust,
                    "attachment": emotion_result.attachment,
                    "curiosity": emotion_result.curiosity,
                    "fatigue": emotion_result.fatigue,
                    "confidence": emotion_result.confidence,
                    "note": emotion_result.note,
                },
            },
        }

        context_path = self._save_context(context_data)
        latest_context_path = self.context_dir / "latest_personality_context.json"

        return PersonalityContextBuildResult(
            status="completed" if ready else "blocked",
            phase="Phase6-5 Personality Context Builder",
            personality_profile_ready=profile_result.personality_profile_ready,
            tone_profile_ready=tone_result.tone_profile_ready,
            emotion_state_ready=emotion_result.emotion_state_ready,
            context_created=ready,
            context_path=str(context_path),
            latest_context_path=str(latest_context_path),
            auto_response_injection=False,
            conversation_engine_modified=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=ready,
        )

    def _save_context(self, context_data: Dict[str, Any]) -> Path:
        filename = f"personality_context_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = self.context_dir / filename

        with path.open("w", encoding="utf-8") as f:
            json.dump(context_data, f, ensure_ascii=False, indent=2)

        latest_path = self.context_dir / "latest_personality_context.json"
        with latest_path.open("w", encoding="utf-8") as f:
            json.dump(context_data, f, ensure_ascii=False, indent=2)

        return path

    def print_result(self, result: PersonalityContextBuildResult) -> None:
        print("=== Phase6-5 Personality Context Builder ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"PersonalityProfileReady: {result.personality_profile_ready}")
        print(f"ToneProfileReady: {result.tone_profile_ready}")
        print(f"EmotionStateReady: {result.emotion_state_ready}")
        print(f"ContextCreated: {result.context_created}")
        print(f"ContextPath: {result.context_path}")
        print(f"LatestContextPath: {result.latest_context_path}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")
        print(f"ConversationEngineModified: {result.conversation_engine_modified}")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: PersonalityContextBuildResult) -> Dict[str, Any]:
        return asdict(result)


def run_phase6_5_test() -> None:
    builder = PersonalityContextBuilder()
    result = builder.build_context()
    builder.print_result(result)


if __name__ == "__main__":
    run_phase6_5_test()