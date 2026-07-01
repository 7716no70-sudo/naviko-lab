from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class MemoryFileStatus:
    name: str
    path: str
    found: bool
    item_count: int
    note: str


@dataclass
class Phase5MemoryStartDiagnosticsReport:
    status: str
    phase: str
    memory_dir_found: bool
    short_memory_ready: bool
    mid_memory_ready: bool
    long_memory_ready: bool
    long_term_memory_count: int
    required_files: List[Dict[str, Any]]
    missing_files: List[str]
    memory_strengthening_ready: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    next_phase: str
    report_path: str
    safe_to_continue: bool


class Phase5MemoryStrengtheningStartDiagnostics:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_dir = self.root_dir / "memory"
        self.report_dir = self.memory_dir / "reports"

        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)

        self.short_memory_path = self.memory_dir / "short_memory.json"
        self.mid_memory_path = self.memory_dir / "mid_memory.json"
        self.long_term_memory_path = self.memory_dir / "long_term_memory.json"

    def run_diagnostics(self) -> Phase5MemoryStartDiagnosticsReport:
        self._ensure_memory_file(
            path=self.short_memory_path,
            source="Naviko Short Memory",
            memory_type="short",
        )

        self._ensure_memory_file(
            path=self.mid_memory_path,
            source="Naviko Mid Memory",
            memory_type="mid",
        )

        self._ensure_memory_file(
            path=self.long_term_memory_path,
            source="Naviko Long Term Memory",
            memory_type="long_term",
        )

        short_status = self._check_memory_file(
            name="short_memory",
            path=self.short_memory_path,
            note="短期記憶。直近会話や一時的な文脈に使う。"
        )

        mid_status = self._check_memory_file(
            name="mid_memory",
            path=self.mid_memory_path,
            note="中期記憶。しばらく保持したい会話傾向や作業文脈に使う。"
        )

        long_status = self._check_memory_file(
            name="long_term_memory",
            path=self.long_term_memory_path,
            note="長期記憶。承認済みの重要記憶だけを保持する。"
        )

        required_files = [
            asdict(short_status),
            asdict(mid_status),
            asdict(long_status),
        ]

        missing_files = [
            item["path"]
            for item in required_files
            if not item["found"]
        ]

        memory_strengthening_ready = (
            self.memory_dir.exists()
            and short_status.found
            and mid_status.found
            and long_status.found
        )

        temp_report = Phase5MemoryStartDiagnosticsReport(
            status="completed" if memory_strengthening_ready else "blocked",
            phase="Phase5-1 Memory Strengthening Start Diagnostics",
            memory_dir_found=self.memory_dir.exists(),
            short_memory_ready=short_status.found,
            mid_memory_ready=mid_status.found,
            long_memory_ready=long_status.found,
            long_term_memory_count=long_status.item_count,
            required_files=required_files,
            missing_files=missing_files,
            memory_strengthening_ready=memory_strengthening_ready,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            next_phase="Phase5-2 Short Memory Recorder",
            report_path="",
            safe_to_continue=memory_strengthening_ready,
        )

        report_path = self.save_report(temp_report)
        temp_report.report_path = str(report_path)
        self._write_json(report_path, asdict(temp_report))

        return temp_report

    def _ensure_memory_file(self, path: Path, source: str, memory_type: str) -> None:
        if path.exists():
            return

        data = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "source": source,
            "memory_type": memory_type,
            "memories": [],
        }

        self._write_json(path, data)

    def _check_memory_file(self, name: str, path: Path, note: str) -> MemoryFileStatus:
        found = path.exists()
        item_count = 0

        if found:
            data = self._read_json(path)
            memories = data.get("memories", [])
            if isinstance(memories, list):
                item_count = len(memories)

        return MemoryFileStatus(
            name=name,
            path=str(path),
            found=found,
            item_count=item_count,
            note=note,
        )

    def save_report(self, report: Phase5MemoryStartDiagnosticsReport) -> Path:
        filename = f"phase5_memory_strengthening_start_diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = self.report_dir / filename
        self._write_json(path, asdict(report))
        return path

    def print_report(self, report: Phase5MemoryStartDiagnosticsReport) -> None:
        print("=== Phase5-1 Memory Strengthening Start Diagnostics ===")
        print(f"status: {report.status}")
        print(f"phase: {report.phase}")
        print(f"MemoryDirFound: {report.memory_dir_found}")
        print(f"ShortMemoryReady: {report.short_memory_ready}")
        print(f"MidMemoryReady: {report.mid_memory_ready}")
        print(f"LongMemoryReady: {report.long_memory_ready}")
        print(f"LongTermMemoryCount: {report.long_term_memory_count}")
        print(f"MemoryStrengtheningReady: {report.memory_strengthening_ready}")

        print("")
        print("[Required Memory Files]")
        for item in report.required_files:
            print(f"- {item.get('name', '')}")
            print(f"  path: {item.get('path', '')}")
            print(f"  found: {item.get('found', False)}")
            print(f"  item_count: {item.get('item_count', 0)}")
            print(f"  note: {item.get('note', '')}")

        print("")
        print("[Missing Files]")
        if not report.missing_files:
            print("- なし")
        else:
            for item in report.missing_files:
                print(f"- {item}")

        print("")
        print(f"SafeMode: {report.safe_mode}")
        print(f"ExternalAI: {report.external_ai}")
        print(f"RealPCOperation: {report.real_pc_operation}")
        print(f"FileDelete: {report.file_delete}")
        print(f"ReportPath: {report.report_path}")
        print(f"NextPhase: {report.next_phase}")
        print(f"SafeToContinue: {report.safe_to_continue}")

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


def run_phase5_1_test() -> None:
    diagnostics = Phase5MemoryStrengtheningStartDiagnostics()
    report = diagnostics.run_diagnostics()
    diagnostics.print_report(report)


if __name__ == "__main__":
    run_phase5_1_test()