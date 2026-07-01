from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class MemoryContextReadResult:
    status: str
    phase: str
    context_file_found: bool
    context_path: str
    short_memory_count: int
    mid_memory_count: int
    long_term_memory_count: int
    context_summary: Dict[str, Any]
    auto_response_injection: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class MemoryContextReader:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_dir = self.root_dir / "memory"
        self.context_dir = self.memory_dir / "contexts"
        self.latest_context_path = self.context_dir / "latest_memory_context.json"

        self.context_dir.mkdir(parents=True, exist_ok=True)

    def read_latest_context(self) -> MemoryContextReadResult:
        context_file_found = self.latest_context_path.exists()
        data = self._read_json(self.latest_context_path)

        memory_context = data.get("memory_context", {})
        if not isinstance(memory_context, dict):
            memory_context = {}

        short_memory = memory_context.get("short_memory", {})
        mid_memory = memory_context.get("mid_memory", {})
        long_term_memory = memory_context.get("long_term_memory", {})

        if not isinstance(short_memory, dict):
            short_memory = {}

        if not isinstance(mid_memory, dict):
            mid_memory = {}

        if not isinstance(long_term_memory, dict):
            long_term_memory = {}

        short_items = short_memory.get("items", [])
        mid_items = mid_memory.get("items", [])
        long_items = long_term_memory.get("items", [])

        if not isinstance(short_items, list):
            short_items = []

        if not isinstance(mid_items, list):
            mid_items = []

        if not isinstance(long_items, list):
            long_items = []

        context_summary = {
            "created_at": data.get("created_at", ""),
            "purpose": data.get("purpose", ""),
            "short_memory_preview": self._preview_items(short_items),
            "mid_memory_preview": self._preview_items(mid_items),
            "long_term_memory_preview": self._preview_items(long_items),
        }

        return MemoryContextReadResult(
            status="completed" if context_file_found else "blocked",
            phase="Phase5-8 Memory Context Reader",
            context_file_found=context_file_found,
            context_path=str(self.latest_context_path),
            short_memory_count=len(short_items),
            mid_memory_count=len(mid_items),
            long_term_memory_count=len(long_items),
            context_summary=context_summary,
            auto_response_injection=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=context_file_found,
        )

    def print_result(self, result: MemoryContextReadResult) -> None:
        print("=== Phase5-8 Memory Context Reader ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"ContextFileFound: {result.context_file_found}")
        print(f"ContextPath: {result.context_path}")
        print(f"ShortMemoryCount: {result.short_memory_count}")
        print(f"MidMemoryCount: {result.mid_memory_count}")
        print(f"LongTermMemoryCount: {result.long_term_memory_count}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")

        print("")
        print("[Context Summary]")
        print(f"created_at: {result.context_summary.get('created_at', '')}")
        print(f"purpose: {result.context_summary.get('purpose', '')}")

        print("")
        print("[Short Memory Preview]")
        self._print_preview(result.context_summary.get("short_memory_preview", []))

        print("")
        print("[Mid Memory Preview]")
        self._print_preview(result.context_summary.get("mid_memory_preview", []))

        print("")
        print("[Long Term Memory Preview]")
        self._print_preview(result.context_summary.get("long_term_memory_preview", []))

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: MemoryContextReadResult) -> Dict[str, Any]:
        return asdict(result)

    def _preview_items(self, items: List[Dict[str, Any]], limit: int = 3) -> List[Dict[str, Any]]:
        preview: List[Dict[str, Any]] = []

        for item in items[:limit]:
            if not isinstance(item, dict):
                continue

            preview.append(
                {
                    "id": item.get("id", ""),
                    "text": item.get("text", ""),
                    "speaker": item.get("speaker", ""),
                    "importance": item.get("importance", ""),
                    "score": item.get("score", 0),
                    "source": item.get("source", ""),
                }
            )

        return preview

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

    def _read_json(self, path: Path) -> Dict[str, Any]:
        try:
            with path.open("r", encoding="utf-8") as f:
                loaded = json.load(f)

            if isinstance(loaded, dict):
                return loaded

            return {}

        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}


def run_phase5_8_test() -> None:
    reader = MemoryContextReader()
    result = reader.read_latest_context()
    reader.print_result(result)


if __name__ == "__main__":
    run_phase5_8_test()