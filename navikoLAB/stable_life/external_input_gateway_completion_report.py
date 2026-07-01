# navikoLAB/stable_life/external_input_gateway_completion_report.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class ExternalInputGatewayCompletionReport:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.gateway_report_path = (
            self.root / "stable_life" / "external_input_gateway"
            / "stable_life_external_input_gateway_report.json"
        )
        self.diagnostics_report_path = (
            self.root / "stable_life" / "external_input_gateway"
            / "external_input_gateway_diagnostics_report.json"
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
        gateway_found, gateway = self._read_json(self.gateway_report_path)
        diagnostics_found, diagnostics = self._read_json(self.diagnostics_report_path)

        gateway_completed = all([
            gateway_found,
            diagnostics_found,
            gateway.get("GatewayCompleted") is True,
            gateway.get("SafeToContinue") is True,
            diagnostics.get("DiagnosticsPassed") is True,
            diagnostics.get("AcceptedInputOK") is True,
            diagnostics.get("RejectedInputOK") is True,
            diagnostics.get("BlockedInputRejected") is True,
            diagnostics.get("NoRealExternalCommunication") is True,
            diagnostics.get("NoRealFileDelete") is True,
            diagnostics.get("NoDangerousAutoPatch") is True,
        ])

        result = {
            "status": "completed",
            "phase": "Phase142 External Input Gateway Completion Report",
            "checked_at": self._now(),
            "ExternalInputGatewayCompleted": gateway_completed,
            "GatewayReportFound": gateway_found,
            "DiagnosticsReportFound": diagnostics_found,
            "AcceptedInputOK": diagnostics.get("AcceptedInputOK") is True,
            "RejectedInputOK": diagnostics.get("RejectedInputOK") is True,
            "BlockedInputRejected": diagnostics.get("BlockedInputRejected") is True,
            "NoRealExternalCommunication": diagnostics.get("NoRealExternalCommunication") is True,
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": gateway_completed,
            "NextPhase": "Phase143 Stable Life Interaction Layer Unified Report",
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"external_input_gateway_completion_report_{timestamp}.json"
        latest_path = self.output_dir / "external_input_gateway_completion_report_latest.json"

        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        latest_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

        result["SavedPath"] = str(output_path)
        result["LatestPath"] = str(latest_path)
        return result


def main() -> None:
    report = ExternalInputGatewayCompletionReport()
    result = report.generate()

    print("=== External Input Gateway Completion Report ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()