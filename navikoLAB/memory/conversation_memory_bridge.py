from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.memory.memory_context_packet_reader import MemoryContextPacketReader


@dataclass
class ConversationMemoryBridgeResult:
    status: str
    phase: str
    conversation_engine_connected: bool
    packet_reader_connected: bool
    packet_file_found: bool
    reference_line_count: int
    memory_reference_lines: List[str]
    bridge_mode: str
    auto_response_injection: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class ConversationMemoryBridge:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.packet_reader = MemoryContextPacketReader(root_dir=root_dir)

    def connect(self) -> ConversationMemoryBridgeResult:
        packet_result = self.packet_reader.read_latest_packet()

        return ConversationMemoryBridgeResult(
            status="completed" if packet_result.packet_file_found else "blocked",
            phase="Phase5-13 Conversation Memory Bridge",
            conversation_engine_connected=True,
            packet_reader_connected=True,
            packet_file_found=packet_result.packet_file_found,
            reference_line_count=packet_result.reference_line_count,
            memory_reference_lines=packet_result.memory_reference_lines,
            bridge_mode="reference_only",
            auto_response_injection=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=packet_result.safe_to_continue,
        )

    def get_memory_references_for_conversation(self) -> List[str]:
        result = self.connect()

        if not result.safe_to_continue:
            return []

        return result.memory_reference_lines

    def build_conversation_reference_block(self) -> Dict[str, Any]:
        result = self.connect()

        return {
            "source": "ConversationMemoryBridge",
            "mode": result.bridge_mode,
            "auto_response_injection": result.auto_response_injection,
            "safe_to_use": result.safe_to_continue,
            "memory_reference_lines": result.memory_reference_lines,
            "instruction": (
                "これはConversationEngine用の記憶参照データです。"
                "返答へ強制的に挿入せず、自然な会話に必要な場合だけ参照します。"
            ),
        }

    def print_result(self, result: ConversationMemoryBridgeResult) -> None:
        print("=== Phase5-13 Conversation Memory Bridge ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"ConversationEngineConnected: {result.conversation_engine_connected}")
        print(f"PacketReaderConnected: {result.packet_reader_connected}")
        print(f"PacketFileFound: {result.packet_file_found}")
        print(f"ReferenceLineCount: {result.reference_line_count}")
        print(f"BridgeMode: {result.bridge_mode}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")

        print("")
        print("[Conversation Memory References]")
        if not result.memory_reference_lines:
            print("- なし")
        else:
            for index, line in enumerate(result.memory_reference_lines, start=1):
                print(f"- {index}: {line}")

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: ConversationMemoryBridgeResult) -> Dict[str, Any]:
        return asdict(result)


def run_phase5_13_test() -> None:
    bridge = ConversationMemoryBridge()
    result = bridge.connect()
    bridge.print_result(result)

    print("")
    print("[Reference Block Check]")
    reference_block = bridge.build_conversation_reference_block()
    print(f"source: {reference_block.get('source', '')}")
    print(f"mode: {reference_block.get('mode', '')}")
    print(f"safe_to_use: {reference_block.get('safe_to_use', False)}")
    print(f"line_count: {len(reference_block.get('memory_reference_lines', []))}")


if __name__ == "__main__":
    run_phase5_13_test()