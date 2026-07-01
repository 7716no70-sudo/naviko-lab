from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.memory.conversation_memory_reference_adapter import ConversationMemoryReferenceAdapter
from navikoLAB.personality.conversation_personality_reference_adapter import ConversationPersonalityReferenceAdapter


@dataclass
class MemoryPersonalityConversationPreviewResult:
    status: str
    phase: str
    user_input: str
    memory_reference_available: bool
    personality_reference_available: bool
    memory_reference_count: int
    name: str
    user_name: str
    primary_goal: str
    base_tone: str
    mood: str
    preview_response: str
    preview_only: bool
    conversation_engine_modified: bool
    auto_response_injection: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class MemoryPersonalityConversationPreview:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_adapter = ConversationMemoryReferenceAdapter(root_dir=root_dir)
        self.personality_adapter = ConversationPersonalityReferenceAdapter(root_dir=root_dir)

    def build_preview(self, user_input: str) -> MemoryPersonalityConversationPreviewResult:
        memory_result = self.memory_adapter.diagnose_adapter()
        personality_result = self.personality_adapter.diagnose_adapter()

        memory_lines = memory_result.get_memory_reference_lines() if hasattr(memory_result, "get_memory_reference_lines") else []
        if not memory_lines:
            memory_lines = self.memory_adapter.get_memory_reference_lines()

        preview_response = self._build_preview_response(
            user_input=user_input,
            memory_lines=memory_lines,
            name=personality_result.name,
            user_name=personality_result.user_name,
            primary_goal=personality_result.primary_goal,
            base_tone=personality_result.base_tone,
            mood=personality_result.mood,
            core_rules=personality_result.core_rules,
        )

        ready = memory_result.safe_to_continue and personality_result.safe_to_continue

        return MemoryPersonalityConversationPreviewResult(
            status="completed" if ready else "blocked",
            phase="Phase6-13 Memory + Personality Conversation Preview",
            user_input=user_input,
            memory_reference_available=memory_result.memory_reference_available,
            personality_reference_available=personality_result.personality_reference_available,
            memory_reference_count=len(memory_lines),
            name=personality_result.name,
            user_name=personality_result.user_name,
            primary_goal=personality_result.primary_goal,
            base_tone=personality_result.base_tone,
            mood=personality_result.mood,
            preview_response=preview_response,
            preview_only=True,
            conversation_engine_modified=False,
            auto_response_injection=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=ready,
        )

    def _build_preview_response(
        self,
        user_input: str,
        memory_lines: List[str],
        name: str,
        user_name: str,
        primary_goal: str,
        base_tone: str,
        mood: str,
        core_rules: List[str],
    ) -> str:
        long_term_memory = ""
        mid_memory = ""
        short_memory = ""

        for line in memory_lines:
            if line.startswith("長期記憶:") and not long_term_memory:
                long_term_memory = line.replace("長期記憶:", "", 1).strip()
            elif line.startswith("中期記憶:") and not mid_memory:
                mid_memory = line.replace("中期記憶:", "", 1).strip()
            elif line.startswith("短期記憶:") and not short_memory:
                short_memory = line.replace("短期記憶:", "", 1).strip()

        should_guard_goal = any(
            "目的" in rule or "第一目標" in rule or "先走らない" in rule
            for rule in core_rules
        )

        safe_name = name if name else "ナビ子"
        safe_user_name = user_name if user_name else "ナオさん"
        safe_goal = primary_goal if primary_goal else "自然に会話できるデスクトップAIになること"
        safe_tone = base_tone if base_tone else "やさしく、落ち着いて、少し親しみやすい"

        lines: List[str] = []

        lines.append(f"{safe_user_name}、確認しました。")

        if mood == "calm":
            lines.append("落ち着いて、今の流れを大切にしながら返答します。")
        else:
            lines.append("今の状態を確認しながら、無理なく返答します。")

        lines.append(f"私は{safe_name}として、まず「{safe_goal}」を第一目標にします。")

        if long_term_memory:
            lines.append(f"長期記憶として「{long_term_memory}」を参照できます。")

        if mid_memory:
            lines.append(f"今の流れとして「{mid_memory}」も覚えています。")

        if short_memory:
            lines.append(f"直近の会話として、{short_memory}ことも参照できます。")

        if should_guard_goal:
            lines.append("目的がぶれそうな内容は、先に止めて確認します。")

        lines.append(f"今回の入力「{user_input}」には、{safe_tone}口調で自然に返答する形を維持します。")

        return "\n".join(lines)

    def print_result(self, result: MemoryPersonalityConversationPreviewResult) -> None:
        print("=== Phase6-13 Memory + Personality Conversation Preview ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"UserInput: {result.user_input}")
        print(f"MemoryReferenceAvailable: {result.memory_reference_available}")
        print(f"PersonalityReferenceAvailable: {result.personality_reference_available}")
        print(f"MemoryReferenceCount: {result.memory_reference_count}")
        print(f"Name: {result.name}")
        print(f"UserName: {result.user_name}")
        print(f"PrimaryGoal: {result.primary_goal}")
        print(f"BaseTone: {result.base_tone}")
        print(f"Mood: {result.mood}")
        print(f"PreviewOnly: {result.preview_only}")
        print(f"ConversationEngineModified: {result.conversation_engine_modified}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")

        print("")
        print("[Preview Response]")
        print(result.preview_response)

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: MemoryPersonalityConversationPreviewResult) -> Dict[str, Any]:
        return asdict(result)


def run_phase6_13_test() -> None:
    preview = MemoryPersonalityConversationPreview()

    result = preview.build_preview(
        user_input="ナビ子、今の記憶と人格を使って自然に返事できる？"
    )

    preview.print_result(result)


if __name__ == "__main__":
    run_phase6_13_test()