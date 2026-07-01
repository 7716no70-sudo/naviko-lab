from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.memory.short_memory_reader import ShortMemoryReader
from navikoLAB.memory.mid_memory_reader import MidMemoryReader
from navikoLAB.agents.long_term_memory_reader import LongTermMemoryReader


@dataclass
class MemoryContextBuildResult:
    status: str
    phase: str
    short_memory_count: int
    mid_memory_count: int
    long_term_memory_count: int
    context_path: str
    context_created: bool
    auto_response_injection: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class MemoryContextBuilder:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_dir = self.root_dir / "memory"
        self.context_dir = self.memory_dir / "contexts"

        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.context_dir.mkdir(parents=True, exist_ok=True)

        self.short_reader = ShortMemoryReader(root_dir=root_dir)
        self.mid_reader = MidMemoryReader(root_dir=root_dir)
        self.long_reader = LongTermMemoryReader(root_dir=root_dir)

    def build_context(self) -> MemoryContextBuildResult:
        short_result = self.short_reader.read()
        mid_result = self.mid_reader.read()
        long_result = self.long_reader.read_long_term_memory()

        context_data = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "phase": "Phase5-7 Memory Context Builder",
            "purpose": "ナビ子が自然な会話を行うための記憶参照コンテキスト",
            "auto_response_injection": False,
            "safe_mode": True,
            "external_ai": False,
            "real_pc_operation": False,
            "file_delete": False,
            "memory_context": {
                "short_memory": {
                    "count": short_result.memory_count,
                    "items": short_result.memories,
                },
                "mid_memory": {
                    "count": mid_result.memory_count,
                    "items": mid_result.memories,
                },
                "long_term_memory": {
                    "count": long_result.memory_count,
                    "items": long_result.memories,
                },
            },
        }

        context_path = self._save_context(context_data)

        return MemoryContextBuildResult(
            status="completed",
            phase="Phase5-7 Memory Context Builder",
            short_memory_count=short_result.memory_count,
            mid_memory_count=mid_result.memory_count,
            long_term_memory_count=long_result.memory_count,
            context_path=str(context_path),
            context_created=True,
            auto_response_injection=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=True,
        )

    def _save_context(self, context_data: Dict[str, Any]) -> Path:
        filename = f"memory_context_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = self.context_dir / filename

        with path.open("w", encoding="utf-8") as f:
            json.dump(context_data, f, ensure_ascii=False, indent=2)

        latest_path = self.context_dir / "latest_memory_context.json"
        with latest_path.open("w", encoding="utf-8") as f:
            json.dump(context_data, f, ensure_ascii=False, indent=2)

        return path

    def print_result(self, result: MemoryContextBuildResult) -> None:
        print("=== Phase5-7 Memory Context Builder ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"ShortMemoryCount: {result.short_memory_count}")
        print(f"MidMemoryCount: {result.mid_memory_count}")
        print(f"LongTermMemoryCount: {result.long_term_memory_count}")
        print(f"ContextCreated: {result.context_created}")
        print(f"ContextPath: {result.context_path}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: MemoryContextBuildResult) -> Dict[str, Any]:
        return asdict(result)


def run_phase5_7_test() -> None:
    builder = MemoryContextBuilder()
    result = builder.build_context()
    builder.print_result(result)


if __name__ == "__main__":
    run_phase5_7_test()