from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.memory.memory_context_connector import MemoryContextConnector


@dataclass
class MemoryContextInjectionPreviewResult:
    status: str
    phase: str
    context_available: bool
    preview_created: bool
    short_memory_count: int
    mid_memory_count: int
    long_term_memory_count: int
    injection_preview: List[str]
    auto_response_injection: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class MemoryContextInjectionPreview:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.connector = MemoryContextConnector(root_dir=root_dir)

    def build_preview(self) -> MemoryContextInjectionPreviewResult:
        connection = self.connector.connect()
        context = connection.referenced_context

        preview_lines: List[str] = []

        short_items = context.get("short_memory_preview", [])
        mid_items = context.get("mid_memory_preview", [])
        long_items = context.get("long_term_memory_preview", [])

        if isinstance(long_items, list):
            for item in long_items:
                if isinstance(item, dict):
                    text = str(item.get("text", "")).strip()
                    if text:
                        preview_lines.append(f"長期記憶: {text}")

        if isinstance(mid_items, list):
            for item in mid_items:
                if isinstance(item, dict):
                    text = str(item.get("text", "")).strip()
                    if text:
                        preview_lines.append(f"中期記憶: {text}")

        if isinstance(short_items, list):
            for item in short_items:
                if isinstance(item, dict):
                    speaker = str(item.get("speaker", "")).strip()
                    text = str(item.get("text", "")).strip()
                    if text:
                        if speaker:
                            preview_lines.append(f"短期記憶: {speaker} は「{text}」と言った")
                        else:
                            preview_lines.append(f"短期記憶: {text}")

        return MemoryContextInjectionPreviewResult(
            status="completed" if connection.context_file_found else "blocked",
            phase="Phase5-10 Memory Context Injection Preview",
            context_available=connection.context_file_found,
            preview_created=bool(preview_lines),
            short_memory_count=connection.short_memory_count,
            mid_memory_count=connection.mid_memory_count,
            long_term_memory_count=connection.long_term_memory_count,
            injection_preview=preview_lines,
            auto_response_injection=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=connection.safe_to_continue,
        )

    def print_result(self, result: MemoryContextInjectionPreviewResult) -> None:
        print("=== Phase5-10 Memory Context Injection Preview ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"ContextAvailable: {result.context_available}")
        print(f"PreviewCreated: {result.preview_created}")
        print(f"ShortMemoryCount: {result.short_memory_count}")
        print(f"MidMemoryCount: {result.mid_memory_count}")
        print(f"LongTermMemoryCount: {result.long_term_memory_count}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")

        print("")
        print("[Injection Preview]")
        if not result.injection_preview:
            print("- プレビューなし")
        else:
            for index, line in enumerate(result.injection_preview, start=1):
                print(f"- {index}: {line}")

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: MemoryContextInjectionPreviewResult) -> Dict[str, Any]:
        return asdict(result)


def run_phase5_10_test() -> None:
    preview = MemoryContextInjectionPreview()
    result = preview.build_preview()
    preview.print_result(result)


if __name__ == "__main__":
    run_phase5_10_test()