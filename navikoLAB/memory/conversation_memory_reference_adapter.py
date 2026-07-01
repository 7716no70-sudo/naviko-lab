from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.memory.conversation_memory_bridge import ConversationMemoryBridge


@dataclass
class ConversationMemoryReferenceAdapterResult:
    status: str
    phase: str
    adapter_ready: bool
    conversation_engine_modified: bool
    memory_reference_available: bool
    reference_line_count: int
    reference_block: Dict[str, Any]
    adapter_mode: str
    auto_response_injection: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class ConversationMemoryReferenceAdapter:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.bridge = ConversationMemoryBridge(root_dir=root_dir)

    def build_reference_block(self) -> Dict[str, Any]:
        bridge_block = self.bridge.build_conversation_reference_block()

        memory_reference_lines = bridge_block.get("memory_reference_lines", [])
        if not isinstance(memory_reference_lines, list):
            memory_reference_lines = []

        safe_lines = [str(line) for line in memory_reference_lines]

        return {
            "source": "ConversationMemoryReferenceAdapter",
            "adapter_mode": "reference_only",
            "safe_to_use": bool(bridge_block.get("safe_to_use", False)),
            "auto_response_injection": False,
            "conversation_engine_modified": False,
            "memory_reference_lines": safe_lines,
            "reference_line_count": len(safe_lines),
            "instruction": (
                "ConversationEngineはこの記憶参照ブロックを必要時だけ参照する。"
                "返答文へ強制注入しない。"
                "ナビ子の自然な会話と目的維持に必要な場合だけ使う。"
            ),
        }

    def diagnose_adapter(self) -> ConversationMemoryReferenceAdapterResult:
        reference_block = self.build_reference_block()

        safe_to_use = bool(reference_block.get("safe_to_use", False))
        reference_line_count = int(reference_block.get("reference_line_count", 0))

        return ConversationMemoryReferenceAdapterResult(
            status="completed" if safe_to_use else "blocked",
            phase="Phase5-15 ConversationEngine Memory Reference Adapter",
            adapter_ready=safe_to_use,
            conversation_engine_modified=False,
            memory_reference_available=reference_line_count > 0,
            reference_line_count=reference_line_count,
            reference_block=reference_block,
            adapter_mode=str(reference_block.get("adapter_mode", "reference_only")),
            auto_response_injection=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=safe_to_use,
        )

    def get_memory_reference_lines(self) -> List[str]:
        reference_block = self.build_reference_block()

        if not bool(reference_block.get("safe_to_use", False)):
            return []

        lines = reference_block.get("memory_reference_lines", [])
        if not isinstance(lines, list):
            return []

        return [str(line) for line in lines]

    def print_result(self, result: ConversationMemoryReferenceAdapterResult) -> None:
        print("=== Phase5-15 ConversationEngine Memory Reference Adapter ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"AdapterReady: {result.adapter_ready}")
        print(f"ConversationEngineModified: {result.conversation_engine_modified}")
        print(f"MemoryReferenceAvailable: {result.memory_reference_available}")
        print(f"ReferenceLineCount: {result.reference_line_count}")
        print(f"AdapterMode: {result.adapter_mode}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")

        print("")
        print("[Reference Lines]")
        lines = result.reference_block.get("memory_reference_lines", [])
        if not isinstance(lines, list) or not lines:
            print("- なし")
        else:
            for index, line in enumerate(lines, start=1):
                print(f"- {index}: {line}")

        print("")
        print("[Adapter Instruction]")
        print(result.reference_block.get("instruction", ""))

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: ConversationMemoryReferenceAdapterResult) -> Dict[str, Any]:
        return asdict(result)


def run_phase5_15_test() -> None:
    adapter = ConversationMemoryReferenceAdapter()
    result = adapter.diagnose_adapter()
    adapter.print_result(result)


if __name__ == "__main__":
    run_phase5_15_test()