from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class PersonalityContextReadResult:
    status: str
    phase: str
    context_file_found: bool
    context_path: str
    name: str
    role: str
    primary_goal: str
    base_tone: str
    user_name: str
    mood: str
    personality_traits: Dict[str, Any]
    core_rules: List[str]
    sample_phrases: List[str]
    auto_response_injection: bool
    conversation_engine_modified: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class PersonalityContextReader:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.personality_dir = self.root_dir / "personality"
        self.context_dir = self.personality_dir / "contexts"
        self.latest_context_path = self.context_dir / "latest_personality_context.json"

        self.context_dir.mkdir(parents=True, exist_ok=True)

    def read_latest_context(self) -> PersonalityContextReadResult:
        context_file_found = self.latest_context_path.exists()
        data = self._read_json(self.latest_context_path)

        context = data.get("personality_context", {})
        if not isinstance(context, dict):
            context = {}

        profile = context.get("profile", {})
        tone = context.get("tone", {})
        emotion = context.get("emotion", {})

        if not isinstance(profile, dict):
            profile = {}

        if not isinstance(tone, dict):
            tone = {}

        if not isinstance(emotion, dict):
            emotion = {}

        traits = profile.get("personality_traits", {})
        if not isinstance(traits, dict):
            traits = {}

        rules = profile.get("core_rules", [])
        if not isinstance(rules, list):
            rules = []

        sample_phrases = tone.get("sample_phrases", [])
        if not isinstance(sample_phrases, list):
            sample_phrases = []

        safe_rules = [str(rule) for rule in rules]
        safe_sample_phrases = [str(phrase) for phrase in sample_phrases]

        ready = (
            context_file_found
            and bool(str(profile.get("name", "")).strip())
            and bool(str(profile.get("primary_goal", "")).strip())
            and bool(str(tone.get("base_tone", "")).strip())
            and bool(str(emotion.get("mood", "")).strip())
        )

        return PersonalityContextReadResult(
            status="completed" if ready else "blocked",
            phase="Phase6-6 Personality Context Reader",
            context_file_found=context_file_found,
            context_path=str(self.latest_context_path),
            name=str(profile.get("name", "")),
            role=str(profile.get("role", "")),
            primary_goal=str(profile.get("primary_goal", "")),
            base_tone=str(tone.get("base_tone", "")),
            user_name=str(tone.get("user_name", "")),
            mood=str(emotion.get("mood", "")),
            personality_traits=traits,
            core_rules=safe_rules,
            sample_phrases=safe_sample_phrases,
            auto_response_injection=False,
            conversation_engine_modified=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=ready,
        )

    def print_result(self, result: PersonalityContextReadResult) -> None:
        print("=== Phase6-6 Personality Context Reader ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"ContextFileFound: {result.context_file_found}")
        print(f"ContextPath: {result.context_path}")
        print(f"Name: {result.name}")
        print(f"Role: {result.role}")
        print(f"PrimaryGoal: {result.primary_goal}")
        print(f"BaseTone: {result.base_tone}")
        print(f"UserName: {result.user_name}")
        print(f"Mood: {result.mood}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")
        print(f"ConversationEngineModified: {result.conversation_engine_modified}")

        print("")
        print("[Personality Traits]")
        if not result.personality_traits:
            print("- なし")
        else:
            for key, value in result.personality_traits.items():
                print(f"- {key}: {value}")

        print("")
        print("[Core Rules]")
        if not result.core_rules:
            print("- なし")
        else:
            for index, rule in enumerate(result.core_rules, start=1):
                print(f"- {index}: {rule}")

        print("")
        print("[Sample Phrases]")
        if not result.sample_phrases:
            print("- なし")
        else:
            for index, phrase in enumerate(result.sample_phrases, start=1):
                print(f"- {index}: {phrase}")

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: PersonalityContextReadResult) -> Dict[str, Any]:
        return asdict(result)

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


def run_phase6_6_test() -> None:
    reader = PersonalityContextReader()
    result = reader.read_latest_context()
    reader.print_result(result)


if __name__ == "__main__":
    run_phase6_6_test()