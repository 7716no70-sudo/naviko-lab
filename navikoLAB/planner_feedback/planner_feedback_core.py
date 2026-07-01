from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"

KNOWLEDGE_DIR = WORKSPACE / "knowledge"
REFLECTION_DIR = WORKSPACE / "reflection"
EXPERIENCE_DIR = WORKSPACE / "experience"

KNOWLEDGE_INDEX = KNOWLEDGE_DIR / "knowledge_learning_index.json"
REFLECTION_EXPERIENCE_INDEX = WORKSPACE / "reflection_experience_index.json"


def _safe_load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _load_recent_json_files(folder: Path, pattern: str, limit: int = 5) -> List[Dict[str, Any]]:
    if not folder.exists():
        return []

    files = sorted(
        folder.glob(pattern),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    records: List[Dict[str, Any]] = []

    for path in files[:limit]:
        data = _safe_load_json(path, {})
        if isinstance(data, dict):
            data["_source_file"] = str(path)
            records.append(data)

    return records


def build_planner_feedback_context(mission: str = "") -> Dict[str, Any]:
    """
    Planner が過去の Knowledge / Reflection / Experience を参照するための
    読み取り専用コンテキストを生成する。
    """

    knowledge_index = _safe_load_json(KNOWLEDGE_INDEX, {})
    reflection_experience_index = _safe_load_json(REFLECTION_EXPERIENCE_INDEX, {})

    recent_knowledge = _load_recent_json_files(
        KNOWLEDGE_DIR,
        "knowledge_record_*.json",
        limit=5,
    )

    recent_reflection = _load_recent_json_files(
        REFLECTION_DIR,
        "reflection_record_*.json",
        limit=5,
    )

    recent_experience = _load_recent_json_files(
        EXPERIENCE_DIR,
        "experience_record_*.json",
        limit=5,
    )

    success_count = 0
    failure_count = 0

    if isinstance(reflection_experience_index, dict):
        success_count = int(reflection_experience_index.get("success_count", 0) or 0)
        failure_count = int(reflection_experience_index.get("failure_count", 0) or 0)

    feedback_context = {
        "phase": "Phase11-1 Planner Feedback Core",
        "mission": mission,
        "read_only": True,
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": True,
        "knowledge_index_loaded": bool(knowledge_index),
        "reflection_experience_index_loaded": bool(reflection_experience_index),
        "recent_knowledge_count": len(recent_knowledge),
        "recent_reflection_count": len(recent_reflection),
        "recent_experience_count": len(recent_experience),
        "success_count": success_count,
        "failure_count": failure_count,
        "planner_hints": {
            "prefer_success_patterns": success_count > 0,
            "avoid_failure_patterns": failure_count > 0,
            "use_knowledge_records": len(recent_knowledge) > 0,
            "use_reflection_records": len(recent_reflection) > 0,
            "use_experience_records": len(recent_experience) > 0,
        },
        "knowledge_index": knowledge_index,
        "reflection_experience_index": reflection_experience_index,
        "recent_knowledge": recent_knowledge,
        "recent_reflection": recent_reflection,
        "recent_experience": recent_experience,
    }

    return feedback_context