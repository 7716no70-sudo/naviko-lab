# navikoLAB/stable_life/stable_identity_synchronization_adapter.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class StableIdentitySynchronizationAdapter:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.feedback_path = (
            self.root
            / "stable_life"
            / "identity_feedback"
            / "life_memory_identity_feedback.json"
        )

        self.output_dir = self.root / "stable_life" / "identity_sync"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_path = self.output_dir / "stable_identity_sync_candidate.json"
        self.history_path = self.output_dir / "stable_identity_sync_history.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def _read_json(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def build_sync_candidate(self) -> dict[str, Any]:
        feedback = self._read_json(self.feedback_path)

        feedback_ready = feedback.get("FeedbackReadyForIdentityLayer") is True
        identity_statement = feedback.get("IdentityStatement", "")
        reflection_text = feedback.get("ReflectionText", "")

        sync_candidate_ready = (
            feedback_ready
            and bool(identity_statement)
            and bool(reflection_text)
        )

        candidate = {
            "status": "completed",
            "phase": "Phase124 Stable Identity Synchronization Adapter",
            "created_at": self._now(),
            "FeedbackLoaded": bool(feedback),
            "FeedbackReady": feedback_ready,
            "SyncCandidateReady": sync_candidate_ready,
            "IdentityStatementCandidate": identity_statement,
            "ReflectionTextCandidate": reflection_text,
            "SuggestedIdentityPatch": {
                "target": "identity_layer",
                "operation": "append_identity_context",
                "content": identity_statement,
                "requires_human_approval": True,
                "auto_apply_allowed": False,
            },
            "OriginalIdentityDirectWrite": False,
            "HumanApprovalRequired": True,
            "AutoApplyAllowed": False,
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": sync_candidate_ready,
            "NextPhase": "Phase125 Identity Sync Diagnostics",
        }

        self.output_path.write_text(
            json.dumps(candidate, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self._append_history(candidate)

        candidate["SavedPath"] = str(self.output_path)
        return candidate

    def _append_history(self, candidate: dict[str, Any]) -> None:
        if self.history_path.exists():
            history = json.loads(self.history_path.read_text(encoding="utf-8"))
        else:
            history = {"count": 0, "items": []}

        history["items"].append(candidate)
        history["count"] = len(history["items"])

        self.history_path.write_text(
            json.dumps(history, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def main() -> None:
    adapter = StableIdentitySynchronizationAdapter()
    result = adapter.build_sync_candidate()

    print("=== Stable Identity Synchronization Adapter ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"FeedbackLoaded: {result['FeedbackLoaded']}")
    print(f"FeedbackReady: {result['FeedbackReady']}")
    print(f"SyncCandidateReady: {result['SyncCandidateReady']}")
    print(f"OriginalIdentityDirectWrite: {result['OriginalIdentityDirectWrite']}")
    print(f"HumanApprovalRequired: {result['HumanApprovalRequired']}")
    print(f"AutoApplyAllowed: {result['AutoApplyAllowed']}")
    print("--- IdentityStatementCandidate ---")
    print(result["IdentityStatementCandidate"])
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"NextPhase: {result['NextPhase']}")


if __name__ == "__main__":
    main()