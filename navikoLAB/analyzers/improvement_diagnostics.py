from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SUGGESTION_DIR = ROOT / "navikoLAB" / "improvement_suggestions"
PLAN_DIR = ROOT / "navikoLAB" / "refactoring_plans"
REFLECTION_DIR = ROOT / "navikoLAB" / "architecture_reflection"


class ImprovementDiagnostics:
    def run(self) -> dict:
        suggestions = list(SUGGESTION_DIR.glob("auto_improvement_suggestions_*.json")) if SUGGESTION_DIR.exists() else []
        plans = list(PLAN_DIR.glob("auto_refactoring_plan_*.json")) if PLAN_DIR.exists() else []
        reflections = list(REFLECTION_DIR.glob("architecture_reflection_*.json")) if REFLECTION_DIR.exists() else []

        missing = []

        if not suggestions:
            missing.append("auto_improvement_suggestions")

        if not plans:
            missing.append("auto_refactoring_plan")

        if not reflections:
            missing.append("architecture_reflection")

        return {
            "status": "passed" if not missing else "warning",
            "suggestion_count": len(suggestions),
            "plan_count": len(plans),
            "reflection_count": len(reflections),
            "missing": missing,
        }


def main() -> None:
    result = ImprovementDiagnostics().run()

    print("=== Improvement Diagnostics ===")
    print(f"状態: {result['status']}")
    print(f"改善候補数: {result['suggestion_count']}")
    print(f"計画数: {result['plan_count']}")
    print(f"設計反省数: {result['reflection_count']}")
    print(f"不足候補: {len(result['missing'])}")

    for item in result["missing"]:
        print(f"- {item}")


if __name__ == "__main__":
    main()