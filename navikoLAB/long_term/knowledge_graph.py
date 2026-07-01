from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LONG_TERM_DIR = ROOT / "navikoLAB" / "long_term"
GRAPH_DIR = LONG_TERM_DIR / "graphs"


class KnowledgeGraph:
    def __init__(self) -> None:
        GRAPH_DIR.mkdir(parents=True, exist_ok=True)

    def build_graph(self) -> dict:
        nodes = [
            {"id": "mission", "type": "concept", "label": "Mission"},
            {"id": "research", "type": "concept", "label": "Research"},
            {"id": "search", "type": "concept", "label": "Search"},
            {"id": "knowledge", "type": "concept", "label": "Knowledge"},
            {"id": "reflection", "type": "concept", "label": "Reflection"},
            {"id": "improvement", "type": "concept", "label": "Improvement"},
        ]

        edges = [
            {"from": "mission", "to": "research", "relation": "drives"},
            {"from": "research", "to": "search", "relation": "uses"},
            {"from": "search", "to": "knowledge", "relation": "creates"},
            {"from": "knowledge", "to": "reflection", "relation": "supports"},
            {"from": "reflection", "to": "improvement", "relation": "generates"},
        ]

        return {
            "status": "completed",
            "graph_type": "knowledge_graph",
            "node_count": len(nodes),
            "edge_count": len(edges),
            "nodes": nodes,
            "edges": edges,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
        }

    def save(self, graph: dict) -> Path:
        output = GRAPH_DIR / f"knowledge_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
        return output

    def run(self) -> dict:
        graph = self.build_graph()
        output = self.save(graph)

        return {
            "status": graph["status"],
            "node_count": graph["node_count"],
            "edge_count": graph["edge_count"],
            "output": str(output),
        }


def main() -> None:
    result = KnowledgeGraph().run()

    print("=== KnowledgeGraph ===")
    print(f"状態: {result['status']}")
    print(f"Node数: {result['node_count']}")
    print(f"Edge数: {result['edge_count']}")
    print(f"保存先: {result['output']}")


if __name__ == "__main__":
    main()