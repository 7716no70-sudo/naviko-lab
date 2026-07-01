from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.personality.personality_profile_reader import PersonalityProfileReader
from navikoLAB.personality.tone_profile_reader import ToneProfileReader
from navikoLAB.personality.emotion_state_reader import EmotionStateReader
from navikoLAB.personality.personality_context_reader import PersonalityContextReader
from navikoLAB.personality.personality_safe_packet_reader import PersonalitySafePacketReader
from navikoLAB.personality.conversation_personality_reference_adapter import ConversationPersonalityReferenceAdapter
from navikoLAB.personality.memory_personality_conversation_adapter import MemoryPersonalityConversationAdapter


@dataclass
class Phase6PersonalityStrengtheningCompletionReport:
    status: str
    phase: str
    completed_items: List[str]
    missing_items: List[str]
    personality_profile_ready: bool
    tone_profile_ready: bool
    emotion_state_ready: bool
    personality_context_ready: bool
    personality_packet_ready: bool
    personality_adapter_ready: bool
    memory_personality_adapter_ready: bool
    name: str
    user_name: str
    primary_goal: str
    base_tone: str
    mood: str
    personality_strengthening_completed: bool
    conversation_engine_modified: bool
    auto_response_injection: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    next_phase: str
    report_path: str
    safe_to_continue: bool


class Phase6PersonalityStrengtheningCompletionReporter:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.report_dir = self.root_dir / "personality" / "reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)

        self.completed_items = [
            "Phase6-1 Personality Strengthening Start Diagnostics",
            "PersonalityProfileReader",
            "ToneProfileReader",
            "EmotionStateReader",
            "PersonalityContextBuilder",
            "PersonalityContextReader",
            "PersonalityResponsePreview",
            "PersonalitySafePacketBuilder",
            "PersonalitySafePacketReader",
            "ConversationPersonalityBridge",
            "PersonalityAwareConversationPreview",
            "ConversationPersonalityReferenceAdapter",
            "MemoryPersonalityConversationPreview",
            "MemoryPersonalityConversationAdapter",
        ]

    def build_report(self) -> Phase6PersonalityStrengtheningCompletionReport:
        profile_result = PersonalityProfileReader(root_dir=str(self.root_dir)).read()
        tone_result = ToneProfileReader(root_dir=str(self.root_dir)).read()
        emotion_result = EmotionStateReader(root_dir=str(self.root_dir)).read()
        context_result = PersonalityContextReader(root_dir=str(self.root_dir)).read_latest_context()
        packet_result = PersonalitySafePacketReader(root_dir=str(self.root_dir)).read_latest_packet()
        personality_adapter_result = ConversationPersonalityReferenceAdapter(root_dir=str(self.root_dir)).diagnose_adapter()
        memory_personality_adapter_result = MemoryPersonalityConversationAdapter(root_dir=str(self.root_dir)).diagnose_adapter()

        missing_items: List[str] = []

        if not profile_result.personality_profile_ready:
            missing_items.append("personality_profile.json")

        if not tone_result.tone_profile_ready:
            missing_items.append("tone_profile.json")

        if not emotion_result.emotion_state_ready:
            missing_items.append("emotion_state.json")

        if not context_result.safe_to_continue:
            missing_items.append("latest_personality_context.json")

        if not packet_result.safe_to_continue:
            missing_items.append("latest_personality_safe_packet.json")

        if not personality_adapter_result.adapter_ready:
            missing_items.append("ConversationPersonalityReferenceAdapter")

        if not memory_personality_adapter_result.adapter_ready:
            missing_items.append("MemoryPersonalityConversationAdapter")

        personality_strengthening_completed = (
            profile_result.personality_profile_ready
            and tone_result.tone_profile_ready
            and emotion_result.emotion_state_ready
            and context_result.safe_to_continue
            and packet_result.safe_to_continue
            and personality_adapter_result.adapter_ready
            and memory_personality_adapter_result.adapter_ready
        )

        temp_report = Phase6PersonalityStrengtheningCompletionReport(
            status="completed" if personality_strengthening_completed else "blocked",
            phase="Phase6-15 Personality Strengthening Completion Report",
            completed_items=self.completed_items,
            missing_items=missing_items,
            personality_profile_ready=profile_result.personality_profile_ready,
            tone_profile_ready=tone_result.tone_profile_ready,
            emotion_state_ready=emotion_result.emotion_state_ready,
            personality_context_ready=context_result.safe_to_continue,
            personality_packet_ready=packet_result.safe_to_continue,
            personality_adapter_ready=personality_adapter_result.adapter_ready,
            memory_personality_adapter_ready=memory_personality_adapter_result.adapter_ready,
            name=profile_result.name,
            user_name=tone_result.user_name,
            primary_goal=profile_result.primary_goal,
            base_tone=tone_result.base_tone,
            mood=emotion_result.mood,
            personality_strengthening_completed=personality_strengthening_completed,
            conversation_engine_modified=False,
            auto_response_injection=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            next_phase="Phase7 Long-Term Memory Strengthening",
            report_path="",
            safe_to_continue=personality_strengthening_completed,
        )

        report_path = self.save_report(temp_report)
        temp_report.report_path = str(report_path)
        self._write_json(report_path, asdict(temp_report))

        return temp_report

    def save_report(self, report: Phase6PersonalityStrengtheningCompletionReport) -> Path:
        filename = f"phase6_personality_strengthening_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = self.report_dir / filename
        self._write_json(path, asdict(report))
        return path

    def print_report(self, report: Phase6PersonalityStrengtheningCompletionReport) -> None:
        print("=== Phase6-15 Personality Strengthening Completion Report ===")
        print(f"status: {report.status}")
        print(f"phase: {report.phase}")
        print(f"PersonalityProfileReady: {report.personality_profile_ready}")
        print(f"ToneProfileReady: {report.tone_profile_ready}")
        print(f"EmotionStateReady: {report.emotion_state_ready}")
        print(f"PersonalityContextReady: {report.personality_context_ready}")
        print(f"PersonalityPacketReady: {report.personality_packet_ready}")
        print(f"PersonalityAdapterReady: {report.personality_adapter_ready}")
        print(f"MemoryPersonalityAdapterReady: {report.memory_personality_adapter_ready}")
        print(f"Name: {report.name}")
        print(f"UserName: {report.user_name}")
        print(f"PrimaryGoal: {report.primary_goal}")
        print(f"BaseTone: {report.base_tone}")
        print(f"Mood: {report.mood}")
        print(f"PersonalityStrengtheningCompleted: {report.personality_strengthening_completed}")

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


def run_phase6_15_test() -> None:
    reporter = Phase6PersonalityStrengtheningCompletionReporter()
    report = reporter.build_report()
    reporter.print_report(report)


if __name__ == "__main__":
    run_phase6_15_test()