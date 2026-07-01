# navikoLAB/stable_life/stable_life_runtime_adapter.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from navikoLAB.stable_life.stable_life_controller import StableLifeController
from navikoLAB.stable_life.stable_life_completion_report import StableLifeCompletionReport


class StableLifeRuntimeAdapter:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.adapter_dir = self.root / "stable_life" / "runtime_adapter"
        self.adapter_dir.mkdir(parents=True, exist_ok=True)

        self.report_path = self.adapter_dir / "stable_life_runtime_adapter_report.json"
        self.history_path = self.adapter_dir / "stable_life_runtime_adapter_history.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def run_from_runtime(self, runtime_event: dict[str, Any]) -> dict[str, Any]:
        event_type = runtime_event.get("event_type", "internal_life_cycle")
        text = runtime_event.get(
            "text",
            "RuntimeからStable Life Kernelを安全統合テストした",
        )

        controller_result = StableLifeController(self.root).run_cycle(text)
        completion_result = StableLifeCompletionReport(self.root).generate()

        integrated = (
            controller_result.get("safe_to_continue") is True
            and completion_result.get("SafeToContinue") is True
        )

        report = {
            "status": "completed",
            "phase": "Phase117 Stable Life Runtime Integration",
            "event_type": event_type,
            "runtime_event": runtime_event,
            "controller_completed": controller_result.get("stable_life_cycle_completed"),
            "completion_confirmed": completion_result.get("StableLifeKernelCompleted"),
            "integrity_score": controller_result.get("integrity_score"),
            "stable_life_runtime_integrated": integrated,
            "real_external_operation": False,
            "real_file_delete": False,
            "dangerous_auto_patch": False,
            "safe_to_continue": integrated,
            "created_at": self._now(),
        }

        self._save(report)
        return report

    def _save(self, report: dict[str, Any]) -> None:
        self.report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        if self.history_path.exists():
            history = json.loads(self.history_path.read_text(encoding="utf-8"))
        else:
            history = {"count": 0, "items": []}

        history["items"].append(report)
        history["count"] = len(history["items"])

        self.history_path.write_text(
            json.dumps(history, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def main() -> None:
    adapter = StableLifeRuntimeAdapter()

    runtime_event = {
        "event_type": "internal_life_cycle",
        "text": "Phase117でStable Life KernelをRuntimeへ接続した",
        "source": "dry_run_runtime_adapter",
    }

    result = adapter.run_from_runtime(runtime_event)

    print("=== Stable Life Runtime Adapter ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"event_type: {result['event_type']}")
    print(f"ControllerCompleted: {result['controller_completed']}")
    print(f"CompletionConfirmed: {result['completion_confirmed']}")
    print(f"IntegrityScore: {result['integrity_score']}")
    print(f"StableLifeRuntimeIntegrated: {result['stable_life_runtime_integrated']}")
    print(f"RealExternalOperation: {result['real_external_operation']}")
    print(f"RealFileDelete: {result['real_file_delete']}")
    print(f"DangerousAutoPatch: {result['dangerous_auto_patch']}")
    print(f"SafeToContinue: {result['safe_to_continue']}")


if __name__ == "__main__":
    main()