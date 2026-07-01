# navikoLAB/stable_life/life_identity_runtime_completion_report.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class LifeIdentityRuntimeCompletionReport:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.bridge_path = (
            self.root / "stable_life" / "identity_runtime_bridge"
            / "life_identity_runtime_bridge_report.json"
        )
        self.diagnostics_path = (
            self.root / "stable_life" / "identity_runtime_bridge"
            / "life_identity_runtime_diagnostics_report.json"
        )

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
        bridge_found, bridge = self._read_json(self.bridge_path)
        diagnostics_found, diagnostics = self._read_json(self.diagnostics_path)

        runtime_completed = all([
            bridge_found,
            diagnostics_found,
            bridge.get("BridgeContextReady") is True,
            bridge.get("RuntimeReadOnly") is True,
            bridge.get("OriginalIdentityDirectWrite") is False,
            bridge.get("AutoApplyAllowed") is False,
            diagnostics.get("DiagnosticsPassed") is True,
            diagnostics.get("SafeToContinue") is True,
        ])

        result = {
            "status": "completed",
            "phase": "Phase129 Life Identity Runtime Completion Report",
            "checked_at": self._now(),
            "LifeIdentityRuntimeCompleted": runtime_completed,
            "BridgeReportFound": bridge_found,
            "DiagnosticsReportFound": diagnostics_found,
            "BridgeContextReady": bridge.get("BridgeContextReady") is True,
            "RuntimeReadOnly": bridge.get("RuntimeReadOnly") is True,
            "OriginalIdentityDirectWrite": bridge.get("OriginalIdentityDirectWrite"),
            "HumanApprovalRequiredForApply": bridge.get("HumanApprovalRequiredForApply"),
            "AutoApplyAllowed": bridge.get("AutoApplyAllowed"),
            "DiagnosticsPassed": diagnostics.get("DiagnosticsPassed") is True,
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": runtime_completed,
            "NextPhase": "Phase130 Stable Life Runtime Unified Report",
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"life_identity_runtime_completion_report_{timestamp}.json"
        latest_path = self.output_dir / "life_identity_runtime_completion_report_latest.json"

        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        latest_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

        result["SavedPath"] = str(output_path)
        result["LatestPath"] = str(latest_path)
        return result


def main() -> None:
    report = LifeIdentityRuntimeCompletionReport()
    result = report.generate()

    print("=== Life Identity Runtime Completion Report ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()