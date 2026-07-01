# navikoLAB/stable_life/life_kernel_continuity_report.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class LifeKernelContinuityReport:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.inputs = {
            "completion": self.root / "stable_life" / "reports" / "stable_life_completion_report_latest.json",
            "runtime_adapter": self.root / "stable_life" / "runtime_adapter" / "stable_life_runtime_adapter_report.json",
            "persistent_loop": self.root / "stable_life" / "persistent_runtime" / "persistent_life_runtime_loop_report.json",
            "diagnostics": self.root / "stable_life" / "diagnostics" / "life_runtime_diagnostics_report.json",
        }

        self.output_dir = self.root / "stable_life" / "continuity"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_path = self.output_dir / "life_kernel_continuity_report.json"

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
        loaded = {}
        data = {}

        for name, path in self.inputs.items():
            ok, value = self._read_json(path)
            loaded[name] = ok
            data[name] = value

        completion_ok = data["completion"].get("StableLifeKernelCompleted") is True
        runtime_ok = data["runtime_adapter"].get("stable_life_runtime_integrated") is True
        loop_ok = data["persistent_loop"].get("PersistentLifeRuntimeLoopCompleted") is True
        diagnostics_ok = data["diagnostics"].get("DiagnosticsPassed") is True

        cycle_count = int(data["persistent_loop"].get("CycleCount", 0))
        safe_cycle_count = int(data["persistent_loop"].get("SafeCycleCount", 0))
        integrity_score = float(data["completion"].get("IntegrityScore", 0.0))

        continuity_established = all([
            all(loaded.values()),
            completion_ok,
            runtime_ok,
            loop_ok,
            diagnostics_ok,
            cycle_count >= 3,
            safe_cycle_count == cycle_count,
            integrity_score >= 0.75,
        ])

        result = {
            "status": "completed",
            "phase": "Phase120 Life Kernel Continuity Report",
            "checked_at": self._now(),
            "InputReportsLoaded": all(loaded.values()),
            "CompletionOK": completion_ok,
            "RuntimeIntegrationOK": runtime_ok,
            "PersistentLoopOK": loop_ok,
            "DiagnosticsOK": diagnostics_ok,
            "CycleCount": cycle_count,
            "SafeCycleCount": safe_cycle_count,
            "IntegrityScore": integrity_score,
            "ContinuityEstablished": continuity_established,
            "LifeKernelStatus": "stable_continuous_life_kernel" if continuity_established else "incomplete",
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": continuity_established,
            "NextPhase": "Phase121 Long-Term Life Memory Consolidation",
        }

        self.output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        result["SavedPath"] = str(self.output_path)
        return result


def main() -> None:
    report = LifeKernelContinuityReport()
    result = report.generate()

    print("=== Life Kernel Continuity Report ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()