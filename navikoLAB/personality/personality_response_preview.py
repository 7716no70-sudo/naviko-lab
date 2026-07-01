from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.personality.personality_context_reader import PersonalityContextReader


@dataclass
class PersonalityResponsePreviewResult:
    status: str
    phase: str
    user_input: str
    context_available: bool
    name: str
    user_name: str
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


class PersonalityResponsePreview:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.context_reader = PersonalityContextReader(root_dir=root_dir)

    def build_preview(self, user_input: str) -> PersonalityResponsePreviewResult:
        context = self.context_reader.read_latest_context()

        preview_response = self._build_response(
            user_input=user_input,
            user_name=context.user_name,
            primary_goal=context.primary_goal,
            base_tone=context.base_tone,
            mood=context.mood,
            core_rules=context.core_rules,
        )

        return PersonalityResponsePreviewResult(
            status="completed" if context.safe_to_continue else "blocked",
            phase="Phase6-7 Personality Response Preview",
            user_input=user_input,
            context_available=context.context_file_found,
            name=context.name,
            user_name=context.user_name,
            base_tone=context.base_tone,
            mood=context.mood,
            preview_response=preview_response,
            preview_only=True,
            conversation_engine_modified=False,
            auto_response_injection=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=context.safe_to_continue,
        )

    def _build_response(
        self,
        user_input: str,
        user_name: str,
        primary_goal: str,
        base_tone: str,
        mood: str,
        core_rules: List[str],
    ) -> str:
        safe_user_name = user_name if user_name else "ナオさん"
        safe_goal = primary_goal if primary_goal else "ナビ子が自然に会話できるAIになること"

        goal_rule_found = any("目的" in rule or "第一目標" in rule for rule in core_rules)

        lines: List[str] = []
        lines.append(f"{safe_user_name}、確認しました。")

        if mood == "calm":
            lines.append("落ち着いて、今の流れを大切にしながら進めます。")
        else:
            lines.append("今の状態を確認しながら、無理なく進めます。")

        lines.append(f"私の第一目標は「{safe_goal}」です。")

        if goal_rule_found:
            lines.append("目的がぶれないように、必要な工程だけを1つずつ進めます。")

        lines.append(f"今回の入力「{user_input}」にも、{base_tone}口調で返答する形にできます。")

        return "\n".join(lines)

    def print_result(self, result: PersonalityResponsePreviewResult) -> None:
        print("=== Phase6-7 Personality Response Preview ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"UserInput: {result.user_input}")
        print(f"ContextAvailable: {result.context_available}")
        print(f"Name: {result.name}")
        print(f"UserName: {result.user_name}")
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

    def to_dict(self, result: PersonalityResponsePreviewResult) -> Dict[str, Any]:
        return asdict(result)


def run_phase6_7_test() -> None:
    preview = PersonalityResponsePreview()

    result = preview.build_preview(
        user_input="ナビ子、今の目的を忘れずに進めよう"
    )

    preview.print_result(result)


if __name__ == "__main__":
    run_phase6_7_test()