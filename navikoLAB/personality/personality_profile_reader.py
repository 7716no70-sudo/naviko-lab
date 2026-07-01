from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class PersonalityProfileReadResult:
    status: str
    phase: str
    profile_file_found: bool
    profile_path: str
    name: str
    role: str
    primary_goal: str
    personality_traits: Dict[str, Any]
    core_rules: List[str]
    personality_profile_ready: bool
    auto_response_injection: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class PersonalityProfileReader:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.personality_dir = self.root_dir / "personality"
        self.profile_path = self.personality_dir / "personality_profile.json"

        self.personality_dir.mkdir(parents=True, exist_ok=True)

    def read(self) -> PersonalityProfileReadResult:
        profile_file_found = self.profile_path.exists()
        data = self._read_json(self.profile_path)

        traits = data.get("personality_traits", {})
        if not isinstance(traits, dict):
            traits = {}

        rules = data.get("core_rules", [])
        if not isinstance(rules, list):
            rules = []

        safe_rules = [str(rule) for rule in rules]

        personality_profile_ready = (
            profile_file_found
            and bool(str(data.get("name", "")).strip())
            and bool(str(data.get("primary_goal", "")).strip())
        )

        return PersonalityProfileReadResult(
            status="completed" if personality_profile_ready else "blocked",
            phase="Phase6-2 Personality Profile Reader",
            profile_file_found=profile_file_found,
            profile_path=str(self.profile_path),
            name=str(data.get("name", "")),
            role=str(data.get("role", "")),
            primary_goal=str(data.get("primary_goal", "")),
            personality_traits=traits,
            core_rules=safe_rules,
            personality_profile_ready=personality_profile_ready,
            auto_response_injection=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=personality_profile_ready,
        )

    def print_result(self, result: PersonalityProfileReadResult) -> None:
        print("=== Phase6-2 Personality Profile Reader ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"ProfileFileFound: {result.profile_file_found}")
        print(f"ProfilePath: {result.profile_path}")
        print(f"Name: {result.name}")
        print(f"Role: {result.role}")
        print(f"PrimaryGoal: {result.primary_goal}")
        print(f"PersonalityProfileReady: {result.personality_profile_ready}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")

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
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: PersonalityProfileReadResult) -> Dict[str, Any]:
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


def run_phase6_2_test() -> None:
    reader = PersonalityProfileReader()
    result = reader.read()
    reader.print_result(result)


if __name__ == "__main__":
    run_phase6_2_test()