from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class ShortMemoryCleanResult:
    status: str
    phase: str
    short_memory_path: str
    archive_path: str
    before_count: int
    after_count: int
    archived_count: int
    max_keep: int
    file_delete: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    safe_to_continue: bool


class ShortMemoryCleaner:
    def __init__(self, root_dir: str = "navikoLAB", max_keep: int = 20) -> None:
        self.root_dir = Path(root_dir)
        self.memory_dir = self.root_dir / "memory"
        self.archive_dir = self.memory_dir / "archive"
        self.short_memory_path = self.memory_dir / "short_memory.json"
        self.max_keep = max_keep

        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_short_memory_file()

    def clean(self) -> ShortMemoryCleanResult:
        data = self._read_json(self.short_memory_path)
        memories = data.get("memories", [])

        if not isinstance(memories, list):
            memories = []

        before_count = len(memories)

        if before_count <= self.max_keep:
            archive_path = self._save_archive([])
            return ShortMemoryCleanResult(
                status="completed",
                phase="Phase5-4 Short Memory Cleaner",
                short_memory_path=str(self.short_memory_path),
                archive_path=str(archive_path),
                before_count=before_count,
                after_count=before_count,
                archived_count=0,
                max_keep=self.max_keep,
                file_delete=False,
                safe_mode=True,
                external_ai=False,
                real_pc_operation=False,
                safe_to_continue=True,
            )

        archive_items = memories[:-self.max_keep]
        keep_items = memories[-self.max_keep:]

        archive_path = self._save_archive(archive_items)

        data["updated_at"] = datetime.now().isoformat(timespec="seconds")
        data["memories"] = keep_items
        self._write_json(self.short_memory_path, data)

        return ShortMemoryCleanResult(
            status="completed",
            phase="Phase5-4 Short Memory Cleaner",
            short_memory_path=str(self.short_memory_path),
            archive_path=str(archive_path),
            before_count=before_count,
            after_count=len(keep_items),
            archived_count=len(archive_items),
            max_keep=self.max_keep,
            file_delete=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            safe_to_continue=True,
        )

    def print_result(self, result: ShortMemoryCleanResult) -> None:
        print("=== Phase5-4 Short Memory Cleaner ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"ShortMemoryPath: {result.short_memory_path}")
        print(f"ArchivePath: {result.archive_path}")
        print(f"BeforeCount: {result.before_count}")
        print(f"AfterCount: {result.after_count}")
        print(f"ArchivedCount: {result.archived_count}")
        print(f"MaxKeep: {result.max_keep}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def _save_archive(self, archive_items: List[Dict[str, Any]]) -> Path:
        filename = f"short_memory_archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = self.archive_dir / filename

        archive_data = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "source": "Phase5-4 Short Memory Cleaner",
            "archive_type": "short_memory_overflow",
            "archived_count": len(archive_items),
            "file_delete": False,
            "items": archive_items,
        }

        self._write_json(path, archive_data)
        return path

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


def run_phase5_4_test() -> None:
    cleaner = ShortMemoryCleaner(max_keep=20)
    result = cleaner.clean()
    cleaner.print_result(result)


if __name__ == "__main__":
    run_phase5_4_test()