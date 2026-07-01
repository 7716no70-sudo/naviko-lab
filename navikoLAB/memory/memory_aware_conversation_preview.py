from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.memory.conversation_memory_bridge import ConversationMemoryBridge


@dataclass
class MemoryAwareConversationPreviewResult:
    status: str
    phase: str
    user_input: str
    memory_reference_count: int
    memory_references: List[str]
    preview_response: str
    preview_only: bool
    conversation_engine_modified: bool
    auto_response_injection: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class MemoryAwareConversationPreview:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.bridge = ConversationMemoryBridge(root_dir=root_dir)

    def build_preview(self, user_input: str) -> MemoryAwareConversationPreviewResult:
        reference_block = self.bridge.build_conversation_reference_block()

        memory_lines = reference_block.get("memory_reference_lines", [])
        if not isinstance(memory_lines, list):
            memory_lines = []

        safe_memory_lines = [str(line) for line in memory_lines]

        preview_response = self._build_safe_preview_response(
            user_input=user_input,
            memory_lines=safe_memory_lines,
        )

        safe_to_use = bool(reference_block.get("safe_to_use", False))

        return MemoryAwareConversationPreviewResult(
            status="completed" if safe_to_use else "blocked",
            phase="Phase5-14 Memory-Aware Conversation Preview",
            user_input=user_input,
            memory_reference_count=len(safe_memory_lines),
            memory_references=safe_memory_lines,
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

    def _build_safe_preview_response(self, user_input: str, memory_lines: List[str]) -> str:
        long_term_focus = ""
        mid_focus = ""
        short_focus = ""

        for line in memory_lines:
            if line.startswith("長期記憶:") and not long_term_focus:
                long_term_focus = line.replace("長期記憶:", "", 1).strip()
            elif line.startswith("中期記憶:") and not mid_focus:
                mid_focus = line.replace("中期記憶:", "", 1).strip()
            elif line.startswith("短期記憶:") and not short_focus:
                short_focus = line.replace("短期記憶:", "", 1).strip()

        response_parts: List[str] = []

        response_parts.append("ナオさん、確認しました。")

        if long_term_focus:
            response_parts.append(
                f"私は「{long_term_focus}」を大事な方針として覚えています。"
            )

        if mid_focus:
            response_parts.append(
                f"今は「{mid_focus}」という流れで進めています。"
            )

        if short_focus:
            response_parts.append(
                f"直近では、{short_focus}ことも参照できます。"
            )

        response_parts.append(
            f"今回の入力「{user_input}」に対しても、目的をぶらさず、ナビ子が自然に会話できるようになる方向で返答します。"
        )

        return "\n".join(response_parts)

    def print_result(self, result: MemoryAwareConversationPreviewResult) -> None:
        print("=== Phase5-14 Memory-Aware Conversation Preview ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"UserInput: {result.user_input}")
        print(f"MemoryReferenceCount: {result.memory_reference_count}")
        print(f"PreviewOnly: {result.preview_only}")
        print(f"ConversationEngineModified: {result.conversation_engine_modified}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")

        print("")
        print("[Memory References]")
        if not result.memory_references:
            print("- なし")
        else:
            for index, line in enumerate(result.memory_references, start=1):
                print(f"- {index}: {line}")

        print("")
        print("[Preview Response]")
        print(result.preview_response)

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: MemoryAwareConversationPreviewResult) -> Dict[str, Any]:
        return asdict(result)


def run_phase5_14_test() -> None:
    preview = MemoryAwareConversationPreview()

    result = preview.build_preview(
        user_input="ナビ子、今の目標を覚えてる？"
    )

    preview.print_result(result)


if __name__ == "__main__":
    run_phase5_14_test()