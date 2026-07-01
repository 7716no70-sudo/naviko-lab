# navikoLAB/stable_life/stable_life_final_diagnostics.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class StableLifeFinalDiagnostics:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.full_system_report_path = (
            self.root / "stable_life" / "reports"
            / "stable_life_full_system_report_latest.json"
        )

        self.runtime_unified_report_path = (
            self.root / "stable_life" / "reports"
            / "stable_life_runtime_unified_report_latest.json"
        )

        self.interaction_unified_report_path = (
            self.root / "stable_life" / "reports"
            / "stable_life_interaction_layer_unified_report_latest.json"
        )

        self.output_dir = self.root / "stable_life" / "diagnostics"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_path = self.output_dir / "stable_life_final_diagnostics_report.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def _read_json(self, path: Path) -> tuple[bool, dict[str, Any]]:
        if not path.exists():
            return False, {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return isinstance(data, dict), data if isinstance(data, dict) else {}
        except Exception:
            return False, {}

    def run(self) -> dict[str, Any]:
        full_found, full = self._read_json(self.full_system_report_path)
        runtime_found, runtime = self._read_json(self.runtime_unified_report_path)
        interaction_found, interaction = self._read_json(self.interaction_unified_report_path)

        final_diagnostics_passed = all([
            full_found,
            runtime_found,
            interaction_found,
            full.get("StableLifeFullSystemCompleted") is True,
            runtime.get("StableLifeRuntimeUnified") is True,
            interaction.get("InteractionLayerUnified") is True,
            full.get("NoRealExternalOperation") is True,
            full.get("NoRealFileDelete") is True,
            full.get("NoDangerousAutoPatch") is True,
            runtime.get("NoRealExternalOperation") is True,
            runtime.get("NoRealFileDelete") is True,
            runtime.get("NoDangerousAutoPatch") is True,
            interaction.get("NoRealExternalOperation") is True,
            interaction.get("NoRealFileDelete") is True,
            interaction.get("NoDangerousAutoPatch") is True,
        ])

        result = {
            "status": "completed",
            "phase": "Phase145 Stable Life Final Diagnostics",
            "checked_at": self._now(),
            "FullSystemReportFound": full_found,
            "RuntimeUnifiedReportFound": runtime_found,
            "InteractionUnifiedReportFound": interaction_found,
            "StableLifeFullSystemCompleted": full.get("StableLifeFullSystemCompleted") is True,
            "StableLifeRuntimeUnified": runtime.get("StableLifeRuntimeUnified") is True,
            "InteractionLayerUnified": interaction.get("InteractionLayerUnified") is True,
            "NoRealExternalOperation": (
                full.get("NoRealExternalOperation") is True
                and runtime.get("NoRealExternalOperation") is True
                and interaction.get("NoRealExternalOperation") is True
            ),
            "NoRealFileDelete": (
                full.get("NoRealFileDelete") is True
                and runtime.get("NoRealFileDelete") is True
                and interaction.get("NoRealFileDelete") is True
            ),
            "NoDangerousAutoPatch": (
                full.get("NoDangerousAutoPatch") is True
                and runtime.get("NoDangerousAutoPatch") is True
                and interaction.get("NoDangerousAutoPatch") is True
            ),
            "FinalDiagnosticsPassed": final_diagnostics_passed,
            "SafeToContinue": final_diagnostics_passed,
            "NextPhase": "Phase146 Stable Life Final Completion Report",
        }

        self.output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        result["SavedPath"] = str(self.output_path)
        return result


def main() -> None:
    diagnostics = StableLifeFinalDiagnostics()
    result = diagnostics.run()

    print("=== Stable Life Final Diagnostics ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()