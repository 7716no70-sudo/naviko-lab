# navikoLAB/stable_life/user_command_bridge_diagnostics.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from navikoLAB.stable_life.stable_life_runtime_user_command_bridge import (
    StableLifeRuntimeUserCommandBridge,
)


class UserCommandBridgeDiagnostics:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.output_dir = self.root / "stable_life" / "user_command_bridge"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_path = self.output_dir / "user_command_bridge_diagnostics_report.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def run(self) -> dict[str, Any]:
        bridge = StableLifeRuntimeUserCommandBridge(self.root)

        accepted_result = bridge.execute_user_command(
            user_command="status",
            text="Phase138 accepted command diagnostics",
        )

        rejected_result = bridge.execute_user_command(
            user_command="delete_all",
            text="Phase138 unsupported command diagnostics",
        )

        accepted_ok = (
            accepted_result.get("CommandAccepted") is True
            and accepted_result.get("CommandSuccess") is True
            and accepted_result.get("BridgeReady") is True
            and accepted_result.get("SafeToContinue") is True
        )

        rejected_ok = (
            rejected_result.get("CommandAccepted") is False
            and rejected_result.get("CommandSuccess") is False
            and rejected_result.get("BridgeReady") is False
            and rejected_result.get("SafeToContinue") is False
        )

        no_real_external_operation = (
            accepted_result.get("RealExternalOperation") is False
            and rejected_result.get("RealExternalOperation") is False
        )

        no_real_file_delete = (
            accepted_result.get("RealFileDelete") is False
            and rejected_result.get("RealFileDelete") is False
        )

        no_dangerous_auto_patch = (
            accepted_result.get("DangerousAutoPatch") is False
            and rejected_result.get("DangerousAutoPatch") is False
        )

        diagnostics_passed = all([
            accepted_ok,
            rejected_ok,
            no_real_external_operation,
            no_real_file_delete,
            no_dangerous_auto_patch,
        ])

        result = {
            "status": "completed",
            "phase": "Phase138 User Command Bridge Diagnostics",
            "checked_at": self._now(),
            "AcceptedCommandOK": accepted_ok,
            "RejectedCommandOK": rejected_ok,
            "UnsupportedCommandRejected": rejected_ok,
            "NoRealExternalOperation": no_real_external_operation,
            "NoRealFileDelete": no_real_file_delete,
            "NoDangerousAutoPatch": no_dangerous_auto_patch,
            "DiagnosticsPassed": diagnostics_passed,
            "SafeToContinue": diagnostics_passed,
            "NextPhase": "Phase139 User Command Bridge Completion Report",
            "AcceptedCommand": accepted_result.get("UserCommand"),
            "RejectedCommand": rejected_result.get("UserCommand"),
        }

        self.output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        result["SavedPath"] = str(self.output_path)
        return result


def main() -> None:
    diagnostics = UserCommandBridgeDiagnostics()
    result = diagnostics.run()

    print("=== User Command Bridge Diagnostics ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()