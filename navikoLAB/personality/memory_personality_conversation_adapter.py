from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.memory.conversation_memory_reference_adapter import ConversationMemoryReferenceAdapter
from navikoLAB.personality.conversation_personality_reference_adapter import ConversationPersonalityReferenceAdapter


@dataclass
class MemoryPersonalityConversationAdapterResult:
    status: str
    phase: str
    adapter_ready: bool
    memory_reference_available: bool
    personality_reference_available: bool
    memory_reference_count: int
    name: str
    user_name: str
    primary_goal: str
    base_tone: str
    mood: str
    adapter_mode: str
    reference_block: Dict[str, Any]
    conversation_engine_modified: bool
    auto_response_injection: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class MemoryPersonalityConversationAdapter:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_adapter = ConversationMemoryReferenceAdapter(root_dir=root_dir)
        self.personality_adapter = ConversationPersonalityReferenceAdapter(root_dir=root_dir)

    def build_reference_block(self) -> Dict[str, Any]:
        memory_result = self.memory_adapter.diagnose_adapter()
        personality_result = self.personality_adapter.diagnose_adapter()

        memory_lines = self.memory_adapter.get_memory_reference_lines()
        personality_block = self.personality_adapter.get_personality_reference()

        safe_to_use = memory_result.safe_to_continue and personality_result.safe_to_continue

        return {
            "source": "MemoryPersonalityConversationAdapter",
            "adapter_mode": "reference_only",
            "safe_to_use": safe_to_use,
            "conversation_engine_modified": False,
            "auto_response_injection": False,
            "memory": {
                "available": memory_result.memory_reference_available,
                "reference_line_count": len(memory_lines),
                "memory_reference_lines": memory_lines,
            },
            "personality": {
                "available": personality_result.personality_reference_available,
                "name": personality_result.name,
                "user_name": personality_result.user_name,
                "primary_goal": personality_result.primary_goal,
                "base_tone": personality_result.base_tone,
                "mood": personality_result.mood,
                "core_rules": personality_result.core_rules,
                "sample_phrases": personality_result.sample_phrases,
                "reference_block": personality_block,
            },
            "instruction": (
                "ConversationEngineはこの統合参照ブロックを必要時だけ参照する。"
                "返答へ強制注入しない。"
                "ナビ子の自然な会話、目的維持、直近文脈の保持に必要な場合だけ使う。"
                "第一目標から外れる場合は、目的がぶれていることを明示して止める。"
            ),
        }

    def diagnose_adapter(self) -> MemoryPersonalityConversationAdapterResult:
        reference_block = self.build_reference_block()

        memory = reference_block.get("memory", {})
        personality = reference_block.get("personality", {})

        if not isinstance(memory, dict):
            memory = {}

        if not isinstance(personality, dict):
            personality = {}

        safe_to_use = bool(reference_block.get("safe_to_use", False))

        memory_reference_available = bool(memory.get("available", False))
        personality_reference_available = bool(personality.get("available", False))
        memory_reference_count = int(memory.get("reference_line_count", 0))

        adapter_ready = (
            safe_to_use
            and memory_reference_available
            and personality_reference_available
        )

        return MemoryPersonalityConversationAdapterResult(
            status="completed" if adapter_ready else "blocked",
            phase="Phase6-14 Memory + Personality Conversation Adapter",
            adapter_ready=adapter_ready,
            memory_reference_available=memory_reference_available,
            personality_reference_available=personality_reference_available,
            memory_reference_count=memory_reference_count,
            name=str(personality.get("name", "")),
            user_name=str(personality.get("user_name", "")),
            primary_goal=str(personality.get("primary_goal", "")),
            base_tone=str(personality.get("base_tone", "")),
            mood=str(personality.get("mood", "")),
            adapter_mode=str(reference_block.get("adapter_mode", "reference_only")),
            reference_block=reference_block,
            conversation_engine_modified=False,
            auto_response_injection=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=adapter_ready,
        )

    def get_conversation_reference(self) -> Dict[str, Any]:
        result = self.diagnose_adapter()

        if not result.safe_to_continue:
            return {}

        return result.reference_block

    def print_result(self, result: MemoryPersonalityConversationAdapterResult) -> None:
        print("=== Phase6-14 Memory + Personality Conversation Adapter ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"AdapterReady: {result.adapter_ready}")
        print(f"MemoryReferenceAvailable: {result.memory_reference_available}")
        print(f"PersonalityReferenceAvailable: {result.personality_reference_available}")
        print(f"MemoryReferenceCount: {result.memory_reference_count}")
        print(f"Name: {result.name}")
        print(f"UserName: {result.user_name}")
        print(f"PrimaryGoal: {result.primary_goal}")
        print(f"BaseTone: {result.base_tone}")
        print(f"Mood: {result.mood}")
        print(f"AdapterMode: {result.adapter_mode}")
        print(f"ConversationEngineModified: {result.conversation_engine_modified}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")

        print("")
        print("[Memory Reference Lines]")
        memory = result.reference_block.get("memory", {})
        if not isinstance(memory, dict):
            memory = {}

        lines = memory.get("memory_reference_lines", [])
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

    def to_dict(self, result: MemoryPersonalityConversationAdapterResult) -> Dict[str, Any]:
        return asdict(result)


def run_phase6_14_test() -> None:
    adapter = MemoryPersonalityConversationAdapter()
    result = adapter.diagnose_adapter()
    adapter.print_result(result)

    print("")
    print("[Integrated Reference Block Check]")
    block = adapter.get_conversation_reference()
    print(f"source: {block.get('source', '')}")
    print(f"adapter_mode: {block.get('adapter_mode', '')}")
    print(f"safe_to_use: {block.get('safe_to_use', False)}")

    memory = block.get("memory", {})
    personality = block.get("personality", {})

    if not isinstance(memory, dict):
        memory = {}

    if not isinstance(personality, dict):
        personality = {}

    print(f"memory_line_count: {memory.get('reference_line_count', 0)}")
    print(f"name: {personality.get('name', '')}")
    print(f"user_name: {personality.get('user_name', '')}")


if __name__ == "__main__":
    run_phase6_14_test()