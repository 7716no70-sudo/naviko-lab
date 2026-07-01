# navikoLAB/stable_life/life_identity_runtime_bridge.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class LifeIdentityRuntimeBridge:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.identity_completion_path = (
            self.root
            / "stable_life"
            / "reports"
            / "stable_life_identity_completion_report_latest.json"
        )

        self.output_dir = self.root / "stable_life" / "identity_runtime_bridge"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.report_path = self.output_dir / "life_identity_runtime_bridge_report.json"
        self.history_path = self.output_dir / "life_identity_runtime_bridge_history.json"

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

    def build_bridge_context(self) -> dict[str, Any]:
        found, completion = self._read_json(self.identity_completion_path)

        completed = completion.get("StableLifeIdentityCompleted") is True
        safe = completion.get("SafeToContinue") is True
        identity_statement = completion.get("IdentityStatement", "")

        bridge_ready = found and completed and safe and bool(identity_statement)

        context = {
            "identity_statement": identity_statement,
            "identity_source_phase": completion.get("phase"),
            "human_approval_required": completion.get("HumanApprovalRequired"),
            "auto_apply_blocked": completion.get("AutoApplyBlocked"),
            "original_identity_direct_write": completion.get("OriginalIdentityDirectWrite"),
        }

        result = {
            "status": "completed",
            "phase": "Phase127 Life Identity Runtime Bridge",
            "created_at": self._now(),
            "IdentityCompletionReportFound": found,
            "StableLifeIdentityCompleted": completed,
            "IdentityCompletionSafe": safe,
            "IdentityStatementPresent": bool(identity_statement),
            "BridgeContextReady": bridge_ready,
            "RuntimeReadableContext": context,
            "OriginalIdentityDirectWrite": False,
            "RuntimeReadOnly": True,
            "HumanApprovalRequiredForApply": True,
            "AutoApplyAllowed": False,
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": bridge_ready,
            "NextPhase": "Phase128 Life Identity Runtime Diagnostics",
        }

        self.report_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self._append_history(result)

        result["SavedPath"] = str(self.report_path)
        return result

    def _append_history(self, result: dict[str, Any]) -> None:
        if self.history_path.exists():
            history = json.loads(self.history_path.read_text(encoding="utf-8"))
        else:
            history = {"count": 0, "items": []}

        history["items"].append(result)
        history["count"] = len(history["items"])

        self.history_path.write_text(
            json.dumps(history, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def main() -> None:
    bridge = LifeIdentityRuntimeBridge()
    result = bridge.build_bridge_context()

    print("=== Life Identity Runtime Bridge ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"IdentityCompletionReportFound: {result['IdentityCompletionReportFound']}")
    print(f"StableLifeIdentityCompleted: {result['StableLifeIdentityCompleted']}")
    print(f"IdentityCompletionSafe: {result['IdentityCompletionSafe']}")
    print(f"IdentityStatementPresent: {result['IdentityStatementPresent']}")
    print(f"BridgeContextReady: {result['BridgeContextReady']}")
    print(f"RuntimeReadOnly: {result['RuntimeReadOnly']}")
    print(f"OriginalIdentityDirectWrite: {result['OriginalIdentityDirectWrite']}")
    print(f"HumanApprovalRequiredForApply: {result['HumanApprovalRequiredForApply']}")
    print(f"AutoApplyAllowed: {result['AutoApplyAllowed']}")
    print("--- RuntimeReadableContext ---")
    print(json.dumps(result["RuntimeReadableContext"], ensure_ascii=False, indent=2))
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"NextPhase: {result['NextPhase']}")


if __name__ == "__main__":
    main()