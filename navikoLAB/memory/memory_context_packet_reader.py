from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class MemoryContextPacketReadResult:
    status: str
    phase: str
    packet_file_found: bool
    packet_path: str
    created_at: str
    purpose: str
    injection_mode: str
    auto_response_injection: bool
    reference_line_count: int
    memory_reference_lines: List[str]
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class MemoryContextPacketReader:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.memory_dir = self.root_dir / "memory"
        self.injection_dir = self.memory_dir / "injection_packets"
        self.latest_packet_path = self.injection_dir / "latest_memory_context_safe_packet.json"

        self.injection_dir.mkdir(parents=True, exist_ok=True)

    def read_latest_packet(self) -> MemoryContextPacketReadResult:
        packet_file_found = self.latest_packet_path.exists()
        data = self._read_json(self.latest_packet_path)

        lines = data.get("memory_reference_lines", [])
        if not isinstance(lines, list):
            lines = []

        safe_lines = [str(line) for line in lines]

        return MemoryContextPacketReadResult(
            status="completed" if packet_file_found else "blocked",
            phase="Phase5-12 Memory Context Packet Reader",
            packet_file_found=packet_file_found,
            packet_path=str(self.latest_packet_path),
            created_at=str(data.get("created_at", "")),
            purpose=str(data.get("purpose", "")),
            injection_mode=str(data.get("injection_mode", "reference_only")),
            auto_response_injection=bool(data.get("auto_response_injection", False)),
            reference_line_count=len(safe_lines),
            memory_reference_lines=safe_lines,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=packet_file_found,
        )

    def print_result(self, result: MemoryContextPacketReadResult) -> None:
        print("=== Phase5-12 Memory Context Packet Reader ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"PacketFileFound: {result.packet_file_found}")
        print(f"PacketPath: {result.packet_path}")
        print(f"CreatedAt: {result.created_at}")
        print(f"Purpose: {result.purpose}")
        print(f"InjectionMode: {result.injection_mode}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")
        print(f"ReferenceLineCount: {result.reference_line_count}")

        print("")
        print("[Memory Reference Lines]")
        if not result.memory_reference_lines:
            print("- なし")
        else:
            for index, line in enumerate(result.memory_reference_lines, start=1):
                print(f"- {index}: {line}")

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: MemoryContextPacketReadResult) -> Dict[str, Any]:
        return asdict(result)

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


def run_phase5_12_test() -> None:
    reader = MemoryContextPacketReader()
    result = reader.read_latest_packet()
    reader.print_result(result)


if __name__ == "__main__":
    run_phase5_12_test()