from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class LongTermMemoryIndexItem:
    memory_id: str
    text: str
    importance: str
    score: int
    source: str
    memory_type: str
    keywords: List[str]
    priority: int
    safe_adopted: bool


@dataclass
class LongTermMemoryIndexBuildResult:
    status: str
    phase: str
    long_term_memory_found: bool
    memory_count: int
    index_count: int
    index_path: str
    index_created: bool
    memory_modified: bool
    auto_adoption: bool
    human_approval_required: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class LongTermMemoryIndexBuilder:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_dir = self.root_dir / "memory"
        self.long_term_memory_path = self.memory_dir / "long_term_memory.json"
        self.index_path = self.memory_dir / "long_term_memory_index.json"

        self.memory_dir.mkdir(parents=True, exist_ok=True)

    def build_index(self) -> LongTermMemoryIndexBuildResult:
        memory_found = self.long_term_memory_path.exists()
        memory_data = self._read_json(self.long_term_memory_path)

        raw_memories = memory_data.get("memories", [])
        if not isinstance(raw_memories, list):
            raw_memories = []

        index_items: List[LongTermMemoryIndexItem] = []

        for item in raw_memories:
            if not isinstance(item, dict):
                continue

            text = str(item.get("text", ""))
            importance = str(item.get("importance", ""))
            score = self._to_int(item.get("score", 0))

            index_items.append(
                LongTermMemoryIndexItem(
                    memory_id=str(item.get("id", "")),
                    text=text,
                    importance=importance,
                    score=score,
                    source=str(item.get("source", "")),
                    memory_type=str(item.get("memory_type", "")),
                    keywords=self._extract_keywords(text),
                    priority=self._calculate_priority(importance, score, text),
                    safe_adopted=bool(item.get("safe_adopted", False)),
                )
            )

        index_data = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "phase": "Phase7-2 Long-Term Memory Index Builder",
            "source": "Naviko Long Term Memory Index",
            "index_type": "long_term_memory_index",
            "memory_modified": False,
            "auto_adoption": False,
            "human_approval_required": True,
            "item_count": len(index_items),
            "items": [asdict(item) for item in index_items],
        }

        self._write_json(self.index_path, index_data)

        return LongTermMemoryIndexBuildResult(
            status="completed" if memory_found else "blocked",
            phase="Phase7-2 Long-Term Memory Index Builder",
            long_term_memory_found=memory_found,
            memory_count=len(raw_memories),
            index_count=len(index_items),
            index_path=str(self.index_path),
            index_created=True,
            memory_modified=False,
            auto_adoption=False,
            human_approval_required=True,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=memory_found,
        )

    def _extract_keywords(self, text: str) -> List[str]:
        keyword_candidates = [
            "ナビ子",
            "起動",
            "自然",
            "会話",
            "デスクトップAI",
            "第一目標",
            "最優先",
            "記憶",
            "人格",
            "目的",
            "安全",
            "長期記憶",
        ]

        keywords: List[str] = []

        for keyword in keyword_candidates:
            if keyword in text and keyword not in keywords:
                keywords.append(keyword)

        if not keywords and text:
            keywords.append(text[:20])

        return keywords

    def _calculate_priority(self, importance: str, score: int, text: str) -> int:
        priority = score

        if importance == "high":
            priority += 3
        elif importance == "medium":
            priority += 2
        elif importance == "low":
            priority += 1

        if "最優先" in text:
            priority += 2

        if "第一目標" in text or "起動" in text or "自然に会話" in text:
            priority += 2

        return priority

    def print_result(self, result: LongTermMemoryIndexBuildResult) -> None:
        print("=== Phase7-2 Long-Term Memory Index Builder ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"LongTermMemoryFound: {result.long_term_memory_found}")
        print(f"MemoryCount: {result.memory_count}")
        print(f"IndexCount: {result.index_count}")
        print(f"IndexPath: {result.index_path}")
        print(f"IndexCreated: {result.index_created}")
        print(f"MemoryModified: {result.memory_modified}")
        print(f"AutoAdoption: {result.auto_adoption}")
        print(f"HumanApprovalRequired: {result.human_approval_required}")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def _to_int(self, value: Any) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

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

    def _write_json(self, path: Path, data: Dict[str, Any]) -> None:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def run_phase7_2_test() -> None:
    builder = LongTermMemoryIndexBuilder()
    result = builder.build_index()
    builder.print_result(result)


if __name__ == "__main__":
    run_phase7_2_test()