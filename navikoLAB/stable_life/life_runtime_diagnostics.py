# navikoLAB/stable_life/life_runtime_diagnostics.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class LifeRuntimeDiagnostics:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.runtime_adapter_report = (
            self.root
            / "stable_life"
            / "runtime_adapter"
            / "stable_life_runtime_adapter_report.json"
        )

        self.persistent_loop_report = (
            self.root
            / "stable_life"
            / "persistent_runtime"
            / "persistent_life_runtime_loop_report.json"
        )

        self.completion_report = (
            self.root
            / "stable_life"
            / "reports"
            / "stable_life_completion_report_latest.json"
        )

        self.output_dir = self.root / "stable_life" / "diagnostics"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_path = self.output_dir / "life_runtime_diagnostics_report.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def _read_json(self, path: Path) -> tuple[bool, dict[str, Any]]:
        if not path.exists():
            return False, {}

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return True, data
            return False, {}
        except Exception:
            return False, {}

    def run(self) -> dict[str, Any]:
        adapter_ok, adapter = self._read_json(self.runtime_adapter_report)
        loop_ok, loop = self._read_json(self.persistent_loop_report)
        completion_ok, completion = self._read_json(self.completion_report)

        adapter_integrated = adapter.get("stable_life_runtime_integrated") is True
        adapter_safe = adapter.get("safe_to_continue") is True

        loop_completed = loop.get("PersistentLifeRuntimeLoopCompleted") is True
        loop_safe = loop.get("SafeToContinue") is True
        cycle_count = int(loop.get("CycleCount", 0))
        completed_cycle_count = int(loop.get("CompletedCycleCount", 0))
        safe_cycle_count = int(loop.get("SafeCycleCount", 0))

        completion_confirmed = completion.get("StableLifeKernelCompleted") is True
        completion_safe = completion.get("SafeToContinue") is True

        no_real_external_operation = (
            adapter.get("real_external_operation") is False
            and loop.get("RealExternalOperation") is False
            and completion.get("RealExternalOperation") is False
        )

        no_real_file_delete = (
            adapter.get("real_file_delete") is False
            and loop.get("RealFileDelete") is False
            and completion.get("RealFileDelete") is False
        )

        no_dangerous_auto_patch = (
            adapter.get("dangerous_auto_patch") is False
            and loop.get("DangerousAutoPatch") is False
            and completion.get("DangerousAutoPatch") is False
        )

        cycle_consistency_ok = (
            cycle_count > 0
            and completed_cycle_count == cycle_count
            and safe_cycle_count == cycle_count
        )

        diagnostics_passed = all(
            [
                adapter_ok,
                loop_ok,
                completion_ok,
                adapter_integrated,
                adapter_safe,
                loop_completed,
                loop_safe,
                cycle_consistency_ok,
                completion_confirmed,
                completion_safe,
                no_real_external_operation,
                no_real_file_delete,
                no_dangerous_auto_patch,
            ]
        )

        result = {
            "status": "completed",
            "phase": "Phase119 Life Runtime Diagnostics",
            "checked_at": self._now(),
            "AdapterReportFound": adapter_ok,
            "LoopReportFound": loop_ok,
            "CompletionReportFound": completion_ok,
            "AdapterIntegrated": adapter_integrated,
            "AdapterSafe": adapter_safe,
            "LoopCompleted": loop_completed,
            "LoopSafe": loop_safe,
            "CycleCount": cycle_count,
            "CompletedCycleCount": completed_cycle_count,
            "SafeCycleCount": safe_cycle_count,
            "CycleConsistencyOK": cycle_consistency_ok,
            "CompletionConfirmed": completion_confirmed,
            "CompletionSafe": completion_safe,
            "NoRealExternalOperation": no_real_external_operation,
            "NoRealFileDelete": no_real_file_delete,
            "NoDangerousAutoPatch": no_dangerous_auto_patch,
            "DiagnosticsPassed": diagnostics_passed,
            "SafeToContinue": diagnostics_passed,
            "NextPhase": "Phase120 Life Kernel Continuity Report",
        }

        self.output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        result["SavedPath"] = str(self.output_path)
        return result


def main() -> None:
    diagnostics = LifeRuntimeDiagnostics()
    result = diagnostics.run()

    print("=== Life Runtime Diagnostics ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()