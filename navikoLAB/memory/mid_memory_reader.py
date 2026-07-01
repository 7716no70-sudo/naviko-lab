from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class MidMemoryReadResult:
    status: str
    phase: str
    mid_memory_file_found: bool
    memory_count: int
    memories: List[Dict[str, Any]]
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    auto_response_injection: bool
    safe_to_continue: bool


class MidMemoryReader:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_dir = self.root_dir / "memory"
        self.mid_memory_path = self.memory_dir / "mid_memory.json"

        self.memory_dir.mkdir(parents=True, exist_ok=True)

    def read(self) -> MidMemoryReadResult:
        file_found = self.mid_memory_path.exists()
        data = self._read_json(self.mid_memory_path)

        raw_memories = data.get("memories", [])
        memories: List[Dict[str, Any]] = []

        if isinstance(raw_memories, list):
            memories = [
                item for item in raw_memories
                if isinstance(item, dict)
            ]

        return MidMemoryReadResult(
            status="completed",
            phase="Phase5-6 Mid Memory Reader",
            mid_memory_file_found=file_found,
            memory_count=len(memories),
            memories=memories,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            auto_response_injection=False,
            safe_to_continue=True,
        )

    def print_result(self, result: MidMemoryReadResult) -> None:
        print("=== Phase5-6 Mid Memory Reader ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"MidMemoryFileFound: {result.mid_memory_file_found}")
        print(f"MemoryCount: {result.memory_count}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")

        print("")
        print("[Mid Memories]")

        if not result.memories:
            print("- 中期記憶なし")
        else:
            for index, item in enumerate(result.memories, start=1):
                print(f"- MidMemory {index}")
                print(f"  id: {item.get('id', '')}")
                print(f"  text: {item.get('text', '')}")
                print(f"  source: {item.get('source', '')}")
                print(f"  importance: {item.get('importance', '')}")
                print(f"  score: {item.get('score', 0)}")
                print(f"  reason: {item.get('reason', '')}")

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: MidMemoryReadResult) -> Dict[str, Any]:
        return asdict(result)

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


def run_phase5_6_test() -> None:
    reader = MidMemoryReader()
    result = reader.read()
    reader.print_result(result)


if __name__ == "__main__":
    run_phase5_6_test()