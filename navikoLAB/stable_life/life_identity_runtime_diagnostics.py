# navikoLAB/stable_life/life_identity_runtime_diagnostics.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class LifeIdentityRuntimeDiagnostics:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.bridge_report_path = (
            self.root
            / "stable_life"
            / "identity_runtime_bridge"
            / "life_identity_runtime_bridge_report.json"
        )

        self.output_dir = self.root / "stable_life" / "identity_runtime_bridge"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_path = self.output_dir / "life_identity_runtime_diagnostics_report.json"

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
        found, bridge = self._read_json(self.bridge_report_path)

        context = bridge.get("RuntimeReadableContext", {})

        diagnostics_passed = all([
            found,
            bridge.get("BridgeContextReady") is True,
            bridge.get("RuntimeReadOnly") is True,
            bridge.get("OriginalIdentityDirectWrite") is False,
            bridge.get("HumanApprovalRequiredForApply") is True,
            bridge.get("AutoApplyAllowed") is False,
            bool(context.get("identity_statement")),
            context.get("auto_apply_blocked") is True,
            context.get("original_identity_direct_write") is False,
        ])

        result = {
            "status": "completed",
            "phase": "Phase128 Life Identity Runtime Diagnostics",
            "checked_at": self._now(),
            "BridgeReportFound": found,
            "BridgeContextReady": bridge.get("BridgeContextReady") is True,
            "RuntimeReadOnly": bridge.get("RuntimeReadOnly") is True,
            "OriginalIdentityDirectWrite": bridge.get("OriginalIdentityDirectWrite"),
            "HumanApprovalRequiredForApply": bridge.get("HumanApprovalRequiredForApply"),
            "AutoApplyAllowed": bridge.get("AutoApplyAllowed"),
            "RuntimeIdentityStatementPresent": bool(context.get("identity_statement")),
            "ContextAutoApplyBlocked": context.get("auto_apply_blocked"),
            "ContextOriginalIdentityDirectWrite": context.get("original_identity_direct_write"),
            "DiagnosticsPassed": diagnostics_passed,
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": diagnostics_passed,
            "NextPhase": "Phase129 Life Identity Runtime Completion Report",
        }

        self.output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        result["SavedPath"] = str(self.output_path)
        return result


def main() -> None:
    diagnostics = LifeIdentityRuntimeDiagnostics()
    result = diagnostics.run()

    print("=== Life Identity Runtime Diagnostics ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()