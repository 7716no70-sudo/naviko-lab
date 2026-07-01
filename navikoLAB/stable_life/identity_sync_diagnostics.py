# navikoLAB/stable_life/identity_sync_diagnostics.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class IdentitySyncDiagnostics:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.candidate_path = (
            self.root
            / "stable_life"
            / "identity_sync"
            / "stable_identity_sync_candidate.json"
        )

        self.output_dir = self.root / "stable_life" / "identity_sync"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_path = self.output_dir / "identity_sync_diagnostics_report.json"

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
        found, candidate = self._read_json(self.candidate_path)

        patch = candidate.get("SuggestedIdentityPatch", {})

        diagnostics_passed = all([
            found,
            candidate.get("SyncCandidateReady") is True,
            candidate.get("OriginalIdentityDirectWrite") is False,
            candidate.get("HumanApprovalRequired") is True,
            candidate.get("AutoApplyAllowed") is False,
            patch.get("requires_human_approval") is True,
            patch.get("auto_apply_allowed") is False,
            bool(candidate.get("IdentityStatementCandidate")),
        ])

        result = {
            "status": "completed",
            "phase": "Phase125 Identity Sync Diagnostics",
            "checked_at": self._now(),
            "CandidateFound": found,
            "SyncCandidateReady": candidate.get("SyncCandidateReady") is True,
            "OriginalIdentityDirectWrite": candidate.get("OriginalIdentityDirectWrite"),
            "HumanApprovalRequired": candidate.get("HumanApprovalRequired"),
            "AutoApplyAllowed": candidate.get("AutoApplyAllowed"),
            "PatchRequiresHumanApproval": patch.get("requires_human_approval"),
            "PatchAutoApplyAllowed": patch.get("auto_apply_allowed"),
            "IdentityStatementPresent": bool(candidate.get("IdentityStatementCandidate")),
            "DiagnosticsPassed": diagnostics_passed,
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": diagnostics_passed,
            "NextPhase": "Phase126 Stable Life Identity Completion Report",
        }

        self.output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        result["SavedPath"] = str(self.output_path)
        return result


def main() -> None:
    diagnostics = IdentitySyncDiagnostics()
    result = diagnostics.run()

    print("=== Identity Sync Diagnostics ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()