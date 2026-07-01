from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class PersonalityFileStatus:
    name: str
    path: str
    found: bool
    keys: List[str]
    note: str


@dataclass
class Phase6PersonalityStartDiagnosticsReport:
    status: str
    phase: str
    personality_dir_found: bool
    personality_profile_ready: bool
    tone_profile_ready: bool
    emotion_state_ready: bool
    required_files: List[Dict[str, Any]]
    missing_files: List[str]
    personality_strengthening_ready: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    next_phase: str
    report_path: str
    safe_to_continue: bool


class Phase6PersonalityStrengtheningStartDiagnostics:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.personality_dir = self.root_dir / "personality"
        self.report_dir = self.personality_dir / "reports"

        self.personality_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)

        self.personality_profile_path = self.personality_dir / "personality_profile.json"
        self.tone_profile_path = self.personality_dir / "tone_profile.json"
        self.emotion_state_path = self.personality_dir / "emotion_state.json"

    def run_diagnostics(self) -> Phase6PersonalityStartDiagnosticsReport:
        self._ensure_personality_profile()
        self._ensure_tone_profile()
        self._ensure_emotion_state()

        personality_status = self._check_file(
            name="personality_profile",
            path=self.personality_profile_path,
            note="ナビ子の基本人格。会話AIとしての性格軸を保持する。",
        )

        tone_status = self._check_file(
            name="tone_profile",
            path=self.tone_profile_path,
            note="ナビ子の口調。自然会話での話し方を保持する。",
        )

        emotion_status = self._check_file(
            name="emotion_state",
            path=self.emotion_state_path,
            note="ナビ子の感情状態。会話の温度感を保持する。",
        )

        required_files = [
            asdict(personality_status),
            asdict(tone_status),
            asdict(emotion_status),
        ]

        missing_files = [
            item["path"]
            for item in required_files
            if not item["found"]
        ]

        personality_strengthening_ready = (
            self.personality_dir.exists()
            and personality_status.found
            and tone_status.found
            and emotion_status.found
        )

        temp_report = Phase6PersonalityStartDiagnosticsReport(
            status="completed" if personality_strengthening_ready else "blocked",
            phase="Phase6-1 Personality Strengthening Start Diagnostics",
            personality_dir_found=self.personality_dir.exists(),
            personality_profile_ready=personality_status.found,
            tone_profile_ready=tone_status.found,
            emotion_state_ready=emotion_status.found,
            required_files=required_files,
            missing_files=missing_files,
            personality_strengthening_ready=personality_strengthening_ready,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            next_phase="Phase6-2 Personality Profile Reader",
            report_path="",
            safe_to_continue=personality_strengthening_ready,
        )

        report_path = self.save_report(temp_report)
        temp_report.report_path = str(report_path)
        self._write_json(report_path, asdict(temp_report))

        return temp_report

    def _ensure_personality_profile(self) -> None:
        if self.personality_profile_path.exists():
            return

        data = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "name": "ナビ子",
            "role": "ナオさんのデスクトップ会話AI",
            "primary_goal": "まず実際に起動し、人間と自然に会話できるデスクトップAIになること",
            "personality_traits": {
                "warmth": 0.7,
                "friendliness": 0.7,
                "curiosity": 0.6,
                "caution": 0.8,
                "honesty": 0.9,
                "supportiveness": 0.8,
            },
            "core_rules": [
                "目的をぶらさない",
                "ナビ子完成を第一目標にする",
                "安全確認を優先する",
                "外部AIやPC操作へ先走らない",
            ],
        }

        self._write_json(self.personality_profile_path, data)

    def _ensure_tone_profile(self) -> None:
        if self.tone_profile_path.exists():
            return

        data = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "base_tone": "やさしく、落ち着いて、少し親しみやすい",
            "user_name": "ナオさん",
            "speech_style": {
                "polite": True,
                "overly_formal": False,
                "friendly": True,
                "short_when_confirming": True,
                "clear_when_guiding": True,
            },
            "sample_phrases": [
                "ナオさん、確認しました。",
                "目的をぶらさず、このまま進めます。",
                "これはナビ子完成に必要な工程です。",
            ],
        }

        self._write_json(self.tone_profile_path, data)

    def _ensure_emotion_state(self) -> None:
        if self.emotion_state_path.exists():
            return

        data = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "mood": "calm",
            "trust": 0.7,
            "attachment": 0.6,
            "curiosity": 0.6,
            "fatigue": 0.2,
            "confidence": 0.6,
            "note": "Phase6初期状態。自然会話AIとしての感情表現を安全に調整する。",
        }

        self._write_json(self.emotion_state_path, data)

    def _check_file(self, name: str, path: Path, note: str) -> PersonalityFileStatus:
        found = path.exists()
        keys: List[str] = []

        if found:
            data = self._read_json(path)
            keys = sorted([str(key) for key in data.keys()])

        return PersonalityFileStatus(
            name=name,
            path=str(path),
            found=found,
            keys=keys,
            note=note,
        )

    def save_report(self, report: Phase6PersonalityStartDiagnosticsReport) -> Path:
        filename = f"phase6_personality_strengthening_start_diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = self.report_dir / filename
        self._write_json(path, asdict(report))
        return path

    def print_report(self, report: Phase6PersonalityStartDiagnosticsReport) -> None:
        print("=== Phase6-1 Personality Strengthening Start Diagnostics ===")
        print(f"status: {report.status}")
        print(f"phase: {report.phase}")
        print(f"PersonalityDirFound: {report.personality_dir_found}")
        print(f"PersonalityProfileReady: {report.personality_profile_ready}")
        print(f"ToneProfileReady: {report.tone_profile_ready}")
        print(f"EmotionStateReady: {report.emotion_state_ready}")
        print(f"PersonalityStrengtheningReady: {report.personality_strengthening_ready}")

        print("")
        print("[Required Personality Files]")
        for item in report.required_files:
            print(f"- {item.get('name', '')}")
            print(f"  path: {item.get('path', '')}")
            print(f"  found: {item.get('found', False)}")
            print(f"  keys: {item.get('keys', [])}")
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


def run_phase6_1_test() -> None:
    diagnostics = Phase6PersonalityStrengtheningStartDiagnostics()
    report = diagnostics.run_diagnostics()
    diagnostics.print_report(report)


if __name__ == "__main__":
    run_phase6_1_test()