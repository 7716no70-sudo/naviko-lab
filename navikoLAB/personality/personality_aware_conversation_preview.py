from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.personality.conversation_personality_bridge import ConversationPersonalityBridge


@dataclass
class PersonalityAwareConversationPreviewResult:
    status: str
    phase: str
    user_input: str
    personality_reference_available: bool
    name: str
    user_name: str
    base_tone: str
    mood: str
    primary_goal: str
    preview_response: str
    preview_only: bool
    conversation_engine_modified: bool
    auto_response_injection: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class PersonalityAwareConversationPreview:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.bridge = ConversationPersonalityBridge(root_dir=root_dir)

    def build_preview(self, user_input: str) -> PersonalityAwareConversationPreviewResult:
        reference = self.bridge.get_personality_reference_for_conversation()

        safe_to_use = bool(reference.get("safe_to_use", False))

        name = str(reference.get("name", "ナビ子"))
        user_name = str(reference.get("user_name", "ナオさん"))
        base_tone = str(reference.get("base_tone", "やさしく、落ち着いて、少し親しみやすい"))
        mood = str(reference.get("mood", "calm"))
        primary_goal = str(reference.get("primary_goal", "自然に会話できるデスクトップAIになること"))

        preview_response = self._build_preview_response(
            user_input=user_input,
            name=name,
            user_name=user_name,
            base_tone=base_tone,
            mood=mood,
            primary_goal=primary_goal,
            core_rules=reference.get("core_rules", []),
        )

        return PersonalityAwareConversationPreviewResult(
            status="completed" if safe_to_use else "blocked",
            phase="Phase6-11 Personality-Aware Conversation Preview",
            user_input=user_input,
            personality_reference_available=safe_to_use,
            name=name,
            user_name=user_name,
            base_tone=base_tone,
            mood=mood,
            primary_goal=primary_goal,
            preview_response=preview_response,
            preview_only=True,
            conversation_engine_modified=False,
            auto_response_injection=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=safe_to_use,
        )

    def _build_preview_response(
        self,
        user_input: str,
        name: str,
        user_name: str,
        base_tone: str,
        mood: str,
        primary_goal: str,
        core_rules: Any,
    ) -> str:
        rules: List[str] = []
        if isinstance(core_rules, list):
            rules = [str(rule) for rule in core_rules]

        should_guard_goal = any(
            "目的" in rule or "第一目標" in rule or "先走らない" in rule
            for rule in rules
        )

        lines: List[str] = []

        lines.append(f"{user_name}、確認しました。")

        if mood == "calm":
            lines.append("落ち着いて、今の流れを大切にしながら進めます。")
        else:
            lines.append("今の状態を見ながら、無理なく進めます。")

        lines.append(f"私は{name}として、まず「{primary_goal}」を大事にします。")

        if should_guard_goal:
            lines.append("目的がぶれそうな内容は、先に止めて確認します。")

        lines.append(f"今回の入力「{user_input}」には、{base_tone}口調で自然に返答する形を維持します。")

        return "\n".join(lines)

    def print_result(self, result: PersonalityAwareConversationPreviewResult) -> None:
        print("=== Phase6-11 Personality-Aware Conversation Preview ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"UserInput: {result.user_input}")
        print(f"PersonalityReferenceAvailable: {result.personality_reference_available}")
        print(f"Name: {result.name}")
        print(f"UserName: {result.user_name}")
        print(f"BaseTone: {result.base_tone}")
        print(f"Mood: {result.mood}")
        print(f"PrimaryGoal: {result.primary_goal}")
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

    def to_dict(self, result: PersonalityAwareConversationPreviewResult) -> Dict[str, Any]:
        return asdict(result)


def run_phase6_11_test() -> None:
    preview = PersonalityAwareConversationPreview()

    result = preview.build_preview(
        user_input="ナビ子、これからも自然に話せるようにしていこう"
    )

    preview.print_result(result)


if __name__ == "__main__":
    run_phase6_11_test()