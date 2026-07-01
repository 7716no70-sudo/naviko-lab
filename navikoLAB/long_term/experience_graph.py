from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LONG_TERM_DIR = ROOT / "navikoLAB" / "long_term"
GRAPH_DIR = LONG_TERM_DIR / "graphs"


class ExperienceGraph:
    def __init__(self) -> None:
        GRAPH_DIR.mkdir(parents=True, exist_ok=True)

    def build_graph(self) -> dict:
        nodes = [
            {"id": "execution", "type": "experience", "label": "Execution"},
            {"id": "success", "type": "experience", "label": "Success"},
            {"id": "failure", "type": "experience", "label": "Failure"},
            {"id": "diagnostics", "type": "experience", "label": "Diagnostics"},
            {"id": "safety", "type": "experience", "label": "Safety"},
            {"id": "learning", "type": "experience", "label": "Learning"},
        ]

        edges = [
            {"from": "execution", "to": "success", "relation": "may_result_in"},
            {"from": "execution", "to": "failure", "relation": "may_result_in"},
            {"from": "failure", "to": "diagnostics", "relation": "requires"},
            {"from": "diagnostics", "to": "safety", "relation": "checks"},
            {"from": "success", "to": "learning", "relation": "creates"},
            {"from": "failure", "to": "learning", "relation": "creates"},
        ]

        return {
            "status": "completed",
            "graph_type": "experience_graph",
            "node_count": len(nodes),
            "edge_count": len(edges),
            "nodes": nodes,
            "edges": edges,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
        }

    def save(self, graph: dict) -> Path:
        output = GRAPH_DIR / f"experience_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
    result = ExperienceGraph().run()

    print("=== ExperienceGraph ===")
    print(f"状態: {result['status']}")
    print(f"Node数: {result['node_count']}")
    print(f"Edge数: {result['edge_count']}")
    print(f"保存先: {result['output']}")


if __name__ == "__main__":
    main()