from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class ToneProfileReadResult:
    status: str
    phase: str
    tone_file_found: bool
    tone_path: str
    base_tone: str
    user_name: str
    speech_style: Dict[str, Any]
    sample_phrases: List[str]
    tone_profile_ready: bool
    auto_response_injection: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class ToneProfileReader:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.personality_dir = self.root_dir / "personality"
        self.tone_path = self.personality_dir / "tone_profile.json"

        self.personality_dir.mkdir(parents=True, exist_ok=True)

    def read(self) -> ToneProfileReadResult:
        tone_file_found = self.tone_path.exists()
        data = self._read_json(self.tone_path)

        speech_style = data.get("speech_style", {})
        if not isinstance(speech_style, dict):
            speech_style = {}

        sample_phrases = data.get("sample_phrases", [])
        if not isinstance(sample_phrases, list):
            sample_phrases = []

        safe_sample_phrases = [str(phrase) for phrase in sample_phrases]

        tone_profile_ready = (
            tone_file_found
            and bool(str(data.get("base_tone", "")).strip())
            and bool(str(data.get("user_name", "")).strip())
        )

        return ToneProfileReadResult(
            status="completed" if tone_profile_ready else "blocked",
            phase="Phase6-3 Tone Profile Reader",
            tone_file_found=tone_file_found,
            tone_path=str(self.tone_path),
            base_tone=str(data.get("base_tone", "")),
            user_name=str(data.get("user_name", "")),
            speech_style=speech_style,
            sample_phrases=safe_sample_phrases,
            tone_profile_ready=tone_profile_ready,
            auto_response_injection=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=tone_profile_ready,
        )

    def print_result(self, result: ToneProfileReadResult) -> None:
        print("=== Phase6-3 Tone Profile Reader ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"ToneFileFound: {result.tone_file_found}")
        print(f"TonePath: {result.tone_path}")
        print(f"BaseTone: {result.base_tone}")
        print(f"UserName: {result.user_name}")
        print(f"ToneProfileReady: {result.tone_profile_ready}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")

        print("")
        print("[Speech Style]")
        if not result.speech_style:
            print("- なし")
        else:
            for key, value in result.speech_style.items():
                print(f"- {key}: {value}")

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

    def to_dict(self, result: ToneProfileReadResult) -> Dict[str, Any]:
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


def run_phase6_3_test() -> None:
    reader = ToneProfileReader()
    result = reader.read()
    reader.print_result(result)


if __name__ == "__main__":
    run_phase6_3_test()