from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOOP_DIR = ROOT / "navikoLAB" / "autonomy" / "loops"


class AutonomySafetyChecker:
    def run(self) -> dict:
        loop_files = list(LOOP_DIR.glob("self_improvement_loop_*.json")) if LOOP_DIR.exists() else []

        risks = []

        if not loop_files:
            risks.append("self_improvement_loop_missing")

        return {
            "status": "passed" if not risks else "warning",
            "loop_count": len(loop_files),
            "original_write_allowed": False,
            "auto_apply_allowed": False,
            "human_approval_required": True,
            "risks": risks,
        }


def main() -> None:
    result = AutonomySafetyChecker().run()

    print("=== Autonomy Safety Checker ===")
    print(f"状態: {result['status']}")
    print(f"Loop数: {result['loop_count']}")
    print(f"Original書込許可: {result['original_write_allowed']}")
    print(f"自動反映許可: {result['auto_apply_allowed']}")
    print(f"人間承認必須: {result['human_approval_required']}")
    print(f"Risk数: {len(result['risks'])}")

    for risk in result["risks"]:
        print(f"- {risk}")


if __name__ == "__main__":
    main()