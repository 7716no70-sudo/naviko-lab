from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT_DIR = ROOT / "navikoLAB" / "finalization" / "safety_audits"


class FinalSafetyDiagnostics:
    def run(self) -> dict:
        audits = list(AUDIT_DIR.glob("final_safety_audit_*.json")) if AUDIT_DIR.exists() else []

        missing = []

        if not audits:
            missing.append("final_safety_audit")

        return {
            "status": "passed" if not missing else "warning",
            "audit_count": len(audits),
            "missing": missing,
        }


def main() -> None:
    result = FinalSafetyDiagnostics().run()

    print("=== Final Safety Diagnostics ===")
    print(f"状態: {result['status']}")
    print(f"Audit数: {result['audit_count']}")
    print(f"不足候補: {len(result['missing'])}")

    for item in result["missing"]:
        print(f"- {item}")


if __name__ == "__main__":
    main()