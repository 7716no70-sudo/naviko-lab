from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.memory.short_memory_reader import ShortMemoryReader
from navikoLAB.memory.mid_memory_reader import MidMemoryReader
from navikoLAB.agents.long_term_memory_reader import LongTermMemoryReader
from navikoLAB.memory.memory_context_reader import MemoryContextReader
from navikoLAB.memory.memory_context_packet_reader import MemoryContextPacketReader
from navikoLAB.memory.conversation_memory_reference_adapter import ConversationMemoryReferenceAdapter


@dataclass
class Phase5MemoryStrengtheningCompletionReport:
    status: str
    phase: str
    completed_items: List[str]
    missing_items: List[str]
    short_memory_ready: bool
    mid_memory_ready: bool
    long_term_memory_ready: bool
    memory_context_ready: bool
    safe_packet_ready: bool
    conversation_adapter_ready: bool
    short_memory_count: int
    mid_memory_count: int
    long_term_memory_count: int
    reference_line_count: int
    memory_strengthening_completed: bool
    conversation_engine_modified: bool
    auto_response_injection: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    next_phase: str
    report_path: str
    safe_to_continue: bool


class Phase5MemoryStrengtheningCompletionReporter:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.report_dir = self.root_dir / "memory" / "reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)

        self.completed_items = [
            "Phase5-1 Memory Strengthening Start Diagnostics",
            "ShortMemoryRecorder",
            "ShortMemoryReader",
            "ShortMemoryCleaner",
            "MidMemoryRecorder",
            "MidMemoryReader",
            "MemoryContextBuilder",
            "MemoryContextReader",
            "MemoryContextConnector",
            "MemoryContextInjectionPreview",
            "MemoryContextSafeInjector",
            "MemoryContextPacketReader",
            "ConversationMemoryBridge",
            "MemoryAwareConversationPreview",
            "ConversationMemoryReferenceAdapter",
        ]

    def build_report(self) -> Phase5MemoryStrengtheningCompletionReport:
        short_result = ShortMemoryReader(root_dir=str(self.root_dir)).read()
        mid_result = MidMemoryReader(root_dir=str(self.root_dir)).read()
        long_result = LongTermMemoryReader(root_dir=str(self.root_dir)).read_long_term_memory()
        context_result = MemoryContextReader(root_dir=str(self.root_dir)).read_latest_context()
        packet_result = MemoryContextPacketReader(root_dir=str(self.root_dir)).read_latest_packet()
        adapter_result = ConversationMemoryReferenceAdapter(root_dir=str(self.root_dir)).diagnose_adapter()

        missing_items: List[str] = []

        short_memory_ready = short_result.short_memory_file_found
        mid_memory_ready = mid_result.mid_memory_file_found
        long_term_memory_ready = long_result.memory_file_found
        memory_context_ready = context_result.context_file_found
        safe_packet_ready = packet_result.packet_file_found and packet_result.injection_mode == "reference_only"
        conversation_adapter_ready = adapter_result.adapter_ready

        if not short_memory_ready:
            missing_items.append("short_memory.json")

        if not mid_memory_ready:
            missing_items.append("mid_memory.json")

        if not long_term_memory_ready:
            missing_items.append("long_term_memory.json")

        if not memory_context_ready:
            missing_items.append("latest_memory_context.json")

        if not safe_packet_ready:
            missing_items.append("latest_memory_context_safe_packet.json")

        if not conversation_adapter_ready:
            missing_items.append("ConversationMemoryReferenceAdapter")

        memory_strengthening_completed = (
            short_memory_ready
            and mid_memory_ready
            and long_term_memory_ready
            and memory_context_ready
            and safe_packet_ready
            and conversation_adapter_ready
            and adapter_result.safe_to_continue
        )

        temp_report = Phase5MemoryStrengtheningCompletionReport(
            status="completed" if memory_strengthening_completed else "blocked",
            phase="Phase5-16 Memory Strengthening Completion Report",
            completed_items=self.completed_items,
            missing_items=missing_items,
            short_memory_ready=short_memory_ready,
            mid_memory_ready=mid_memory_ready,
            long_term_memory_ready=long_term_memory_ready,
            memory_context_ready=memory_context_ready,
            safe_packet_ready=safe_packet_ready,
            conversation_adapter_ready=conversation_adapter_ready,
            short_memory_count=short_result.memory_count,
            mid_memory_count=mid_result.memory_count,
            long_term_memory_count=long_result.memory_count,
            reference_line_count=adapter_result.reference_line_count,
            memory_strengthening_completed=memory_strengthening_completed,
            conversation_engine_modified=False,
            auto_response_injection=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            next_phase="Phase6 Personality Strengthening",
            report_path="",
            safe_to_continue=memory_strengthening_completed,
        )

        report_path = self.save_report(temp_report)
        temp_report.report_path = str(report_path)
        self._write_json(report_path, asdict(temp_report))

        return temp_report

    def save_report(self, report: Phase5MemoryStrengtheningCompletionReport) -> Path:
        filename = f"phase5_memory_strengthening_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = self.report_dir / filename
        self._write_json(path, asdict(report))
        return path

    def print_report(self, report: Phase5MemoryStrengtheningCompletionReport) -> None:
        print("=== Phase5-16 Memory Strengthening Completion Report ===")
        print(f"status: {report.status}")
        print(f"phase: {report.phase}")
        print(f"ShortMemoryReady: {report.short_memory_ready}")
        print(f"MidMemoryReady: {report.mid_memory_ready}")
        print(f"LongTermMemoryReady: {report.long_term_memory_ready}")
        print(f"MemoryContextReady: {report.memory_context_ready}")
        print(f"SafePacketReady: {report.safe_packet_ready}")
        print(f"ConversationAdapterReady: {report.conversation_adapter_ready}")
        print(f"ShortMemoryCount: {report.short_memory_count}")
        print(f"MidMemoryCount: {report.mid_memory_count}")
        print(f"LongTermMemoryCount: {report.long_term_memory_count}")
        print(f"ReferenceLineCount: {report.reference_line_count}")
        print(f"MemoryStrengtheningCompleted: {report.memory_strengthening_completed}")

        print("")
        print("[Completed Items]")
        for item in report.completed_items:
            print(f"- {item}")

        print("")
        print("[Missing Items]")
        if not report.missing_items:
            print("- なし")
        else:
            for item in report.missing_items:
                print(f"- {item}")

        print("")
        print(f"ConversationEngineModified: {report.conversation_engine_modified}")
        print(f"AutoResponseInjection: {report.auto_response_injection}")
        print(f"SafeMode: {report.safe_mode}")
        print(f"ExternalAI: {report.external_ai}")
        print(f"RealPCOperation: {report.real_pc_operation}")
        print(f"FileDelete: {report.file_delete}")
        print(f"ReportPath: {report.report_path}")
        print(f"NextPhase: {report.next_phase}")
        print(f"SafeToContinue: {report.safe_to_continue}")

    def _write_json(self, path: Path, data: Dict[str, Any]) -> None:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def run_phase5_16_test() -> None:
    reporter = Phase5MemoryStrengtheningCompletionReporter()
    report = reporter.build_report()
    reporter.print_report(report)


if __name__ == "__main__":
    run_phase5_16_test()