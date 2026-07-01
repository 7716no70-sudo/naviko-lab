from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class LongTermMemoryIndexReadResult:
    status: str
    phase: str
    index_file_found: bool
    index_path: str
    index_type: str
    item_count: int
    items: List[Dict[str, Any]]
    memory_modified: bool
    auto_adoption: bool
    human_approval_required: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class LongTermMemoryIndexReader:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_dir = self.root_dir / "memory"
        self.index_path = self.memory_dir / "long_term_memory_index.json"

        self.memory_dir.mkdir(parents=True, exist_ok=True)

    def read_index(self) -> LongTermMemoryIndexReadResult:
        index_file_found = self.index_path.exists()
        data = self._read_json(self.index_path)

        raw_items = data.get("items", [])
        if not isinstance(raw_items, list):
            raw_items = []

        safe_items = [
            item for item in raw_items
            if isinstance(item, dict)
        ]

        return LongTermMemoryIndexReadResult(
            status="completed" if index_file_found else "blocked",
            phase="Phase7-3 Long-Term Memory Index Reader",
            index_file_found=index_file_found,
            index_path=str(self.index_path),
            index_type=str(data.get("index_type", "")),
            item_count=len(safe_items),
            items=safe_items,
            memory_modified=False,
            auto_adoption=False,
            human_approval_required=True,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=index_file_found,
        )

    def print_result(self, result: LongTermMemoryIndexReadResult) -> None:
        print("=== Phase7-3 Long-Term Memory Index Reader ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"IndexFileFound: {result.index_file_found}")
        print(f"IndexPath: {result.index_path}")
        print(f"IndexType: {result.index_type}")
        print(f"ItemCount: {result.item_count}")
        print(f"MemoryModified: {result.memory_modified}")
        print(f"AutoAdoption: {result.auto_adoption}")
        print(f"HumanApprovalRequired: {result.human_approval_required}")

        print("")
        print("[Index Items]")
        if not result.items:
            print("- 索引なし")
        else:
            for index, item in enumerate(result.items, start=1):
                print(f"- Index {index}")
                print(f"  memory_id: {item.get('memory_id', '')}")
                print(f"  text: {item.get('text', '')}")
                print(f"  importance: {item.get('importance', '')}")
                print(f"  score: {item.get('score', 0)}")
                print(f"  priority: {item.get('priority', 0)}")
                print(f"  keywords: {item.get('keywords', [])}")
                print(f"  safe_adopted: {item.get('safe_adopted', False)}")

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: LongTermMemoryIndexReadResult) -> Dict[str, Any]:
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


def run_phase7_3_test() -> None:
    reader = LongTermMemoryIndexReader()
    result = reader.read_index()
    reader.print_result(result)


if __name__ == "__main__":
    run_phase7_3_test()