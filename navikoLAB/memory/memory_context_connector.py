from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.memory.memory_context_reader import MemoryContextReader


@dataclass
class MemoryContextConnectionResult:
    status: str
    phase: str
    conversation_engine_connected: bool
    memory_context_reader_connected: bool
    context_file_found: bool
    short_memory_count: int
    mid_memory_count: int
    long_term_memory_count: int
    referenced_context: Dict[str, Any]
    auto_response_injection: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class MemoryContextConnector:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.reader = MemoryContextReader(root_dir=root_dir)

    def connect(self) -> MemoryContextConnectionResult:
        context_result = self.reader.read_latest_context()

        return MemoryContextConnectionResult(
            status="completed" if context_result.context_file_found else "blocked",
            phase="Phase5-9 Memory Context Connector",
            conversation_engine_connected=True,
            memory_context_reader_connected=True,
            context_file_found=context_result.context_file_found,
            short_memory_count=context_result.short_memory_count,
            mid_memory_count=context_result.mid_memory_count,
            long_term_memory_count=context_result.long_term_memory_count,
            referenced_context=context_result.context_summary,
            auto_response_injection=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=context_result.safe_to_continue,
        )

    def print_result(self, result: MemoryContextConnectionResult) -> None:
        print("=== Phase5-9 Memory Context Connector ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"ConversationEngineConnected: {result.conversation_engine_connected}")
        print(f"MemoryContextReaderConnected: {result.memory_context_reader_connected}")
        print(f"ContextFileFound: {result.context_file_found}")
        print(f"ShortMemoryCount: {result.short_memory_count}")
        print(f"MidMemoryCount: {result.mid_memory_count}")
        print(f"LongTermMemoryCount: {result.long_term_memory_count}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")

        print("")
        print("[Referenced Context]")
        print(f"created_at: {result.referenced_context.get('created_at', '')}")
        print(f"purpose: {result.referenced_context.get('purpose', '')}")

        print("")
        print("[Short Memory Preview]")
        self._print_preview(result.referenced_context.get("short_memory_preview", []))

        print("")
        print("[Mid Memory Preview]")
        self._print_preview(result.referenced_context.get("mid_memory_preview", []))

        print("")
        print("[Long Term Memory Preview]")
        self._print_preview(result.referenced_context.get("long_term_memory_preview", []))

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: MemoryContextConnectionResult) -> Dict[str, Any]:
        return asdict(result)

    def _print_preview(self, preview_items: Any) -> None:
        if not isinstance(preview_items, list) or not preview_items:
            print("- なし")
            return

        for index, item in enumerate(preview_items, start=1):
            if not isinstance(item, dict):
                continue

            print(f"- Item {index}")
            print(f"  id: {item.get('id', '')}")
            print(f"  speaker: {item.get('speaker', '')}")
            print(f"  text: {item.get('text', '')}")
            print(f"  importance: {item.get('importance', '')}")
            print(f"  score: {item.get('score', 0)}")
            print(f"  source: {item.get('source', '')}")


def run_phase5_9_test() -> None:
    connector = MemoryContextConnector()
    result = connector.connect()
    connector.print_result(result)


if __name__ == "__main__":
    run_phase5_9_test()