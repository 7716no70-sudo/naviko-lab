from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.personality.personality_safe_packet_reader import PersonalitySafePacketReader


@dataclass
class ConversationPersonalityBridgeResult:
    status: str
    phase: str
    conversation_engine_connected: bool
    packet_reader_connected: bool
    packet_file_found: bool
    name: str
    user_name: str
    primary_goal: str
    base_tone: str
    mood: str
    core_rules: List[str]
    sample_phrases: List[str]
    bridge_mode: str
    auto_response_injection: bool
    conversation_engine_modified: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class ConversationPersonalityBridge:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.packet_reader = PersonalitySafePacketReader(root_dir=root_dir)

    def connect(self) -> ConversationPersonalityBridgeResult:
        packet = self.packet_reader.read_latest_packet()

        return ConversationPersonalityBridgeResult(
            status="completed" if packet.safe_to_continue else "blocked",
            phase="Phase6-10 Conversation Personality Bridge",
            conversation_engine_connected=True,
            packet_reader_connected=True,
            packet_file_found=packet.packet_file_found,
            name=packet.name,
            user_name=packet.user_name,
            primary_goal=packet.primary_goal,
            base_tone=packet.base_tone,
            mood=packet.mood,
            core_rules=packet.core_rules,
            sample_phrases=packet.sample_phrases,
            bridge_mode="reference_only",
            auto_response_injection=False,
            conversation_engine_modified=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=packet.safe_to_continue,
        )

    def build_personality_reference_block(self) -> Dict[str, Any]:
        result = self.connect()

        return {
            "source": "ConversationPersonalityBridge",
            "mode": result.bridge_mode,
            "safe_to_use": result.safe_to_continue,
            "auto_response_injection": result.auto_response_injection,
            "conversation_engine_modified": result.conversation_engine_modified,
            "name": result.name,
            "user_name": result.user_name,
            "primary_goal": result.primary_goal,
            "base_tone": result.base_tone,
            "mood": result.mood,
            "core_rules": result.core_rules,
            "sample_phrases": result.sample_phrases,
            "instruction": (
                "これはConversationEngine用の人格参照データです。"
                "返答へ強制的に挿入せず、ナビ子らしい自然な会話に必要な場合だけ参照します。"
                "第一目標から外れそうな場合は、目的がぶれていることを明示して止めます。"
            ),
        }

    def get_personality_reference_for_conversation(self) -> Dict[str, Any]:
        block = self.build_personality_reference_block()

        if not bool(block.get("safe_to_use", False)):
            return {}

        return block

    def print_result(self, result: ConversationPersonalityBridgeResult) -> None:
        print("=== Phase6-10 Conversation Personality Bridge ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"ConversationEngineConnected: {result.conversation_engine_connected}")
        print(f"PacketReaderConnected: {result.packet_reader_connected}")
        print(f"PacketFileFound: {result.packet_file_found}")
        print(f"Name: {result.name}")
        print(f"UserName: {result.user_name}")
        print(f"PrimaryGoal: {result.primary_goal}")
        print(f"BaseTone: {result.base_tone}")
        print(f"Mood: {result.mood}")
        print(f"BridgeMode: {result.bridge_mode}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")
        print(f"ConversationEngineModified: {result.conversation_engine_modified}")

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

    def to_dict(self, result: ConversationPersonalityBridgeResult) -> Dict[str, Any]:
        return asdict(result)


def run_phase6_10_test() -> None:
    bridge = ConversationPersonalityBridge()
    result = bridge.connect()
    bridge.print_result(result)

    print("")
    print("[Personality Reference Block Check]")
    block = bridge.build_personality_reference_block()
    print(f"source: {block.get('source', '')}")
    print(f"mode: {block.get('mode', '')}")
    print(f"safe_to_use: {block.get('safe_to_use', False)}")
    print(f"name: {block.get('name', '')}")
    print(f"user_name: {block.get('user_name', '')}")
    print(f"base_tone: {block.get('base_tone', '')}")


if __name__ == "__main__":
    run_phase6_10_test()