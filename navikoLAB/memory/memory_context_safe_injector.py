from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.memory.memory_context_injection_preview import MemoryContextInjectionPreview


@dataclass
class MemoryContextSafeInjectionPacket:
    created_at: str
    purpose: str
    injection_mode: str
    auto_response_injection: bool
    memory_reference_lines: List[str]
    instruction: str


@dataclass
class MemoryContextSafeInjectorResult:
    status: str
    phase: str
    packet_created: bool
    packet_path: str
    reference_line_count: int
    injection_mode: str
    auto_response_injection: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class MemoryContextSafeInjector:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_dir = self.root_dir / "memory"
        self.injection_dir = self.memory_dir / "injection_packets"

        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.injection_dir.mkdir(parents=True, exist_ok=True)

        self.preview_builder = MemoryContextInjectionPreview(root_dir=root_dir)

    def build_safe_injection_packet(self) -> MemoryContextSafeInjectorResult:
        preview_result = self.preview_builder.build_preview()

        packet = MemoryContextSafeInjectionPacket(
            created_at=datetime.now().isoformat(timespec="seconds"),
            purpose="ナビ子が自然な会話を行うための安全な記憶参照データ",
            injection_mode="reference_only",
            auto_response_injection=False,
            memory_reference_lines=preview_result.injection_preview,
            instruction=(
                "このデータは会話応答の参考情報です。"
                "返答へ強制注入せず、自然な会話に必要な場合だけ参照します。"
            ),
        )

        packet_path = self._save_packet(packet)

        return MemoryContextSafeInjectorResult(
            status="completed" if preview_result.context_available else "blocked",
            phase="Phase5-11 Memory Context Safe Injector",
            packet_created=preview_result.context_available,
            packet_path=str(packet_path),
            reference_line_count=len(packet.memory_reference_lines),
            injection_mode=packet.injection_mode,
            auto_response_injection=packet.auto_response_injection,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=preview_result.safe_to_continue,
        )

    def _save_packet(self, packet: MemoryContextSafeInjectionPacket) -> Path:
        filename = f"memory_context_safe_packet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = self.injection_dir / filename

        packet_data = asdict(packet)

        with path.open("w", encoding="utf-8") as f:
            json.dump(packet_data, f, ensure_ascii=False, indent=2)

        latest_path = self.injection_dir / "latest_memory_context_safe_packet.json"
        with latest_path.open("w", encoding="utf-8") as f:
            json.dump(packet_data, f, ensure_ascii=False, indent=2)

        return path

    def print_result(self, result: MemoryContextSafeInjectorResult) -> None:
        print("=== Phase5-11 Memory Context Safe Injector ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"PacketCreated: {result.packet_created}")
        print(f"PacketPath: {result.packet_path}")
        print(f"ReferenceLineCount: {result.reference_line_count}")
        print(f"InjectionMode: {result.injection_mode}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: MemoryContextSafeInjectorResult) -> Dict[str, Any]:
        return asdict(result)


def run_phase5_11_test() -> None:
    injector = MemoryContextSafeInjector()
    result = injector.build_safe_injection_packet()
    injector.print_result(result)


if __name__ == "__main__":
    run_phase5_11_test()