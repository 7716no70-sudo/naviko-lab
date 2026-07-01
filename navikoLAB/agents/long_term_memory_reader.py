from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class LongTermMemoryItem:
    id: str
    created_at: str
    text: str
    importance: str
    score: int
    reason: str
    source: str
    memory_type: str
    safe_adopted: bool


@dataclass
class LongTermMemoryReadResult:
    status: str
    phase: str
    memory_file_found: bool
    memory_count: int
    memories: List[Dict[str, Any]]
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class LongTermMemoryReader:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_dir = self.root_dir / "memory"
        self.long_term_memory_path = self.memory_dir / "long_term_memory.json"

        self.memory_dir.mkdir(parents=True, exist_ok=True)

    def read_long_term_memory(self) -> LongTermMemoryReadResult:
        memory_file_found = self.long_term_memory_path.exists()
        data = self._read_json(self.long_term_memory_path)

        raw_memories = data.get("memories", [])
        memories: List[LongTermMemoryItem] = []

        if isinstance(raw_memories, list):
            for item in raw_memories:
                if not isinstance(item, dict):
                    continue

                memories.append(
                    LongTermMemoryItem(
                        id=str(item.get("id", "")),
                        created_at=str(item.get("created_at", "")),
                        text=str(item.get("text", "")),
                        importance=str(item.get("importance", "")),
                        score=int(item.get("score", 0)),
                        reason=str(item.get("reason", "")),
                        source=str(item.get("source", "")),
                        memory_type=str(item.get("memory_type", "")),
                        safe_adopted=bool(item.get("safe_adopted", False)),
                    )
                )

        return LongTermMemoryReadResult(
            status="completed",
            phase="Phase4-14 Long Term Memory Reader",
            memory_file_found=memory_file_found,
            memory_count=len(memories),
            memories=[asdict(item) for item in memories],
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=True,
        )

    def print_result(self, result: LongTermMemoryReadResult) -> None:
        print("=== Phase4-14 Long Term Memory Reader ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"MemoryFileFound: {result.memory_file_found}")
        print(f"MemoryCount: {result.memory_count}")

        print("")
        print("[Long Term Memories]")

        if not result.memories:
            print("- 長期記憶なし")
        else:
            for index, item in enumerate(result.memories, start=1):
                print(f"- Memory {index}")
                print(f"  id: {item.get('id', '')}")
                print(f"  text: {item.get('text', '')}")
                print(f"  importance: {item.get('importance', '')}")
                print(f"  score: {item.get('score', 0)}")
                print(f"  reason: {item.get('reason', '')}")
                print(f"  source: {item.get('source', '')}")
                print(f"  memory_type: {item.get('memory_type', '')}")
                print(f"  safe_adopted: {item.get('safe_adopted', False)}")

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

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


def run_phase4_14_test() -> None:
    reader = LongTermMemoryReader()
    result = reader.read_long_term_memory()
    reader.print_result(result)


if __name__ == "__main__":
    run_phase4_14_test()