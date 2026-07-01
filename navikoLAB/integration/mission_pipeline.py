from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PIPELINE_DIR = ROOT / "navikoLAB" / "integration" / "pipelines"


class MissionPipeline:
    def __init__(self) -> None:
        PIPELINE_DIR.mkdir(parents=True, exist_ok=True)

    def build_pipeline(self, mission: str) -> dict:
        steps = [
            {
                "step": 1,
                "name": "MissionManager",
                "purpose": "ユーザー目的をMissionとして整理する。",
                "input": mission,
                "output": "mission_object",
            },
            {
                "step": 2,
                "name": "TaskPlanner",
                "purpose": "Missionを実行可能なタスクへ分解する。",
                "input": "mission_object",
                "output": "task_plan",
            },
            {
                "step": 3,
                "name": "CapabilityRouter",
                "purpose": "必要なCapabilityを選択する。",
                "input": "task_plan",
                "output": "capability_selection",
            },
            {
                "step": 4,
                "name": "ConnectorDispatcher",
                "purpose": "Capabilityに対応するConnectorへ処理を振り分ける。",
                "input": "capability_selection",
                "output": "connector_result",
            },
            {
                "step": 5,
                "name": "SearchDispatcher",
                "purpose": "必要に応じて検索処理へ接続する。",
                "input": "connector_result",
                "output": "search_result",
            },
            {
                "step": 6,
                "name": "DeepSearchEngine",
                "purpose": "検索結果を深掘りして要約・構造化する。",
                "input": "search_result",
                "output": "deep_search_summary",
            },
            {
                "step": 7,
                "name": "KnowledgeBase",
                "purpose": "得られた知識を保存する。",
                "input": "deep_search_summary",
                "output": "knowledge_record",
            },
            {
                "step": 8,
                "name": "ExperienceManager",
                "purpose": "実行経験として保存する。",
                "input": "knowledge_record",
                "output": "experience_record",
            },
            {
                "step": 9,
                "name": "KnowledgeReflection",
                "purpose": "知識と経験から振り返りを行う。",
                "input": "experience_record",
                "output": "reflection_result",
            },
            {
                "step": 10,
                "name": "AutoImprovementSuggestion",
                "purpose": "改善候補を生成する。",
                "input": "reflection_result",
                "output": "improvement_suggestion",
            },
            {
                "step": 11,
                "name": "AutoRefactoringPlan",
                "purpose": "改善候補から改修計画を作る。",
                "input": "improvement_suggestion",
                "output": "refactoring_plan",
            },
            {
                "step": 12,
                "name": "OriginalNaviko",
                "purpose": "安全確認後、オリジナルナビ子へ反映候補として渡す。",
                "input": "refactoring_plan",
                "output": "original_adoption_candidate",
            },
        ]

        return {
            "status": "simulation_completed",
            "mode": "safe_pipeline_simulation",
            "mission": mission,
            "step_count": len(steps),
            "steps": steps,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
        }

    def save(self, pipeline: dict) -> Path:
        output = PIPELINE_DIR / f"mission_pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        output.write_text(
            json.dumps(pipeline, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return output

    def run(self, mission: str) -> dict:
        pipeline = self.build_pipeline(mission)
        output = self.save(pipeline)

        return {
            "status": pipeline["status"],
            "mode": pipeline["mode"],
            "mission": mission,
            "step_count": pipeline["step_count"],
            "output": str(output),
        }


def main() -> None:
    mission = "TODOアプリを作りたい"
    result = MissionPipeline().run(mission)

    print("=== MissionPipeline ===")
    print(f"状態: {result['status']}")
    print(f"Mode: {result['mode']}")
    print(f"Mission: {result['mission']}")
    print(f"Step数: {result['step_count']}")
    print(f"保存先: {result['output']}")


if __name__ == "__main__":
    main()