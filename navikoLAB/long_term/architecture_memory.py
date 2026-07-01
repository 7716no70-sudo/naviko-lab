from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LONG_TERM_DIR = ROOT / "navikoLAB" / "long_term"
ARCHITECTURE_DIR = LONG_TERM_DIR / "architecture_memory"


class ArchitectureMemory:
    def __init__(self) -> None:
        ARCHITECTURE_DIR.mkdir(parents=True, exist_ok=True)

    def build_memory(self) -> dict:
        return {
            "status": "completed",
            "architecture_name": "Naviko Autonomous AI Orchestration Architecture",
            "layers": [
                "Mission",
                "Planning",
                "Capability",
                "Connector",
                "Search",
                "Knowledge",
                "Experience",
                "Reflection",
                "Improvement",
                "OriginalAdoption",
            ],
            "principles": [
                "LABで実験する",
                "Originalを直接自動変更しない",
                "人間承認を必須にする",
                "小さな独立モジュールで追加する",
                "CompletionReportで工程を閉じる",
            ],
            "safety_policy": {
                "auto_apply_allowed": False,
                "original_write_allowed": False,
                "human_approval_required": True,
            },
            "generated_at": datetime.now().isoformat(timespec="seconds"),
        }

    def save(self, memory: dict) -> Path:
        output = ARCHITECTURE_DIR / f"architecture_memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output.write_text(json.dumps(memory, ensure_ascii=False, indent=2), encoding="utf-8")
        return output

    def run(self) -> dict:
        memory = self.build_memory()
        output = self.save(memory)

        return {
            "status": memory["status"],
            "layer_count": len(memory["layers"]),
            "principle_count": len(memory["principles"]),
            "output": str(output),
        }


def main() -> None:
    result = ArchitectureMemory().run()

    print("=== ArchitectureMemory ===")
    print(f"状態: {result['status']}")
    print(f"Layer数: {result['layer_count']}")
    print(f"Principle数: {result['principle_count']}")
    print(f"保存先: {result['output']}")


if __name__ == "__main__":
    main()