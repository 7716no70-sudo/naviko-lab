from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CHECK_TARGETS = {
    "Mission": ["navikoLAB/mission", "navikoLAB/missions", "navikoLAB/mission_manager"],
    "TaskPlanner": ["navikoLAB/task_planner.py", "navikoLAB/action_planner.py"],
    "Capabilities": ["navikoLAB/capabilities"],
    "Connectors": ["navikoLAB/connectors"],
    "Research": ["navikoLAB/research"],
    "Knowledge": ["navikoLAB/knowledge"],
    "Experience": ["navikoLAB/experience"],
    "Analyzers": ["navikoLAB/analyzers"],
    "Documentation": ["navikoLAB/docs"],
    "Improvement": ["navikoLAB/improvement_suggestions", "navikoLAB/refactoring_plans"],
    "Integration": ["navikoLAB/integration"],
    "Autonomy": ["navikoLAB/autonomy"],
    "LongTerm": ["navikoLAB/long_term"],
}


class FinalIntegrationDiagnostics:
    def run(self) -> dict:
        results = {}
        missing = []

        for name, candidates in CHECK_TARGETS.items():
            matched = None

            for candidate in candidates:
                path = ROOT / candidate
                if path.exists():
                    matched = str(path)
                    break

            exists = matched is not None
            results[name] = {
                "exists": exists,
                "matched_path": matched,
                "candidates": [str(ROOT / candidate) for candidate in candidates],
            }

            if not exists:
                missing.append(name)

        return {
            "status": "passed" if not missing else "warning",
            "target_count": len(CHECK_TARGETS),
            "passed_count": len(CHECK_TARGETS) - len(missing),
            "missing_count": len(missing),
            "missing": missing,
            "results": results,
        }


def main() -> None:
    result = FinalIntegrationDiagnostics().run()

    print("=== Final Integration Diagnostics ===")
    print(f"状態: {result['status']}")
    print(f"確認項目数: {result['target_count']}")
    print(f"通過数: {result['passed_count']}")
    print(f"不足数: {result['missing_count']}")

    for item in result["missing"]:
        print(f"- {item}")


if __name__ == "__main__":
    main()