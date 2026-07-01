from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.agents.long_term_memory_reader import LongTermMemoryReader


@dataclass
class MemoryAgentLongTermConnectionResult:
    status: str
    phase: str
    memory_agent_connected: bool
    long_term_reader_connected: bool
    memory_file_found: bool
    memory_count: int
    referenced_memories: List[Dict[str, Any]]
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    auto_response_injection: bool
    safe_to_continue: bool


class MemoryAgentLongTermConnector:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.reader = LongTermMemoryReader(root_dir=root_dir)

    def connect_and_read(self) -> MemoryAgentLongTermConnectionResult:
        read_result = self.reader.read_long_term_memory()

        return MemoryAgentLongTermConnectionResult(
            status="completed",
            phase="Phase4-15 MemoryAgent Long Term Reader Connection",
            memory_agent_connected=True,
            long_term_reader_connected=True,
            memory_file_found=read_result.memory_file_found,
            memory_count=read_result.memory_count,
            referenced_memories=read_result.memories,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            auto_response_injection=False,
            safe_to_continue=True,
        )

    def print_result(self, result: MemoryAgentLongTermConnectionResult) -> None:
        print("=== Phase4-15 MemoryAgent Long Term Connector ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"MemoryAgentConnected: {result.memory_agent_connected}")
        print(f"LongTermReaderConnected: {result.long_term_reader_connected}")
        print(f"MemoryFileFound: {result.memory_file_found}")
        print(f"MemoryCount: {result.memory_count}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")

        print("")
        print("[Referenced Long Term Memories]")

        if not result.referenced_memories:
            print("- 長期記憶参照なし")
        else:
            for index, item in enumerate(result.referenced_memories, start=1):
                print(f"- Memory {index}")
                print(f"  id: {item.get('id', '')}")
                print(f"  text: {item.get('text', '')}")
                print(f"  importance: {item.get('importance', '')}")
                print(f"  score: {item.get('score', 0)}")
                print(f"  safe_adopted: {item.get('safe_adopted', False)}")

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: MemoryAgentLongTermConnectionResult) -> Dict[str, Any]:
        return asdict(result)


def run_phase4_15_test() -> None:
    connector = MemoryAgentLongTermConnector()
    result = connector.connect_and_read()
    connector.print_result(result)


if __name__ == "__main__":
    run_phase4_15_test()