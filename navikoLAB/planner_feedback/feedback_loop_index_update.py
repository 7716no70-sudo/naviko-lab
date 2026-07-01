from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "workspace" / "feedback_loop"
REFLECTION_DIR = WORKSPACE / "reflection_candidates"
EXPERIENCE_DIR = WORKSPACE / "experience_candidates"
INDEX_PATH = WORKSPACE / "feedback_loop_index.json"


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _load_existing_index():
    if INDEX_PATH.exists():
        data = _load_json(INDEX_PATH)
        if isinstance(data, dict):
            return data

    return {
        "phase": "Phase14-5 Feedback Loop Index Update",
        "updated_at": None,
        "reflection_candidates": [],
        "experience_candidates": [],
        "counts": {
            "reflection": 0,
            "experience": 0,
        },
        "workspace_only": True,
        "original_write": False,
        "file_delete": False,
        "risk_count": 0,
        "safe_to_continue": True,
    }


def _collect_candidates(folder: Path):
    results = []
    folder.mkdir(parents=True, exist_ok=True)

    for path in sorted(folder.glob("*.json")):
        data = _load_json(path)
        if data is None:
            continue

        results.append({
            "filename": path.name,
            "path": str(path),
            "data": data,
        })

    return results


def update_feedback_loop_index():
    index = _load_existing_index()

    reflections = _collect_candidates(REFLECTION_DIR)
    experiences = _collect_candidates(EXPERIENCE_DIR)

    index["updated_at"] = datetime.now().isoformat(timespec="seconds")
    index["reflection_candidates"] = reflections
    index["experience_candidates"] = experiences
    index["counts"] = {
        "reflection": len(reflections),
        "experience": len(experiences),
    }
    index["workspace_only"] = True
    index["original_write"] = False
    index["file_delete"] = False
    index["risk_count"] = 0
    index["safe_to_continue"] = True

    WORKSPACE.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return index


if __name__ == "__main__":
    result = update_feedback_loop_index()

    print("=== Feedback Loop Index Update ===")
    print("状態: completed")
    print("工程: Phase14-5 Feedback Loop Index Update")
    print(f"ReflectionCount: {result['counts']['reflection']}")
    print(f"ExperienceCount: {result['counts']['experience']}")
    print(f"WorkspaceOnly: {result['workspace_only']}")
    print(f"OriginalWrite: {result['original_write']}")
    print(f"FileDelete: {result['file_delete']}")
    print(f"RiskCount: {result['risk_count']}")
    print(f"SafeToContinue: {result['safe_to_continue']}")
    print(f"保存先: {INDEX_PATH}")