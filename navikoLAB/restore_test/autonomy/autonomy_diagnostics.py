from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOOP_DIR = ROOT / "navikoLAB" / "autonomy" / "loops"


class AutonomyDiagnostics:
    def run(self) -> dict:
        loops = list(LOOP_DIR.glob("self_improvement_loop_*.json")) if LOOP_DIR.exists() else []

        missing = []

        if not loops:
            missing.append("self_improvement_loop")

        return {
            "status": "passed" if not missing else "warning",
            "loop_count": len(loops),
            "missing": missing,
        }


def main() -> None:
    result = AutonomyDiagnostics().run()

    print("=== Autonomy Diagnostics ===")
    print(f"状態: {result['status']}")
    print(f"Loop数: {result['loop_count']}")
    print(f"不足候補: {len(result['missing'])}")

    for item in result["missing"]:
        print(f"- {item}")


if __name__ == "__main__":
    main()