from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class PersonalitySafePacketReadResult:
    status: str
    phase: str
    packet_file_found: bool
    packet_path: str
    created_at: str
    purpose: str
    packet_mode: str
    auto_response_injection: bool
    conversation_engine_modified: bool
    name: str
    user_name: str
    role: str
    primary_goal: str
    base_tone: str
    mood: str
    personality_traits: Dict[str, Any]
    core_rules: List[str]
    sample_phrases: List[str]
    instruction: str
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class PersonalitySafePacketReader:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.personality_dir = self.root_dir / "personality"
        self.packet_dir = self.personality_dir / "packets"
        self.latest_packet_path = self.packet_dir / "latest_personality_safe_packet.json"

        self.packet_dir.mkdir(parents=True, exist_ok=True)

    def read_latest_packet(self) -> PersonalitySafePacketReadResult:
        packet_file_found = self.latest_packet_path.exists()
        data = self._read_json(self.latest_packet_path)

        traits = data.get("personality_traits", {})
        if not isinstance(traits, dict):
            traits = {}

        rules = data.get("core_rules", [])
        if not isinstance(rules, list):
            rules = []

        phrases = data.get("sample_phrases", [])
        if not isinstance(phrases, list):
            phrases = []

        packet_mode = str(data.get("packet_mode", "reference_only"))

        safe_to_continue = (
            packet_file_found
            and packet_mode == "reference_only"
            and bool(str(data.get("name", "")).strip())
            and bool(str(data.get("primary_goal", "")).strip())
        )

        return PersonalitySafePacketReadResult(
            status="completed" if safe_to_continue else "blocked",
            phase="Phase6-9 Personality Safe Packet Reader",
            packet_file_found=packet_file_found,
            packet_path=str(self.latest_packet_path),
            created_at=str(data.get("created_at", "")),
            purpose=str(data.get("purpose", "")),
            packet_mode=packet_mode,
            auto_response_injection=bool(data.get("auto_response_injection", False)),
            conversation_engine_modified=bool(data.get("conversation_engine_modified", False)),
            name=str(data.get("name", "")),
            user_name=str(data.get("user_name", "")),
            role=str(data.get("role", "")),
            primary_goal=str(data.get("primary_goal", "")),
            base_tone=str(data.get("base_tone", "")),
            mood=str(data.get("mood", "")),
            personality_traits=traits,
            core_rules=[str(rule) for rule in rules],
            sample_phrases=[str(phrase) for phrase in phrases],
            instruction=str(data.get("instruction", "")),
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=safe_to_continue,
        )

    def print_result(self, result: PersonalitySafePacketReadResult) -> None:
        print("=== Phase6-9 Personality Safe Packet Reader ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"PacketFileFound: {result.packet_file_found}")
        print(f"PacketPath: {result.packet_path}")
        print(f"CreatedAt: {result.created_at}")
        print(f"Purpose: {result.purpose}")
        print(f"PacketMode: {result.packet_mode}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")
        print(f"ConversationEngineModified: {result.conversation_engine_modified}")
        print(f"Name: {result.name}")
        print(f"UserName: {result.user_name}")
        print(f"Role: {result.role}")
        print(f"PrimaryGoal: {result.primary_goal}")
        print(f"BaseTone: {result.base_tone}")
        print(f"Mood: {result.mood}")

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
        print("[Instruction]")
        print(result.instruction if result.instruction else "なし")

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: PersonalitySafePacketReadResult) -> Dict[str, Any]:
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


def run_phase6_9_test() -> None:
    reader = PersonalitySafePacketReader()
    result = reader.read_latest_packet()
    reader.print_result(result)


if __name__ == "__main__":
    run_phase6_9_test()