# navikoLAB/stable_life/stable_life_runtime_unified_report.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class StableLifeRuntimeUnifiedReport:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.inputs = {
            "stable_life_completion": self.root / "stable_life" / "reports" / "stable_life_completion_report_latest.json",
            "life_kernel_continuity": self.root / "stable_life" / "continuity" / "life_kernel_continuity_report.json",
            "long_term_life_memory": self.root / "stable_life" / "long_term_life_memory" / "long_term_life_memory_summary.json",
            "stable_life_identity": self.root / "stable_life" / "reports" / "stable_life_identity_completion_report_latest.json",
            "life_identity_runtime": self.root / "stable_life" / "reports" / "life_identity_runtime_completion_report_latest.json",
            "life_runtime_diagnostics": self.root / "stable_life" / "diagnostics" / "life_runtime_diagnostics_report.json",
        }

        self.output_dir = self.root / "stable_life" / "reports"
        self.output_dir.mkdir(parents=True, exist_ok=True)

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

    def generate(self) -> dict[str, Any]:
        found = {}
        data = {}

        for name, path in self.inputs.items():
            ok, value = self._read_json(path)
            found[name] = ok
            data[name] = value

        stable_life_completed = data["stable_life_completion"].get("StableLifeKernelCompleted") is True
        continuity_established = data["life_kernel_continuity"].get("ContinuityEstablished") is True
        long_term_memory_ready = data["long_term_life_memory"].get("LongTermLifeMemoryReady") is True
        identity_completed = data["stable_life_identity"].get("StableLifeIdentityCompleted") is True
        identity_runtime_completed = data["life_identity_runtime"].get("LifeIdentityRuntimeCompleted") is True
        runtime_diagnostics_passed = data["life_runtime_diagnostics"].get("DiagnosticsPassed") is True

        no_external = all([
            data["stable_life_completion"].get("RealExternalOperation") is False,
            data["life_kernel_continuity"].get("RealExternalOperation") is False,
            data["long_term_life_memory"].get("RealExternalOperation") is False,
            data["stable_life_identity"].get("RealExternalOperation") is False,
            data["life_identity_runtime"].get("RealExternalOperation") is False,
            data["life_runtime_diagnostics"].get("NoRealExternalOperation") is True,
        ])

        no_delete = all([
            data["stable_life_completion"].get("RealFileDelete") is False,
            data["life_kernel_continuity"].get("RealFileDelete") is False,
            data["long_term_life_memory"].get("RealFileDelete") is False,
            data["stable_life_identity"].get("RealFileDelete") is False,
            data["life_identity_runtime"].get("RealFileDelete") is False,
            data["life_runtime_diagnostics"].get("NoRealFileDelete") is True,
        ])

        no_dangerous_patch = all([
            data["stable_life_completion"].get("DangerousAutoPatch") is False,
            data["life_kernel_continuity"].get("DangerousAutoPatch") is False,
            data["long_term_life_memory"].get("DangerousAutoPatch") is False,
            data["stable_life_identity"].get("DangerousAutoPatch") is False,
            data["life_identity_runtime"].get("DangerousAutoPatch") is False,
            data["life_runtime_diagnostics"].get("NoDangerousAutoPatch") is True,
        ])

        unified_completed = all([
            all(found.values()),
            stable_life_completed,
            continuity_established,
            long_term_memory_ready,
            identity_completed,
            identity_runtime_completed,
            runtime_diagnostics_passed,
            no_external,
            no_delete,
            no_dangerous_patch,
        ])

        identity_statement = data["stable_life_identity"].get("IdentityStatement", "")

        result = {
            "status": "completed",
            "phase": "Phase130 Stable Life Runtime Unified Report",
            "checked_at": self._now(),
            "StableLifeRuntimeUnified": unified_completed,
            "InputReportCount": len(self.inputs),
            "MissingInputCount": len([k for k, v in found.items() if not v]),
            "StableLifeKernelCompleted": stable_life_completed,
            "ContinuityEstablished": continuity_established,
            "LongTermLifeMemoryReady": long_term_memory_ready,
            "StableLifeIdentityCompleted": identity_completed,
            "LifeIdentityRuntimeCompleted": identity_runtime_completed,
            "RuntimeDiagnosticsPassed": runtime_diagnostics_passed,
            "NoRealExternalOperation": no_external,
            "NoRealFileDelete": no_delete,
            "NoDangerousAutoPatch": no_dangerous_patch,
            "IdentityStatement": identity_statement,
            "UnifiedStatus": "stable_life_runtime_unified" if unified_completed else "incomplete",
            "SafeToContinue": unified_completed,
            "NextPhase": "Phase131 Stable Life Runtime Scheduler",
            "MissingInputs": [k for k, v in found.items() if not v],
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"stable_life_runtime_unified_report_{timestamp}.json"
        latest_path = self.output_dir / "stable_life_runtime_unified_report_latest.json"

        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        latest_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

        result["SavedPath"] = str(output_path)
        result["LatestPath"] = str(latest_path)
        return result


def main() -> None:
    report = StableLifeRuntimeUnifiedReport()
    result = report.generate()

    print("=== Stable Life Runtime Unified Report ===")
    for key, value in result.items():
        if isinstance(value, list):
            print(f"{key}:")
            for item in value:
                print(f"- {item}")
        else:
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()