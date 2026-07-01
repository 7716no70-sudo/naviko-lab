from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.personality.personality_context_reader import PersonalityContextReader


@dataclass
class PersonalitySafePacket:
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


@dataclass
class PersonalitySafePacketBuildResult:
    status: str
    phase: str
    context_available: bool
    packet_created: bool
    packet_path: str
    latest_packet_path: str
    packet_mode: str
    auto_response_injection: bool
    conversation_engine_modified: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class PersonalitySafePacketBuilder:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.personality_dir = self.root_dir / "personality"
        self.packet_dir = self.personality_dir / "packets"

        self.personality_dir.mkdir(parents=True, exist_ok=True)
        self.packet_dir.mkdir(parents=True, exist_ok=True)

        self.context_reader = PersonalityContextReader(root_dir=root_dir)

    def build_packet(self) -> PersonalitySafePacketBuildResult:
        context = self.context_reader.read_latest_context()

        packet = PersonalitySafePacket(
            created_at=datetime.now().isoformat(timespec="seconds"),
            purpose="ナビ子が自然な会話を行うための人格・口調・感情の安全参照データ",
            packet_mode="reference_only",
            auto_response_injection=False,
            conversation_engine_modified=False,
            name=context.name,
            user_name=context.user_name,
            role=context.role,
            primary_goal=context.primary_goal,
            base_tone=context.base_tone,
            mood=context.mood,
            personality_traits=context.personality_traits,
            core_rules=context.core_rules,
            sample_phrases=context.sample_phrases,
            instruction=(
                "このパケットはConversationEngine用の人格参照データです。"
                "返答へ強制注入せず、ナビ子らしい自然な会話に必要な場合だけ参照します。"
                "第一目標から外れる場合は、目的がぶれていることを明示して止めます。"
            ),
        )

        packet_path = self._save_packet(packet)
        latest_packet_path = self.packet_dir / "latest_personality_safe_packet.json"

        return PersonalitySafePacketBuildResult(
            status="completed" if context.safe_to_continue else "blocked",
            phase="Phase6-8 Personality Safe Packet Builder",
            context_available=context.safe_to_continue,
            packet_created=context.safe_to_continue,
            packet_path=str(packet_path),
            latest_packet_path=str(latest_packet_path),
            packet_mode=packet.packet_mode,
            auto_response_injection=packet.auto_response_injection,
            conversation_engine_modified=packet.conversation_engine_modified,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=context.safe_to_continue,
        )

    def _save_packet(self, packet: PersonalitySafePacket) -> Path:
        filename = f"personality_safe_packet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = self.packet_dir / filename

        packet_data = asdict(packet)

        with path.open("w", encoding="utf-8") as f:
            json.dump(packet_data, f, ensure_ascii=False, indent=2)

        latest_path = self.packet_dir / "latest_personality_safe_packet.json"
        with latest_path.open("w", encoding="utf-8") as f:
            json.dump(packet_data, f, ensure_ascii=False, indent=2)

        return path

    def print_result(self, result: PersonalitySafePacketBuildResult) -> None:
        print("=== Phase6-8 Personality Safe Packet Builder ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"ContextAvailable: {result.context_available}")
        print(f"PacketCreated: {result.packet_created}")
        print(f"PacketPath: {result.packet_path}")
        print(f"LatestPacketPath: {result.latest_packet_path}")
        print(f"PacketMode: {result.packet_mode}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")
        print(f"ConversationEngineModified: {result.conversation_engine_modified}")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: PersonalitySafePacketBuildResult) -> Dict[str, Any]:
        return asdict(result)


def run_phase6_8_test() -> None:
    builder = PersonalitySafePacketBuilder()
    result = builder.build_packet()
    builder.print_result(result)


if __name__ == "__main__":
    run_phase6_8_test()