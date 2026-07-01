from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class LongTermMemoryFileStatus:
    name: str
    path: str
    found: bool
    item_count: int
    note: str


@dataclass
class Phase7LongTermMemoryStartDiagnosticsReport:
    status: str
    phase: str
    memory_dir_found: bool
    long_term_memory_ready: bool
    long_term_index_ready: bool
    long_term_review_ready: bool
    long_term_memory_count: int
    required_files: List[Dict[str, Any]]
    missing_files: List[str]
    long_term_strengthening_ready: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    auto_adoption: bool
    human_approval_required: bool
    next_phase: str
    report_path: str
    safe_to_continue: bool


class Phase7LongTermMemoryStartDiagnostics:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_dir = self.root_dir / "memory"
        self.report_dir = self.memory_dir / "reports"

        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)

        self.long_term_memory_path = self.memory_dir / "long_term_memory.json"
        self.long_term_index_path = self.memory_dir / "long_term_memory_index.json"
        self.long_term_review_path = self.memory_dir / "long_term_memory_review.json"

    def run_diagnostics(self) -> Phase7LongTermMemoryStartDiagnosticsReport:
        self._ensure_long_term_memory_file()
        self._ensure_index_file()
        self._ensure_review_file()

        memory_status = self._check_memory_file(
            name="long_term_memory",
            path=self.long_term_memory_path,
            note="承認済みの重要記憶を保持する正式な長期記憶ファイル。",
        )

        index_status = self._check_memory_file(
            name="long_term_memory_index",
            path=self.long_term_index_path,
            note="長期記憶を検索・参照しやすくするための索引ファイル。",
        )

        review_status = self._check_memory_file(
            name="long_term_memory_review",
            path=self.long_term_review_path,
            note="長期記憶の見直し候補や確認履歴を保持するレビュー用ファイル。",
        )

        required_files = [
            asdict(memory_status),
            asdict(index_status),
            asdict(review_status),
        ]

        missing_files = [
            item["path"]
            for item in required_files
            if not item["found"]
        ]

        long_term_strengthening_ready = (
            self.memory_dir.exists()
            and memory_status.found
            and index_status.found
            and review_status.found
        )

        temp_report = Phase7LongTermMemoryStartDiagnosticsReport(
            status="completed" if long_term_strengthening_ready else "blocked",
            phase="Phase7-1 Long-Term Memory Strengthening Start Diagnostics",
            memory_dir_found=self.memory_dir.exists(),
            long_term_memory_ready=memory_status.found,
            long_term_index_ready=index_status.found,
            long_term_review_ready=review_status.found,
            long_term_memory_count=memory_status.item_count,
            required_files=required_files,
            missing_files=missing_files,
            long_term_strengthening_ready=long_term_strengthening_ready,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            auto_adoption=False,
            human_approval_required=True,
            next_phase="Phase7-2 Long-Term Memory Index Builder",
            report_path="",
            safe_to_continue=long_term_strengthening_ready,
        )

        report_path = self.save_report(temp_report)
        temp_report.report_path = str(report_path)
        self._write_json(report_path, asdict(temp_report))

        return temp_report

    def _ensure_long_term_memory_file(self) -> None:
        if self.long_term_memory_path.exists():
            return

        data = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "source": "Naviko Long Term Memory",
            "memory_type": "long_term",
            "memories": [],
        }

        self._write_json(self.long_term_memory_path, data)

    def _ensure_index_file(self) -> None:
        if self.long_term_index_path.exists():
            return

        data = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "source": "Naviko Long Term Memory Index",
            "index_type": "long_term_memory_index",
            "auto_generated": True,
            "items": [],
        }

        self._write_json(self.long_term_index_path, data)

    def _ensure_review_file(self) -> None:
        if self.long_term_review_path.exists():
            return

        data = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "source": "Naviko Long Term Memory Review",
            "review_type": "long_term_memory_review",
            "human_approval_required": True,
            "auto_delete": False,
            "items": [],
        }

        self._write_json(self.long_term_review_path, data)

    def _check_memory_file(self, name: str, path: Path, note: str) -> LongTermMemoryFileStatus:
        found = path.exists()
        item_count = 0

        if found:
            data = self._read_json(path)

            memories = data.get("memories", [])
            items = data.get("items", [])

            if isinstance(memories, list):
                item_count = len(memories)
            elif isinstance(items, list):
                item_count = len(items)

        return LongTermMemoryFileStatus(
            name=name,
            path=str(path),
            found=found,
            item_count=item_count,
            note=note,
        )

    def save_report(self, report: Phase7LongTermMemoryStartDiagnosticsReport) -> Path:
        filename = f"phase7_long_term_memory_start_diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = self.report_dir / filename
        self._write_json(path, asdict(report))
        return path

    def print_report(self, report: Phase7LongTermMemoryStartDiagnosticsReport) -> None:
        print("=== Phase7-1 Long-Term Memory Strengthening Start Diagnostics ===")
        print(f"status: {report.status}")
        print(f"phase: {report.phase}")
        print(f"MemoryDirFound: {report.memory_dir_found}")
        print(f"LongTermMemoryReady: {report.long_term_memory_ready}")
        print(f"LongTermIndexReady: {report.long_term_index_ready}")
        print(f"LongTermReviewReady: {report.long_term_review_ready}")
        print(f"LongTermMemoryCount: {report.long_term_memory_count}")
        print(f"LongTermStrengtheningReady: {report.long_term_strengthening_ready}")

        print("")
        print("[Required Long-Term Memory Files]")
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
        print(f"AutoAdoption: {report.auto_adoption}")
        print(f"HumanApprovalRequired: {report.human_approval_required}")
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


def run_phase7_1_test() -> None:
    diagnostics = Phase7LongTermMemoryStartDiagnostics()
    report = diagnostics.run_diagnostics()
    diagnostics.print_report(report)


if __name__ == "__main__":
    run_phase7_1_test()