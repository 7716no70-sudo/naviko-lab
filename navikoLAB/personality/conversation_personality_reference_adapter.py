from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.personality.conversation_personality_bridge import ConversationPersonalityBridge


@dataclass
class ConversationPersonalityReferenceAdapterResult:
    status: str
    phase: str
    adapter_ready: bool
    personality_reference_available: bool
    name: str
    user_name: str
    primary_goal: str
    base_tone: str
    mood: str
    core_rules: List[str]
    sample_phrases: List[str]
    reference_block: Dict[str, Any]
    adapter_mode: str
    auto_response_injection: bool
    conversation_engine_modified: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class ConversationPersonalityReferenceAdapter:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.bridge = ConversationPersonalityBridge(root_dir=root_dir)

    def build_reference_block(self) -> Dict[str, Any]:
        bridge_block = self.bridge.build_personality_reference_block()

        core_rules = bridge_block.get("core_rules", [])
        if not isinstance(core_rules, list):
            core_rules = []

        sample_phrases = bridge_block.get("sample_phrases", [])
        if not isinstance(sample_phrases, list):
            sample_phrases = []

        return {
            "source": "ConversationPersonalityReferenceAdapter",
            "adapter_mode": "reference_only",
            "safe_to_use": bool(bridge_block.get("safe_to_use", False)),
            "auto_response_injection": False,
            "conversation_engine_modified": False,
            "name": str(bridge_block.get("name", "ナビ子")),
            "user_name": str(bridge_block.get("user_name", "ナオさん")),
            "primary_goal": str(bridge_block.get("primary_goal", "")),
            "base_tone": str(bridge_block.get("base_tone", "")),
            "mood": str(bridge_block.get("mood", "")),
            "core_rules": [str(rule) for rule in core_rules],
            "sample_phrases": [str(phrase) for phrase in sample_phrases],
            "instruction": (
                "ConversationEngineはこの人格参照ブロックを必要時だけ参照する。"
                "返答へ強制注入しない。"
                "ナビ子らしい自然な会話と第一目標維持に必要な場合だけ使う。"
            ),
        }

    def diagnose_adapter(self) -> ConversationPersonalityReferenceAdapterResult:
        reference_block = self.build_reference_block()

        safe_to_use = bool(reference_block.get("safe_to_use", False))
        name = str(reference_block.get("name", ""))
        user_name = str(reference_block.get("user_name", ""))
        primary_goal = str(reference_block.get("primary_goal", ""))
        base_tone = str(reference_block.get("base_tone", ""))
        mood = str(reference_block.get("mood", ""))

        core_rules = reference_block.get("core_rules", [])
        if not isinstance(core_rules, list):
            core_rules = []

        sample_phrases = reference_block.get("sample_phrases", [])
        if not isinstance(sample_phrases, list):
            sample_phrases = []

        personality_reference_available = (
            safe_to_use
            and bool(name)
            and bool(user_name)
            and bool(primary_goal)
            and bool(base_tone)
            and bool(mood)
        )

        return ConversationPersonalityReferenceAdapterResult(
            status="completed" if personality_reference_available else "blocked",
            phase="Phase6-12 ConversationEngine Personality Reference Adapter",
            adapter_ready=personality_reference_available,
            personality_reference_available=personality_reference_available,
            name=name,
            user_name=user_name,
            primary_goal=primary_goal,
            base_tone=base_tone,
            mood=mood,
            core_rules=[str(rule) for rule in core_rules],
            sample_phrases=[str(phrase) for phrase in sample_phrases],
            reference_block=reference_block,
            adapter_mode=str(reference_block.get("adapter_mode", "reference_only")),
            auto_response_injection=False,
            conversation_engine_modified=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=personality_reference_available,
        )

    def get_personality_reference(self) -> Dict[str, Any]:
        result = self.diagnose_adapter()

        if not result.safe_to_continue:
            return {}

        return result.reference_block

    def print_result(self, result: ConversationPersonalityReferenceAdapterResult) -> None:
        print("=== Phase6-12 ConversationEngine Personality Reference Adapter ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"AdapterReady: {result.adapter_ready}")
        print(f"PersonalityReferenceAvailable: {result.personality_reference_available}")
        print(f"Name: {result.name}")
        print(f"UserName: {result.user_name}")
        print(f"PrimaryGoal: {result.primary_goal}")
        print(f"BaseTone: {result.base_tone}")
        print(f"Mood: {result.mood}")
        print(f"AdapterMode: {result.adapter_mode}")
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
        print("[Adapter Instruction]")
        print(result.reference_block.get("instruction", ""))

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: ConversationPersonalityReferenceAdapterResult) -> Dict[str, Any]:
        return asdict(result)


def run_phase6_12_test() -> None:
    adapter = ConversationPersonalityReferenceAdapter()
    result = adapter.diagnose_adapter()
    adapter.print_result(result)


if __name__ == "__main__":
    run_phase6_12_test()