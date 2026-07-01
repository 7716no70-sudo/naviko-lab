from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class MidMemoryItem:
    id: str
    created_at: str
    text: str
    source: str
    memory_type: str
    importance: str
    score: int
    reason: str


@dataclass
class MidMemoryRecordResult:
    status: str
    phase: str
    recorded: bool
    mid_memory_path: str
    before_count: int
    after_count: int
    recorded_item: Dict[str, Any]
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    long_term_auto_adoption: bool
    safe_to_continue: bool


class MidMemoryRecorder:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_dir = self.root_dir / "memory"
        self.mid_memory_path = self.memory_dir / "mid_memory.json"

        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_mid_memory_file()

    def record(
        self,
        text: str,
        source: str = "ShortMemory",
        importance: str = "medium",
        score: int = 2,
        reason: str = "会話文脈としてしばらく保持するため",
    ) -> MidMemoryRecordResult:
        data = self._read_json(self.mid_memory_path)
        memories = data.get("memories", [])

        if not isinstance(memories, list):
            memories = []

        before_count = len(memories)

        item = MidMemoryItem(
            id=f"mmm_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            created_at=datetime.now().isoformat(timespec="seconds"),
            text=text,
            source=source,
            memory_type="mid",
            importance=importance,
            score=score,
            reason=reason,
        )

        memories.append(asdict(item))

        data["updated_at"] = datetime.now().isoformat(timespec="seconds")
        data["memories"] = memories

        self._write_json(self.mid_memory_path, data)

        return MidMemoryRecordResult(
            status="completed",
            phase="Phase5-5 Mid Memory Recorder",
            recorded=True,
            mid_memory_path=str(self.mid_memory_path),
            before_count=before_count,
            after_count=len(memories),
            recorded_item=asdict(item),
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            long_term_auto_adoption=False,
            safe_to_continue=True,
        )

    def read_all(self) -> List[Dict[str, Any]]:
        data = self._read_json(self.mid_memory_path)
        memories = data.get("memories", [])

        if isinstance(memories, list):
            return [item for item in memories if isinstance(item, dict)]

        return []

    def print_result(self, result: MidMemoryRecordResult) -> None:
        print("=== Phase5-5 Mid Memory Recorder ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"Recorded: {result.recorded}")
        print(f"MidMemoryPath: {result.mid_memory_path}")
        print(f"BeforeCount: {result.before_count}")
        print(f"AfterCount: {result.after_count}")

        print("")
        print("[Recorded Mid Memory]")
        print(f"id: {result.recorded_item.get('id', '')}")
        print(f"text: {result.recorded_item.get('text', '')}")
        print(f"source: {result.recorded_item.get('source', '')}")
        print(f"importance: {result.recorded_item.get('importance', '')}")
        print(f"score: {result.recorded_item.get('score', 0)}")
        print(f"reason: {result.recorded_item.get('reason', '')}")

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"LongTermAutoAdoption: {result.long_term_auto_adoption}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def _ensure_mid_memory_file(self) -> None:
        if self.mid_memory_path.exists():
            return

        data = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "source": "Naviko Mid Memory",
            "memory_type": "mid",
            "memories": [],
        }

        self._write_json(self.mid_memory_path, data)

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


def run_phase5_5_test() -> None:
    recorder = MidMemoryRecorder()

    result = recorder.record(
        text="ナビ子は記憶を強化して、直近の会話文脈を保てるようにする",
        source="Phase5-5 test",
        importance="medium",
        score=2,
        reason="Phase5のMemory強化方針に関係するため",
    )

    recorder.print_result(result)


if __name__ == "__main__":
    run_phase5_5_test()