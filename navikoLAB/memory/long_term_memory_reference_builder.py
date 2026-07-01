from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.memory.long_term_memory_searcher import LongTermMemorySearcher


@dataclass
class LongTermMemoryReferenceBuildResult:
    status: str
    phase: str
    query: str
    search_ready: bool
    hit_count: int
    reference_block_created: bool
    reference_block: Dict[str, Any]
    memory_modified: bool
    auto_adoption: bool
    human_approval_required: bool
    auto_response_injection: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class LongTermMemoryReferenceBuilder:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.searcher = LongTermMemorySearcher(root_dir=root_dir)

    def build_reference(self, query: str) -> LongTermMemoryReferenceBuildResult:
        search_result = self.searcher.search(query=query)

        safe_hits = [
            hit for hit in search_result.hits
            if isinstance(hit, dict) and bool(hit.get("safe_adopted", False))
        ]

        reference_lines: List[str] = []

        for hit in safe_hits:
            text = str(hit.get("text", "")).strip()
            if not text:
                continue

            reference_lines.append(
                f"長期記憶参照: {text}"
            )

        reference_block = {
            "source": "LongTermMemoryReferenceBuilder",
            "mode": "reference_only",
            "query": query,
            "safe_to_use": search_result.safe_to_continue,
            "hit_count": len(safe_hits),
            "reference_line_count": len(reference_lines),
            "reference_lines": reference_lines,
            "hits": safe_hits,
            "memory_modified": False,
            "auto_adoption": False,
            "human_approval_required": True,
            "auto_response_injection": False,
            "instruction": (
                "これはConversationEngine用の長期記憶参照ブロックです。"
                "返答へ強制注入せず、自然な会話や第一目標維持に必要な場合だけ参照します。"
            ),
        }

        reference_block_created = search_result.safe_to_continue

        return LongTermMemoryReferenceBuildResult(
            status="completed" if reference_block_created else "blocked",
            phase="Phase7-5 Long-Term Memory Reference Builder",
            query=query,
            search_ready=search_result.safe_to_continue,
            hit_count=len(safe_hits),
            reference_block_created=reference_block_created,
            reference_block=reference_block,
            memory_modified=False,
            auto_adoption=False,
            human_approval_required=True,
            auto_response_injection=False,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=reference_block_created,
        )

    def print_result(self, result: LongTermMemoryReferenceBuildResult) -> None:
        print("=== Phase7-5 Long-Term Memory Reference Builder ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"Query: {result.query}")
        print(f"SearchReady: {result.search_ready}")
        print(f"HitCount: {result.hit_count}")
        print(f"ReferenceBlockCreated: {result.reference_block_created}")
        print(f"MemoryModified: {result.memory_modified}")
        print(f"AutoAdoption: {result.auto_adoption}")
        print(f"HumanApprovalRequired: {result.human_approval_required}")
        print(f"AutoResponseInjection: {result.auto_response_injection}")

        print("")
        print("[Reference Lines]")
        lines = result.reference_block.get("reference_lines", [])
        if not isinstance(lines, list) or not lines:
            print("- なし")
        else:
            for index, line in enumerate(lines, start=1):
                print(f"- {index}: {line}")

        print("")
        print("[Instruction]")
        print(result.reference_block.get("instruction", ""))

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: LongTermMemoryReferenceBuildResult) -> Dict[str, Any]:
        return asdict(result)


def run_phase7_5_test() -> None:
    builder = LongTermMemoryReferenceBuilder()

    result = builder.build_reference(
        query="ナビ子の第一目標と自然な会話"
    )

    builder.print_result(result)


if __name__ == "__main__":
    run_phase7_5_test()