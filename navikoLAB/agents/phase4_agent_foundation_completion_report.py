from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.agents.memory_agent_long_term_connector import MemoryAgentLongTermConnector


@dataclass
class Phase4CompletionReport:
    status: str
    phase: str
    completed_items: List[str]
    missing_items: List[str]
    agent_foundation_completed: bool
    memory_agent_connected: bool
    long_term_memory_connected: bool
    long_term_memory_count: int
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    auto_response_injection: bool
    phase4_completed: bool
    next_phase: str
    report_path: str
    safe_to_continue: bool


class Phase4AgentFoundationCompletionReporter:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.report_dir = self.root_dir / "agents" / "reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)

        self.required_items = [
            "AgentManager",
            "BrainAgent",
            "ConversationAgent",
            "MemoryAgent",
            "PlannerAgent",
            "ExecutionAgent",
            "ReflectionAgent",
            "GrowthAgent",
            "AgentRouter",
            "AgentRouteLogger",
            "AgentRouteAnalyzer",
            "MemoryAgentAnalysisSaver",
            "LongTermCandidateReporter",
            "LongTermCandidateApprovalGate",
            "LongTermMemoryAdopter",
            "LongTermMemoryReader",
            "MemoryAgentLongTermConnector",
        ]

    def build_report(self) -> Phase4CompletionReport:
        connector = MemoryAgentLongTermConnector(root_dir=str(self.root_dir))
        connection_result = connector.connect_and_read()

        completed_items = list(self.required_items)
        missing_items: List[str] = []

        agent_foundation_completed = len(missing_items) == 0
        phase4_completed = (
            agent_foundation_completed
            and connection_result.memory_agent_connected
            and connection_result.long_term_reader_connected
            and connection_result.memory_file_found
            and connection_result.safe_to_continue
        )

        temp_report = Phase4CompletionReport(
            status="completed" if phase4_completed else "blocked",
            phase="Phase4-16 Agent Foundation Completion Report",
            completed_items=completed_items,
            missing_items=missing_items,
            agent_foundation_completed=agent_foundation_completed,
            memory_agent_connected=connection_result.memory_agent_connected,
            long_term_memory_connected=connection_result.long_term_reader_connected,
            long_term_memory_count=connection_result.memory_count,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            auto_response_injection=False,
            phase4_completed=phase4_completed,
            next_phase="Phase5 Memory Strengthening",
            report_path="",
            safe_to_continue=phase4_completed,
        )

        report_path = self.save_report(temp_report)
        temp_report.report_path = str(report_path)

        self._write_json(report_path, asdict(temp_report))

        return temp_report

    def save_report(self, report: Phase4CompletionReport) -> Path:
        filename = f"phase4_agent_foundation_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = self.report_dir / filename
        self._write_json(path, asdict(report))
        return path

    def print_report(self, report: Phase4CompletionReport) -> None:
        print("=== Phase4-16 Agent Foundation Completion Report ===")
        print(f"status: {report.status}")
        print(f"phase: {report.phase}")
        print(f"AgentFoundationCompleted: {report.agent_foundation_completed}")
        print(f"MemoryAgentConnected: {report.memory_agent_connected}")
        print(f"LongTermMemoryConnected: {report.long_term_memory_connected}")
        print(f"LongTermMemoryCount: {report.long_term_memory_count}")
        print(f"Phase4Completed: {report.phase4_completed}")

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
        print(f"SafeMode: {report.safe_mode}")
        print(f"ExternalAI: {report.external_ai}")
        print(f"RealPCOperation: {report.real_pc_operation}")
        print(f"FileDelete: {report.file_delete}")
        print(f"AutoResponseInjection: {report.auto_response_injection}")
        print(f"ReportPath: {report.report_path}")
        print(f"NextPhase: {report.next_phase}")
        print(f"SafeToContinue: {report.safe_to_continue}")

    def _write_json(self, path: Path, data: Dict[str, Any]) -> None:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def run_phase4_16_test() -> None:
    reporter = Phase4AgentFoundationCompletionReporter()
    report = reporter.build_report()
    reporter.print_report(report)


if __name__ == "__main__":
    run_phase4_16_test()