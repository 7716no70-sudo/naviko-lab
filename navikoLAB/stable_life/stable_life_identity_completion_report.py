# navikoLAB/stable_life/stable_life_identity_completion_report.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class StableLifeIdentityCompletionReport:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.inputs = {
            "life_memory": self.root / "stable_life" / "long_term_life_memory" / "long_term_life_memory_summary.json",
            "reflection": self.root / "stable_life" / "reflection" / "life_memory_reflection.json",
            "identity_feedback": self.root / "stable_life" / "identity_feedback" / "life_memory_identity_feedback.json",
            "identity_sync_candidate": self.root / "stable_life" / "identity_sync" / "stable_identity_sync_candidate.json",
            "identity_sync_diagnostics": self.root / "stable_life" / "identity_sync" / "identity_sync_diagnostics_report.json",
        }

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
        found = {}
        data = {}

        for name, path in self.inputs.items():
            ok, value = self._read_json(path)
            found[name] = ok
            data[name] = value

        life_memory_ready = data["life_memory"].get("LongTermLifeMemoryReady") is True
        reflection_ready = data["reflection"].get("ReflectionReady") is True
        feedback_ready = data["identity_feedback"].get("FeedbackReadyForIdentityLayer") is True
        sync_ready = data["identity_sync_candidate"].get("SyncCandidateReady") is True
        diagnostics_passed = data["identity_sync_diagnostics"].get("DiagnosticsPassed") is True

        human_approval_required = (
            data["identity_sync_candidate"].get("HumanApprovalRequired") is True
            and data["identity_sync_diagnostics"].get("HumanApprovalRequired") is True
        )

        auto_apply_blocked = (
            data["identity_sync_candidate"].get("AutoApplyAllowed") is False
            and data["identity_sync_diagnostics"].get("AutoApplyAllowed") is False
        )

        original_identity_direct_write = (
            data["identity_feedback"].get("OriginalIdentityDirectWrite") is True
            or data["identity_sync_candidate"].get("OriginalIdentityDirectWrite") is True
            or data["identity_sync_diagnostics"].get("OriginalIdentityDirectWrite") is True
        )

        stable_life_identity_completed = all([
            all(found.values()),
            life_memory_ready,
            reflection_ready,
            feedback_ready,
            sync_ready,
            diagnostics_passed,
            human_approval_required,
            auto_apply_blocked,
            not original_identity_direct_write,
        ])

        identity_statement = data["identity_sync_candidate"].get(
            "IdentityStatementCandidate",
            "",
        )

        result = {
            "status": "completed",
            "phase": "Phase126 Stable Life Identity Completion Report",
            "checked_at": self._now(),
            "StableLifeIdentityCompleted": stable_life_identity_completed,
            "InputReportCount": len(self.inputs),
            "MissingInputCount": len([k for k, v in found.items() if not v]),
            "LifeMemoryReady": life_memory_ready,
            "ReflectionReady": reflection_ready,
            "FeedbackReady": feedback_ready,
            "SyncCandidateReady": sync_ready,
            "DiagnosticsPassed": diagnostics_passed,
            "HumanApprovalRequired": human_approval_required,
            "AutoApplyBlocked": auto_apply_blocked,
            "OriginalIdentityDirectWrite": original_identity_direct_write,
            "IdentityStatement": identity_statement,
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": stable_life_identity_completed,
            "NextPhase": "Phase127 Life Identity Runtime Bridge",
            "MissingInputs": [k for k, v in found.items() if not v],
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"stable_life_identity_completion_report_{timestamp}.json"
        latest_path = self.output_dir / "stable_life_identity_completion_report_latest.json"

        output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        latest_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        result["SavedPath"] = str(output_path)
        result["LatestPath"] = str(latest_path)
        return result


def main() -> None:
    report = StableLifeIdentityCompletionReport()
    result = report.generate()

    print("=== Stable Life Identity Completion Report ===")
    for key, value in result.items():
        if isinstance(value, list):
            print(f"{key}:")
            for item in value:
                print(f"- {item}")
        else:
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()