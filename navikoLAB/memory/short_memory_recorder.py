from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class ShortMemoryItem:
    id: str
    created_at: str
    speaker: str
    text: str
    source: str
    memory_type: str
    importance: str
    score: int


@dataclass
class ShortMemoryRecordResult:
    status: str
    phase: str
    recorded: bool
    short_memory_path: str
    before_count: int
    after_count: int
    recorded_item: Dict[str, Any]
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    long_term_auto_adoption: bool
    safe_to_continue: bool


class ShortMemoryRecorder:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_dir = self.root_dir / "memory"
        self.short_memory_path = self.memory_dir / "short_memory.json"

        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_short_memory_file()

    def record(
        self,
        speaker: str,
        text: str,
        source: str = "Conversation",
        importance: str = "low",
        score: int = 1,
    ) -> ShortMemoryRecordResult:
        data = self._read_json(self.short_memory_path)
        memories = data.get("memories", [])

        if not isinstance(memories, list):
            memories = []

        before_count = len(memories)

        item = ShortMemoryItem(
            id=f"stm_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            created_at=datetime.now().isoformat(timespec="seconds"),
            speaker=speaker,
            text=text,
            source=source,
            memory_type="short",
            importance=importance,
            score=score,
        )

        memories.append(asdict(item))

        data["updated_at"] = datetime.now().isoformat(timespec="seconds")
        data["memories"] = memories

        self._write_json(self.short_memory_path, data)

        after_count = len(memories)

        return ShortMemoryRecordResult(
            status="completed",
            phase="Phase5-2 Short Memory Recorder",
            recorded=True,
            short_memory_path=str(self.short_memory_path),
            before_count=before_count,
            after_count=after_count,
            recorded_item=asdict(item),
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            long_term_auto_adoption=False,
            safe_to_continue=True,
        )

    def read_all(self) -> List[Dict[str, Any]]:
        data = self._read_json(self.short_memory_path)
        memories = data.get("memories", [])

        if isinstance(memories, list):
            return [item for item in memories if isinstance(item, dict)]

        return []

    def print_result(self, result: ShortMemoryRecordResult) -> None:
        print("=== Phase5-2 Short Memory Recorder ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"Recorded: {result.recorded}")
        print(f"ShortMemoryPath: {result.short_memory_path}")
        print(f"BeforeCount: {result.before_count}")
        print(f"AfterCount: {result.after_count}")

        print("")
        print("[Recorded Short Memory]")
        print(f"id: {result.recorded_item.get('id', '')}")
        print(f"speaker: {result.recorded_item.get('speaker', '')}")
        print(f"text: {result.recorded_item.get('text', '')}")
        print(f"source: {result.recorded_item.get('source', '')}")
        print(f"importance: {result.recorded_item.get('importance', '')}")
        print(f"score: {result.recorded_item.get('score', 0)}")

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"LongTermAutoAdoption: {result.long_term_auto_adoption}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def _ensure_short_memory_file(self) -> None:
        if self.short_memory_path.exists():
            return

        data = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "source": "Naviko Short Memory",
            "memory_type": "short",
            "memories": [],
        }

        self._write_json(self.short_memory_path, data)

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


def run_phase5_2_test() -> None:
    recorder = ShortMemoryRecorder()

    result = recorder.record(
        speaker="user",
        text="ナビ子、今日は記憶を強くしていこう",
        source="Phase5-2 test conversation",
        importance="low",
        score=1,
    )

    recorder.print_result(result)


if __name__ == "__main__":
    run_phase5_2_test()