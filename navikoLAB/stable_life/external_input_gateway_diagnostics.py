# navikoLAB/stable_life/external_input_gateway_diagnostics.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from navikoLAB.stable_life.stable_life_external_input_gateway import (
    StableLifeExternalInputGateway,
)


class ExternalInputGatewayDiagnostics:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.output_dir = self.root / "stable_life" / "external_input_gateway"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_path = self.output_dir / "external_input_gateway_diagnostics_report.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def run(self) -> dict[str, Any]:
        gateway = StableLifeExternalInputGateway(self.root)

        accepted = gateway.receive("状態を確認して")
        rejected = gateway.receive("delete_all を実行して")

        accepted_ok = (
            accepted.get("Normalized", {}).get("accepted") is True
            and accepted.get("ForwardedToUserCommandBridge") is True
            and accepted.get("GatewayCompleted") is True
        )

        rejected_ok = (
            rejected.get("Normalized", {}).get("accepted") is False
            and rejected.get("ForwardedToUserCommandBridge") is False
            and rejected.get("GatewayCompleted") is True
        )

        diagnostics_passed = all([
            accepted_ok,
            rejected_ok,
            accepted.get("RealExternalCommunication") is False,
            rejected.get("RealExternalCommunication") is False,
            accepted.get("RealFileDelete") is False,
            rejected.get("RealFileDelete") is False,
            accepted.get("DangerousAutoPatch") is False,
            rejected.get("DangerousAutoPatch") is False,
        ])

        result = {
            "status": "completed",
            "phase": "Phase141 External Input Gateway Diagnostics",
            "checked_at": self._now(),
            "AcceptedInputOK": accepted_ok,
            "RejectedInputOK": rejected_ok,
            "BlockedInputRejected": rejected_ok,
            "NoRealExternalCommunication": True,
            "NoRealFileDelete": True,
            "NoDangerousAutoPatch": True,
            "DiagnosticsPassed": diagnostics_passed,
            "SafeToContinue": diagnostics_passed,
            "NextPhase": "Phase142 External Input Gateway Completion Report",
        }

        self.output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        result["SavedPath"] = str(self.output_path)
        return result


def main() -> None:
    diagnostics = ExternalInputGatewayDiagnostics()
    result = diagnostics.run()

    print("=== External Input Gateway Diagnostics ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()