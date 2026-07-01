from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List

from navikoLAB.memory.long_term_memory_index_reader import LongTermMemoryIndexReader


@dataclass
class LongTermMemorySearchHit:
    memory_id: str
    text: str
    importance: str
    score: int
    priority: int
    keywords: List[str]
    match_score: int
    match_reasons: List[str]
    safe_adopted: bool


@dataclass
class LongTermMemorySearchResult:
    status: str
    phase: str
    query: str
    index_file_found: bool
    index_item_count: int
    hit_count: int
    hits: List[Dict[str, Any]]
    memory_modified: bool
    auto_adoption: bool
    human_approval_required: bool
    safe_mode: bool
    external_ai: bool
    real_pc_operation: bool
    file_delete: bool
    safe_to_continue: bool


class LongTermMemorySearcher:
    def __init__(self, root_dir: str = "navikoLAB") -> None:
        self.root_dir = Path(root_dir)
        self.index_reader = LongTermMemoryIndexReader(root_dir=root_dir)

    def search(self, query: str) -> LongTermMemorySearchResult:
        index_result = self.index_reader.read_index()
        safe_query = query.strip()

        hits: List[LongTermMemorySearchHit] = []

        for item in index_result.items:
            hit = self._score_item(safe_query, item)
            if hit.match_score > 0:
                hits.append(hit)

        hits.sort(
            key=lambda item: (item.match_score, item.priority, item.score),
            reverse=True,
        )

        return LongTermMemorySearchResult(
            status="completed" if index_result.index_file_found else "blocked",
            phase="Phase7-4 Long-Term Memory Searcher",
            query=safe_query,
            index_file_found=index_result.index_file_found,
            index_item_count=index_result.item_count,
            hit_count=len(hits),
            hits=[asdict(hit) for hit in hits],
            memory_modified=False,
            auto_adoption=False,
            human_approval_required=True,
            safe_mode=True,
            external_ai=False,
            real_pc_operation=False,
            file_delete=False,
            safe_to_continue=index_result.safe_to_continue,
        )

    def _score_item(self, query: str, item: Dict[str, Any]) -> LongTermMemorySearchHit:
        text = str(item.get("text", ""))
        importance = str(item.get("importance", ""))
        score = self._to_int(item.get("score", 0))
        priority = self._to_int(item.get("priority", 0))

        raw_keywords = item.get("keywords", [])
        if not isinstance(raw_keywords, list):
            raw_keywords = []

        keywords = [str(keyword) for keyword in raw_keywords]

        match_score = 0
        match_reasons: List[str] = []

        if query and query in text:
            match_score += 5
            match_reasons.append("query_text_exact_match")

        for keyword in keywords:
            if keyword and keyword in query:
                match_score += 3
                match_reasons.append(f"query_contains_keyword:{keyword}")

            if keyword and keyword in text and keyword in query:
                match_score += 2
                match_reasons.append(f"text_keyword_match:{keyword}")

        query_tokens = self._split_query(query)
        for token in query_tokens:
            if token and token in text:
                match_score += 1
                match_reasons.append(f"token_match:{token}")

        if "目標" in query and ("第一目標" in text or "最優先" in text):
            match_score += 4
            match_reasons.append("goal_related_match")

        if "目的" in query and ("第一目標" in text or "最優先" in text):
            match_score += 4
            match_reasons.append("purpose_related_match")

        if "ナビ子" in query and "ナビ子" in text:
            match_score += 2
            match_reasons.append("naviko_match")

        if "会話" in query and "会話" in text:
            match_score += 2
            match_reasons.append("conversation_match")

        if "起動" in query and "起動" in text:
            match_score += 2
            match_reasons.append("startup_match")

        if match_score > 0 and importance == "high":
            match_score += 1
            match_reasons.append("high_importance_bonus")

        return LongTermMemorySearchHit(
            memory_id=str(item.get("memory_id", "")),
            text=text,
            importance=importance,
            score=score,
            priority=priority,
            keywords=keywords,
            match_score=match_score,
            match_reasons=match_reasons,
            safe_adopted=bool(item.get("safe_adopted", False)),
        )

    def _split_query(self, query: str) -> List[str]:
        separators = [" ", "　", "、", "。", "？", "?", "！", "!", "・", "\n", "\t"]

        tokens = [query]

        for separator in separators:
            next_tokens: List[str] = []
            for token in tokens:
                next_tokens.extend(token.split(separator))
            tokens = next_tokens

        return [
            token.strip()
            for token in tokens
            if token.strip()
        ]

    def print_result(self, result: LongTermMemorySearchResult) -> None:
        print("=== Phase7-4 Long-Term Memory Searcher ===")
        print(f"status: {result.status}")
        print(f"phase: {result.phase}")
        print(f"Query: {result.query}")
        print(f"IndexFileFound: {result.index_file_found}")
        print(f"IndexItemCount: {result.index_item_count}")
        print(f"HitCount: {result.hit_count}")
        print(f"MemoryModified: {result.memory_modified}")
        print(f"AutoAdoption: {result.auto_adoption}")
        print(f"HumanApprovalRequired: {result.human_approval_required}")

        print("")
        print("[Search Hits]")
        if not result.hits:
            print("- 該当なし")
        else:
            for index, hit in enumerate(result.hits, start=1):
                print(f"- Hit {index}")
                print(f"  memory_id: {hit.get('memory_id', '')}")
                print(f"  text: {hit.get('text', '')}")
                print(f"  importance: {hit.get('importance', '')}")
                print(f"  score: {hit.get('score', 0)}")
                print(f"  priority: {hit.get('priority', 0)}")
                print(f"  match_score: {hit.get('match_score', 0)}")
                print(f"  match_reasons: {hit.get('match_reasons', [])}")
                print(f"  safe_adopted: {hit.get('safe_adopted', False)}")

        print("")
        print(f"SafeMode: {result.safe_mode}")
        print(f"ExternalAI: {result.external_ai}")
        print(f"RealPCOperation: {result.real_pc_operation}")
        print(f"FileDelete: {result.file_delete}")
        print(f"SafeToContinue: {result.safe_to_continue}")

    def to_dict(self, result: LongTermMemorySearchResult) -> Dict[str, Any]:
        return asdict(result)

    def _to_int(self, value: Any) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0


def run_phase7_4_test() -> None:
    searcher = LongTermMemorySearcher()

    result = searcher.search(
        query="ナビ子の第一目標と自然な会話"
    )

    searcher.print_result(result)


if __name__ == "__main__":
    run_phase7_4_test()