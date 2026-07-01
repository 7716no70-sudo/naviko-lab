from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def save_feedback_loop_records(
    root_dir: Path,
    reflection_candidate: Dict[str, Any],
    experience_candidate: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Feedback Loop 用の Reflection / Experience 候補を
    Workspace配下へ安全保存する。
    Original書込み・削除・外部操作は行わない。
    """

    root = Path(root_dir)
    feedback_dir = root / "feedback_loop"
    reflection_dir = feedback_dir / "reflection_candidates"
    experience_dir = feedback_dir / "experience_candidates"

    reflection_dir.mkdir(parents=True, exist_ok=True)
    experience_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    reflection_path = reflection_dir / f"reflection_candidate_{timestamp}.json"
    experience_path = experience_dir / f"experience_candidate_{timestamp}.json"

    reflection_path.write_text(
        json.dumps(reflection_candidate, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    experience_path.write_text(
        json.dumps(experience_candidate, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "phase": "Phase14-4 Feedback Loop Workspace Save Adapter",
        "feedback_loop_saved": True,
        "reflection_saved": reflection_path.exists(),
        "experience_saved": experience_path.exists(),
        "reflection_path": str(reflection_path),
        "experience_path": str(experience_path),
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "external_operation": False,
        "real_gui_operation": False,
        "risk_count": 0,
        "safe_to_continue": True,
    }