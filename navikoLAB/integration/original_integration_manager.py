from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INTEGRATION_DIR = ROOT / "navikoLAB" / "integration"
REPORT_DIR = ROOT / "navikoLAB" / "integration" / "reports"

MODULE_CHECKS = {
    "MissionManager": [
        "navikoLAB/mission",
        "navikoLAB/missions",
        "navikoLAB/mission_manager",
        "navikoLAB/managers",
    ],
    "TaskPlanner": [
        "navikoLAB/task_planner.py",
        "navikoLAB/action_planner.py",
        "navikoLAB/planners",
        "navikoLAB/planner",
        "navikoLAB/task_planner",
        "navikoLAB/task",
    ],
    "CapabilityRouter": [
        "navikoLAB/capabilities",
    ],
    "ConnectorDispatcher": [
        "navikoLAB/connectors",
    ],
    "SearchDispatcher": [
        "navikoLAB/research",
        "navikoLAB/search",
    ],
    "DeepSearchEngine": [
        "navikoLAB/research",
        "navikoLAB/deep_search",
        "navikoLAB/search",
    ],
    "KnowledgeBase": [
        "navikoLAB/knowledge",
    ],
    "ExperienceManager": [
        "navikoLAB/experience",
    ],
    "KnowledgeReflection": [
        "navikoLAB/reflection",
        "navikoLAB/knowledge_reflection",
    ],
    "AutoImprovementSuggestion": [
        "navikoLAB/improvement_suggestions",
    ],
    "AutoRefactoringPlan": [
        "navikoLAB/refactoring_plans",
    ],
}


class OriginalIntegrationManager:
    def __init__(self) -> None:
        INTEGRATION_DIR.mkdir(parents=True, exist_ok=True)
        REPORT_DIR.mkdir(parents=True, exist_ok=True)

    def check_modules(self) -> dict:
        results = {}

        for name, relative_paths in MODULE_CHECKS.items():
            checked_paths = [
                ROOT / relative_path
                for relative_path in relative_paths
            ]

            existing_paths = [
                path
                for path in checked_paths
                if path.exists()
            ]

            results[name] = {
                "paths": [str(path) for path in checked_paths],
                "matched_path": str(existing_paths[0]) if existing_paths else None,
                "exists": bool(existing_paths),
            }

        return results

    def build_integration_map(self, module_results: dict) -> dict:
        pipeline = [
            "MissionManager",
            "TaskPlanner",
            "CapabilityRouter",
            "ConnectorDispatcher",
            "SearchDispatcher",
            "DeepSearchEngine",
            "KnowledgeBase",
            "ExperienceManager",
            "KnowledgeReflection",
            "AutoImprovementSuggestion",
            "AutoRefactoringPlan",
            "OriginalNaviko",
        ]

        missing = [
            name
            for name, info in module_results.items()
            if not info.get("exists")
        ]

        return {
            "status": "ready" if not missing else "partial",
            "pipeline": pipeline,
            "module_count": len(module_results),
            "missing": missing,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

    def save(self, integration_map: dict, module_results: dict) -> Path:
        output = REPORT_DIR / f"original_integration_map_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        data = {
            "stage": "第32工程 Original Naviko統合",
            "integration_map": integration_map,
            "modules": module_results,
        }

        output.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return output

    def run(self) -> dict:
        module_results = self.check_modules()
        integration_map = self.build_integration_map(module_results)
        output = self.save(integration_map, module_results)

        return {
            "status": integration_map["status"],
            "module_count": integration_map["module_count"],
            "missing_count": len(integration_map["missing"]),
            "missing": integration_map["missing"],
            "output": str(output),
        }


def main() -> None:
    result = OriginalIntegrationManager().run()

    print("=== OriginalIntegrationManager ===")
    print(f"状態: {result['status']}")
    print(f"確認Module数: {result['module_count']}")
    print(f"不足Module数: {result['missing_count']}")

    for item in result["missing"]:
        print(f"- {item}")

    print(f"保存先: {result['output']}")


if __name__ == "__main__":
    main()